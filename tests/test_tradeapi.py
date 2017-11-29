from unittest import TestCase
import requests
from requests import Response
from requests import RequestException
from six.moves.urllib.parse import urlencode
from mock import Mock
from blockex.tradeapi import BlockExTradeApi
from blockex.tradeapi import OrderType
from blockex.tradeapi import OfferType


# Unit tests
class TestTradeApi(TestCase):
    def setUp(self):
        self.get_access_token_mock = Mock(return_value=
            {
                'access_token': 'SomeAccessToken',
                'expires_in': 86399,
            })

        self.trade_api = BlockExTradeApi(
            'https://test.api.url/',
            'CorrectApiID',
            'CorrectUsername',
            'CorrectPassword')
        self.trade_api.get_access_token = self.get_access_token_mock


class TestTradeApiInit(TestTradeApi):
    def test_init(self):
        self.assertEqual(self.trade_api.api_url, 'https://test.api.url/')
        self.assertEqual(self.trade_api.api_id, 'CorrectApiID')
        self.assertEqual(self.trade_api.username, 'CorrectUsername')
        self.assertEqual(self.trade_api.password, 'CorrectPassword')
        self.assertIsNone(self.trade_api.access_token)


class TestTradeApiLogin(TestCase):
    def setUp(self):
        self.trade_api = BlockExTradeApi(
            'https://test.api.url/',
            'CorrectApiID',
            'CorrectUsername',
            'CorrectPassword')

    def test_authorized_login(self):
        response = Response()
        response.status_code = 200
        response._content = '{"access_token":"SomeAccessToken", "expires_in":86399}'.encode()
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        login_response = self.trade_api.login()

        post_mock.assert_called_once_with(
            'https://test.api.url/oauth/token',
            data={
                'grant_type': 'password',
                'username': 'CorrectUsername',
                'password': 'CorrectPassword',
                'client_id': 'CorrectApiID'
            })

        self.assertEqual(login_response, 'SomeAccessToken')

    def test_unauthorized_login(self):
        self.trade_api = BlockExTradeApi(
            'https://test.api.url/',
            'CorrectApiID',
            'CorrectUsername',
            'WrongPassword')

        response = Response()
        response.status_code = 400
        response._content = '{"error":"invalid_client"}'.encode()
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        with self.assertRaises(RequestException):
            self.trade_api.login()

        post_mock.assert_called_once_with(
            'https://test.api.url/oauth/token',
            data={
                'grant_type': 'password',
                'username': 'CorrectUsername',
                'password': 'WrongPassword',
                'client_id': 'CorrectApiID'
            })


class TestTradeApiLogout(TestTradeApi):
    def test_logout_when_logged_in(self):
        self.trade_api.login()
        self.assertEqual(self.trade_api.access_token, 'SomeAccessToken')

        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        self.trade_api.logout()

        post_mock.assert_called_once_with(
            'https://test.api.url/oauth/logout',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIsNone(self.trade_api.access_token)

    def test_logout_when_not_logged_in(self):
        post_mock = Mock()
        requests.post = post_mock

        self.assertIsNone(self.trade_api.access_token)

        self.trade_api.logout()

        post_mock.assert_not_called()


class TestTradeApiGetOrders(TestTradeApi):
    def test_successful_get_orders_without_filter(self):
        response = Response()
        response.status_code = 200
        orders_list = """
            [{"orderID": "32592",
            "price": 13.40,
            "initialQuantity": 32.50,
            "quantity": 32.50,
            "dateCreated": "2017-10-09T09:32:24.735659+00:00",
            "offerType": 1,
            "type": 1,
            "status": 15,
            "instrumentID": 1,
            "trades": null},
            {"orderID": "32593",
            "price": 11.34,
            "initialQuantity": 26.00,
            "quantity": 26.00,
            "dateCreated": "2017-10-09T09:35:10.61228+00:00",
            "offerType": 1,
            "type": 1,
            "status": 20,
            "instrumentID": 1,
            "trades": null}]"""
        response._content = orders_list.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        get_orders_response = self.trade_api.get_orders()

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/get?',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertEqual(get_orders_response, response.json())

    def test_successful_get_orders_with_filter(self):
        response = Response()
        response.status_code = 200
        orders_list = """
            [{"orderID": "32592",
            "price": 13.40,
            "initialQuantity": 32.50,
            "quantity": 32.50,
            "dateCreated": "2017-10-09T09:32:24.735659+00:00",
            "offerType": 1,
            "type": 1,
            "status": 15,
            "instrumentID": 1,
            "trades": null},
            {"orderID": "32593",
            "price": 11.34,
            "initialQuantity": 26.00,
            "quantity": 26.00,
            "dateCreated": "2017-10-09T09:35:10.61228+00:00",
            "offerType": 1,
            "type": 1,
            "status": 20,
            "instrumentID": 1,
            "trades": null}]"""
        response._content = orders_list.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        get_orders_response = self.trade_api.get_orders(
            1, OrderType.LIMIT, OfferType.BID, '10,20', True, 50)

        data = {}
        data['instrumentID'] = 1
        data['orderType'] = 'Limit'
        data['offerType'] = 'Bid'
        data['status'] = '10,20'
        data['loadExecutions'] = 'True'
        data['maxCount'] = 50

        query_string = urlencode(data)
        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/get?' + query_string,
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertEqual(get_orders_response, response.json())

    def test_unsuccessful_get_orders(self):
        response = Response()
        response.status_code = 400
        response._content = '{"message": "Unknown trader"}'.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        with self.assertRaises(RequestException):
            self.trade_api.get_orders()

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/get?',
            headers={'Authorization': 'Bearer SomeAccessToken'})


class TestTradeApiGetMarketOrders(TestTradeApi):
    def test_successful_get_market_orders_without_filter(self):
        response = Response()
        response.status_code = 200
        market_orders_list = """
            [{"orderID": "31635",
            "price": 5.00,
            "initialQuantity": 270.00,
            "quantity": 0.00,
            "dateCreated": "2017-05-14T09:19:53.335+00:00",
            "offerType": 1,
            "type": 1,
            "status": 40,
            "instrumentID": 1,
            "trades": null},
            {"orderID": "31636",
            "price": 1.00,
            "initialQuantity": 260.00,
            "quantity": 0.00,
            "dateCreated": "2017-05-14T09:19:55.782+00:00",
            "offerType": 1,
            "type": 1,
            "status": 40,
            "instrumentID": 1,
            "trades": null}]"""
        response._content = market_orders_list.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        get_market_orders_response = self.trade_api.get_market_orders(1)

        data = {
            'apiID': 'CorrectApiID',
            'instrumentID': 1
        }

        query_string = urlencode(data)
        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/getMarketOrders?' + query_string)

        self.assertEqual(get_market_orders_response, response.json())

    def test_successful_get_market_orders_with_filter(self):
        response = Response()
        response.status_code = 200
        market_orders_list = """
            [{"orderID": "31635",
            "price": 5.00,
            "initialQuantity": 270.00,
            "quantity": 0.00,
            "dateCreated": "2017-05-14T09:19:53.335+00:00",
            "offerType": 1,
            "type": 1,
            "status": 40,
            "instrumentID": 1,
            "trades": null},
            {"orderID": "31636",
            "price": 1.00,
            "initialQuantity": 260.00,
            "quantity": 0.00,
            "dateCreated": "2017-05-14T09:19:55.782+00:00",
            "offerType": 1,
            "type": 1,
            "status": 40,
            "instrumentID": 1,
            "trades": null}]"""
        response._content = market_orders_list.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        get_market_orders_response = self.trade_api.get_market_orders(
            1, OrderType.LIMIT, OfferType.BID, '10,20', 50)

        data = {
            'apiID': 'CorrectApiID',
            'instrumentID': 1,
            'orderType': 'Limit',
            'offerType': 'Bid',
            'status': '10,20',
            'maxCount': '50'
        }

        query_string = urlencode(data)
        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/getMarketOrders?' + query_string)

        self.assertEqual(get_market_orders_response, response.json())

    def test_unsuccessful_get_market_orders(self):
        response = Response()
        response.status_code = 400
        response._content = '{"message": "Invalid partner API id"}'.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        self.trade_api.api_id = 'IncorrectApiID'

        with self.assertRaises(RequestException):
            self.trade_api.get_market_orders(1)

        data = {
            'apiID': 'IncorrectApiID',
            'instrumentID': 1
        }

        query_string = urlencode(data)
        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/getMarketOrders?' + query_string)


class TestTradeApiCreateOrder(TestTradeApi):
    def test_successful_create_order(self):
        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        self.trade_api.create_order(OfferType.BID,
                                    OrderType.LIMIT,
                                    1,
                                    15.2,
                                    3.7)

        data = {
            'offerType': 'Bid',
            'orderType': 'Limit',
            'instrumentID': 1,
            'price': 15.2,
            'quantity': 3.7
        }

        query_string = urlencode(data)
        post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/create?' + query_string,
            headers={'Authorization': 'Bearer SomeAccessToken'})

    def test_unsuccessful_create_order(self):
        response = Response()
        response.status_code = 400
        response._content = '{"message": "Unknown trader"}'.encode()
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        with self.assertRaises(RequestException):
            self.trade_api.create_order(OfferType.BID,
                                        OrderType.LIMIT,
                                        1,
                                        15.2,
                                        3.7)

        data = {
            'offerType': 'Bid',
            'orderType': 'Limit',
            'instrumentID': 1,
            'price': 15.2,
            'quantity': 3.7
        }

        query_string = urlencode(data)
        post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/create?' + query_string,
            headers={'Authorization': 'Bearer SomeAccessToken'})


class TestTradeApiCancelOrder(TestTradeApi):
    def test_successful_cancel_order(self):
        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        self.trade_api.cancel_order(32598)

        post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/cancel?orderID=32598',
            headers={'Authorization': 'Bearer SomeAccessToken'})

    def test_unsuccessful_cancel_order(self):
        response = Response()
        response.status_code = 400
        response._content = '{"message": "Unknown trader"}'.encode()
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        with self.assertRaises(RequestException):
            self.trade_api.cancel_order(32598)

        post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/cancel?orderID=32598',
            headers={'Authorization': 'Bearer SomeAccessToken'})


class TestTradeApiCancelAllOrders(TestTradeApi):
    def test_successful_cancel_all_orders(self):
        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        self.trade_api.cancel_all_orders(1)

        post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/cancelall?instrumentID=1',
            headers={'Authorization': 'Bearer SomeAccessToken'})

    def test_unsuccessful_cancel_all_orders(self):
        response = Response()
        response.status_code = 400
        response._content = '{"message": "Unknown trader"}'.encode()
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        with self.assertRaises(RequestException):
            self.trade_api.cancel_all_orders(1)

        post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/cancelall?instrumentID=1',
            headers={'Authorization': 'Bearer SomeAccessToken'})


class TestTradeApiGetTraderInstruments(TestTradeApi):
    def test_successful_get_trader_instruments(self):
        response = Response()
        response.status_code = 200
        instruments_list = """
            [{"id": 1,
            "description": "Bitcoin/Euro",
            "name": "BTC/EUR",
            "baseCurrencyID": 43,
            "quoteCurrencyID": 2,
            "minOrderAmount": 0.000000000000,
            "commissionFeePercent": 0.020000000000},
            {"id": 2,
            "description": "Ethereum/Euro",
            "name": "ETH/EUR",
            "baseCurrencyID": 46,
            "quoteCurrencyID": 2,
            "minOrderAmount": 9.000000000000,
            "commissionFeePercent": 0.025000000000}]"""
        response._content = instruments_list.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        get_trader_instruments_response =\
            self.trade_api.get_trader_instruments()

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/traderinstruments',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertEqual(get_trader_instruments_response, response.json())

    def test_unsuccessful_get_trader_instruments(self):
        response = Response()
        response.status_code = 400
        response._content = '{"message": "Unknown trader"}'.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        with self.assertRaises(RequestException):
            self.trade_api.get_trader_instruments()

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/traderinstruments',
            headers={'Authorization': 'Bearer SomeAccessToken'})


class TestTradeApiGetPartnerInstruments(TestTradeApi):
    def test_successful_get_partner_instruments(self):
        response = Response()
        response.status_code = 200
        instruments_list = """
            [{"id": 1,
            "description": "Bitcoin/Euro",
            "name": "BTC/EUR",
            "baseCurrencyID": 43,
            "quoteCurrencyID": 2,
            "minOrderAmount": 0.000000000000,
            "commissionFeePercent": 0.020000000000},
            {"id": 2,
            "description": "Ethereum/Euro",
            "name": "ETH/EUR",
            "baseCurrencyID": 46,
            "quoteCurrencyID": 2,
            "minOrderAmount": 9.000000000000,
            "commissionFeePercent": 0.025000000000}]"""
        response._content = instruments_list.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        get_partner_instruments_response =\
            self.trade_api.get_partner_instruments()

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/' +
            'partnerinstruments?apiID=CorrectApiID')

        self.assertEqual(get_partner_instruments_response,
                         response.json())

    def test_unsuccessful_get_partner_instruments(self):
        response = Response()
        response.status_code = 400
        response._content = '{"message": "Invalid partner"}'.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        self.trade_api.api_id = 'IncorrectApiID'
        with self.assertRaises(RequestException):
            self.trade_api.get_partner_instruments()

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/' +
            'partnerinstruments?apiID=IncorrectApiID')


class TestTradeApiMakeAuthorizedRequest(TestTradeApi):
    def test_make_authorized_get_request_when_not_logged_in(self):
        response = Response()
        response.status_code = 200
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        make_authorized_request_response =\
            self.trade_api._BlockExTradeApi__make_authorized_request(
                'get',
                'ResourceURL')

        self.get_access_token_mock.assert_called_once()
        self.assertEqual(self.trade_api.access_token, 'SomeAccessToken')

        get_mock.assert_called_once_with(
            'ResourceURL',
            headers={'Authorization': 'Bearer SomeAccessToken'})
        self.assertEqual(make_authorized_request_response.status_code, 200)

    def test_make_authorized_post_request_when_not_logged_in(self):
        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        make_authorized_request_response =\
            self.trade_api._BlockExTradeApi__make_authorized_request(
                'post',
                'ResourceURL')

        self.get_access_token_mock.assert_called_once()
        self.assertEqual(self.trade_api.access_token, 'SomeAccessToken')

        post_mock.assert_called_once_with(
            'ResourceURL',
            headers={'Authorization': 'Bearer SomeAccessToken'})
        self.assertEqual(make_authorized_request_response.status_code, 200)

    def test_make_authorized_invalid_request_when_not_logged_in(self):
        with self.assertRaises(AssertionError):
            self.trade_api._BlockExTradeApi__make_authorized_request(
                'WrongType',
                'ResourceURL')

        self.get_access_token_mock.assert_not_called()
        self.assertIsNone(self.trade_api.access_token)

    def test_make_authorized_get_request_when_logged_in(self):
        self.assertIsNone(self.trade_api.access_token)
        self.trade_api.login()

        response = Response()
        response.status_code = 200
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        make_authorized_request_response =\
            self.trade_api._BlockExTradeApi__make_authorized_request(
                'get',
                'ResourceURL')

        self.get_access_token_mock.assert_called_once()
        self.assertEqual(self.trade_api.access_token, 'SomeAccessToken')

        get_mock.assert_called_once_with(
            'ResourceURL',
            headers={'Authorization': 'Bearer SomeAccessToken'})
        self.assertEqual(make_authorized_request_response.status_code, 200)

    def test_make_authorized_post_request_when_logged_in(self):
        self.assertIsNone(self.trade_api.access_token)
        self.trade_api.login()

        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        make_authorized_request_response =\
            self.trade_api._BlockExTradeApi__make_authorized_request(
                'post',
                'ResourceURL')

        self.get_access_token_mock.assert_called_once()
        self.assertEqual(self.trade_api.access_token, 'SomeAccessToken')

        post_mock.assert_called_once_with(
            'ResourceURL',
            headers={'Authorization': 'Bearer SomeAccessToken'})
        self.assertEqual(make_authorized_request_response.status_code, 200)

    def test_make_authorized_invalid_request_when_logged_in(self):
        self.assertIsNone(self.trade_api.access_token)
        self.trade_api.login()

        with self.assertRaises(AssertionError):
            self.trade_api._BlockExTradeApi__make_authorized_request(
                'WrongType',
                'ResourceURL')

        self.get_access_token_mock.assert_called_once()
        self.assertEqual(self.trade_api.access_token, 'SomeAccessToken')

    def test_make_authorized_get_request_when_token_expired(self):
        self.assertIsNone(self.trade_api.access_token)
        self.trade_api.login()

        response = Response()
        response.status_code = 200
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        make_authorized_request_response =\
            self.trade_api._BlockExTradeApi__make_authorized_request(
                'get',
                'ResourceURL')

        self.assertEqual(self.get_access_token_mock.call_count, 1)
        self.assertEqual(self.trade_api.access_token, 'SomeAccessToken')

        get_mock.assert_called_with(
            'ResourceURL',
            headers={'Authorization': 'Bearer SomeAccessToken'})
        self.assertEqual(get_mock.call_count, 1)
        self.assertEqual(make_authorized_request_response.status_code, 200)

    def test_make_authorized_post_request_when_token_expired(self):
        self.assertIsNone(self.trade_api.access_token)
        self.trade_api.login()

        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        make_authorized_request_response =\
            self.trade_api._BlockExTradeApi__make_authorized_request(
                'post', 'ResourceURL')

        self.assertEqual(self.get_access_token_mock.call_count, 1)
        self.assertEqual(self.trade_api.access_token, 'SomeAccessToken')

        post_mock.assert_called_with(
            'ResourceURL',
            headers={'Authorization': 'Bearer SomeAccessToken'})
        self.assertEqual(post_mock.call_count, 1)
        self.assertEqual(make_authorized_request_response.status_code, 200)

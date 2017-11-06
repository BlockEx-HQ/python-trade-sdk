import requests
from requests import Response
from six.moves.urllib.parse import urlencode
from unittest import TestCase
from mock import Mock
from BlockExTradeApi import BlockExTradeApi


# Unit tests
class TestTradeApi(TestCase):
    def setUp(self):
        response = Response()
        response.status_code = 200
        response._content = '{"access_token":"SomeAccessToken"}'.encode()
        self.get_access_token_mock = Mock(return_value={
                'response': response,
                'access_token': 'SomeAccessToken'
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
    def test_authorized_login(self):
        self.trade_api = BlockExTradeApi(
            'https://test.api.url/',
            'CorrectApiID',
            'CorrectUsername',
            'CorrectPassword')

        response = Response()
        response.status_code = 200
        response._content = '{"access_token":"SomeAccessToken"}'.encode()
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

        self.assertIn('response', login_response)
        self.assertEqual(login_response['response'].status_code, 200)
        self.assertEqual(login_response['response'].content,
                         '{"access_token":"SomeAccessToken"}'.encode())

        self.assertIn('access_token', login_response)
        self.assertEqual(login_response['access_token'], 'SomeAccessToken')

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

        login_response = self.trade_api.login()

        post_mock.assert_called_once_with(
            'https://test.api.url/oauth/token',
            data={
                'grant_type': 'password',
                'username': 'CorrectUsername',
                'password': 'WrongPassword',
                'client_id': 'CorrectApiID'
            })

        self.assertIn('response', login_response)
        self.assertEqual(login_response['response'].status_code, 400)
        self.assertEqual(login_response['response'].content,
                         '{"error":"invalid_client"}'.encode())

        self.assertNotIn('access_token', login_response)


class TestTradeApiLogout(TestTradeApi):
    def test_logout_when_logged_in(self):
        self.trade_api.login()
        self.assertEqual(self.trade_api.access_token, 'SomeAccessToken')

        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        logout_response = self.trade_api.logout()

        post_mock.assert_called_once_with(
            'https://test.api.url/oauth/logout',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', logout_response)
        self.assertEqual(logout_response['response'].status_code, 200)
        self.assertIsNone(self.trade_api.access_token)

    def test_logout_when_not_logged_in(self):
        post_mock = Mock()
        requests.post = post_mock

        self.assertIsNone(self.trade_api.access_token)

        logout_response = self.trade_api.logout()

        post_mock.assert_not_called()

        self.assertIn('response', logout_response)
        self.assertIsNone(logout_response['response'])


class TestTradeApiGetOrders(TestTradeApi):
    def test_successful_get_orders_without_filter(self):
        response = Response()
        response.status_code = 200
        orders_list = '[{"orderID": "32592",'
        orders_list += '"price": 13.40,'
        orders_list += '"initialQuantity": 32.50,'
        orders_list += '"quantity": 32.50,'
        orders_list += '"dateCreated": "2017-10-09T09:32:24.735659+00:00",'
        orders_list += '"offerType": 1,'
        orders_list += '"type": 1,'
        orders_list += '"status": 15,'
        orders_list += '"instrumentID": 1,'
        orders_list += '"trades": null},'
        orders_list += '{"orderID": "32593",'
        orders_list += '"price": 11.34,'
        orders_list += '"initialQuantity": 26.00,'
        orders_list += '"quantity": 26.00,'
        orders_list += '"dateCreated": "2017-10-09T09:35:10.61228+00:00",'
        orders_list += '"offerType": 1,'
        orders_list += '"type": 1,'
        orders_list += '"status": 20,'
        orders_list += '"instrumentID": 1,'
        orders_list += '"trades": null}]'
        response._content = orders_list.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        get_orders_response = self.trade_api.get_orders()

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/get?',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', get_orders_response)
        self.assertEqual(get_orders_response['response'].status_code, 200)
        self.assertEqual(get_orders_response['response'].content,
                         orders_list.encode())

        self.assertIn('data', get_orders_response)
        self.assertEqual(get_orders_response['data'],
                         response.json())

    def test_successful_get_orders_with_filter(self):
        response = Response()
        response.status_code = 200
        orders_list = '[{"orderID": "32592",'
        orders_list += '"price": 13.40,'
        orders_list += '"initialQuantity": 32.50,'
        orders_list += '"quantity": 32.50,'
        orders_list += '"dateCreated": "2017-10-09T09:32:24.735659+00:00",'
        orders_list += '"offerType": 1,'
        orders_list += '"type": 1,'
        orders_list += '"status": 15,'
        orders_list += '"instrumentID": 1,'
        orders_list += '"trades": null},'
        orders_list += '{"orderID": "32593",'
        orders_list += '"price": 11.34,'
        orders_list += '"initialQuantity": 26.00,'
        orders_list += '"quantity": 26.00,'
        orders_list += '"dateCreated": "2017-10-09T09:35:10.61228+00:00",'
        orders_list += '"offerType": 1,'
        orders_list += '"type": 1,'
        orders_list += '"status": 20,'
        orders_list += '"instrumentID": 1,'
        orders_list += '"trades": null}]'
        response._content = orders_list.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        get_orders_response = self.trade_api.get_orders(
            1, 'Limit', 'Bid', '10,20', 'true', 50)

        data = {}
        data['instrumentID'] = 1
        data['orderType'] = 'Limit'
        data['offerType'] = 'Bid'
        data['status'] = '10,20'
        data['loadExecutions'] = 'true'
        data['maxCount'] = 50

        query_string = urlencode(data)
        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/get?' + query_string,
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', get_orders_response)
        self.assertEqual(get_orders_response['response'].status_code, 200)
        self.assertEqual(get_orders_response['response'].content,
                         orders_list.encode())

        self.assertIn('data', get_orders_response)
        self.assertEqual(get_orders_response['data'],
                         response.json())

    def test_unsuccessful_get_orders(self):
        response = Response()
        response.status_code = 400
        response._content = '{"message": "Unknown trader"}'.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        get_orders_response = self.trade_api.get_orders()

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/get?',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', get_orders_response)
        self.assertEqual(get_orders_response['response'].status_code, 400)
        self.assertEqual(get_orders_response['response'].content,
                         '{"message": "Unknown trader"}'.encode())

        self.assertNotIn('data', get_orders_response)


class TestTradeApiGetMarketOrders(TestTradeApi):
    def test_successful_get_market_orders_without_filter(self):
        response = Response()
        response.status_code = 200
        market_orders_list = '[{"orderID": "31635",'
        market_orders_list += '"price": 5.00,'
        market_orders_list += '"initialQuantity": 270.00,'
        market_orders_list += '"quantity": 0.00,'
        market_orders_list += '"dateCreated": "2017-05-14T09:19:53.335+00:00",'
        market_orders_list += '"offerType": 1,'
        market_orders_list += '"type": 1,'
        market_orders_list += '"status": 40,'
        market_orders_list += '"instrumentID": 1,'
        market_orders_list += '"trades": null},'
        market_orders_list += '{"orderID": "31636",'
        market_orders_list += '"price": 1.00,'
        market_orders_list += '"initialQuantity": 260.00,'
        market_orders_list += '"quantity": 0.00,'
        market_orders_list += '"dateCreated": "2017-05-14T09:19:55.782+00:00",'
        market_orders_list += '"offerType": 1,'
        market_orders_list += '"type": 1,'
        market_orders_list += '"status": 40,'
        market_orders_list += '"instrumentID": 1,'
        market_orders_list += '"trades": null}]'
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

        self.assertIn('response', get_market_orders_response)
        self.assertEqual(get_market_orders_response['response'].status_code,
                         200)
        self.assertEqual(get_market_orders_response['response'].content,
                         market_orders_list.encode())

        self.assertIn('data', get_market_orders_response)
        self.assertEqual(get_market_orders_response['data'],
                         response.json())

    def test_successful_get_market_orders_with_filter(self):
        response = Response()
        response.status_code = 200
        market_orders_list = '[{"orderID": "31635",'
        market_orders_list += '"price": 5.00,'
        market_orders_list += '"initialQuantity": 270.00,'
        market_orders_list += '"quantity": 0.00,'
        market_orders_list += '"dateCreated": "2017-05-14T09:19:53.335+00:00",'
        market_orders_list += '"offerType": 1,'
        market_orders_list += '"type": 1,'
        market_orders_list += '"status": 40,'
        market_orders_list += '"instrumentID": 1,'
        market_orders_list += '"trades": null},'
        market_orders_list += '{"orderID": "31636",'
        market_orders_list += '"price": 1.00,'
        market_orders_list += '"initialQuantity": 260.00,'
        market_orders_list += '"quantity": 0.00,'
        market_orders_list += '"dateCreated": "2017-05-14T09:19:55.782+00:00",'
        market_orders_list += '"offerType": 1,'
        market_orders_list += '"type": 1,'
        market_orders_list += '"status": 40,'
        market_orders_list += '"instrumentID": 1,'
        market_orders_list += '"trades": null}]'
        response._content = market_orders_list.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        get_market_orders_response = self.trade_api.get_market_orders(
            1, 'Limit', 'Bid', '10,20', 50)

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

        self.assertIn('response', get_market_orders_response)
        self.assertEqual(get_market_orders_response['response'].status_code,
                         200)
        self.assertEqual(get_market_orders_response['response'].content,
                         market_orders_list.encode())

        self.assertIn('data', get_market_orders_response)
        self.assertEqual(get_market_orders_response['data'],
                         response.json())

    def test_unsuccessful_get_market_orders(self):
        response = Response()
        response.status_code = 400
        response._content = '{"message": "Invalid partner API id"}'.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        self.trade_api.api_id = 'IncorrectApiID'
        get_orders_response = self.trade_api.get_market_orders(1)

        data = {
            'apiID': 'IncorrectApiID',
            'instrumentID': 1
        }

        query_string = urlencode(data)
        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/getMarketOrders?' + query_string)

        self.assertIn('response', get_orders_response)
        self.assertEqual(get_orders_response['response'].status_code, 400)
        self.assertEqual(get_orders_response['response'].content,
                         '{"message": "Invalid partner API id"}'.encode())

        self.assertNotIn('data', get_orders_response)


class TestTradeApiCreateOrder(TestTradeApi):
    def test_create_order(self):
        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        create_order_response = self.trade_api.create_order(
            'Bid', 'Limit', 1, 15.2, 3.7)

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

        self.assertIn('response', create_order_response)
        self.assertEqual(create_order_response['response'].status_code, 200)


class TestTradeApiCancelOrder(TestTradeApi):
    def test_cancel_order(self):
        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        cancel_order_response = self.trade_api.cancel_order(32598)

        post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/cancel?orderID=32598',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', cancel_order_response)
        self.assertEqual(cancel_order_response['response'].status_code, 200)


class TestTradeApiCancelAllOrders(TestTradeApi):
    def test_cancel_all_orders(self):
        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        cancel_all_orders_response = self.trade_api.cancel_all_orders(1)

        post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/cancelall?instrumentID=1',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', cancel_all_orders_response)
        self.assertEqual(cancel_all_orders_response['response'].status_code,
                         200)


class TestTradeApiGetTraderInstruments(TestTradeApi):
    def test_successful_get_trader_instruments(self):
        response = Response()
        response.status_code = 200
        instruments_list = '[{"id": 1,'
        instruments_list += '"description": "Bitcoin/Euro",'
        instruments_list += '"name": "BTC/EUR",'
        instruments_list += '"baseCurrencyID": 43,'
        instruments_list += '"quoteCurrencyID": 2,'
        instruments_list += '"minOrderAmount": 0.000000000000,'
        instruments_list += '"commissionFeePercent": 0.020000000000},'
        instruments_list += '{"id": 2,'
        instruments_list += '"description": "Ethereum/Euro",'
        instruments_list += '"name": "ETH/EUR",'
        instruments_list += '"baseCurrencyID": 46,'
        instruments_list += '"quoteCurrencyID": 2,'
        instruments_list += '"minOrderAmount": 9.000000000000,'
        instruments_list += '"commissionFeePercent": 0.025000000000}]'
        response._content = instruments_list.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        get_trader_instruments_response =\
            self.trade_api.get_trader_instruments()

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/traderinstruments',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', get_trader_instruments_response)
        self.assertEqual(
            get_trader_instruments_response['response'].status_code,
            200)
        self.assertEqual(
            get_trader_instruments_response['response'].content,
            instruments_list.encode())

        self.assertIn('data', get_trader_instruments_response)
        self.assertEqual(get_trader_instruments_response['data'],
                         response.json())

    def test_unsuccessful_get_trader_instruments(self):
        response = Response()
        response.status_code = 400
        response._content = '{"message": "Unknown trader"}'.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        get_trader_instruments_response =\
            self.trade_api.get_trader_instruments()

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/traderinstruments',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', get_trader_instruments_response)
        self.assertEqual(
            get_trader_instruments_response['response'].status_code,
            400)
        self.assertEqual(
            get_trader_instruments_response['response'].content,
            '{"message": "Unknown trader"}'.encode())

        self.assertNotIn('data', get_trader_instruments_response)


class TestTradeApiGetPartnerInstruments(TestTradeApi):
    def test_successful_get_partner_instruments(self):
        response = Response()
        response.status_code = 200
        instruments_list = '[{"id": 1,"description": "Bitcoin/Euro",'
        instruments_list += '"name": "BTC/EUR",'
        instruments_list += '"baseCurrencyID": 43,'
        instruments_list += '"quoteCurrencyID": 2,'
        instruments_list += '"minOrderAmount": 0.000000000000,'
        instruments_list += '"commissionFeePercent": 0.020000000000},'
        instruments_list += '{"id": 2,"description": "Ethereum/Euro",'
        instruments_list += '"name": "ETH/EUR",'
        instruments_list += '"baseCurrencyID": 46,'
        instruments_list += '"quoteCurrencyID": 2,'
        instruments_list += '"minOrderAmount": 9.000000000000,'
        instruments_list += '"commissionFeePercent": 0.025000000000}]'
        response._content = instruments_list.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        get_partner_instruments_response =\
            self.trade_api.get_partner_instruments()

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/' +
            'partnerinstruments?apiID=CorrectApiID')

        self.assertIn('response', get_partner_instruments_response)
        self.assertEqual(
            get_partner_instruments_response['response'].status_code,
            200)
        self.assertEqual(
            get_partner_instruments_response['response'].content,
            instruments_list.encode())

        self.assertIn('data', get_partner_instruments_response)
        self.assertEqual(get_partner_instruments_response['data'],
                         response.json())

    def test_unsuccessful_get_partner_instruments(self):
        response = Response()
        response.status_code = 400
        response._content = '{"message": "Invalid partner"}'.encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        self.trade_api.api_id = 'IncorrectApiID'
        get_partner_instruments_response =\
            self.trade_api.get_partner_instruments()

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/' +
            'partnerinstruments?apiID=IncorrectApiID')

        self.assertIn('response', get_partner_instruments_response)
        self.assertEqual(
            get_partner_instruments_response['response'].status_code,
            400)
        self.assertEqual(
            get_partner_instruments_response['response'].content,
            '{"message": "Invalid partner"}'.encode())

        self.assertNotIn('data', get_partner_instruments_response)


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
        with self.assertRaises(ValueError):
            self.trade_api._BlockExTradeApi__make_authorized_request(
                'WrongType',
                'ResourceURL')

        self.get_access_token_mock.assert_called_once()
        self.assertEqual(self.trade_api.access_token, 'SomeAccessToken')

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

        with self.assertRaises(ValueError):
            self.trade_api._BlockExTradeApi__make_authorized_request(
                'WrongType',
                'ResourceURL')

        self.get_access_token_mock.assert_called_once()
        self.assertEqual(self.trade_api.access_token, 'SomeAccessToken')

    def test_make_authorized_get_request_when_token_expired(self):
        self.assertIsNone(self.trade_api.access_token)
        self.trade_api.login()

        response = Response()
        response.status_code = 401
        response._content =\
            '{"message": "Authorization has been denied for this request."}'\
                .encode()
        get_mock = Mock(return_value=response)
        requests.get = get_mock

        make_authorized_request_response =\
            self.trade_api._BlockExTradeApi__make_authorized_request(
                'get',
                'ResourceURL')

        self.assertEqual(self.get_access_token_mock.call_count, 2)
        self.assertEqual(self.trade_api.access_token, 'SomeAccessToken')

        get_mock.assert_called_with(
            'ResourceURL',
            headers={'Authorization': 'Bearer SomeAccessToken'})
        self.assertEqual(get_mock.call_count, 2)
        self.assertEqual(make_authorized_request_response.status_code, 401)

    def test_make_authorized_post_request_when_token_expired(self):
        self.assertIsNone(self.trade_api.access_token)
        self.trade_api.login()

        response = Response()
        response.status_code = 401
        response._content =\
            '{"message": "Authorization has been denied for this request."}'\
                .encode()
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        make_authorized_request_response =\
            self.trade_api._BlockExTradeApi__make_authorized_request(
                'post', 'ResourceURL')

        self.assertEqual(self.get_access_token_mock.call_count, 2)
        self.assertEqual(self.trade_api.access_token, 'SomeAccessToken')

        post_mock.assert_called_with(
            'ResourceURL',
            headers={'Authorization': 'Bearer SomeAccessToken'})
        self.assertEqual(post_mock.call_count, 2)
        self.assertEqual(make_authorized_request_response.status_code, 401)

import sys
from unittest import TestCase

import requests
from blockex.tradeapi import interface, tradeapi
from mock import Mock

if sys.version_info >= (3, 0):
    from urllib.parse import urlencode  # pragma: no cover
else:
    from urllib import urlencode  # pragma: no cover

Response = requests.Response
RequestException = requests.RequestException

FIXTURE_INSTRUMENT_ID = 1
FIXTURE_ACCESS_TOKEN = "SomeAccessToken"
FIXTURE_API_URL = "https://test.api.url/"
FIXTURE_API_ID = "CorrectApiID"
FIXTURE_USERNAME = "CorrectUsername"
FIXTURE_PASSWORD = "CorrectPassword"
FIXTURE_BAD_PASSWORD = "bad_password"


# Unit tests
class TestTradeApi(TestCase):
    def setUp(self):
        self.get_access_token_mock = Mock(return_value={
            'access_token': FIXTURE_ACCESS_TOKEN,
            'expires_in': 86399,
        })
        self.trade_api = tradeapi.BlockExTradeApi(
            api_url=FIXTURE_API_URL, api_id=FIXTURE_API_ID,
            username=FIXTURE_USERNAME, password=FIXTURE_PASSWORD)

        self.trade_api.get_access_token = self.get_access_token_mock


class TestTradeApiInit(TestTradeApi):
    def test_init(self):
        self.assertEqual(self.trade_api.api_url, FIXTURE_API_URL)
        self.assertEqual(self.trade_api.api_id, FIXTURE_API_ID)
        self.assertEqual(self.trade_api.username, FIXTURE_USERNAME)
        self.assertEqual(self.trade_api.password, FIXTURE_PASSWORD)
        self.assertIsNone(self.trade_api.access_token)


class TestTradeApiGetOrders(TestTradeApi):
    def setUp(self):
        super().setUp()

        self.orders_list = """
            [{"orderID": "32592",
            "price": "13.40",
            "initialQuantity": "32.50",
            "quantity": "32.50",
            "dateCreated": "2017-10-09T09:32:24.735659+00:00",
            "offerType": 1,
            "type": 1,
            "status": 15,
            "instrumentID": 1,
            "trades": null},
            {"orderID": "32593",
            "price": "11.34",
            "initialQuantity": "26.00",
            "quantity": "26.00",
            "dateCreated": "2017-10-09T09:35:10.61228+00:00",
            "offerType": 1,
            "type": 1,
            "status": 20,
            "instrumentID": 1,
            "trades": null}]"""

        self.response = Response()
        self.response.status_code = interface.SUCCESS
        self.response._content = self.orders_list.encode()
        self.get_mock = Mock(return_value=self.response)
        requests.get = self.get_mock

    def test_successful_get_orders_without_filter(self):
        get_orders_response = self.trade_api.get_orders()

        self.get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/get?',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        orders = self.response.json()
        for order in orders:
            tradeapi.convert_order_numbers(order)
        self.assertEqual(get_orders_response, orders)

    def test_successful_get_orders_with_filter(self):
        get_orders_response = self.trade_api.get_orders(
            FIXTURE_INSTRUMENT_ID, interface.OrderType.LIMIT, interface.OfferType.BID,
            [interface.OrderStatus.PENDING, interface.OrderStatus.PLACED],
            True, 50)

        data = {}
        data['instrumentID'] = FIXTURE_INSTRUMENT_ID
        data['loadExecutions'] = 'True'
        data['maxCount'] = 50
        data['orderType'] = 'Limit'
        data['offerType'] = 'Bid'
        data['status'] = '10,20'

        query_string = urlencode(data)
        self.get_mock.assert_called_once_with('https://test.api.url/api/orders/get?' + query_string,
                                              headers={'Authorization': 'Bearer SomeAccessToken'})

        orders = self.response.json()
        for order in orders:
            tradeapi.convert_order_numbers(order)
        self.assertEqual(get_orders_response, orders)

    def test_unsuccessful_get_orders(self):
        self.response.status_code = interface.BAD_REQUEST
        self.response._content = '{"message": "Unknown trader"}'.encode()

        with self.assertRaises(RequestException):
            self.trade_api.get_orders()

        self.get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/get?',
            headers={'Authorization': 'Bearer SomeAccessToken'})


class TestTradeApiGetMarketOrders(TestTradeApi):
    def setUp(self):
        super().setUp()

        self.market_orders_list = """
            [{"orderID": "31635",
            "price": "5.00",
            "initialQuantity": "270.00",
            "quantity": "0.00",
            "dateCreated": "2017-05-14T09:19:53.335+00:00",
            "offerType": 1,
            "type": 1,
            "status": 40,
            "instrumentID": 1,
            "trades": null},
            {"orderID": "31636",
            "price": "1.00",
            "initialQuantity": "260.00",
            "quantity": "0.00",
            "dateCreated": "2017-05-14T09:19:55.782+00:00",
            "offerType": 1,
            "type": 1,
            "status": 40,
            "instrumentID": 1,
            "trades": null}]"""

        self.response = Response()
        self.response.status_code = interface.SUCCESS
        self.response._content = self.market_orders_list.encode()
        self.get_mock = Mock(return_value=self.response)
        requests.get = self.get_mock

    def test_successful_get_market_orders_without_filter(self):
        get_market_orders_response = self.trade_api.get_market_orders(FIXTURE_INSTRUMENT_ID)

        data = {
            'apiID': 'CorrectApiID',
            'instrumentID': FIXTURE_INSTRUMENT_ID
        }

        query_string = urlencode(data)
        self.get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/getMarketOrders?' + query_string)

        orders = self.response.json()
        for order in orders:
            tradeapi.convert_order_numbers(order)
        self.assertEqual(get_market_orders_response, orders)

    def test_successful_get_market_orders_with_filter(self):
        get_market_orders_response = self.trade_api.get_market_orders(
            FIXTURE_INSTRUMENT_ID, interface.OrderType.LIMIT, interface.OfferType.BID,
            [interface.OrderStatus.PENDING, interface.OrderStatus.PLACED],
            50)

        data = {
            'apiID': 'CorrectApiID',
            'instrumentID': FIXTURE_INSTRUMENT_ID,
            'maxCount': '50',
            'orderType': 'Limit',
            'offerType': 'Bid',
            'status': '10,20'
        }

        query_string = urlencode(data)
        self.get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/getMarketOrders?' + query_string)

        orders = self.response.json()
        for order in orders:
            tradeapi.convert_order_numbers(order)
        self.assertEqual(get_market_orders_response, orders)

    def test_unsuccessful_get_market_orders(self):
        self.response.status_code = interface.BAD_REQUEST
        self.response._content = '{"message": "Invalid partner API id"}'.encode()

        self.trade_api.api_id = 'IncorrectApiID'

        with self.assertRaises(RequestException):
            self.trade_api.get_market_orders(FIXTURE_INSTRUMENT_ID)

        data = {
            'apiID': 'IncorrectApiID',
            'instrumentID': FIXTURE_INSTRUMENT_ID
        }

        query_string = urlencode(data)
        self.get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/getMarketOrders?' + query_string)


class TestTradeApiGetTradesHistory(TestTradeApi):
    def setUp(self):
        super().setUp()

        self.trades_history = """
            {
                "trades": [
                    {"tradeID": 1,
                     "price": 5,
                     "totalPrice": 5.00,
                     "quantity": 0.00,
                     "tradeDate": "2017-05-14T09:16:20.335+00:00",
                     "currencyID": 6,
                     "quoteCurrencyID": 7,
                     "instrumentID": 1,
                     "offerType": 1
                    },
                    {"tradeID": 2,
                     "price": 6,
                     "totalPrice": 6.00,
                     "quantity": 1.00,
                     "tradeDate": "2017-05-14T09:19:53.335+00:00",
                     "currencyID": 7,
                     "quoteCurrencyID": 7,
                     "instrumentID": 1,
                     "offerType": 1
                    }
                    ],
                "pageSize": 1,
                "pageIndex": 2,
                "totalCount": 2
            }
            """
        self.headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        self.response = Response()
        self.response.status_code = interface.SUCCESS
        self.response._content = self.trades_history.encode()
        self.post_mock = Mock(return_value=self.response)
        requests.post = self.post_mock

    def test_successful_get_trades_history_without_filter(self):
        get_trades_history_response = self.trade_api.get_trades_history()

        data = {'apiID': 'CorrectApiID'}

        self.post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/getTradesHistory?',
            data=urlencode(data),
            headers=self.headers)

        orders = self.response.json()
        self.assertEqual(get_trades_history_response, orders)

    def test_successful_get_trades_history_with_filter(self):
        get_trades_history_response = self.trade_api.get_trades_history(
            instrument_id=FIXTURE_INSTRUMENT_ID, currency_id=1, sort_by=interface.SortBy.DATE)

        data = {
            'apiID': 'CorrectApiID',
            'currencyID': 1,
            'instrumentID': FIXTURE_INSTRUMENT_ID,
            'sortBy': interface.SortBy.DATE.value
        }

        self.post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/getTradesHistory?',
            data=urlencode(data),
            headers=self.headers)

        orders = self.response.json()
        self.assertEqual(get_trades_history_response, orders)

    def test_unsuccessful_get_trades_history(self):
        self.response.status_code = interface.BAD_REQUEST
        self.response._content = '{"message": "Invalid partner API id"}'.encode()

        self.trade_api.api_id = 'IncorrectApiID'

        with self.assertRaises(RequestException):
            self.trade_api.get_trades_history(FIXTURE_INSTRUMENT_ID)

        data = {
            'apiID': 'IncorrectApiID',
            'instrumentID': FIXTURE_INSTRUMENT_ID
        }

        self.post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/getTradesHistory?',
            data=urlencode(data),
            headers=self.headers)


class TestTradeApiCreateOrder(TestTradeApi):
    def setUp(self):
        super().setUp()

        self.response = Response()
        self.response.status_code = interface.SUCCESS
        self.post_mock = Mock(return_value=self.response)
        requests.post = self.post_mock

    def test_unsuccessful_create_order(self):
        self.response.status_code = interface.BAD_REQUEST
        self.response._content = '{"message": "Unknown trader"}'.encode()

        with self.assertRaises(RequestException):
            self.trade_api.create_order(interface.OfferType.BID, interface.OrderType.LIMIT,
                                        FIXTURE_INSTRUMENT_ID, 15.2, 3.7)

        data = {
            'offerType': 'Bid',
            'orderType': 'Limit',
            'instrumentID': FIXTURE_INSTRUMENT_ID,
            'price': 15.2,
            'quantity': 3.7
        }

        query_string = urlencode(data)
        self.post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/create?' + query_string,
            headers={'Authorization': 'Bearer SomeAccessToken'})


class TestTradeApiCancelOrder(TestTradeApi):
    def setUp(self):
        super().setUp()

        self.response = Response()
        self.response.status_code = interface.SUCCESS
        self.post_mock = Mock(return_value=self.response)
        requests.post = self.post_mock

    def test_successful_cancel_order(self):
        self.trade_api.cancel_order(32598)

        self.post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/cancel?orderID=32598',
            headers={'Authorization': 'Bearer SomeAccessToken'})

    def test_unsuccessful_cancel_order(self):
        self.response.status_code = interface.BAD_REQUEST
        self.response._content = '{"message": "Unknown trader"}'.encode()

        with self.assertRaises(RequestException):
            self.trade_api.cancel_order(32598)

        self.post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/cancel?orderID=32598',
            headers={'Authorization': 'Bearer SomeAccessToken'})


class TestTradeApiCancelAllOrders(TestTradeApi):
    def setUp(self):
        super().setUp()

        self.response = Response()
        self.response.status_code = interface.SUCCESS
        self.post_mock = Mock(return_value=self.response)
        requests.post = self.post_mock

    def test_successful_cancel_all_orders(self):
        self.trade_api.cancel_all_orders(FIXTURE_INSTRUMENT_ID)

        self.post_mock.assert_called_once_with(
            "https://test.api.url/api/orders/cancelall?instrumentID=" + str(FIXTURE_INSTRUMENT_ID),
            headers={'Authorization': 'Bearer SomeAccessToken'})

    def test_unsuccessful_cancel_all_orders(self):
        self.response.status_code = interface.BAD_REQUEST
        self.response._content = '{"message": "Unknown trader"}'.encode()

        with self.assertRaises(RequestException):
            self.trade_api.cancel_all_orders(FIXTURE_INSTRUMENT_ID)

        self.post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/cancelall?instrumentID=1',
            headers={'Authorization': 'Bearer SomeAccessToken'})


class TestTradeApiGetTraderInstruments(TestTradeApi):
    def setUp(self):
        super().setUp()

        self.response = Response()
        self.response.status_code = interface.SUCCESS
        self.get_mock = Mock(return_value=self.response)
        requests.get = self.get_mock

    def test_successful_get_trader_instruments(self):
        instruments_list = """
            [{"id": 1,
            "description": "Bitcoin/Euro",
            "name": "BTC/EUR",
            "baseCurrencyID": 43,
            "quoteCurrencyID": 2,
            "minOrderAmount": "0.020000000000",
            "commissionFeePercent": 0.020000000000},
            {"id": 2,
            "description": "Ethereum/Euro",
            "name": "ETH/EUR",
            "baseCurrencyID": 46,
            "quoteCurrencyID": 2,
            "minOrderAmount": "9.000000000000",
            "commissionFeePercent": 0.025000000000}]"""

        self.response._content = instruments_list.encode()
        get_trader_instruments_response = self.trade_api.get_trader_instruments()

        self.get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/traderinstruments',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        instruments = self.response.json()
        for instrument in instruments:
            tradeapi.convert_instrument_numbers(instrument)
        self.assertEqual(get_trader_instruments_response, instruments)

    def test_unsuccessful_get_trader_instruments(self):
        self.response.status_code = interface.BAD_REQUEST
        self.response._content = '{"message": "Unknown trader"}'.encode()

        with self.assertRaises(RequestException):
            self.trade_api.get_trader_instruments()

        self.get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/traderinstruments',
            headers={'Authorization': 'Bearer SomeAccessToken'})


class TestTradeApiGetPartnerInstruments(TestTradeApi):
    def setUp(self):
        super().setUp()

        self.response = Response()
        self.response.status_code = interface.SUCCESS
        self.get_mock = Mock(return_value=self.response)
        requests.get = self.get_mock

    def test_successful_get_partner_instruments(self):
        instruments_list = """
            [{{"id": {instrument_id},
            "description": "Bitcoin/Euro",
            "name": "BTC/EUR",
            "baseCurrencyID": 43,
            "quoteCurrencyID": 2,
            "minOrderAmount": "0.020000000000",
            "commissionFeePercent": "0.020000000000"}},
            {{"id": 2,
            "description": "Ethereum/Euro",
            "name": "ETH/EUR",
            "baseCurrencyID": 46,
            "quoteCurrencyID": 2,
            "minOrderAmount": "9.000000000000",
            "commissionFeePercent": 0.025000000000}}]""".format(instrument_id = FIXTURE_INSTRUMENT_ID)

        self.response._content = instruments_list.encode()
        partner_instruments_response = self.trade_api.get_partner_instruments()

        self.get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/' +
            'partnerinstruments?apiID=CorrectApiID')

        instruments = self.response.json()
        for instrument in instruments:
            tradeapi.convert_instrument_numbers(instrument)
        self.assertEqual(partner_instruments_response, instruments)

    def test_unsuccessful_get_partner_instruments(self):
        self.response.status_code = interface.BAD_REQUEST
        self.response._content = '{"message": "Invalid partner"}'.encode()

        self.trade_api.api_id = 'IncorrectApiID'
        with self.assertRaises(RequestException):
            self.trade_api.get_partner_instruments()

        self.get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/' + 'partnerinstruments?apiID=IncorrectApiID')

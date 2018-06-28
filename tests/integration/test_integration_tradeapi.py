import decimal
import os
from unittest import skip, TestCase

from blockex.tradeapi import interface
from blockex.tradeapi.tradeapi import BlockExTradeApi
from requests import RequestException

FIXTURE_BAD_PASSWORD = 'BadPassword'
FIXTURE_BAD_API_ID = 'xxx'
FIXTURE_INSTRUMENT_ID = 4


# Integration tests
class TestTradeApi(TestCase):
    def setUp(self):
        self.client = BlockExTradeApi(api_url=os.environ.get('BLOCKEX_TEST_TRADEAPI_URL'),
                                      api_id=os.environ.get('BLOCKEX_TEST_TRADEAPI_ID'),
                                      username=os.environ.get('BLOCKEX_TEST_TRADEAPI_USERNAME'),
                                      password=os.environ.get('BLOCKEX_TEST_TRADEAPI_PASSWORD'))


class TestTradeApiLoginLogout(TestTradeApi):
    def test_authorized_login(self):
        login_response = self.client.login()
        self.assertIsNotNone(login_response)

    def test_unauthorized_login(self):
        self.client.password = FIXTURE_BAD_PASSWORD
        with self.assertRaises(RequestException):
            self.client.login()

    def test_logout(self):
        self.client.login()
        self.assertIsNotNone(self.client.access_token)

        self.client.logout()
        self.assertIsNone(self.client.access_token)


class TestTradeApiGetOrders(TestTradeApi):
    def test_successful_get_orders_without_filter(self):
        get_orders_response = self.client.get_orders()
        self.assertIsNotNone(get_orders_response)

    def test_successful_get_orders_with_filter(self):
        get_orders_response = self.client.get_orders(
            FIXTURE_INSTRUMENT_ID,
            interface.OrderType.LIMIT, interface.OfferType.BID,
            [interface.OrderStatus.PENDING, interface.OrderStatus.PLACED],
            True, 50)

        self.assertIsNotNone(get_orders_response)

    def test_unsuccessful_get_orders(self):
        self.client.password = FIXTURE_BAD_PASSWORD
        with self.assertRaises(RequestException):
            self.client.get_orders()


class TestTradeApiGetMarketOrders(TestTradeApi):
    def test_successful_get_market_orders_without_filter(self):
        get_market_orders_response = self.client.get_market_orders(FIXTURE_INSTRUMENT_ID)
        self.assertIsNotNone(get_market_orders_response)

    def test_successful_get_market_orders_with_filter(self):
        get_market_orders_response = self.client.get_market_orders(
            FIXTURE_INSTRUMENT_ID,
            interface.OrderType.LIMIT, interface.OfferType.BID,
            [interface.OrderStatus.PENDING, interface.OrderStatus.PLACED], 5)

        self.assertIsNotNone(get_market_orders_response)

    def test_unsuccessful_get_market_orders(self):
        self.client.api_id = FIXTURE_BAD_API_ID
        with self.assertRaises(RequestException):
            self.client.get_market_orders(FIXTURE_INSTRUMENT_ID)


class TestTradeApiGetTradesHistory(TestTradeApi):
    def test_successful_get_trades_history_without_filter(self):
        get_trades_history_response = self.client.get_trades_history()
        self.assertIsNotNone(get_trades_history_response)

    def test_successful_get_trades_history_with_filter(self):
        get_trades_history_response = self.client.get_trades_history(
            instrument_id=FIXTURE_INSTRUMENT_ID, sort_by=interface.SortBy.DATE)

        self.assertIsNotNone(get_trades_history_response)

    @skip
    def test_unsuccessful_get_trades_history(self):
        #TODO: Remove skip after BACKEND-1416 task
        self.client.api_id = FIXTURE_BAD_API_ID
        with self.assertRaises(RequestException):
            self.client.get_trades_history()


class TestTradeApiGetLatestPrice(TestTradeApi):
    def test_successful_get_trades_history_without_filter(self):
        get_latest_price_response = self.client.get_latest_price(FIXTURE_INSTRUMENT_ID)
        self.assertIsNotNone(get_latest_price_response)
        self.assertTrue(isinstance(get_latest_price_response, decimal.Decimal))

    def test_successful_get_trades_history_with_filter(self):
        get_latest_price_response = self.client.get_latest_price(instrument_id=FIXTURE_INSTRUMENT_ID)
        self.assertIsNotNone(get_latest_price_response)

    @skip
    def test_unsuccessful_get_trades_history(self):
        #TODO: Remove skip after BACKEND-1416 task
        self.client.api_id = FIXTURE_BAD_API_ID
        with self.assertRaises(RequestException):
            self.client.get_latest_price(FIXTURE_INSTRUMENT_ID)


class TestTradeApiCreateOrder(TestTradeApi):
    def test_successful_create_order(self):
        instrument = self.client.get_trader_instruments()[0]
        self.client.create_order(interface.OfferType.BID, interface.OrderType.LIMIT,
                                 instrument['id'], 5.2, 0.3)

    def test_unsuccessful_create_order(self):
        with self.assertRaises(RequestException):
            self.client.create_order(interface.OfferType.BID, interface.OrderType.LIMIT,
                                     -1, 5.2, 0.3)


class TestTradeApiCancelOrder(TestTradeApi):
    def test_successful_cancel_order(self):
        instrument = self.client.get_trader_instruments()[0]
        self.client.create_order(interface.OfferType.BID, interface.OrderType.LIMIT,
                                 instrument['id'],
                                 5.2, 0.3)

        # Gets orders in statuses Pending, Placed or PartiallyExecuted
        orders = self.client.get_orders(
            instrument['id'],
            status=[interface.OrderStatus.PENDING, interface.OrderStatus.PLACED, interface.OrderStatus.PARTEXECUTED],
            max_count=1)

        if orders:
            self.client.cancel_order(orders[0]['orderID'])

    def test_unsuccessful_cancel_order(self):
        with self.assertRaises(RequestException):
            self.client.cancel_order(-1)


class TestTradeApiCancelAllOrders(TestTradeApi):
    def test_successful_cancel_all_orders(self):
        self.client.cancel_all_orders(FIXTURE_INSTRUMENT_ID)

    def test_unsuccessful_cancel_all_orders(self):
        with self.assertRaises(RequestException):
            self.client.cancel_all_orders('')


class TestTradeApiGetTraderInstruments(TestTradeApi):
    def test_successful_get_trader_instruments(self):
        get_trader_instruments_response = self.client.get_trader_instruments()

        self.assertIsNotNone(get_trader_instruments_response)
        self.assertGreater(len(get_trader_instruments_response), 0)

    def test_unsuccessful_get_trader_instruments(self):
        self.client.password = FIXTURE_BAD_PASSWORD
        with self.assertRaises(RequestException):
            self.client.get_trader_instruments()


class TestTradeApiGetPartnerInstruments(TestTradeApi):
    def test_successful_get_partner_instruments(self):
        response = self.client.get_partner_instruments()

        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)

    def test_unsuccessful_get_partner_instruments(self):
        self.client.api_id = FIXTURE_BAD_API_ID
        with self.assertRaises(RequestException):
            self.client.get_partner_instruments()

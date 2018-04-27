import os
from unittest import TestCase

from blockex.tradeapi import interface
from blockex.tradeapi.tradeapi import BlockExTradeApi
from requests import RequestException

FIXTURE_BAD_PASSWORD = 'BadPassword'
FIXTURE_BAD_API_ID = '67935ee1-7c36-4367-843a-0c66d92bea0d'
FIXTURE_INSTRUMENT_ID = 1


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
        get_market_orders_response = self.client.get_market_orders(1)

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
            self.client.get_market_orders(1)


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
        self.client.cancel_all_orders(1)

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

from unittest import TestCase
import test_integration_config
from requests import RequestException
from blockex.tradeapi import BlockExTradeApi
from blockex.tradeapi import OrderType
from blockex.tradeapi import OfferType


# Integration tests
class TestTradeApi(TestCase):
    def setUp(self):
        if not test_integration_config.API_URL:
            raise ValueError(
                'api_url must be set. Check test_integration_config.py.')
        if not test_integration_config.API_ID:
            raise ValueError(
                'api_id must be set. Check test_integration_config.py.')
        if not test_integration_config.USERNAME:
            raise ValueError(
                'username must be set. Check test_integration_config.py.')
        if not test_integration_config.PASSWORD:
            raise ValueError(
                'password must be set. Check test_integration_config.py.')

        self.trade_api = BlockExTradeApi(
            test_integration_config.API_URL,
            test_integration_config.API_ID,
            test_integration_config.USERNAME,
            test_integration_config.PASSWORD)


class TestTradeApiLoginLogout(TestTradeApi):
    def test_authorized_login(self):
        login_response = self.trade_api.login()
        self.assertIsNotNone(login_response)

    def test_unauthorized_login(self):
        self.trade_api.password = 'WrongPassword'

        with self.assertRaises(RequestException):
            self.trade_api.login()

    def test_logout(self):
        self.trade_api.login()
        self.assertIsNotNone(self.trade_api.access_token)

        self.trade_api.logout()

        self.assertIsNone(self.trade_api.access_token)


class TestTradeApiGetOrders(TestTradeApi):
    def test_successful_get_orders_without_filter(self):
        get_orders_response = self.trade_api.get_orders()

        self.assertIsNotNone(get_orders_response)

    def test_successful_get_orders_with_filter(self):
        get_orders_response = self.trade_api.get_orders(
            1, OrderType.LIMIT, OfferType.BID, '10,20', True, 50)

        self.assertIsNotNone(get_orders_response)

    def test_unsuccessful_get_orders(self):
        self.trade_api.password = 'WrongPassword'

        with self.assertRaises(RequestException):
            self.trade_api.get_orders()


class TestTradeApiGetMarketOrders(TestTradeApi):
    def test_successful_get_market_orders_without_filter(self):
        get_market_orders_response = self.trade_api.get_market_orders(1)

        self.assertIsNotNone(get_market_orders_response)

    def test_successful_get_market_orders_with_filter(self):
        get_market_orders_response = self.trade_api.get_market_orders(
            1, OrderType.LIMIT, OfferType.BID, '10,20', 5)

        self.assertIsNotNone(get_market_orders_response)

    def test_unsuccessful_get_market_orders(self):
        self.trade_api.api_id = 'WrongApiID'

        with self.assertRaises(RequestException):
            self.trade_api.get_market_orders(1)


class TestTradeApiCreateOrder(TestTradeApi):
    def test_successful_create_order(self):
        instrument = self.trade_api.get_trader_instruments()[0]
        self.trade_api.create_order(OfferType.BID,
                                    OrderType.LIMIT,
                                    instrument['id'],
                                    5.2,
                                    0.3)

    def test_unsuccessful_create_order(self):
        with self.assertRaises(RequestException):
            self.trade_api.create_order(OfferType.BID,
                                        OrderType.LIMIT,
                                        -1,
                                        5.2,
                                        0.3)


class TestTradeApiCancelOrder(TestTradeApi):
    def test_successful_cancel_order(self):
        instrument = self.trade_api.get_trader_instruments()[0]
        self.trade_api.create_order(OfferType.BID,
                                    OrderType.LIMIT,
                                    instrument['id'],
                                    5.2,
                                    0.3)

        # Gets orders in statuses Pending, Placed or PartiallyExecuted
        orders = self.trade_api.get_orders(
            instrument['id'], status='10,20,50', max_count=1)
        if orders.__len__() > 0:
            self.trade_api.cancel_order(orders[0]['orderID'])

    def test_unsuccessful_cancel_order(self):
        with self.assertRaises(RequestException):
            self.trade_api.cancel_order(-1)


class TestTradeApiCancelAllOrders(TestTradeApi):
    def test_successful_cancel_all_orders(self):
        self.trade_api.cancel_all_orders(1)

    def test_unsuccessful_cancel_all_orders(self):
        with self.assertRaises(RequestException):
            self.trade_api.cancel_all_orders('')


class TestTradeApiGetTraderInstruments(TestTradeApi):
    def test_successful_get_trader_instruments(self):
        get_trader_instruments_response =\
            self.trade_api.get_trader_instruments()

        self.assertIsNotNone(get_trader_instruments_response)
        self.assertGreater(
            get_trader_instruments_response.__len__(), 0)

    def test_unsuccessful_get_trader_instruments(self):
        self.trade_api.password = 'WrongPassword'
        with self.assertRaises(RequestException):
            self.trade_api.get_trader_instruments()


class TestTradeApiGetPartnerInstruments(TestTradeApi):
    def test_successful_get_partner_instruments(self):
        get_partner_instruments_response =\
            self.trade_api.get_partner_instruments()

        self.assertIsNotNone(get_partner_instruments_response)
        self.assertGreater(
            get_partner_instruments_response.__len__(), 0)

    def test_unsuccessful_get_partner_instruments(self):
        self.trade_api.api_id = 'WrongApiID'
        with self.assertRaises(RequestException):
            self.trade_api.get_partner_instruments()

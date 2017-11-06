import test_integration_config
from unittest import TestCase
from BlockExTradeApi import BlockExTradeApi


# Integration tests
class TestTradeApi(TestCase):
    def setUp(self):
        if not test_integration_config.api_url:
            raise ValueError('The API URL must be set. Check test_integration_config.py.')
        if not test_integration_config.api_id:
            raise ValueError('The API ID must be set. Check test_integration_config.py.')
        if not test_integration_config.username:
            raise ValueError('The Trader''s username must be set. Check test_integration_config.py.')
        if not test_integration_config.password:
            raise ValueError('The Trader''s password must be set. Check test_integration_config.py.')

        self.trade_api = BlockExTradeApi(
            test_integration_config.api_url,
            test_integration_config.api_id,
            test_integration_config.username,
            test_integration_config.password)


class TestTradeApiLoginLogout(TestTradeApi):
    def test_authorized_login(self):
        login_response = self.trade_api.login()

        self.assertIn('response', login_response)
        self.assertEqual(login_response['response'].status_code, 200)

        self.assertIn('access_token', login_response)

    def test_unauthorized_login(self):
        self.trade_api.password = 'WrongPassword'
        login_response = self.trade_api.login()

        self.assertIn('response', login_response)
        self.assertNotEqual(login_response['response'].status_code, 200)

        self.assertNotIn('access_token', login_response)

    def test_logout(self):
        self.trade_api.login()
        self.assertIsNotNone(self.trade_api.access_token)

        logout_response = self.trade_api.logout()

        self.assertIn('response', logout_response)
        self.assertEqual(logout_response['response'].status_code, 200)
        self.assertIsNone(self.trade_api.access_token)


class TestTradeApiGetOrders(TestTradeApi):
    def test_successful_get_orders_without_filter(self):
        get_orders_response = self.trade_api.get_orders()

        self.assertIn('response', get_orders_response)
        self.assertEqual(get_orders_response['response'].status_code, 200)

        self.assertIn('data', get_orders_response)

    def test_successful_get_orders_with_filter(self):
        get_orders_response = self.trade_api.get_orders(
            1, 'Limit', 'Bid', '10,20', 'true', 50)

        self.assertIn('response', get_orders_response)
        self.assertEqual(get_orders_response['response'].status_code, 200)

        self.assertIn('data', get_orders_response)

    def test_unsuccessful_get_orders(self):
        self.trade_api.password = 'WrongPassword'
        get_orders_response = self.trade_api.get_orders()

        self.assertIn('response', get_orders_response)
        self.assertNotEqual(get_orders_response['response'].status_code, 200)

        self.assertNotIn('data', get_orders_response)


class TestTradeApiGetMarketOrders(TestTradeApi):
    def test_successful_get_market_orders_without_filter(self):
        get_market_orders_response = self.trade_api.get_market_orders(1)

        self.assertIn('response', get_market_orders_response)
        self.assertEqual(
            get_market_orders_response['response'].status_code, 200)

        self.assertIn('data', get_market_orders_response)

    def test_successful_get_market_orders_with_filter(self):
        get_market_orders_response = self.trade_api.get_market_orders(
            1, 'Limit', 'Bid', '10,20', 5)

        self.assertIn('response', get_market_orders_response)
        self.assertEqual(
            get_market_orders_response['response'].status_code, 200)

        self.assertIn('data', get_market_orders_response)

    def test_unsuccessful_get_market_orders(self):
        self.trade_api.api_id = 'WrongApiID'
        get_orders_response = self.trade_api.get_market_orders(1)

        self.assertIn('response', get_orders_response)
        self.assertNotEqual(get_orders_response['response'].status_code, 200)

        self.assertNotIn('data', get_orders_response)


class TestTradeApiCreateOrder(TestTradeApi):
    def test_create_order(self):
        instrument = self.trade_api.get_trader_instruments()['data'][0]
        create_order_response = self.trade_api.create_order(
            'Bid', 'Limit', instrument['id'], 5.2, 0.3)

        self.assertIn('response', create_order_response)
        self.assertEqual(create_order_response['response'].status_code, 200)


class TestTradeApiCancelOrder(TestTradeApi):
    def test_cancel_order(self):
        instrument = self.trade_api.get_trader_instruments()['data'][0]
        self.trade_api.create_order('Bid', 'Limit', instrument['id'], 5.2, 0.3)

        # Gets orders in statuses Pending, Placed or PartiallyExecuted
        orders = self.trade_api.get_orders(
            instrument['id'], status='10,20,50', max_count=1)['data']
        if orders.__len__() > 0:
            cancel_order_response =\
                self.trade_api.cancel_order(orders[0]['orderID'])

            self.assertIn('response', cancel_order_response)
            self.assertEqual(
                cancel_order_response['response'].status_code, 200)


class TestTradeApiCancelAllOrders(TestTradeApi):
    def test_cancel_all_orders(self):
        cancel_all_orders_response = self.trade_api.cancel_all_orders(1)

        self.assertIn('response', cancel_all_orders_response)
        self.assertEqual(
            cancel_all_orders_response['response'].status_code, 200)


class TestTradeApiGetTraderInstruments(TestTradeApi):
    def test_successful_get_trader_instruments(self):
        get_trader_instruments_response =\
            self.trade_api.get_trader_instruments()

        self.assertIn('response', get_trader_instruments_response)
        self.assertEqual(
            get_trader_instruments_response['response'].status_code, 200)

        self.assertIn('data', get_trader_instruments_response)
        self.assertGreater(
            get_trader_instruments_response['data'].__len__(), 0)

    def test_unsuccessful_get_trader_instruments(self):
        self.trade_api.password = 'WrongPassword'
        get_trader_instruments_response =\
            self.trade_api.get_trader_instruments()

        self.assertIn('response', get_trader_instruments_response)
        self.assertNotEqual(
            get_trader_instruments_response['response'].status_code, 200)

        self.assertNotIn('data', get_trader_instruments_response)


class TestTradeApiGetPartnerInstruments(TestTradeApi):
    def test_successful_get_partner_instruments(self):
        get_partner_instruments_response =\
            self.trade_api.get_partner_instruments()

        self.assertIn('response', get_partner_instruments_response)
        self.assertEqual(
            get_partner_instruments_response['response'].status_code, 200)

        self.assertIn('data', get_partner_instruments_response)
        self.assertGreater(
            get_partner_instruments_response['data'].__len__(), 0)

    def test_unsuccessful_get_partner_instruments(self):
        self.trade_api.api_id = 'WrongApiID'
        get_partner_instruments_response =\
            self.trade_api.get_partner_instruments()

        self.assertIn('response', get_partner_instruments_response)
        self.assertNotEqual(
            get_partner_instruments_response['response'].status_code, 200)

        self.assertNotIn('data', get_partner_instruments_response)

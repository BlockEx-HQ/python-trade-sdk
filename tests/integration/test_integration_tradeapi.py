import decimal

import pytest

import arrow
from requests import RequestException

from blockex.tradeapi import interface

FIXTURE_BAD_PASSWORD = 'BadPassword'
FIXTURE_BAD_API_ID = 'xxx'
FIXTURE_INSTRUMENT_ID = 4


@pytest.mark.usefixtures('client')
class TestTradeApiLoginLogout:
    def test_authorized_login(self):
        login_response = self.client.login()
        assert login_response is not None

    def test_unauthorized_login(self):
        self.client.password = FIXTURE_BAD_PASSWORD
        with pytest.raises(RequestException):
            self.client.login()

    def test_logout(self):
        self.client.login()
        assert self.client.access_token is not None

        self.client.logout()
        assert self.client.access_token is None


@pytest.mark.usefixtures('client')
class TestTradeApiInfo:

    @pytest.fixture(autouse=True)
    def trade_info_struct(self):
        self.trade_type_check = {'traderID': str,
                                 'firstName': str,
                                 'lastName': str,
                                 'username': str,
                                 'email': str,
                                 'registrationDate': str,
                                 'currency': str,
                                 'currencyID': int,
                                 'language': str,
                                 'languageID': int,
                                 'country': str,
                                 'countryID': int,
                                 'currenciesTotals': list}

        self.trade_info_currency = {'currencyID': int,
                                    'currencyName': str,
                                    'isCrypto': bool,
                                    'realBalance': decimal.Decimal,
                                    'availableBalance': decimal.Decimal,
                                    'avgBuyPrice': decimal.Decimal,
                                    'totalPortfolioValue': decimal.Decimal}

    def test_successful_get_trade_info(self):
        get_trade_info_response = self.client.get_trader_info()
        assert get_trade_info_response is not None

        for key, val_type in self.trade_type_check.items():
            assert isinstance(get_trade_info_response.get(key), val_type)

        for currency in get_trade_info_response['currenciesTotals']:
            for key, val_type in self.trade_info_currency.items():
                assert isinstance(currency.get(key), val_type)

    def test_unsuccessful_get_trade_info(self):
        self.client.password = FIXTURE_BAD_PASSWORD
        with pytest.raises(RequestException):
            self.client.get_trader_info()


@pytest.mark.usefixtures('client')
class TestTradeApiGetOrders:
    def test_successful_get_orders_without_filter(self):
        get_orders_response = self.client.get_orders()
        assert get_orders_response is not None

    def test_successful_get_orders_with_filter(self):
        get_orders_response = self.client.get_orders(
            FIXTURE_INSTRUMENT_ID,
            interface.OrderType.LIMIT, interface.OfferType.BID,
            [interface.OrderStatus.PENDING, interface.OrderStatus.PLACED],
            True, 50)

        assert get_orders_response is not None

    def test_unsuccessful_get_orders(self):
        self.client.password = FIXTURE_BAD_PASSWORD
        with pytest.raises(RequestException):
            self.client.get_orders()


@pytest.mark.usefixtures('client')
class TestTradeApiGetMarketOrders:
    def test_successful_get_market_orders_without_filter(self):
        get_market_orders_response = self.client.get_market_orders(FIXTURE_INSTRUMENT_ID)
        assert get_market_orders_response is not None

    def test_successful_get_market_orders_with_filter(self):
        get_market_orders_response = self.client.get_market_orders(
            FIXTURE_INSTRUMENT_ID,
            interface.OrderType.LIMIT, interface.OfferType.BID,
            [interface.OrderStatus.PENDING, interface.OrderStatus.PLACED], 5)

        assert get_market_orders_response is not None

    def test_unsuccessful_get_market_orders(self):
        self.client.api_id = FIXTURE_BAD_API_ID
        with pytest.raises(RequestException):
            self.client.get_market_orders(FIXTURE_INSTRUMENT_ID)


@pytest.mark.usefixtures('client')
class TestTradeApiGetTradesHistory:
    @pytest.fixture(autouse=True)
    def trade_history_struct(self):
        self.trade_type_check = {'tradeID': int,
                                 'price': decimal.Decimal,
                                 'totalPrice': decimal.Decimal,
                                 'quantity': decimal.Decimal,
                                 'tradeDate': str,
                                 'currencyID': int,
                                 'quoteCurrencyID': int,
                                 'instrumentID': int}

    def test_successful_get_trades_history_without_filter(self):
        get_trades_history_response = self.client.get_trades_history()
        assert get_trades_history_response is not None

        trades = get_trades_history_response['trades']
        assert len(trades) == 10
        for trade in trades:
            for key, val_type in self.trade_type_check.items():
                assert isinstance(trade.get(key), val_type)

    def test_successful_get_trades_history_with_filter(self):
        prev_trade_date = None

        get_trades_history_response = self.client.get_trades_history(
            instrument_id=FIXTURE_INSTRUMENT_ID, sort_by=interface.SortBy.DATE)

        assert get_trades_history_response is not None
        trades = get_trades_history_response['trades']
        assert len(trades) == 10
        for trade in trades:
            for key, val_type in self.trade_type_check.items():
                assert isinstance(trade.get(key), val_type)
            if prev_trade_date is None:
                prev_trade_date = arrow.get(trade.get('tradeDate')).datetime

            assert prev_trade_date <= arrow.get(trade.get('tradeDate')).datetime
            prev_trade_date = arrow.get(trade.get('tradeDate')).datetime

    @pytest.mark.skip(reason="blocked by BACKEND-1416 task")
    def test_unsuccessful_get_trades_history(self):
        #TODO: Remove skip after BACKEND-1416 task
        self.client.api_id = FIXTURE_BAD_API_ID
        with pytest.raises(RequestException):
            self.client.get_trades_history()


@pytest.mark.usefixtures('client')
class TestTradeApiGetLatestPrice:
    def test_successful_get_trades_history_without_filter(self):
        get_latest_price_response = self.client.get_latest_price(FIXTURE_INSTRUMENT_ID)
        assert get_latest_price_response is not None
        assert isinstance(get_latest_price_response, decimal.Decimal)

    def test_successful_get_trades_history_with_filter(self):
        get_latest_price_response = self.client.get_latest_price(instrument_id=FIXTURE_INSTRUMENT_ID)
        assert get_latest_price_response is not None

    @pytest.mark.skip(reason="blocked by BACKEND-1416 task")
    def test_unsuccessful_get_trades_history(self):
        #TODO: Remove skip after BACKEND-1416 task
        self.client.api_id = FIXTURE_BAD_API_ID
        with pytest.raises(RequestException):
            self.client.get_latest_price(FIXTURE_INSTRUMENT_ID)


@pytest.mark.usefixtures('client')
class TestTradeApiCreateOrder:
    def test_successful_create_order(self):
        instrument = self.client.get_trader_instruments()[0]
        self.client.create_order(interface.OfferType.BID, interface.OrderType.LIMIT,
                                 instrument['id'], 5.2, 0.3)

    def test_unsuccessful_create_order(self):
        with pytest.raises(RequestException):
            self.client.create_order(interface.OfferType.BID, interface.OrderType.LIMIT,
                                     -1, 5.2, 0.3)


@pytest.mark.usefixtures('client')
class TestTradeApiCancelOrder:
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
        with pytest.raises(RequestException):
            self.client.cancel_order(-1)


@pytest.mark.usefixtures('client')
class TestTradeApiCancelAllOrders:
    def test_successful_cancel_all_orders(self):
        self.client.cancel_all_orders(FIXTURE_INSTRUMENT_ID)

    def test_unsuccessful_cancel_all_orders(self):
        with pytest.raises(RequestException):
            self.client.cancel_all_orders('')


@pytest.mark.usefixtures('client')
class TestTradeApiGetTraderInstruments:
    def test_successful_get_trader_instruments(self):
        get_trader_instruments_response = self.client.get_trader_instruments()

        assert get_trader_instruments_response is not None
        assert len(get_trader_instruments_response) > 0

    def test_unsuccessful_get_trader_instruments(self):
        self.client.password = FIXTURE_BAD_PASSWORD
        with pytest.raises(RequestException):
            self.client.get_trader_instruments()


@pytest.mark.usefixtures('client')
class TestTradeApiGetPartnerInstruments:
    def test_successful_get_partner_instruments(self):
        response = self.client.get_partner_instruments()

        assert response is not None
        assert len(response) > 0

    def test_unsuccessful_get_partner_instruments(self):
        self.client.api_id = FIXTURE_BAD_API_ID
        with pytest.raises(RequestException):
            self.client.get_partner_instruments()

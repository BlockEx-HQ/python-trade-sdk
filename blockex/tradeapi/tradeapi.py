"""BlockEx Trade API client library"""

import decimal
import sys
from operator import itemgetter

from blockex.tradeapi import interface

from .auth import Auth
from .helper import DictConditional, get_error_message, head, message_raiser

if sys.version_info >= (3, 0):
    from urllib.parse import urlencode  # pragma: no cover
else:
    from urllib import urlencode  # pragma: no cover


class BlockExTradeApi(Auth):
    """BlockEx Trade API wrapper"""

    def __init__(self, username, password, api_url=None, api_id=None):
        self._open_orders = set()

        Auth.__init__(self, username, password, api_url, api_id)

    def get_orders(self,
                   instrument_id=None,
                   order_type=None,
                   offer_type=None,
                   status=None,
                   load_executions=None,
                   max_count=None):
        """Gets the orders of the trader with the ability to apply filters.

        :param instrument_id: Instrument ID. Use get_trader_instruments()
            to retrieve list of available instruments and their IDs. Optional.
        :type instrument_id: int
        :param order_type: Order type. Optional.
        :type order_type: OrderType
        :param offer_type: Offer type. Optional.
        :type offer_type: OfferType
        :param status: Order status. List of OrderStatus values. Optional.
        :type status: list
        :param load_executions: Sets whether to load executed trades for an order.
            Defaults to False. Optional.
        :type load_executions: boolean
        :param max_count: Maximum number of items returned. Default value is 100. Optional.
        :type max_count: int
        :returns: The list of orders.
        :rtype: list of dicts. Each element has the following data:\n
            orderID (string)\n
            price (float)\n
            initialQuantity (float)\n
            quantity (float)\n
            dateCreated (string)\n
            offerType (int) - Possible values 1 (Bid) and 2 (Ask).\n
            type (int) - Possible values 1 (Limit), 2 (Market) and 3 (Stop).\n
            status (int) - Possible values 10 (Pending), 15 (Failed),
            20 (Placed), 30 (Rejected), 40 (Cancelled), 50 (PartiallyExecuted)
            and 60 (Executed).\n
            instrumentID (int)\n
            trades (list of dict)
        :raises: requests.RequestException

        """

        data = DictConditional()
        data['instrumentID'] = instrument_id
        data['loadExecutions'] = load_executions
        data['maxCount'] = max_count

        if order_type is not None:
            if not isinstance(order_type, interface.OrderType):
                raise ValueError('order_type must be of type OrderType')
            data['orderType'] = order_type.value
        if offer_type is not None:
            if not isinstance(offer_type, interface.OfferType):
                raise ValueError('offer_type must be of type OfferType')
            data['offerType'] = offer_type.value
        if status is not None:
            status_values = []
            for item in status:
                assert isinstance(item, interface.OrderStatus)
                status_values.append(item.value)
            data['status'] = ','.join(status_values)

        query_string = urlencode(data)
        response = self.make_authorized_request(self.get_path, interface.ApiPath.GET_ORDERS.value + query_string)

        if response.status_code != interface.SUCCESS:
            message_raiser('Failed to get the orders. {error_message}',
                           error_message=get_error_message(response))

        orders = response.json()
        for order in orders:
            convert_order_numbers(order)
        return orders

    def get_market_orders(self, instrument_id,
                          order_type=None,
                          offer_type=None,
                          status=None,
                          max_count=None):
        """Gets the market orders with the ability to apply filters.

        :param instrument_id: Instrument identifier. Use get_trader_instruments()
            to retrieve list of available instruments and their IDs. Optional.
        :type instrument_id: int
        :param order_type: Order type. Optional.
        :type order_type: OrderType
        :param offer_type: Offer type. Optional.
        :type offer_type: OfferType
        :param status: Order status, list of OrderStatus values. Optional.
        :type status: list
        :param max_count: Maximum number of items returned. Default value is 100. Optional.
        :type max_count: int
        :returns: The list of orders.
        :rtype: list of dicts. Each element has the following data:\n
            orderID (string)\n
            price (float)\n
            initialQuantity (float)\n
            quantity (float)\n
            dateCreated (string)\n
            offerType (int) - Possible values 1 (Bid) and 2 (Ask).\n
            type (int) - Possible values 1 (Limit), 2 (Market) and 3 (Stop).\n
            status (int) - Possible values 10 (Pending), 15 (Failed),
            20 (Placed), 30 (Rejected), 40 (Cancelled), 50 (PartiallyExecuted)
            and 60 (Executed).\n
            instrumentID (int)\n
            trades (list of dict)
        :raises: requests.RequestException

        """

        data = DictConditional(apiID=self.api_id, instrumentID=instrument_id)
        data['maxCount'] = max_count

        if order_type is not None:
            if not isinstance(order_type, interface.OrderType):
                raise ValueError('order_type must be of type OrderType')
            data['orderType'] = order_type.value
        if offer_type is not None:
            if not isinstance(offer_type, interface.OfferType):
                raise ValueError('offer_type must be of type OfferType')
            data['offerType'] = offer_type.value
        if status is not None:
            status_values = []
            for item in status:
                assert isinstance(item, interface.OrderStatus)
                status_values.append(item.value)
            data['status'] = ','.join(status_values)

        query_string = urlencode(data)
        response = self.get_path(interface.ApiPath.GET_MARKET_ORDERS.value + query_string)
        if response.status_code != interface.SUCCESS:
            message_raiser('Failed to get the market orders. {error_message}',
                           error_message=get_error_message(response))

        orders = response.json()
        for order in orders:
            convert_order_numbers(order)
        return orders

    def get_latest_price(self, instrument_id):
        """Gets latest trade price for given instrument.

        :param instrument_id: Instrument identifier. Use get_trader_instruments()
            to retrieve list of available instruments and their IDs. Optional.
        :type instrument_id: int

        """

        data = {
            'ApiID': self.api_id,
            'InstrumentID': instrument_id,
            "SortDesc": "true",
            "SortBy": "date",
            "PageSize": "1",
        }

        #TODO: querying full history is a silly way to retrieve latest price
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        response = self.post_path(interface.ApiPath.GET_TRADES_HISTORY.value, data=urlencode(data), headers=headers)

        if response.status_code != interface.SUCCESS:
            message_raiser('Failed to get the market latest price. {error_message}',
                           error_message=get_error_message(response))

        trades = response.json()
        return head(trades.get('trades'), default=[]).get('price')

    def get_highest_bid_order(self, instrument_id):
        """Gets highest bid price for given instrument.

        :param instrument_id: Instrument identifier. Use get_trader_instruments()
            to retrieve list of available instruments and their IDs. Optional.
        :type instrument_id: int

        """

        #TODO: we'll be in trouble once we have more than 1000 orders at once
        orders = self.get_market_orders(instrument_id, max_count=1000,
                                        status=[interface.OrderStatus.PLACED],
                                        offer_type=interface.OfferType.BID)

        highest_order = max(orders, key=itemgetter('price')) if orders else {}
        return highest_order

    def get_lowest_ask_order(self, instrument_id):
        """Gets lowest ask price for given instrument.

        :param instrument_id: Instrument identifier. Use get_trader_instruments()
            to retrieve list of available instruments and their IDs. Optional.
        :type instrument_id: int

        """

        #TODO: we'll be in trouble once we have more than 1000 orders at once
        orders = self.get_market_orders(instrument_id, max_count=1000,
                                        status=[interface.OrderStatus.PLACED],
                                        offer_type=interface.OfferType.ASK)

        lowest_order = min(orders, key=itemgetter('price')) if orders else {}
        return lowest_order

    def create_order(self, offer_type, order_type, instrument_id, price, quantity):
        """Places an order.

        :param offer_type: Offer type.
        :type offer_type: OfferType
        :param order_type: Order type.
        :type order_type: OrderType
        :param instrument_id: Instrument ID. Use get_trader_instruments()
            to retrieve list of available instruments and their IDs.
        :type instrument_id: int
        :param price: Price
        :type price: float
        :param quantity: Quantity
        :type quantity: float
        :raises: requests.RequestException

        """

        if not isinstance(order_type, interface.OrderType):
            raise ValueError('order_type must be of type OrderType')

        if not isinstance(offer_type, interface.OfferType):
            raise ValueError('offer_type must be of type OfferType')

        data = {
            'offerType': offer_type.value,
            'orderType': order_type.value,
            'instrumentID': instrument_id,
            'price': price,
            'quantity': quantity
        }

        query_string = urlencode(data)
        response = self.make_authorized_request(self.post_path, interface.ApiPath.CREATE_ORDER.value + query_string)

        if response.status_code != interface.SUCCESS:
            message_raiser('Failed to create an order. {error_message}',
                           error_message=get_error_message(response))

        orders = self.get_orders(status=[interface.OrderStatus.PENDING,
                                         interface.OrderStatus.PLACED,
                                         interface.OrderStatus.PARTEXECUTED],
                                 load_executions=False)

        # Order by date return last order ID
        order_set = set(order['orderID'] for order in orders)
        self._open_orders = order_set

    def cancel_order(self, order_id):
        """Cancels a specific order.

        :param order_id: Order identifier
        :type order_id: int
        :raises: requests.RequestException

        """

        data = {'orderID': order_id}
        query_string = urlencode(data)
        response = self.make_authorized_request(self.post_path, interface.ApiPath.CANCEL_ORDER.value + query_string)

        if response.status_code != interface.SUCCESS:
            message_raiser('Failed to cancel the order. {error_message}',
                           error_message=get_error_message(response))

        self._open_orders.discard(order_id)


    def cancel_all_orders(self, instrument_id):
        """Cancels all the orders of the trader for a specific instrument.

        :param instrument_id: Instrument identifier.
            Use get_trader_instruments() to retrieve them.\n
        :type instrument_id: int
        :raises: requests.RequestException

        """

        data = {'instrumentID': instrument_id}
        query_string = urlencode(data)
        response = self.make_authorized_request(self.post_path,
                                                interface.ApiPath.CANCEL_ALL_ORDERS.value + query_string)

        if response.status_code != interface.SUCCESS:
            message_raiser('Failed to cancel all orders. {error_message}',
                           error_message=get_error_message(response))

    def get_trader_instruments(self):
        """Gets the available instruments for the trader.

        :returns: The list of instruments.
        :rtype: list of dicts. Each element has the following data:\n
            id (int)\n
            description (string)\n
            name (string)\n
            baseCurrencyID (int) - The currency you bid for, i.e. for the
            Bitcoin/Euro base currency is the Bitcoin.\n
            quoteCurrencyID (int) - The currency you pay with, i.e. for the
            Bitcoin/Euro quote currency is the Euro.\n
            minOrderAmount (float) - The minimum order amount for an order.
            Every order having an amount less than that, will be rejected.\n
            commissionFeePercent (float) - The percent of the commission
            fee when trading this instrument. The value is a decimal between 0 and 1.
        :raises: requests.RequestException

        """

        response = self.make_authorized_request(self.get_path, interface.ApiPath.GET_TRADER_INSTRUMENTS.value)
        if response.status_code == interface.SUCCESS:
            instruments = response.json()
            for instrument in instruments:
                convert_instrument_numbers(instrument)
            return instruments

        message_raiser('Failed to get the trader instruments. {error_message}',
                       error_message=get_error_message(response))

    def get_partner_instruments(self):
        """Gets the available instruments for the partner.

        :returns: The list of instruments.
        :rtype: list of dicts. Each element has the following data:\n
            id (int)\n
            description (string)\n
            name (string)\n
            baseCurrencyID (int) - The currency you bid for, i.e. for the
            Bitcoin/Euro base currency is the Bitcoin.\n
            quoteCurrencyID (int) - The currency you pay with, i.e. for the
            Bitcoin/Euro quote currency is the Euro.\n
            minOrderAmount (float) - The minimum order amount for an order.
            Every order having an amount less than that, will be rejected.\n
            commissionFeePercent (float) - The percent of the commission fee
            when trading this instrument The value is a decimal between 0 and 1.\n
        :raises: requests.RequestException

        """

        data = {'apiID': self.api_id}
        query_string = urlencode(data)
        response = self.get_path(interface.ApiPath.GET_PARTNER_INSTRUMENTS.value + query_string)
        if response.status_code != interface.SUCCESS:
            message_raiser('Failed to get the partner instruments. {error_message}',
                           error_message=get_error_message(response))

        instruments = response.json()
        for instrument in instruments:
            convert_instrument_numbers(instrument)
        return instruments


def convert_instrument_numbers(instrument):
    """
    Cast minOrderAmount value to Decimal

    :param instrument: dict
    :return: dict
    """

    context = decimal.getcontext()
    instrument['minOrderAmount'] = context.create_decimal(instrument['minOrderAmount'])


def convert_order_numbers(order):
    """
    Cast incoming values to int or Decimal

    :param order: dict
    :return: dict

    """

    context = decimal.getcontext()
    order['orderID'] = int(order['orderID'])
    order['initialQuantity'] = context.create_decimal(order['initialQuantity'])
    order['price'] = context.create_decimal(order['price'])
    order['quantity'] = context.create_decimal(order['quantity'])

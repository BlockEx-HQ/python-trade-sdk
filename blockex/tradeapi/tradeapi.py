"""BlockEx Trade API client library"""
import datetime
import decimal
from urllib.parse import urlencode
import requests

from blockex.tradeapi import C


class BlockExTradeApi(object):
    """BlockEx Trade API wrapper"""

    def __init__(self, username, password, api_url=None, api_id=None):
        assert username
        assert password

        self.api_url = api_url if api_url else C.DEFAULT_API_URL
        self.api_id = api_id if api_id else C.DEFAULT_API_URL
        self.username = username
        self.password = password
        self.access_token = None
        self.access_token_expires = None

    def get_access_token(self):
        """Gets the access token."""
        data = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'client_id': self.api_id
        }

        response = requests.post(f"{self.api_url}{C.ApiPath.LOGIN.value}", data=data)
        if response.status_code == C.SUCCESS:
            return response.json()
        else:
            exception_message = 'Login failed. {error_message}'.format(
                error_message=get_error_message(response))
            raise requests.RequestException(exception_message)

    def login(self):
        """
        Performs a login and stores the received access token.

        :returns: The access token of the logged in trader
        :rtype: dict
        :raises: requests.RequestException
        """

        access_token = self.get_access_token()
        self.access_token = access_token['access_token']
        self.access_token_expires = datetime.datetime.now() +\
            datetime.timedelta(seconds=access_token['expires_in'])
        return self.access_token

    def logout(self):
        """
        Performs a logout when logged in and deletes the stored access token.

        :raises: requests.RequestException
        """

        if self.access_token is not None:
            headers = {'Authorization': 'Bearer ' + self.access_token}
            response = requests.post(
                f"{self.api_url}{C.ApiPath.LOGOUT.value}",
                headers=headers)
            if response.status_code == C.SUCCESS:
                self.access_token = None
            else:
                exception_message = 'Logout failed. {error_message}'.format(
                    error_message=get_error_message(response))
                raise requests.RequestException(exception_message)

    def get_orders(
            self,
            instrument_id=None,
            order_type=None,
            offer_type=None,
            status=None,
            load_executions=None,
            max_count=None):
        """
        Gets the orders of the trader with the ability to apply filters.

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
        data = {}
        if instrument_id is not None:
            data['instrumentID'] = instrument_id
        if order_type is not None:
            if not isinstance(order_type, C.OrderType):
                raise ValueError('order_type must be of type OrderType')
            data['orderType'] = order_type.value
        if offer_type is not None:
            if not isinstance(offer_type, C.OfferType):
                raise ValueError('offer_type must be of type OfferType')
            data['offerType'] = offer_type.value
        if status is not None:
            status_values = []
            for item in status:
                assert isinstance(item, C.OrderStatus)
                status_values.append(item.value)
            data['status'] = ','.join(status_values)
        if load_executions is not None:
            data['loadExecutions'] = load_executions
        if max_count is not None:
            data['maxCount'] = max_count

        query_string = urlencode(data)
        response = self._make_authorized_request(
            'get', f"{self.api_url}{C.ApiPath.GET_ORDERS.value}{query_string}")

        if response.status_code == C.SUCCESS:
            orders = response.json()
            for order in orders:
                convert_order_numbers(order)
            return orders
        else:
            exception_message = 'Failed to get the orders. {error_message}'.format(
                error_message=get_error_message(response))
            raise requests.RequestException(exception_message)

    def get_market_orders(
            self,
            instrument_id,
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
        data = {
            'apiID': self.api_id,
            'instrumentID': instrument_id
        }
        if order_type is not None:
            if not isinstance(order_type, C.OrderType):
                raise ValueError('order_type must be of type OrderType')
            data['orderType'] = order_type.value
        if offer_type is not None:
            if not isinstance(offer_type, C.OfferType):
                raise ValueError('offer_type must be of type OfferType')
            data['offerType'] = offer_type.value
        if status is not None:
            status_values = []
            for item in status:
                assert isinstance(item, C.OrderStatus)
                status_values.append(item.value)
            data['status'] = ','.join(status_values)
        if max_count is not None:
            data['maxCount'] = max_count

        query_string = urlencode(data)
        response = requests.get(f"{self.api_url}{C.ApiPath.GET_MARKET_ORDERS.value}{query_string}")
        if response.status_code == C.SUCCESS:
            orders = response.json()
            for order in orders:
                convert_order_numbers(order)
            return orders
        else:
            exception_message = 'Failed to get the market orders. {error_message}'.format(
                error_message=get_error_message(response))
            raise requests.RequestException(exception_message)

    def create_order(
            self,
            offer_type,
            order_type,
            instrument_id,
            price,
            quantity):
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
        if not isinstance(order_type, C.OrderType):
            raise ValueError('order_type must be of type OrderType')

        if not isinstance(offer_type, C.OfferType):
            raise ValueError('offer_type must be of type OfferType')

        data = {
            'offerType': offer_type.value,
            'orderType': order_type.value,
            'instrumentID': instrument_id,
            'price': price,
            'quantity': quantity
        }

        query_string = urlencode(data)
        response = self._make_authorized_request(
            'post', f"{self.api_url}{C.ApiPath.CREATE_ORDER.value}{query_string}")

        if response.status_code != C.SUCCESS:
            exception_message = 'Failed to create an order. {error_message}'.format(
                error_message=get_error_message(response))
            raise requests.RequestException(exception_message)

    def cancel_order(self, order_id):
        """Cancels a specific order.

        :param order_id: Order identifier
        :type order_id: int
        :raises: requests.RequestException
        """
        data = {'orderID': order_id}
        query_string = urlencode(data)
        response = self._make_authorized_request(
            'post', f"{self.api_url}{C.ApiPath.CANCEL_ORDER.value}{query_string}")

        if response.status_code != C.SUCCESS:
            exception_message = 'Failed to cancel the order. {error_message}'.format(
                error_message=get_error_message(response))
            raise requests.RequestException(exception_message)

    def cancel_all_orders(self, instrument_id):
        """Cancels all the orders of the trader for a specific instrument.

        :param instrument_id: Instrument identifier.
        Use get_trader_instruments() to retrieve them.\n
        :type instrument_id: int
        :raises: requests.RequestException
        """
        data = {'instrumentID': instrument_id}
        query_string = urlencode(data)
        response = self._make_authorized_request(
            'post',
            f"{self.api_url}{C.ApiPath.CANCEL_ALL_ORDERS.value}{query_string}")

        if response.status_code != C.SUCCESS:
            exception_message = 'Failed to cancel all orders. {error_message}'.format(
                error_message=get_error_message(response))
            raise requests.RequestException(exception_message)

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
        response = self._make_authorized_request(
            'get', f"{self.api_url}{C.ApiPath.GET_TRADER_INSTRUMENTS.value}")
        if response.status_code == C.SUCCESS:
            instruments = response.json()
            for instrument in instruments:
                convert_instrument_numbers(instrument)
            return instruments
        else:
            exception_message = 'Failed to get the trader instruments. {error_message}'.format(
                error_message=get_error_message(response))
            raise requests.RequestException(exception_message)

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
        response = requests.get(f"{self.api_url}{C.ApiPath.GET_PARTNER_INSTRUMENTS.value}"
                                f"{query_string}")
        if response.status_code == C.SUCCESS:
            instruments = response.json()
            for instrument in instruments:
                convert_instrument_numbers(instrument)
            return instruments
        else:
            exception_message = 'Failed to get the partner instruments. {error_message}'.format(
                error_message=get_error_message(response))
            raise requests.RequestException(exception_message)

    def _make_authorized_request(self, request_type, url):
        request_type = request_type.lower()
        assert request_type in ('get', 'post')

        # Not logged in or the access token has expired
        current_time = datetime.datetime.now()
        if self.access_token is None or self.access_token_expires < current_time:
            self.login()

        bearer = self.access_token if self.access_token else ''
        headers = {'Authorization': f"Bearer {bearer}"}
        method = getattr(requests, request_type)

        response = method(url, headers=headers)

        if is_unauthorized_response(response):
            self.login()
            bearer = self.access_token if self.access_token else ''
            headers = {'Authorization': 'Bearer ' + bearer}
            response = method(url, headers=headers)

        return response


def is_unauthorized_response(response):
    """Checks if a response is unauthorized."""
    if response.status_code == C.UNAUTHORIZED:
        response_content = response.json()
        message = 'Authorization has been denied for this request.'
        if 'message' in response_content:
            if response_content['message'] == message:
                return True

    return False


def get_error_message(response):
    """Gets an error message for a response."""
    response_json = response.json()
    if 'error' in response_json:
        error_message = ' Message: {message}'.format(message=response_json['error'])
    elif 'message' in response_json:
        error_message = ' Message: {message}'.format(message=response_json['message'])
    else:
        error_message = ''

    return error_message


def convert_instrument_numbers(instrument):
    """
    cast minOrderAmount value to Decimal

    :param instrument: dict
    :return: dict
    """
    instrument['minOrderAmount'] = \
        decimal.getcontext().create_decimal(instrument['minOrderAmount'])


def convert_order_numbers(order):
    """
    cast incoming values to int or Decimal

    :param order: dict
    :return: dict
    """
    context = decimal.getcontext()
    order['orderID'] = int(order['orderID'])
    order['initialQuantity'] = context.create_decimal(order['initialQuantity'])
    order['price'] = context.create_decimal(order['price'])
    order['quantity'] = context.create_decimal(order['quantity'])
"""BlockEx Trade API client library"""
from enum import Enum
import datetime
import decimal
import requests
from requests import RequestException
from six.moves.urllib.parse import urlencode


class OrderType(Enum):
    """Order type enumeration"""
    LIMIT = 'Limit'
    MARKET = 'Market'
    STOP = 'Stop'


class OfferType(Enum):
    """Offer type enumeration"""
    BID = 'Bid'
    ASK = 'Ask'


class BlockExTradeApi(object):
    """Implementation of  methods needed to access the BlockEx Trading API"""
    LOGIN_PATH = 'oauth/token'
    LOGOUT_PATH = 'oauth/logout'
    GET_ORDERS_PATH = 'api/orders/get?'
    GET_MARKET_ORDERS_PATH = 'api/orders/getMarketOrders?'
    CREATE_ORDER_PATH = 'api/orders/create?'
    CANCEL_ORDER_PATH = 'api/orders/cancel?'
    CANCEL_ALL_ORDERS_PATH = 'api/orders/cancelall?'
    GET_TRADER_INSTRUMENTS_PATH = 'api/orders/traderinstruments'
    GET_PARTNER_INSTRUMENTS_PATH = 'api/orders/partnerinstruments?'

    def __init__(self, api_url, api_id, username, password):
        assert api_url
        assert api_id
        assert username
        assert password

        self.api_url = api_url
        self.api_id = api_id
        self.username = username
        self.password = password
        self.access_token = None
        self.access_token_expiry_time = None

    def get_access_token(self):
        """Gets the access token."""
        data = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'client_id': self.api_id
        }

        response = requests.post(self.api_url + self.LOGIN_PATH, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            exception_message = 'Login failed. {error_message}'.format(
                error_message=get_error_message(response))
            raise RequestException(exception_message)

    def login(self):
        """Performs a login and stores the received access token."""
        access_token = self.get_access_token()
        self.access_token = access_token['access_token']
        self.access_token_expiry_time = datetime.datetime.now() +\
            datetime.timedelta(seconds=access_token['expires_in'])
        return self.access_token

    def logout(self):
        """Performs a logout when logged in and deletes the stored access token."""
        if self.access_token is not None:
            headers = {'Authorization': 'Bearer ' + self.access_token}
            response = requests.post(
                self.api_url + self.LOGOUT_PATH,
                headers=headers)
            if response.status_code == 200:
                self.access_token = None
            else:
                exception_message = 'Logout failed. {error_message}'.format(
                    error_message=get_error_message(response))
                raise RequestException(exception_message)

    def get_orders(
            self,
            instrument_id=None,
            order_type=None,
            offer_type=None,
            status=None,
            load_executions=None,
            max_count=None):
        """Gets the orders of the trader with the ability to apply filters."""
        data = {}
        if instrument_id is not None:
            data['instrumentID'] = instrument_id
        if order_type is not None:
            if not isinstance(order_type, OrderType):
                raise ValueError('order_type must be of type OrderType')
            data['orderType'] = order_type.value
        if offer_type is not None:
            if not isinstance(offer_type, OfferType):
                raise ValueError('offer_type must be of type OfferType')
            data['offerType'] = offer_type.value
        if status is not None:
            data['status'] = status
        if load_executions is not None:
            data['loadExecutions'] = load_executions
        if max_count is not None:
            data['maxCount'] = max_count

        query_string = urlencode(data)
        response = self.__make_authorized_request(
            'get',
            self.api_url + self.GET_ORDERS_PATH + query_string)

        if response.status_code == 200:
            orders = response.json()
            for order in orders:
                convert_order_number_fields(order)
            return orders
        else:
            exception_message = 'Failed to get the orders. {error_message}'.format(
                error_message=get_error_message(response))
            raise RequestException(exception_message)

    def get_market_orders(
            self,
            instrument_id,
            order_type=None,
            offer_type=None,
            status=None,
            max_count=None):
        """Gets the market orders with the ability to apply filters."""
        data = {
            'apiID': self.api_id,
            'instrumentID': instrument_id
        }
        if order_type is not None:
            if not isinstance(order_type, OrderType):
                raise ValueError('order_type must be of type OrderType')
            data['orderType'] = order_type.value
        if offer_type is not None:
            if not isinstance(offer_type, OfferType):
                raise ValueError('offer_type must be of type OfferType')
            data['offerType'] = offer_type.value
        if status is not None:
            data['status'] = status
        if max_count is not None:
            data['maxCount'] = max_count

        query_string = urlencode(data)
        response = requests.get(
            self.api_url + self.GET_MARKET_ORDERS_PATH + query_string)
        if response.status_code == 200:
            orders = response.json()
            for order in orders:
                convert_order_number_fields(order)
            return orders
        else:
            exception_message = 'Failed to get the market orders. {error_message}'.format(
                error_message=get_error_message(response))
            raise RequestException(exception_message)

    def create_order(
            self,
            offer_type,
            order_type,
            instrument_id,
            price,
            quantity):
        """Places an order."""
        if not isinstance(order_type, OrderType):
            raise ValueError('order_type must be of type OrderType')

        if not isinstance(offer_type, OfferType):
            raise ValueError('offer_type must be of type OfferType')

        data = {
            'offerType': offer_type.value,
            'orderType': order_type.value,
            'instrumentID': instrument_id,
            'price': price,
            'quantity': quantity
        }

        query_string = urlencode(data)
        response = self.__make_authorized_request(
            'post',
            self.api_url + self.CREATE_ORDER_PATH + query_string)

        if response.status_code != 200:
            exception_message = 'Failed to create an order. {error_message}'.format(
                error_message=get_error_message(response))
            raise RequestException(exception_message)

    def cancel_order(self, order_id):
        """Cancels a specific order."""
        data = {'orderID': order_id}
        query_string = urlencode(data)
        response = self.__make_authorized_request(
            'post',
            self.api_url + self.CANCEL_ORDER_PATH + query_string)

        if response.status_code != 200:
            exception_message = 'Failed to cancel the order. {error_message}'.format(
                error_message=get_error_message(response))
            raise RequestException(exception_message)

    def cancel_all_orders(self, instrument_id):
        """Cancels all the orders of the trader for a specific instrument."""
        data = {'instrumentID': instrument_id}
        query_string = urlencode(data)
        response = self.__make_authorized_request(
            'post',
            self.api_url + self.CANCEL_ALL_ORDERS_PATH + query_string)

        if response.status_code != 200:
            exception_message = 'Failed to cancel all orders. {error_message}'.format(
                error_message=get_error_message(response))
            raise RequestException(exception_message)

    def get_trader_instruments(self):
        """Gets the available instruments for the trader."""
        response = self.__make_authorized_request(
            'get',
            self.api_url + self.GET_TRADER_INSTRUMENTS_PATH)
        if response.status_code == 200:
            instruments = response.json()
            for instrument in instruments:
                convert_instrument_number_fields(instrument)
            return instruments
        else:
            exception_message = 'Failed to get the trader instruments. {error_message}'.format(
                error_message=get_error_message(response))
            raise RequestException(exception_message)

    def get_partner_instruments(self):
        """Gets the available instruments for the partner."""
        data = {'apiID': self.api_id}
        query_string = urlencode(data)
        response = requests.get(
            self.api_url + self.GET_PARTNER_INSTRUMENTS_PATH + query_string)
        if response.status_code == 200:
            instruments = response.json()
            for instrument in instruments:
                convert_instrument_number_fields(instrument)
            return instruments
        else:
            exception_message = 'Failed to get the partner instruments. {error_message}'.format(
                error_message=get_error_message(response))
            raise RequestException(exception_message)

    def __make_authorized_request(self, request_type, url):
        request_type = request_type.lower()
        assert request_type in ('get', 'post')

        # Not logged in or the access token has expired
        current_time = datetime.datetime.now()
        if self.access_token is None or self.access_token_expiry_time < current_time:
            self.login()

        bearer = self.access_token if self.access_token else ''
        headers = {'Authorization': 'Bearer ' + bearer}
        if request_type == 'get':
            response = requests.get(url, headers=headers)
        elif request_type == 'post':
            response = requests.post(url, headers=headers)

        if is_unauthorized_response(response):
            self.login()
            bearer = self.access_token if self.access_token else ''
            headers = {'Authorization': 'Bearer ' + bearer}
            if request_type == 'get':
                response = requests.get(url, headers=headers)
            elif request_type == 'post':
                response = requests.post(url, headers=headers)

        return response

def is_unauthorized_response(response):
    """Checks if a response is unauthorized."""
    if response.status_code == 401:
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

def convert_instrument_number_fields(instrument):
    instrument['minOrderAmount'] = \
        decimal.getcontext().create_decimal(instrument['minOrderAmount'])

def convert_order_number_fields(order):
    order['orderID'] = int(order['orderID'])
    order['initialQuantity'] = \
        decimal.getcontext().create_decimal(order['initialQuantity'])
    order['price'] = \
        decimal.getcontext().create_decimal(order['price'])
    order['quantity'] = \
        decimal.getcontext().create_decimal(order['quantity'])

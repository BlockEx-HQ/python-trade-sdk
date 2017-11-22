import requests
from requests import RequestException
from six.moves.urllib.parse import urlencode
from enum import Enum


class OrderType(Enum):
    LIMIT = 'Limit'
    MARKET = 'Market'
    STOP = 'Stop'


class OfferType(Enum):
    BID = 'Bid'
    ASK = 'Ask'


class BlockExTradeApi:
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
        self.api_url = api_url
        self.api_id = api_id
        self.username = username
        self.password = password
        self.access_token = None

    def get_access_token(self):
        data = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'client_id': self.api_id
        }

        response = requests.post(self.api_url + self.LOGIN_PATH, data=data)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            exception_message = 'Login failed.' +\
                self.__get_error_message(response)
            raise RequestException(exception_message)

    def login(self):
        self.access_token = self.get_access_token()
        return self.access_token

    def logout(self):
        if self.access_token is not None:
            headers = {'Authorization': 'Bearer ' + self.access_token}
            response = requests.post(
                self.api_url + self.LOGOUT_PATH,
                headers=headers)
            if response.status_code == 200:
                self.access_token = None
            else:
                exception_message = 'Logout failed.' +\
                    self.__get_error_message(response)
                raise RequestException(exception_message)

    def get_orders(
            self,
            instrument_id=None,
            order_type=None,
            offer_type=None,
            status=None,
            load_executions=None,
            max_count=None):
        data = {}
        if instrument_id is not None:
            data['instrumentID'] = instrument_id
        if order_type is not None:
            if type(order_type) is not OrderType:
                raise ValueError('order_type must be of type OrderType')
            data['orderType'] = order_type.value
        if offer_type is not None:
            if type(offer_type) is not OfferType:
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
            return response.json()
        else:
            exception_message = 'Failed to get the orders.' +\
                self.__get_error_message(response)
            raise RequestException(exception_message)

    def get_market_orders(
            self,
            instrument_id,
            order_type=None,
            offer_type=None,
            status=None,
            max_count=None):
        data = {
            'apiID': self.api_id,
            'instrumentID': instrument_id
        }
        if order_type is not None:
            if type(order_type) is not OrderType:
                raise ValueError('order_type must be of type OrderType')
            data['orderType'] = order_type.value
        if offer_type is not None:
            if type(offer_type) is not OfferType:
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
            return response.json()
        else:
            exception_message = 'Failed to get the market orders.' +\
                self.__get_error_message(response)
            raise RequestException(exception_message)

    def create_order(
            self,
            offer_type,
            order_type,
            instrument_id,
            price,
            quantity):
        if type(order_type) is not OrderType:
            raise ValueError('order_type must be of type OrderType')

        if type(offer_type) is not OfferType:
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
            exception_message = 'Failed to create an order.' +\
                self.__get_error_message(response)
            raise RequestException(exception_message)

    def cancel_order(self, order_id):
        data = {'orderID': order_id}
        query_string = urlencode(data)
        response = self.__make_authorized_request(
            'post',
            self.api_url + self.CANCEL_ORDER_PATH + query_string)

        if response.status_code != 200:
            exception_message = 'Failed to cancel the order.' +\
                self.__get_error_message(response)
            raise RequestException(exception_message)

    def cancel_all_orders(self, instrument_id):
        data = {'instrumentID': instrument_id}
        query_string = urlencode(data)
        response = self.__make_authorized_request(
            'post',
            self.api_url + self.CANCEL_ALL_ORDERS_PATH + query_string)

        if response.status_code != 200:
            exception_message = 'Failed to cancel all orders.' +\
                self.__get_error_message(response)
            raise RequestException(exception_message)

    def get_trader_instruments(self):
        response = self.__make_authorized_request(
            'get',
            self.api_url + self.GET_TRADER_INSTRUMENTS_PATH)
        if response.status_code == 200:
            return response.json()
        else:
            exception_message = 'Failed to get the trader instruments.' +\
                self.__get_error_message(response)
            raise RequestException(exception_message)

    def get_partner_instruments(self):
        data = {'apiID': self.api_id}
        query_string = urlencode(data)
        response = requests.get(
            self.api_url + self.GET_PARTNER_INSTRUMENTS_PATH + query_string)
        if response.status_code == 200:
            return response.json()
        else:
            exception_message = 'Failed to get the partner instruments.' +\
                self.__get_error_message(response)
            raise RequestException(exception_message)

    def __make_authorized_request(self, request_type, url):
        request_type = request_type.lower()
        assert request_type in ('get', 'post')

        if self.access_token is None:  # Not logged in
            self.login()

        bearer = self.access_token if self.access_token else ''
        headers = {'Authorization': 'Bearer ' + bearer}
        if request_type == 'get':
            response = requests.get(url, headers=headers)
        elif request_type == 'post':
            response = requests.post(url, headers=headers)

        # If the access token has expired, a new login is required
        if self.__is_unauthorized_response(response):
            self.login()
            bearer = self.access_token if self.access_token else ''
            headers = {'Authorization': 'Bearer ' + bearer}
            if request_type == 'get':
                response = requests.get(url, headers=headers)
            elif request_type == 'post':
                response = requests.post(url, headers=headers)

        return response

    def __is_unauthorized_response(self, response):
        if response.status_code == 401:
            response_content = response.json()
            message = 'Authorization has been denied for this request.'
            if 'message' in response_content:
                if response_content['message'] == message:
                    return True

        return False

    def __get_error_message(self, response):
        response_json = response.json()
        if 'error' in response_json:
            return ' Message: ' + response_json['error']
        elif 'message' in response_json:
            return ' Message: ' + response_json['message']
        else:
            return ''

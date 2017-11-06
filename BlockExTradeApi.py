import requests
from six.moves.urllib.parse import urlencode


class BlockExTradeApi:
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

        response = requests.post(self.api_url + 'oauth/token', data=data)
        if response.status_code == 200:
            result = {
                'response': response,
                'access_token': response.json()['access_token']
            }
        else:
            result = {'response': response}

        return result

    def login(self):
        get_access_token_result = self.get_access_token()
        if 'access_token' in get_access_token_result:
            self.access_token = get_access_token_result['access_token']

        return get_access_token_result

    def logout(self):
        if self.access_token is not None:
            headers = {'Authorization': 'Bearer ' + self.access_token}
            response = requests.post(
                self.api_url + 'oauth/logout',
                headers=headers)
            if response.status_code == 200:
                self.access_token = None
        else:
            response = None

        return {'response': response}

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
            data['orderType'] = order_type
        if offer_type is not None:
            data['offerType'] = offer_type
        if status is not None:
            data['status'] = status
        if load_executions is not None:
            data['loadExecutions'] = load_executions
        if max_count is not None:
            data['maxCount'] = max_count

        query_string = urlencode(data)
        response = self.__make_authorized_request(
            'get',
            self.api_url + 'api/orders/get?' + query_string)

        if response.status_code == 200:
            result = {
                'response': response,
                'data': response.json()
            }
        else:
            result = {'response': response}

        return result

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
            data['orderType'] = order_type
        if offer_type is not None:
            data['offerType'] = offer_type
        if status is not None:
            data['status'] = status
        if max_count is not None:
            data['maxCount'] = max_count

        query_string = urlencode(data)
        response = requests.get(
            self.api_url + 'api/orders/getMarketOrders?' + query_string)
        if response.status_code == 200:
            result = {
                'response': response,
                'data': response.json()
            }
        else:
            result = {'response': response}

        return result

    def create_order(
            self,
            offer_type,
            order_type,
            instrument_id,
            price,
            quantity):
        data = {
            'offerType': offer_type,
            'orderType': order_type,
            'instrumentID': instrument_id,
            'price': price,
            'quantity': quantity
        }

        query_string = urlencode(data)
        response = self.__make_authorized_request(
            'post',
            self.api_url + 'api/orders/create?' + query_string)
        return {'response': response}

    def cancel_order(self, order_id):
        data = {'orderID': order_id}
        query_string = urlencode(data)
        response = self.__make_authorized_request(
            'post',
            self.api_url + 'api/orders/cancel?' + query_string)
        return {'response': response}

    def cancel_all_orders(self, instrument_id):
        data = {'instrumentID': instrument_id}
        query_string = urlencode(data)
        response = self.__make_authorized_request(
            'post',
            self.api_url + 'api/orders/cancelall?' + query_string)
        return {'response': response}

    def get_trader_instruments(self):
        response = self.__make_authorized_request(
            'get',
            self.api_url + 'api/orders/traderinstruments')
        if response.status_code == 200:
            result = {
                'response': response,
                'data': response.json()
            }
        else:
            result = {'response': response}

        return result

    def get_partner_instruments(self):
        data = {'apiID': self.api_id}
        query_string = urlencode(data)
        response = requests.get(
            self.api_url + 'api/orders/partnerinstruments?' + query_string)
        if response.status_code == 200:
            result = {
                'response': response,
                'data': response.json()
            }
        else:
            result = {'response': response}

        return result

    def __make_authorized_request(self, request_type, url):
        if self.access_token is None:  # Not logged in
            self.login()

        bearer = self.access_token if self.access_token else ''
        headers = {'Authorization': 'Bearer ' + bearer}
        if request_type == 'get':
            response = requests.get(url, headers=headers)
        elif request_type == 'post':
            response = requests.post(url, headers=headers)
        else:
            raise ValueError('The request type must be get or post')

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

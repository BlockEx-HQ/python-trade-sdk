import requests
from urllib.parse import urlencode

class BlockExTradeApi:
    def __init__(self, api_url):
        self.api_url = api_url

    def login(self, username, password, api_id):
        data = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': api_id
        }

        response = requests.post(self.api_url + 'oauth/token', data=data)
        if response.status_code == 200:
            result = {
                'response': response,
                'access_token': response.json()['access_token']
            }
        else:
            result = { 'response': response }

        return result

    def logout(self, access_token):
        headers = { 'Authorization': 'Bearer ' + access_token }
        response = requests.post(self.api_url + 'oauth/logout', headers=headers)
        return { 'response': response }

    def get_orders(
            self,
            access_token,
            instrument_id=None,
            type=None,
            offer_type=None,
            status=None,
            load_executions=None,
            max_count=None):
        headers = { 'Authorization': 'Bearer ' + access_token }
        data = {}
        if instrument_id is not None:
            data['instrumentID'] = instrument_id
        if type is not None:
            data['type'] = type
        if offer_type is not None:
            data['offerType'] = offer_type
        if status is not None:
            data['status'] = status
        if load_executions is not None:
            data['loadExecutions'] = load_executions
        if max_count is not None:
            data['maxCount'] = max_count

        query_string = urlencode(data)
        response = requests.get(self.api_url + 'api/orders/get?' + query_string, headers=headers)
        if response.status_code == 200:
            result = {
                'response': response,
                'data': response.json()
            }
        else:
            result = { 'response': response }

        return result

    def get_market_orders(
            self,
            access_token,
            api_id,
            instrument_id,
            type=None,
            offer_type=None,
            status=None,
            max_count=None):
        headers = { 'Authorization': 'Bearer ' + access_token }
        data = {
            'apiID': api_id,
            'instrumentID': instrument_id
        }
        if type is not None:
            data['type'] = type
        if offer_type is not None:
            data['offerType'] = offer_type
        if status is not None:
            data['status'] = status
        if max_count is not None:
            data['maxCount'] = max_count

        query_string = urlencode(data)
        response = requests.get(self.api_url + 'api/orders/getMarketOrders?' + query_string, headers=headers)
        if response.status_code == 200:
            result = {
                'response': response,
                'data': response.json()
            }
        else:
            result = { 'response': response }

        return result

    def create_order(
            self,
            access_token,
            bidask,
            order_type,
            instrument_id,
            price,
            shares):
        headers = { 'Authorization': 'Bearer ' + access_token }
        data = {
            'bidask': bidask,
            'orderType': order_type,
            'instrumentID': instrument_id,
            'price': price,
            'shares': shares
        }

        query_string = urlencode(data)
        response = requests.post(self.api_url + 'api/orders/create?' + query_string, headers=headers)
        return { 'response': response }

    def cancel_order(self, access_token, order_id):
        headers = { 'Authorization': 'Bearer ' + access_token }
        data = { 'orderID': order_id }
        query_string = urlencode(data)
        response = requests.post(self.api_url + 'api/orders/cancel?' + query_string, headers=headers)
        return { 'response': response }

    def cancel_all_orders(self, access_token, instrument_id):
        headers = { 'Authorization': 'Bearer ' + access_token }
        data = { 'instrumentID': instrument_id }
        query_string = urlencode(data)
        response = requests.post(self.api_url + 'api/orders/cancelall?' + query_string, headers=headers)
        return { 'response': response }

    def get_trader_instruments(self, access_token):
        headers = { 'Authorization': 'Bearer ' + access_token }
        response = requests.get(self.api_url + 'api/orders/traderinstruments', headers=headers)
        if response.status_code == 200:
            result = {
                'response': response,
                'data': response.json()
            }
        else:
            result = { 'response': response }

        return result

    def get_partner_instruments(self, access_token, api_id):
        headers = { 'Authorization': 'Bearer ' + access_token }
        data = { 'apiID': api_id }
        query_string = urlencode(data)
        response = requests.get(self.api_url + 'api/orders/partnerinstruments?' + query_string, headers=headers)
        if response.status_code == 200:
            result = {
                'response': response,
                'data': response.json()
            }
        else:
            result = { 'response': response }

        return result

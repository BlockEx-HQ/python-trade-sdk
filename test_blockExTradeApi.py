import requests
from requests import Response
from unittest import TestCase
from unittest.mock import Mock
from BlockExTradeApi import BlockExTradeApi

class TestTradeApi(TestCase):
    def setUp(self):
        self.trade_api = BlockExTradeApi('https://test.api.url/')

class TestTradeApiInit(TestTradeApi):
    def test_init(self):
        self.assertEqual(self.trade_api.api_url, 'https://test.api.url/')

class TestTradeApiLogin(TestTradeApi):
    def test_authorized_login(self):
        authorized_response = Response()
        authorized_response.status_code = 200
        authorized_response._content = '{"access_token":"SomeAccessToken"}'.encode()
        post_mock = Mock(return_value=authorized_response)
        requests.post = post_mock

        login_response = self.trade_api.login('CorrectUsername', 'CorrectPassword', 'CorrectApiID')

        post_mock.assert_called_once_with(
            'https://test.api.url/oauth/token',
            data = {
                'grant_type': 'password',
                'username': 'CorrectUsername',
                'password': 'CorrectPassword',
                'client_id': 'CorrectApiID'
            })

        self.assertIn('response', login_response)
        self.assertEqual(login_response['response'].status_code, 200)
        self.assertEqual(login_response['response'].content, '{"access_token":"SomeAccessToken"}'.encode())

        self.assertIn('access_token', login_response)
        self.assertEqual(login_response['access_token'], 'SomeAccessToken')

    def test_unauthorized_login(self):
        unauthorized_response = Response()
        unauthorized_response.status_code = 400
        unauthorized_response._content = '{"error":"invalid_client"}'.encode()
        post_mock = Mock(return_value=unauthorized_response)
        requests.post = post_mock

        login_response = self.trade_api.login('CorrectUsername', 'WrongPassword', 'CorrectApiID')

        post_mock.assert_called_once_with(
            'https://test.api.url/oauth/token',
            data={
                'grant_type': 'password',
                'username': 'CorrectUsername',
                'password': 'WrongPassword',
                'client_id': 'CorrectApiID'
            })

        self.assertIn('response', login_response)
        self.assertEqual(login_response['response'].status_code, 400)
        self.assertEqual(login_response['response'].content, '{"error":"invalid_client"}'.encode())

        self.assertNotIn('access_token', login_response)

class TestTradeApiLogout(TestTradeApi):
    def test_logout(self):
        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        logout_response = self.trade_api.logout('SomeAccessToken')

        post_mock.assert_called_once_with(
            'https://test.api.url/oauth/logout',
            headers={ 'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', logout_response)
        self.assertEqual(logout_response['response'].status_code, 200)

class TestTradeApiGetOrders(TestTradeApi):
    def test_successful_get_orders_without_filter(self):
        successful_response = Response()
        successful_response.status_code = 200
        orders_list = '[{"orderID": "32592","price": 13.40,"initialQuantity": 32.50,"quantity": 32.50,"dateCreated": "2017-10-09T09:32:24.735659+00:00","offerType": 1,"type": 1,"status": 15,"instrumentID": 1,"trades": null},'
        orders_list += '{"orderID": "32593","price": 11.34,"initialQuantity": 26.00,"quantity": 26.00,"dateCreated": "2017-10-09T09:35:10.61228+00:00","offerType": 1,"type": 1,"status": 20,"instrumentID": 1,"trades": null}]'
        successful_response._content = orders_list.encode()
        get_mock = Mock(return_value=successful_response)
        requests.get = get_mock

        get_orders_response = self.trade_api.get_orders('SomeAccessToken')

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/get?',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', get_orders_response)
        self.assertEqual(get_orders_response['response'].status_code, 200)
        self.assertEqual(get_orders_response['response'].content, orders_list.encode())

        self.assertIn('data', get_orders_response)
        self.assertEqual(get_orders_response['data'], successful_response.json())

    def test_successful_get_orders_with_filter(self):
        successful_response = Response()
        successful_response.status_code = 200
        orders_list = '[{"orderID": "32592","price": 13.40,"initialQuantity": 32.50,"quantity": 32.50,"dateCreated": "2017-10-09T09:32:24.735659+00:00","offerType": 1,"type": 1,"status": 15,"instrumentID": 1,"trades": null},'
        orders_list += '{"orderID": "32593","price": 11.34,"initialQuantity": 26.00,"quantity": 26.00,"dateCreated": "2017-10-09T09:35:10.61228+00:00","offerType": 1,"type": 1,"status": 20,"instrumentID": 1,"trades": null}]'
        successful_response._content = orders_list.encode()
        get_mock = Mock(return_value=successful_response)
        requests.get = get_mock

        get_orders_response = self.trade_api.get_orders('SomeAccessToken', 1, 'Limit', 'Bid', '10,20', 'true', 50)

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/get?instrumentID=1&type=Limit&offerType=Bid&status=10%2C20&loadExecutions=true&maxCount=50',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', get_orders_response)
        self.assertEqual(get_orders_response['response'].status_code, 200)
        self.assertEqual(get_orders_response['response'].content, orders_list.encode())

        self.assertIn('data', get_orders_response)
        self.assertEqual(get_orders_response['data'], successful_response.json())

    def test_unsuccessful_get_orders(self):
        unsuccessful_response = Response()
        unsuccessful_response.status_code = 400
        unsuccessful_response._content = '{"message": "Unknown trader"}'.encode()
        get_mock = Mock(return_value=unsuccessful_response)
        requests.get = get_mock

        get_orders_response = self.trade_api.get_orders('SomeAccessToken')

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/get?',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', get_orders_response)
        self.assertEqual(get_orders_response['response'].status_code, 400)
        self.assertEqual(get_orders_response['response'].content, '{"message": "Unknown trader"}'.encode())

        self.assertNotIn('data', get_orders_response)

class TestTradeApiGetMarketOrders(TestTradeApi):
    def test_successful_get_market_orders_without_filter(self):
        successful_response = Response()
        successful_response.status_code = 200
        market_orders_list = '[{"orderID": "31635","price": 5.00,"initialQuantity": 270.00,"quantity": 0.00,"dateCreated": "2017-05-14T09:19:53.335+00:00","offerType": 1,"type": 1,"status": 40,"instrumentID": 1,"trades": null},'
        market_orders_list += '{"orderID": "31636","price": 1.00,"initialQuantity": 260.00,"quantity": 0.00,"dateCreated": "2017-05-14T09:19:55.782+00:00","offerType": 1,"type": 1,"status": 40,"instrumentID": 1,"trades": null}]'
        successful_response._content = market_orders_list.encode()
        get_mock = Mock(return_value=successful_response)
        requests.get = get_mock

        get_market_orders_response = self.trade_api.get_market_orders('SomeAccessToken', 'CorrectApiID', 1)

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/getMarketOrders?apiID=CorrectApiID&instrumentID=1',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', get_market_orders_response)
        self.assertEqual(get_market_orders_response['response'].status_code, 200)
        self.assertEqual(get_market_orders_response['response'].content, market_orders_list.encode())

        self.assertIn('data', get_market_orders_response)
        self.assertEqual(get_market_orders_response['data'], successful_response.json())

    def test_successful_get_market_orders_with_filter(self):
        successful_response = Response()
        successful_response.status_code = 200
        market_orders_list = '[{"orderID": "31635","price": 5.00,"initialQuantity": 270.00,"quantity": 0.00,"dateCreated": "2017-05-14T09:19:53.335+00:00","offerType": 1,"type": 1,"status": 40,"instrumentID": 1,"trades": null},'
        market_orders_list += '{"orderID": "31636","price": 1.00,"initialQuantity": 260.00,"quantity": 0.00,"dateCreated": "2017-05-14T09:19:55.782+00:00","offerType": 1,"type": 1,"status": 40,"instrumentID": 1,"trades": null}]'
        successful_response._content = market_orders_list.encode()
        get_mock = Mock(return_value=successful_response)
        requests.get = get_mock

        get_market_orders_response = self.trade_api.get_market_orders('SomeAccessToken', 'CorrectApiID', 1, 'Limit', 'Bid', '10,20', 50)

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/getMarketOrders?apiID=CorrectApiID&instrumentID=1&type=Limit&offerType=Bid&status=10%2C20&maxCount=50',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', get_market_orders_response)
        self.assertEqual(get_market_orders_response['response'].status_code, 200)
        self.assertEqual(get_market_orders_response['response'].content, market_orders_list.encode())

        self.assertIn('data', get_market_orders_response)
        self.assertEqual(get_market_orders_response['data'], successful_response.json())

    def test_unsuccessful_get_market_orders(self):
        unsuccessful_response = Response()
        unsuccessful_response.status_code = 400
        unsuccessful_response._content = '{"message": "Invalid partner API id"}'.encode()
        get_mock = Mock(return_value=unsuccessful_response)
        requests.get = get_mock

        get_orders_response = self.trade_api.get_market_orders('SomeAccessToken', 'IncorrectApiID', 1)

        get_mock.assert_called_once_with(
            'https://test.api.url/api/orders/getMarketOrders?apiID=IncorrectApiID&instrumentID=1',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', get_orders_response)
        self.assertEqual(get_orders_response['response'].status_code, 400)
        self.assertEqual(get_orders_response['response'].content, '{"message": "Invalid partner API id"}'.encode())

        self.assertNotIn('data', get_orders_response)

class TestTradeApiCreateOrder(TestTradeApi):
    def test_create_order(self):
        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        create_order_response = self.trade_api.create_order('SomeAccessToken', 'Bid', 'LO', 1, 15.2, 3.7)

        post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/create?bidask=Bid&orderType=LO&instrumentID=1&price=15.2&shares=3.7',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', create_order_response)
        self.assertEqual(create_order_response['response'].status_code, 200)

class TestTradeApiCancelOrder(TestTradeApi):
    def test_cancel_order(self):
        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        cancel_order_response = self.trade_api.cancel_order('SomeAccessToken', 32598)

        post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/cancel?orderID=32598',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', cancel_order_response)
        self.assertEqual(cancel_order_response['response'].status_code, 200)

class TestTradeApiCancelAllOrders(TestTradeApi):
    def test_cancel_all_orders(self):
        response = Response()
        response.status_code = 200
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        cancel_all_orders_response = self.trade_api.cancel_all_orders('SomeAccessToken', 1)

        post_mock.assert_called_once_with(
            'https://test.api.url/api/orders/cancelall?instrumentID=1',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIn('response', cancel_all_orders_response)
        self.assertEqual(cancel_all_orders_response['response'].status_code, 200)

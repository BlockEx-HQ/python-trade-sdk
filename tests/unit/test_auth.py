from unittest import TestCase

import requests
from blockex.tradeapi import interface, tradeapi
from mock import Mock

Response = requests.Response
RequestException = requests.RequestException

FIXTURE_INSTRUMENT_ID = 1
FIXTURE_ACCESS_TOKEN = "SomeAccessToken"
FIXTURE_API_URL = "https://test.api.url/"
FIXTURE_API_ID = "CorrectApiID"
FIXTURE_USERNAME = "CorrectUsername"
FIXTURE_PASSWORD = "CorrectPassword"
FIXTURE_BAD_PASSWORD = "bad_password"

class TestTradeApi(TestCase):
    def setUp(self):
        self.get_access_token_mock = Mock(return_value={
            'access_token': FIXTURE_ACCESS_TOKEN,
            'expires_in': 86399,
        })
        self.trade_api = tradeapi.BlockExTradeApi(
            api_url=FIXTURE_API_URL, api_id=FIXTURE_API_ID,
            username=FIXTURE_USERNAME, password=FIXTURE_PASSWORD)

        self.trade_api.get_access_token = self.get_access_token_mock

class TestTradeApiLogin(TestCase):
    def setUp(self):
        self.trade_api = tradeapi.Auth(
            api_url=FIXTURE_API_URL, api_id=FIXTURE_API_ID,
            username=FIXTURE_USERNAME, password=FIXTURE_PASSWORD)
        self.trade_api = tradeapi.BlockExTradeApi(
            api_url=FIXTURE_API_URL, api_id=FIXTURE_API_ID,
            username=FIXTURE_USERNAME, password=FIXTURE_PASSWORD)

    def test_authorized_login(self):
        response = Response()
        response.status_code = interface.SUCCESS
        response._content = '{"access_token":"SomeAccessToken", "expires_in":86399}'.encode()
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        login_response = self.trade_api.login()

        post_mock.assert_called_once_with(
            FIXTURE_API_URL + "oauth/token",
            data={
                'grant_type': 'password',
                'username': FIXTURE_USERNAME,
                'password': FIXTURE_PASSWORD,
                'client_id': FIXTURE_API_ID,
            })

        self.assertEqual(login_response, FIXTURE_ACCESS_TOKEN)

    def test_unauthorized_login(self):
        self.trade_api = tradeapi.Auth(
            api_url=FIXTURE_API_URL, api_id=FIXTURE_API_ID,
            username=FIXTURE_USERNAME, password=FIXTURE_BAD_PASSWORD)
        self.trade_api = tradeapi.BlockExTradeApi(
            api_url=FIXTURE_API_URL, api_id=FIXTURE_API_ID,
            username=FIXTURE_USERNAME, password=FIXTURE_BAD_PASSWORD)

        response = Response()
        response.status_code = interface.BAD_REQUEST
        response._content = '{"error":"invalid_client"}'.encode()
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        with self.assertRaises(RequestException):
            self.trade_api.login()

        post_mock.assert_called_once_with(
            'https://test.api.url/oauth/token',
            data={
                'grant_type': 'password',
                'username': FIXTURE_USERNAME,
                'password': FIXTURE_BAD_PASSWORD,
                'client_id': FIXTURE_API_ID
            })


class TestTradeApiLogout(TestTradeApi):
    def test_logout_when_logged_in(self):
        self.trade_api.login()
        self.assertEqual(self.trade_api.access_token, FIXTURE_ACCESS_TOKEN)

        response = Response()
        response.status_code = interface.SUCCESS
        post_mock = Mock(return_value=response)
        requests.post = post_mock

        self.trade_api.logout()

        post_mock.assert_called_once_with(
            'https://test.api.url/oauth/logout',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        self.assertIsNone(self.trade_api.access_token)

    def test_logout_when_not_logged_in(self):
        post_mock = Mock()
        requests.post = post_mock

        self.assertIsNone(self.trade_api.access_token)
        self.trade_api.logout()
        post_mock.assert_not_called()

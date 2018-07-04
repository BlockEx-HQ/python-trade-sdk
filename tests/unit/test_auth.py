import pytest

import requests
from blockex.tradeapi import interface, tradeapi


@pytest.mark.usefixtures('mocker')
@pytest.mark.usefixtures('trade_api')
class TestTradeApiLogin:

    def test_authorized_login(self):
        # Restore native get_access_token
        self.response._content = '{"access_token":"SomeAccessToken", "expires_in":86399}'.encode()
        self.trade_api.get_access_token = self.old_get_access_token
        login_response = self.trade_api.login()

        self.post_mock.assert_called_once_with(
            pytest.FIXTURE_API_URL + "oauth/token",
            data={
                'grant_type': 'password',
                'username': pytest.FIXTURE_USERNAME,
                'password': pytest.FIXTURE_PASSWORD,
                'client_id': pytest.FIXTURE_API_ID,
            })

        assert login_response == pytest.FIXTURE_ACCESS_TOKEN

    def test_unauthorized_login(self):
        unauthorized_trade_api = tradeapi.BlockExTradeApi(
            api_url=pytest.FIXTURE_API_URL, api_id=pytest.FIXTURE_API_ID,
            username=pytest.FIXTURE_USERNAME, password=pytest.FIXTURE_BAD_PASSWORD)

        self.response.status_code = interface.BAD_REQUEST
        self.response._content = '{"error":"invalid_client"}'.encode()

        with pytest.raises(requests.RequestException):
            unauthorized_trade_api.login()

        self.post_mock.assert_called_once_with(
            'https://test.api.url/oauth/token',
            data={
                'grant_type': 'password',
                'username': pytest.FIXTURE_USERNAME,
                'password': pytest.FIXTURE_BAD_PASSWORD,
                'client_id': pytest.FIXTURE_API_ID
            })

    def test_logout_when_logged_in(self):
        self.trade_api.login()
        assert self.trade_api.access_token == pytest.FIXTURE_ACCESS_TOKEN

        self.trade_api.logout()

        self.post_mock.assert_called_once_with(
            'https://test.api.url/oauth/logout',
            headers={'Authorization': 'Bearer SomeAccessToken'})

        assert self.trade_api.access_token is None

    def test_logout_when_not_logged_in(self):
        post_mock = self.mocker.Mock()
        requests.post = post_mock

        assert self.trade_api.access_token is None
        self.trade_api.logout()
        post_mock.assert_not_called()

    def authorized_request_when_not_logged_in(self, req_method, req_mock):
        self.response.status_code = interface.BAD_REQUEST
        self.response._content = '{"error":"invalid_client"}'.encode()

        authorized_response = self.trade_api.make_authorized_request(req_method, 'ResourceURL')

        self.get_access_token_mock.assert_called_once()
        assert self.trade_api.access_token == pytest.FIXTURE_ACCESS_TOKEN

        req_mock.assert_called_once_with(self.trade_api.api_url + 'ResourceURL',
                                         headers={'Authorization': 'Bearer SomeAccessToken'})
        assert authorized_response.status_code == interface.BAD_REQUEST

    def test_make_authorized_post_request_when_not_logged_in(self):
        self.authorized_request_when_not_logged_in(self.trade_api.post_path, self.post_mock)

    def test_make_authorized_get_request_when_not_logged_in(self):
        self.authorized_request_when_not_logged_in(self.trade_api.get_path, self.get_mock)

    def authorized_request_when_logged_in(self, req_method, req_mock):
        self.trade_api.login()

        authorized_response = self.trade_api.make_authorized_request(req_method, 'ResourceURL')

        assert self.trade_api.access_token == pytest.FIXTURE_ACCESS_TOKEN

        req_mock.assert_called_once_with(self.trade_api.api_url + 'ResourceURL',
                                         headers={'Authorization': 'Bearer SomeAccessToken'})
        assert authorized_response.status_code == interface.SUCCESS

    def test_make_authorized_post_request_when_logged_in(self):
        self.trade_api.login()
        self.authorized_request_when_logged_in(self.trade_api.post_path, self.post_mock)
        assert self.get_access_token_mock.call_count == 2

    def test_make_authorized_get_request_when_logged_in(self):
        self.trade_api.login()
        self.authorized_request_when_logged_in(self.trade_api.get_path, self.get_mock)
        assert self.get_access_token_mock.call_count == 2

    def test_make_authorized_get_request_when_token_expired(self):
        self.authorized_request_when_logged_in(self.trade_api.get_path, self.get_mock)
        self.get_access_token_mock.assert_called_once()

    def test_make_authorized_post_request_when_token_expired(self):
        self.authorized_request_when_logged_in(self.trade_api.post_path, self.post_mock)
        self.get_access_token_mock.assert_called_once()

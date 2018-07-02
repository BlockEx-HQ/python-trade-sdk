import pytest
import requests

from blockex.tradeapi import interface, tradeapi


@pytest.fixture
def global_variable():
    pytest.FIXTURE_ACCESS_TOKEN = "SomeAccessToken"
    pytest.FIXTURE_API_URL = "https://test.api.url/"
    pytest.FIXTURE_API_ID = "CorrectApiID"
    pytest.FIXTURE_USERNAME = "CorrectUsername"
    pytest.FIXTURE_PASSWORD = "CorrectPassword"
    pytest.FIXTURE_BAD_PASSWORD = "bad_password"


@pytest.fixture()
def trade_api(request, mocker, global_variable):
    request.cls.get_access_token_mock = mocker.Mock(return_value={
        'access_token': pytest.FIXTURE_ACCESS_TOKEN,
        'expires_in': 86399,
    })

    request.cls.trade_api = tradeapi.BlockExTradeApi(
        api_url=pytest.FIXTURE_API_URL, api_id=pytest.FIXTURE_API_ID,
        username=pytest.FIXTURE_USERNAME, password=pytest.FIXTURE_PASSWORD)

    request.cls.old_get_access_token = request.cls.trade_api.get_access_token
    request.cls.trade_api.get_access_token = request.cls.get_access_token_mock

    request.cls.response = requests.Response()
    request.cls.response.status_code = interface.SUCCESS

    request.cls.post_mock = mocker.Mock(return_value=request.cls.response)
    requests.post = request.cls.post_mock
    request.cls.get_mock = mocker.Mock(return_value=request.cls.response)
    requests.get = request.cls.get_mock


@pytest.fixture()
def mocker(request, mocker):
    request.cls.mocker = mocker
    return mocker

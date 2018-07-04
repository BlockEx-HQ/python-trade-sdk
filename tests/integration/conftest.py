import os

import pytest

from blockex.tradeapi.tradeapi import BlockExTradeApi


@pytest.fixture()
def client(request):
    request.cls.client = BlockExTradeApi(
        api_url=os.environ.get('BLOCKEX_TEST_TRADEAPI_URL'),
        api_id=os.environ.get('BLOCKEX_TEST_TRADEAPI_ID'),
        username=os.environ.get('BLOCKEX_TEST_TRADEAPI_USERNAME'),
        password=os.environ.get('BLOCKEX_TEST_TRADEAPI_PASSWORD'))

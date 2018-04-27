# BlockEx Trade API SDK
_v0.0.3_

## Description
BlockEx Trade API SDK is a Python client package for the Trade API
of BlockEx Digital Asset eXchange Platform. It's purpose is to provide an
easy integration of Python-based systems with the BlockEx Trade API.

The module consists of client implementations of API resources that
can generally be grouped into four categories:

 - Trader authentication
 - Getting instruments
 - Getting open orders
 - Placing/cancelling orders
 - Receiving trade events

[Documentation](http://blockex.trade-sdk.readthedocs.org/en/latest/index.html)

# License
[![License](http://img.shields.io/badge/Licence-MIT-brightgreen.svg)](LICENSE)

# Installation
Tested and working on Python 2.7 .. 3.6.4+.

blockex-tradeapi is [available on PyPI](http://pypi.python.org/pypi/blockex.trade-sdk/)
``` bash
pip install blockex.trade-sdk
```

## Usage

Below is a set of short example, see full example in
`docs/examples/naive_trading.py` in this package's repo.

```
#!/usr/bin/env python
from blockex.tradeapi import interface
from blockex.tradeapi.tradeapi import BlockExTradeApi

API_URL = 'https://api.blockex.com/'
API_ID = '7c11fb8e-f744-47ee-aec2-9da5eb83ad84'
USERNAME = ''
PASSWORD = ''

# initiate the API wrapper object:
trade_api = BlockExTradeApi(USERNAME, PASSWORD, API_URL, API_ID)
# get list of available trader instruments
trader_instruments = trade_api.get_trader_instruments()
# Pick an instrument to work with
instrument_id = trader_instruments[0]['id']

# get full list of trader orders
orders = trade_api.get_orders()
# get filtered list of trader orders
orders_filtered = trade_api.get_orders(instrument_id=instrument_id,
                                       order_type=interface.OrderType.LIMIT,
                                       offer_type=interface.OfferType.BID,
                                       status=[interface.OrderStatus.PENDING,
                                               interface.OrderStatus.PLACED],
                                       load_executions=True,
                                       max_count=5)
# get full list of market orders
market_orders = trade_api.get_market_orders(instrument_id=instrument_id)
# get filtered list of market orders
market_orders_filtered = trade_api.get_market_orders(
    instrument_id=instrument_id,
    order_type=interface.OrderType.LIMIT,
    offer_type=interface.OfferType.BID,
    status=[interface.OrderStatus.PENDING,
            interface.OrderStatus.PLACED],
    max_count=5)

# place order
trade_api.create_order(instrument_id=instrument_id,
                       offer_type=interface.OfferType.BID,
                       order_type=interface.OrderType.LIMIT,
                       price=5.2,
                       quantity=1)

# cancel orders
orders_filtered = trade_api.get_orders(instrument_id=instrument_id,
                                       status=[interface.OrderStatus.PENDING,
                                               interface.OrderStatus.PLACED])
# Cancel an order
for order in orders_filtered:
    order_id = order['orderID']
    print('Create BID order', order_id)
    trade_api.cancel_order(order_id=order_id)
    print('Cancel BID order', order_id)

# cancel all orders for given instrument
trade_api.cancel_all_orders(instrument_id=instrument_id)

```

This example only shows how to try naive trading.
For more examples. Take a look at the [examples](docs/examples/) directory.


## Tests
To run the tests locally check out the SDK source
and install `test` extra with `pip install -e .[test]`

### Unit tests
Run unit tests with `pytest tests/unit/`

### Integration tests
Integration tests run against the real API and need setting up trader
account that you want to test with. You need to provide two env vars:
`BLOCKEX_TEST_TRADEAPI_USERNAME` and `BLOCKEX_TEST_TRADEAPI_PASSWORD`
to make tests work.

By default tests will run against
[blockexmarkets.com](https://blockexmarkets.com) API. To run tests against
another API instance provide optional `BLOCKEX_TEST_TRADEAPI_URL`
and `BLOCKEX_TEST_TRADEAPI_ID` env vars.

Run integration tests with `pytest tests/integration/`.

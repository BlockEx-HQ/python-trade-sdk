# BlockEx Trade API SDK
_v0.0.1_

## Description
BlockEx Trade API SDK is a Python client package for the Trade API
of BlockEx Digital Asset eXchange Platform. Its purpose is to provide an
easy integration of Python-based systems with the BlockEx Trade API.

The module consists of client implementations of API resources that
can generally be grouped into four categories:

 - Trader authentication
 - Getting instruments
 - Getting open orders
 - Placing/cancelling orders
 - Receiving trade events

## Installation
Tested and working on Python 3.6.4+.

```
pip install git+https://github.com/BlockEx-HQ/python-trade-sdk --process-dependency-links
```

## Usage examples

Below is a set of short example, see full example in 
`examples/trade_api.py` in this package's repo.

```
# initiate the API wrapper object:
trade_api = BlockExTradeApi('username', 'password')

# get list of available trader instruments
trader_instruments = trade_api.get_trader_instruments()

# get full list of trader orders
orders = trade_api.get_orders()

# get filtered list of trader orders
orders_filtered = trade_api.get_orders(instrument_id=1,
                                       order_type=OrderType.LIMIT,
                                       offer_type=OfferType.BID,
                                       status='10,20',
                                       load_executions=True,
                                       max_count=5)

# get full list of market orders
market_orders = trade_api.get_market_orders(instrument_id=1)

# get filtered list of market orders
market_orders_filtered = trade_api.get_market_orders(
	instrument_id=1,
	order_type=OrderType.LIMIT,
	offer_type=OfferType.BID,
	status='10,20',
	max_count=5)

# place order
trade_api.create_order(offer_type=OfferType.BID,
                       order_type=OrderType.LIMIT,
                       instrument_id=1,
                       price=5.2,
                       quantity=1)

# cancel order
trade_api.cancel_order(order_id=32598)

# cancel all orders for given instrument
trade_api.cancel_all_orders(instrument_id=1)
```

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

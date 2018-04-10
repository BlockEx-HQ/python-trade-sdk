# BlockEx Trade API SDK

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
Tested and working on Python 2.7.* and Python 3.6.*.

```
pip install blockex.tradeapi
```

## Usage examples

Please see full example in `examples/trade_api.py` in this package's repo.

```
# initiate the API wrapper object:
trade_api = BlockExTradeApi('https://api.blockex.com/', PartnerAPI,
                            '<traderusername>', '<traderpassword>')

# get list of available trader instruments
trader_instruments = trade_api.get_trader_instruments()

# get list of available partner instruments
partner_instruments = trade_api.get_partner_instruments()

# get unfiltered list of trader orders
orders = trade_api.get_orders()

# get filtered list of trader orders
orders_filtered = trade_api.get_orders(instrument_id=1,
                                       order_type=OrderType.LIMIT,
                                       offer_type=OfferType.BID,
                                       status='10,20',
                                       load_executions=True,
                                       max_count=5)

# get unfiltered list of market orders
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

# cancel all order for instrument
trade_api.cancel_all_orders(instrument_id=1)
```

## Long

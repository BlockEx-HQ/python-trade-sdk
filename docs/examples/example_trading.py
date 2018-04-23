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

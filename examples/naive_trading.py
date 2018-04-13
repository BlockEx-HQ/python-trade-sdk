#!/usr/bin/env python
from signalr_aio import Connection
import json

from blockex.tradeapi.tradeapi import BlockExTradeApi
from blockex.tradeapi import C


API_URL = 'https://api.blockex.com/'
API_ID = '7c11fb8e-f744-47ee-aec2-9da5eb83ad84'
USERNAME = ''
PASSWORD = ''

# own orders need to be tracked to separate events
own_orders = set()

# order executed event handler
async def order_executed(msg):
    order_details = json.loads(msg)
    print(f">>> instrument {order_details['instrumentID']} "
          f"new price {order_details['price']}")

    if order_details['id'] in own_orders:
        print(f">>> OWN ORDER {order_details['id']} EXECUTED ")
        own_orders.discard(order_details['id'])

# generic message event handler
async def on_message(msg):
    print('>>> MSG', msg)


if __name__ == "__main__":
    # setup REST API connection
    trade_api = BlockExTradeApi(USERNAME, PASSWORD, API_URL, API_ID)
    access_token = trade_api.login()

    # setup SignalR connecton
    connection = Connection(f"{API_URL}/signalr", session=None)
    hub = connection.register_hub('TradingHub')

    # set event handlers
    hub.client.on('MarketOrdersRefreshed', on_message)
    hub.client.on('MarketTradesRefreshed', on_message)

    trader_instruments = trade_api.get_trader_instruments()

    # pick an instrument to work with
    instrument_id = trader_instruments[0]['id']

    # cancel all orders for instrument 0
    trade_api.cancel_all_orders(instrument_id=instrument_id)

    # get highest bid order and consume it
    highest_bid_order = trade_api.get_highest_bid_order(instrument_id=instrument_id)
    trade_api.create_order(offer_type=C.OfferType.ASK,
                           order_type=C.OrderType.LIMIT,
                           instrument_id=instrument_id,
                           price=highest_bid_order['price'],
                           quantity=highest_bid_order['quantity'])

    # get lowest ask order and consume it
    lowest_ask_order = trade_api.get_lowest_ask_order(instrument_id=instrument_id)
    trade_api.create_order(offer_type=C.OfferType.ASK,
                           order_type=C.OrderType.LIMIT,
                           instrument_id=instrument_id,
                           price=lowest_ask_order['price'],
                           quantity=lowest_ask_order['quantity'])

    # set new ask 0.05 EUR off
    lowest_ask_order = trade_api.get_lowest_ask_order(instrument_id=instrument_id)
    trade_api.create_order(offer_type=C.OfferType.ASK,
                           order_type=C.OrderType.LIMIT,
                           instrument_id=instrument_id,
                           price=lowest_ask_order['price']+0.05,
                           quantity=lowest_ask_order['quantity'])

    # get own ask orders
    my_ask_orders = trade_api.get_orders(instrument_id=instrument_id,
                                         order_type=C.OrderType.LIMIT,
                                         offer_type=C.OfferType.ASK,
                                         status=[C.OrderStatus.PLACED],
                                         load_executions=False,
                                         max_count=1)
    # cancel all own ask orders
    for order in my_ask_orders:
        trade_api.cancel_order(order['id'])

    # set new, higher ask
    trade_api.create_order(offer_type=C.OfferType.ASK,
                           order_type=C.OrderType.LIMIT,
                           instrument_id=instrument_id,
                           price=lowest_ask_order['price']+0.10,
                           quantity=lowest_ask_order['quantity'])

    #run the event loop
    connection.start()

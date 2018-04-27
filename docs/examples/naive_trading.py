#!/usr/bin/env python
import sys
from decimal import Decimal

from blockex.tradeapi import interface
from blockex.tradeapi.tradeapi import BlockExTradeApi

if sys.version_info < (3, 5, 3):
    sys.exit('Sorry, Python < 3.5.3 is not supported for this example.')
else:
    from signalr_aio import Connection

API_URL = 'https://api.blockex.com/'
API_ID = '7c11fb8e-f744-47ee-aec2-9da5eb83ad84'
USERNAME = ''
PASSWORD = ''

BID_ORDER_PRICE = Decimal(5)
BID_ORDER_QUANTITY = Decimal(0.5)
ASK_ORDER_PRICE = Decimal(1)
ASK_ORDER_QUANTITY = Decimal(0.1)


# Create hub message handler
async def on_message(msg):
    print(msg)


def _cancell_all_orders(trade_api, instrument_id, offertype):
    # Get own orders
    my_orders = trade_api.get_orders(instrument_id=instrument_id,
                                     offer_type=offertype,
                                     order_type=interface.OrderType.LIMIT,
                                     status=[interface.OrderStatus.PLACED],
                                     load_executions=False,
                                     max_count=1)
    # Cancel all own orders
    for order in my_orders:
        name_id = 'orderID' if offertype == interface.OfferType.BID else 'id'
        print('Cancel BID order', order[name_id])
        trade_api.cancel_order(order[name_id])


def highest_bid_order(trade_api, instrument_id):
    # Get highest bid order price and quantity
    highest_bid = trade_api.get_highest_bid_order(instrument_id=instrument_id)
    highest_bid_order_price = highest_bid.get('price') or BID_ORDER_PRICE
    highest_bid_order_quantity = highest_bid.get('quantity') or BID_ORDER_QUANTITY

    # Create highest BID order and consume it
    trade_api.create_order(instrument_id=instrument_id,
                           offer_type=interface.OfferType.BID,
                           order_type=interface.OrderType.LIMIT,
                           price=highest_bid_order_price,
                           quantity=highest_bid_order_quantity)

    # Set new BID 5 EUR off
    highest_bid = trade_api.get_highest_bid_order(instrument_id=instrument_id)
    trade_api.create_order(instrument_id=instrument_id,
                           offer_type=interface.OfferType.BID,
                           order_type=interface.OrderType.LIMIT,
                           price=highest_bid['price'] + BID_ORDER_PRICE,
                           quantity=highest_bid['quantity'] + BID_ORDER_QUANTITY)

    _cancell_all_orders(trade_api, instrument_id, interface.OfferType.BID)

def lowest_ask_order(trade_api, instrument_id):
    lowest_ask = trade_api.get_lowest_ask_order(instrument_id=instrument_id)
    lowest_ask_order_price = lowest_ask.get('price') or ASK_ORDER_QUANTITY
    lowest_ask_order_quantity = lowest_ask.get('quantity') or ASK_ORDER_QUANTITY

    # Get lowest ASK order and consume it
    trade_api.create_order(instrument_id=instrument_id,
                           offer_type=interface.OfferType.ASK,
                           order_type=interface.OrderType.LIMIT,
                           price=lowest_ask_order_price,
                           quantity=lowest_ask_order_quantity)

    _cancell_all_orders(trade_api, instrument_id, interface.OfferType.ASK)

def main():
    # Setup REST API connection
    trade_api = BlockExTradeApi(USERNAME, PASSWORD, API_URL, API_ID)
    _ = trade_api.login() # That's just a example we don't need access_token

    # Setup SignalR connecton
    connection = Connection(f"{API_URL}/signalr", session=None)
    hub = connection.register_hub('TradingHub')

    # Set event handlers
    hub.client.on('MarketOrdersRefreshed', on_message)

    trader_instruments = trade_api.get_trader_instruments()

    # Pick an instrument to work with
    instrument_id = trader_instruments[0]['id']

    # Cancel all orders for instrument 0
    trade_api.cancel_all_orders(instrument_id=instrument_id)

    lowest_ask_order(trade_api, instrument_id)
    highest_bid_order(trade_api, instrument_id)

    # Run the event loop
    connection.start()

if __name__ == "__main__":
    main()

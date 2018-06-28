#!/usr/bin/env python
import os

from blockex.tradeapi import interface
from blockex.tradeapi.tradeapi import BlockExTradeApi

API_URL = os.environ.get('BLOCKEX_TEST_TRADEAPI_URL')
API_ID = os.environ.get('BLOCKEX_TEST_TRADEAPI_ID')
USERNAME = os.environ.get('BLOCKEX_TEST_TRADEAPI_USERNAME')
PASSWORD = os.environ.get('BLOCKEX_TEST_TRADEAPI_PASSWORD')


def main():
    # Create Trade API instance
    trade_api = BlockExTradeApi(username=USERNAME, password=PASSWORD,
                                api_url=API_URL, api_id=API_ID)

    # Get trader instruments
    trader_instruments = trade_api.get_trader_instruments()

    price = trade_api.get_highest_bid_order(instrument_id=trader_instruments[0]['id'])
    print('Highest Bid Order >>>', price)

    price = trade_api.get_lowest_ask_order(instrument_id=trader_instruments[0]['id'])
    print('Lowest Ask Order >>>', price)

    market_orders_filtered = trade_api.get_market_orders(
        instrument_id=trader_instruments[0]['id'],
        order_type=interface.OrderType.LIMIT,
        offer_type=interface.OfferType.ASK,
        status=[interface.OrderStatus.PLACED],
        max_count=2)

    for order in market_orders_filtered:
        print('Orders filtered >>>', order)

    # Get partner instruments
    partner_instruments = trade_api.get_partner_instruments()
    print('Partner Instruments >>>', partner_instruments)

    # Get trader orders unfiltered
    orders = trade_api.get_orders()
    print('Trader Orders >>>', orders)

    # Get trader orders filtered
    orders_filtered = trade_api.get_orders(instrument_id=trader_instruments[0]['id'],
                                           order_type=interface.OrderType.LIMIT,
                                           offer_type=interface.OfferType.BID,
                                           status=[interface.OrderStatus.PENDING,
                                                   interface.OrderStatus.PLACED],
                                           load_executions=True,
                                           max_count=5)
    print('Trader Orders Filtered >>>', orders_filtered)

    # Get market orders unfiltered
    market_orders = trade_api.get_market_orders(instrument_id=trader_instruments[0]['id'])
    orders = trade_api.get_orders()
    print('Market Orders >>>', orders)

    # Get market orders filtered
    market_orders_filtered = trade_api.get_market_orders(
        instrument_id=1,
        order_type=interface.OrderType.LIMIT,
        offer_type=interface.OfferType.BID,
        status=[interface.OrderStatus.PENDING, interface.OrderStatus.PLACED],
        max_count=5)
    print('Market Orders Filtered >>>', orders)

    # cancel all orders
    trade_api.cancel_all_orders(instrument_id=trader_instruments[0]['id'])

    # Place order
    trade_api.create_order(offer_type=interface.OfferType.BID,
                           order_type=interface.OrderType.LIMIT,
                           instrument_id=trader_instruments[0]['id'],
                           price=5.2,
                           quantity=1)

    # get open orders for instrument
    orders_filtered = trade_api.get_orders(instrument_id=trader_instruments[0]['id'],
                                           status=[interface.OrderStatus.PENDING,
                                                   interface.OrderStatus.PLACED])
    print('Trader Orders >>>', orders_filtered)

    # Cancel an order
    trade_api.cancel_order(order_id=orders_filtered[0]['orderID'])


if __name__ == "__main__":
    main()

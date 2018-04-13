from blockex.tradeapi.tradeapi import BlockExTradeApi
from blockex.tradeapi import C


def main():
    API_URL = 'https://api.blockex.com/'
    API_ID = '7c11fb8e-f744-47ee-aec2-9da5eb83ad84'

    USERNAME = ''
    PASSWORD = ''

    # Create Trade API instance
    trade_api = BlockExTradeApi(username=USERNAME,
                                password=PASSWORD,
                                api_url=API_URL,
                                api_id=API_ID,)

    # Get trader instruments
    trader_instruments = trade_api.get_trader_instruments()

    price = trade_api.get_highest_bid_order(instrument_id=trader_instruments[0]['id'])
    print('>>>', price)

    price = trade_api.get_lowest_ask_order(instrument_id=trader_instruments[0]['id'])
    print('>>>', price)

    market_orders_filtered = trade_api.get_market_orders(
        instrument_id=trader_instruments[0]['id'],
        order_type=C.OrderType.LIMIT,
        offer_type=C.OfferType.ASK,
        status=[C.OrderStatus.PLACED],
        max_count=2)
    for order in market_orders_filtered:
        print('>>>', order)

    # Get partner instruments
    partner_instruments = trade_api.get_partner_instruments()
    print('>>> partner instruments:', partner_instruments)

    # Get trader orders unfiltered
    orders = trade_api.get_orders()
    print('>>> trader orders:', orders)

    # Get trader orders filtered
    orders_filtered = trade_api.get_orders(instrument_id=trader_instruments[0]['id'],
                                           order_type=C.OrderType.LIMIT,
                                           offer_type=C.OfferType.BID,
                                           status=[C.OrderStatus.PENDING, C.OrderStatus.PLACED],
                                           load_executions=True,
                                           max_count=5)
    print('>>> trader orders filtered:', orders_filtered)

    # Get market orders unfiltered
    market_orders = trade_api.get_market_orders(instrument_id=trader_instruments[0]['id'])
    orders = trade_api.get_orders()
    print('>>> market orders:', orders)

    # Get market orders filtered
    market_orders_filtered = trade_api.get_market_orders(
        instrument_id=1,
        order_type=C.OrderType.LIMIT,
        offer_type=C.OfferType.BID,
        status=[C.OrderStatus.PENDING, C.OrderStatus.PLACED],
        max_count=5)
    print('>>> market orders filtered:', orders)

    # cancel all orders
    trade_api.cancel_all_orders(instrument_id=trader_instruments[0]['id'])

    # Place order
    trade_api.create_order(offer_type=C.OfferType.BID,
                           order_type=C.OrderType.LIMIT,
                           instrument_id=trader_instruments[0]['id'],
                           price=5.2,
                           quantity=1)

    # get open orders for instrument
    orders_filtered = trade_api.get_orders(instrument_id=trader_instruments[0]['id'],
                                           status=[C.OrderStatus.PENDING, C.OrderStatus.PLACED],
                                           )
    print('>>> trader orders:', orders_filtered)

    # Cancel an order
    trade_api.cancel_order(order_id=orders_filtered[0]['id'])

if __name__ == '__main__':
    main()

from blockex.tradeapi.tradeapi import BlockExTradeApi
from blockex.tradeapi import C


def main():
    # API URL defaults to https://api.blockex.com/
    API_URL = None

    # partner API ID, defaults to 7c11fb8e-f744-47ee-aec2-9da5eb83ad84 (blockexmarkets.com)
    API_ID = None

    # trader username, must be provided
    USERNAME = ''

    # trader password, must be provided
    PASSWORD = ''

    try:
        # Create Trade API instance
        trade_api = BlockExTradeApi(username=USERNAME,
                                    password=PASSWORD,
                                    api_url=API_URL,
                                    api_id=API_ID,)

        # Get trader instruments
        trader_instruments = trade_api.get_trader_instruments()
        print('>>> trader instruments:', trader_instruments)

        # Get partner instruments
        partner_instruments = trade_api.get_partner_instruments()
        print('>>> partner instruments:', partner_instruments)

        # Get trader orders unfiltered
        orders = trade_api.get_orders()
        print('>>> trader orders:', orders)

        # Get trader orders filtered
        orders_filtered = trade_api.get_orders(instrument_id=1,
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

        # Cancel latest order
        trade_api.cancel_order(order_id=orders_filtered[0]['id'])

        # The following scenario gets all the instruments available for the trader and iterates them.
        # For each instrument all orders are cancelled at first. Then the best bid and ask prices are
        # obtained from the existing orders on the market. These best prices are used to create new
        # orders of type 'Market'.
        trader_instruments = trade_api.get_trader_instruments()

        for instrument in trader_instruments:
            try:
                trade_api.cancel_all_orders(instrument['id'])

                ask_market_orders = trade_api.get_market_orders(instrument['id'],
                                                                C.OrderType.MARKET,
                                                                C.OfferType.BID,
                                                                [C.OrderStatus.PLACED,
                                                                 C.OrderStatus.PARTEXECUTED,],
                                                                1000)
                if ask_market_orders:
                    ask_market_orders_prices = [order['price'] for order in ask_market_orders]
                    best_bid_price = min(ask_market_orders_prices)
                    trade_api.create_order(C.OfferType.BID, C.OrderType.LIMIT,
                                           instrument['id'], best_bid_price, 1)

                bid_market_orders = trade_api.get_market_orders(instrument['id'],
                                                                C.OrderType.MARKET,
                                                                C.OfferType.BID,
                                                                [C.OrderStatus.PLACED,
                                                                 C.OrderStatus.PARTEXECUTED,],
                                                                1000)
                if bid_market_orders:
                    bid_market_orders_prices = [order['price'] for order in bid_market_orders]
                    best_ask_price = max(bid_market_orders_prices)
                    trade_api.create_order(C.OfferType.ASK, C.OrderType.LIMIT,
                                           instrument['id'], best_ask_price, 1)
            except Exception as err:
                print(err)
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()

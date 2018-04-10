from blockex.tradeapi.tradeapi import BlockExTradeApi
from blockex.tradeapi import C


def main():
    # The API URL, defaults to https://api.blockex.com/
    api_url = None

    # The Partner's API ID, defaults to 7c11fb8e-f744-47ee-aec2-9da5eb83ad84 (blockexmarkets.com)
    api_id = None

    # The Trader''s username, must be provided
    username = ''

    # The Trader''s password, must be provided
    password = ''

    try:
        # Create Trade API instance
        trade_api = BlockExTradeApi(username=username,
                                    password=password,
                                    api_url=api_url,
                                    api_id=api_id,)

        # Get trader instruments
        trader_instruments = trade_api.get_trader_instruments()

        # Get partner instruments
        partner_instruments = trade_api.get_partner_instruments()

        # Get trader orders unfiltered
        orders = trade_api.get_orders()

        # Get trader orders filtered
        orders_filtered = trade_api.get_orders(instrument_id=1,
                                               order_type=C.OrderType.LIMIT,
                                               offer_type=C.OfferType.BID,
                                               status=[C.OrderStatus.PENDING, C.OrderStatus.PLACED],
                                               load_executions=True,
                                               max_count=5)

        # Get market orders unfiltered
        market_orders = trade_api.get_market_orders(instrument_id=trader_instruments[0]['id'])

        # Get market orders filtered
        market_orders_filtered = trade_api.get_market_orders(
            instrument_id=1,
            order_type=C.OrderType.LIMIT,
            offer_type=C.OfferType.BID,
            status=[C.OrderStatus.PENDING, C.OrderStatus.PLACED],
            max_count=5)

        # Place order
        trade_api.create_order(offer_type=C.OfferType.BID,
                               order_type=C.OrderType.LIMIT,
                               instrument_id=trader_instruments[0]['id'],
                               price=5.2,
                               quantity=1)

        # Cancel order
        trade_api.cancel_order(order_id=32598)

        # Cancel all orders for an instrument
        trade_api.cancel_all_orders(instrument_id=trader_instruments[0]['id'])

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

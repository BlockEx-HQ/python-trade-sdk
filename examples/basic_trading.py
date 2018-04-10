from blockex.tradeapi.tradeapi import BlockExTradeApi
from blockex.tradeapi.tradeapi import OrderType
from blockex.tradeapi.tradeapi import OfferType


def main():
    # The API URL, e.g. https://api.blockex.com/
    api_url = ''

    # The Partner's API ID
    api_id = ''

    # The Trader''s username
    username = ''

    # The Trader''s password
    password = ''

    try:
        # Create Trade API instance
        trade_api = BlockExTradeApi(api_url=api_url,
                                    api_id=api_id,
                                    username=username,
                                    password=password)

        # Get trader instruments
        trader_instruments = trade_api.get_trader_instruments()

        # Get partner instruments
        partner_instruments = trade_api.get_partner_instruments()

        # Get trader orders unfiltered
        orders = trade_api.get_orders()

        # Get trader orders filtered
        orders_filtered = trade_api.get_orders(instrument_id=1,
                                               order_type=OrderType.LIMIT,
                                               offer_type=OfferType.BID,
                                               status='10,20',
                                               load_executions=True,
                                               max_count=5)

        # Get market orders unfiltered
        market_orders = trade_api.get_market_orders(instrument_id=1)

        # Get market orders filtered
        market_orders_filtered = trade_api.get_market_orders(
            instrument_id=1,
            order_type=OrderType.LIMIT,
            offer_type=OfferType.BID,
            status='10,20',
            max_count=5)

        # Place order
        trade_api.create_order(offer_type=OfferType.BID,
                               order_type=OrderType.LIMIT,
                               instrument_id=1,
                               price=5.2,
                               quantity=1)

        # Cancel order
        trade_api.cancel_order(order_id=32598)

        # Cancel all orders for an instrument
        trade_api.cancel_all_orders(instrument_id=1)

        # The following scenario gets all the instruments available for the trader and iterates them.
        # For each instrument all orders are cancelled at first. Then the best bid and ask prices are
        # obtained from the existing orders on the market. These best prices are used to create new
        # orders of type 'Market'.
        trader_instruments = trade_api.get_trader_instruments()

        for instrument in trader_instruments:
            try:
                instrument_id = instrument['id']

                trade_api.cancel_all_orders(instrument_id)

                ask_market_orders = trade_api.get_market_orders(instrument_id, OrderType.MARKET, OfferType.BID, '20,50', 1000)
                if ask_market_orders:
                    ask_market_orders_prices = [order['price'] for order in ask_market_orders]
                    best_bid_price = min(ask_market_orders_prices)
                    trade_api.create_order(OfferType.BID, OrderType.LIMIT, instrument_id, best_bid_price, 1)

                bid_market_orders = trade_api.get_market_orders(instrument_id, OrderType.MARKET, OfferType.BID, '20,50', 1000)
                if bid_market_orders:
                    bid_market_orders_prices = [order['price'] for order in bid_market_orders]
                    best_ask_price = max(bid_market_orders_prices)
                    trade_api.create_order(OfferType.ASK, OrderType.LIMIT, instrument_id, best_ask_price, 1)
            except Exception as err:
                print(err)
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()

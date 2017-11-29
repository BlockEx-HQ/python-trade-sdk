from blockex.tradeapi import BlockExTradeApi
from blockex.tradeapi import OrderType
from blockex.tradeapi import OfferType
from requests import RequestException


def main():
    # The API URL, e.g. https://api.blockex.com/
    api_url = ''

    # The Partner's API ID
    api_id = ''

    # The Trader''s username
    username = ''

    # The Trader''s password
    password = ''

    assert api_url
    assert api_id
    assert username
    assert password

    # Create Trade API instance
    trade_api = BlockExTradeApi(api_url=api_url,
                                api_id=api_id,
                                username=username,
                                password=password)

    # Trade API login
    try:
        access_token = trade_api.login()
    except RequestException as err:
        print(err)

    # Trade API logout
    try:
        trade_api.logout()
    except RequestException as err:
        print(err)

    # Get trader instruments
    try:
        trader_instruments = trade_api.get_trader_instruments()
    except RequestException as err:
        print(err)

    # Get partner instruments
    try:
        partner_instruments = trade_api.get_partner_instruments()
    except RequestException as err:
        print(err)

    # Get trader orders unfiltered
    try:
        orders = trade_api.get_orders()
    except RequestException as err:
        print(err)

    # Get trader orders filtered
    try:
        orders_filtered = trade_api.get_orders(instrument_id=1,
                                               order_type=OrderType.LIMIT,
                                               offer_type=OfferType.BID,
                                               status='10,20',
                                               load_executions=True,
                                               max_count=5)
    except RequestException as err:
        print(err)

    # Get market orders unfiltered
    try:
        market_orders = trade_api.get_market_orders(1)
    except RequestException as err:
        print(err)

    # Get market orders filtered
    try:
        market_orders_filtered = trade_api.get_market_orders(
            instrument_id=1,
            order_type=OrderType.LIMIT,
            offer_type=OfferType.BID,
            status='10,20',
            max_count=5)
    except RequestException as err:
        print(err)

    # Place order
    try:
        trade_api.create_order(offer_type=OfferType.BID,
                               order_type=OrderType.LIMIT,
                               instrument_id=1,
                               price=5.2,
                               quantity=1)
    except RequestException as err:
        print(err)

    # Cancel order
    try:
        trade_api.cancel_order(32598)
    except RequestException as err:
        print(err)

    # Cancel order
    try:
        trade_api.cancel_all_orders(1)
    except RequestException as err:
        print(err)


if __name__ == '__main__':
    main()

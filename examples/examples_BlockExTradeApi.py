from BlockExTradeApi import BlockExTradeApi

# The API URL, e.g. https://api.blockex.com/
api_url = ''

# The Partner's API ID
api_id = ''

# The Trader''s username
username = ''

# The Trader''s password
password = ''

if not api_url:
    raise ValueError('The API URL must be set.')
if not api_id:
    raise ValueError('The API ID must be set.')
if not username:
    raise ValueError('The Trader''s username must be set.')
if not password:
    raise ValueError('The Trader''s password must be set.')

# Create Trade API instance
trade_api = BlockExTradeApi(api_url, api_id, username, password)

# Trade API login
login_result = trade_api.login()
login_response = login_result['response']
if login_response.status_code == 200:
    access_token = login_result['access_token']

# Trade API logout
logout_result = trade_api.logout()
logout_response = logout_result['response']

# Get trader instruments
get_trader_instruments_result = trade_api.get_trader_instruments()
get_trader_instruments_response = get_trader_instruments_result['response']
if get_trader_instruments_response.status_code == 200:
    trader_instruments = get_trader_instruments_result['data']

# Get partner instruments
get_partner_instruments_result = trade_api.get_partner_instruments()
get_partner_instruments_response = get_partner_instruments_result['response']
if get_partner_instruments_response.status_code == 200:
    partner_instruments = get_partner_instruments_result['data']

# Get trader orders unfiltered
get_orders_result = trade_api.get_orders()
get_orders_response = get_orders_result['response']
if get_orders_response.status_code == 200:
    orders = get_orders_result['data']

# Get trader orders filtered
get_orders_filtered_result = trade_api.get_orders(
    1, 'Limit', 'Bid', '10,20', 'true', 5)
get_orders_filtered_response = get_orders_filtered_result['response']
if get_orders_filtered_response.status_code == 200:
    orders_filtered = get_orders_filtered_result['data']

# Get market orders unfiltered
get_market_orders_result = trade_api.get_market_orders(1)
get_market_orders_response = get_market_orders_result['response']
if get_market_orders_response.status_code == 200:
    market_orders = get_market_orders_result['data']

# Get market orders filtered
get_market_orders_filtered_result = trade_api.get_market_orders(
    1, 'Limit', 'Bid', '10,20', 5)
get_market_orders_filtered_response =\
    get_market_orders_filtered_result['response']
if get_market_orders_filtered_response.status_code == 200:
    market_orders_filtered = get_market_orders_filtered_result['data']

# Place order
create_order_result = trade_api.create_order('Bid', 'Limit', 1, 5.2, 1)
create_order_response = create_order_result['response']

# Cancel order
cancel_order_result = trade_api.cancel_order(32598)
cancel_order_response = cancel_order_result['response']

# Cancel order
cancel_all_orders_result = trade_api.cancel_all_orders(1)
cancel_all_orders_response = cancel_all_orders_result['response']

import asyncio
import websockets
from blockex.tradeapi import BlockExTradeApi

# The API URL, e.g. https://api.blockex.com/
API_URL = 'https://api-tst.blockex.com/'

# The Partner's API ID
API_ID = '7c11fb8e-f744-47ee-aec2-9da5eb83ad84'

# The Trader''s username
USERNAME = 'dobri'

# The Trader''s password
PASSWORD = '123qwe!@#'

trade_api = BlockExTradeApi(API_URL, API_ID, USERNAME, PASSWORD)
access_token = trade_api.login()

async def tradeapi_websocket_connection():
    async with websockets.connect('wss://api-tst.blockex.com?access_token=' + access_token) as websocket:
        # Once the websocket connection is established, the messages received from different Trade API events
        # should be handled. Not clear how this is done with the websockets library but it could be connected
        # with the method recv() somehow. The useful events here are:
        # marketOrdersRefreshed - all listeners are notified when there is a change in the orders on the market
        # marketTradesRefreshed - all listeners are notified when there is a change in the trades on the market
        # tradeCreated - the buyer and the seller are notified when their orders are matched and a trade is created

        result = await websocket.recv() # Possibly use recv() somehow?

asyncio.get_event_loop().run_until_complete(tradeapi_websocket_connection())

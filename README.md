# BlockEx Trade API SDK #

## Description ##
BlockEx Trade API SDK is a Python client module for the Trade API of BlockEx Digital Asset Platform. Its purpose is to provide an easy integration of Python-based systems with the BlockEx Trade API.

The module consists of client implementations of API resources that can generally be grouped into four categories:

 - Trader authentication
 - Getting instruments
 - Getting orders
 - Placing/cancelling orders

## Installation ##
```
pip install blockex-tradeapi
```

## Prerequisites ##
Tested on Python 2.7.14 and Python 3.6.2. To install dependencies:
```
pip install six enum34
```

## Usage and Examples
The code can be found in the file `BlockExTradeApi.py`, which is available in the source of this repository. An instance of the class `BlockExTradeApi` must be created and initialized with the URL of the Trade API and the credentials for it. The class is stateful and when an instance of it is logged in the API, it keeps the API access token and uses it for the API requests that are made. In case of API call when the access token has expired, a login is performed and the API request is sent again.

### Examples

#### Create Instance
```
trade_api = BlockExTradeApi('https://api.blockex.com/', '5c65fb8e-f258-12ee-aec2-4da5eb77ad21', 'traderusername', 'traderpassword')
```

The methods of the created instance can be directly used to make API calls.

#### Get trader instruments
```
trader_instruments = trade_api.get_trader_instruments()
```

#### Get partner instruments
```
partner_instruments = trade_api.get_partner_instruments()
```

#### Get trader orders unfiltered
```
orders = trade_api.get_orders()
```

#### Get trader orders filtered
```
orders_filtered = trade_api.get_orders(instrument_id=1,
									   order_type=OrderType.LIMIT,
									   offer_type=OfferType.BID,
									   status='10,20',
									   load_executions=True,
									   max_count=5)
```

#### Get market orders unfiltered
```
market_orders = trade_api.get_market_orders(instrument_id=1)
```

#### Get market orders filtered
```
market_orders_filtered = trade_api.get_market_orders(
	instrument_id=1,
	order_type=OrderType.LIMIT,
	offer_type=OfferType.BID,
	status='10,20',
	max_count=5)
```

#### Place order
```
trade_api.create_order(offer_type=OfferType.BID,
					   order_type=OrderType.LIMIT,
					   instrument_id=1,
					   price=5.2,
					   quantity=1)
```

#### Cancel order
```
trade_api.cancel_order(order_id=32598)
```

#### Cancel all orders for an instrument
```
trade_api.cancel_all_orders(instrument_id=1)
```

#### Create Bid and Ask best price orders for each available instrument
The following scenario gets all the instruments available for the trader and iterates them. For each instrument all orders are cancelled at first. Then the best bid and ask prices are obtained from the existing orders on the market. These best prices are used to create new orders of type 'Market'.

```
trader_instruments = trade_api.get_trader_instruments()
for instrument in trader_instruments:
	try:
		trade_api.cancel_all_orders(instrument_id=1)

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
```

**All the examples can be found in ```examples/examples_tradeapi.py```.**

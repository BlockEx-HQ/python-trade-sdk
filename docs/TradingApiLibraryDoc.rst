``class BlockExTradeApi``
=========================
 This class consists of the implementation of all the methods needed to access the BlockEx Trading API resources supported by the library. The class is stateful and when an instance of it is logged in the API, it keeps the API access token and uses it for the API requests that are made. In case of API call when the access token has expired, a login is performed and the API request is sent again.

 An object of the class can be created using the constructor:

 ``__init__(api_url, api_id, username, password)``

 and providing the necessary values. An example of instance creation is the following:

 ``trade_api = BlockExTradeApi('https://api.blockex.com/', '5c65fb8e-f258-12ee-aec2-4da5eb77ad21', 'traderusername', 'traderpassword')``

Public methods of ``class BlockExTradeApi``
===========================================
 The class consists of public methods for API requests that can be grouped into four categories.

Trader authentication methods
-----------------------------
``login()``
^^^^^^^^^^^
 Performs a login and stores the received access token
 
Arguments:
""""""""""
 No input arguments
 
Return value:
"""""""""""""
 Returns a ``dict`` with an element ``'response'`` that has the response object from the Trading API request. When the response HTTP status code is 200, the dict includes an element ``'access_token'`` with the value of the received access token.
 
Example:
""""""""
 ``trade_api.login()``
 
``logout()``
^^^^^^^^^^^^
 Performs a logout when logged in and deletes the stored access token
 
Arguments:
""""""""""
 No input arguments
 
Return value:
"""""""""""""

 Returns a ``dict`` with an element ``'response'`` that has the response object from the Trading API request.
 
Example:
""""""""
 ``trade_api.logout()``
 
Getting instruments methods
---------------------------
``get_trader_instruments()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 Gets the available instruments for the trader.
 
Arguments:
""""""""""
 No input arguments
 
Return value:
"""""""""""""
 Returns a ``dict`` with an element ``'response'`` that has the response object from the Trading API request. When the response HTTP status code is 200, the dict includes an element ``'data'`` with a list of instruments. Each instrument is a ``dict`` with the following elements:
  - ``id`` (``integer``)
  - ``description`` (``string``)
  - ``name`` (``string``)
  - ``baseCurrencyID`` (``integer``) - The currency you bid for, i.e. for the Bitcoin/Euro pair, base currency is the Bitcoin.
  - ``quoteCurrencyID`` (``integer``) - The currency you pay with, i.e. for the Bitcoin/Euro pair, quote currency is the Euro.
  - ``minOrderAmount`` (``float``) - The minimum order amount for an order. Every order having an amount less than that, will be rejected.
  - ``commissionFeePercent`` (``float``) - The percent of the commission fee when trading this instrument. The value is a decimal between 0 and 1.
 
Example:
""""""""
 ``instruments = trade_api.get_trader_instruments()``
 
 The value of ``instruments['data']`` is:

 ``[{'id': 1, 'description': 'Bitcoin/Euro', 'name': 'BTC/EUR', 'baseCurrencyID': 43, 'quoteCurrencyID': 2, 'minOrderAmount': 0.0, 'commissionFeePercent': 0.02}, {'id': 2, 'description': 'Ethereum/Euro', 'name': 'ETH/EUR', 'baseCurrencyID': 46, 'quoteCurrencyID': 2, 'minOrderAmount': 9.0, 'commissionFeePercent': 0.025}, {'id': 3, 'description': 'XTN/Euro', 'name': 'XTN/EUR', 'baseCurrencyID': 45, 'quoteCurrencyID': 2, 'minOrderAmount': 0.0, 'commissionFeePercent': 0.0}, {'id': 4, 'description': 'ETH4/Euro', 'name': 'ETH4/EUR', 'baseCurrencyID': 47, 'quoteCurrencyID': 2, 'minOrderAmount': 0.0, 'commissionFeePercent': 0.0}]``

``get_partner_instruments()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 Gets the available instruments for the partner.

Arguments:
""""""""""
 No input arguments
 
Return value:
"""""""""""""
 Returns a ``dict`` with an element ``'response'`` that has the response object from the Trading API request. When the response HTTP status code is 200, the ``dict`` includes an element ``'data'`` with a list of instruments. Each instrument is a ``dict`` with the following elements:
  - ``id`` (``integer``)
  - ``description`` (``string``)
  - ``name`` (``string``)
  - ``baseCurrencyID`` (``integer``) - The currency you bid for, i.e. for the Bitcoin/Euro pair, base currency is the Bitcoin.
  - ``quoteCurrencyID`` (``integer``) - The currency you pay with, i.e. for the Bitcoin/Euro pair, quote currency is the Euro.
  - ``minOrderAmount`` (``float``) - The minimum order amount for an order. Every order having an amount less than that, will be rejected.
  - ``commissionFeePercent`` (``float``) - The percent of the commission fee when trading this instrument. The value is a decimal between 0 and 1.

Example:
""""""""
 ``instruments = trade_api.get_partner_instruments()``

 The value of ``instruments['data']`` is:

 ``[{'id': 1, 'description': 'Bitcoin/Euro', 'name': 'BTC/EUR', 'baseCurrencyID': 43, 'quoteCurrencyID': 2, 'minOrderAmount': 0.0, 'commissionFeePercent': 0.02}, {'id': 2, 'description': 'Ethereum/Euro', 'name': 'ETH/EUR', 'baseCurrencyID': 46, 'quoteCurrencyID': 2, 'minOrderAmount': 9.0, 'commissionFeePercent': 0.025}, {'id': 3, 'description': 'XTN/Euro', 'name': 'XTN/EUR', 'baseCurrencyID': 45, 'quoteCurrencyID': 2, 'minOrderAmount': 0.0, 'commissionFeePercent': 0.0}, {'id': 4, 'description': 'ETH4/Euro', 'name': 'ETH4/EUR', 'baseCurrencyID': 47, 'quoteCurrencyID': 2, 'minOrderAmount': 0.0, 'commissionFeePercent': 0.0}]``

Getting orders methods
----------------------
``get_orders(instrument_id=None, order_type=None, offer_type=None, status=None, load_executions=None, max_count=None)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 Gets the orders of the trader with the ability to apply filters.
 
Arguments:
""""""""""
  - ``instrument_id`` (``integer``, *optional*) - Instrument identifier. Use ``get_trader_instruments()`` to retrieve them.
  - ``order_type`` (``string``, *optional*) - Order type. Possible values 'Limit', 'Market' and 'Stop'.
  - ``offer_type`` (``string``, *optional*) - Offer type. Possible values 'Bid' and 'Ask'.
  - ``status`` (``string``, *optional*) - Order status. A comma separated list of integers with possible values 10(Pending), 15(Failed), 20(Placed), 30(Rejected), 40(Cancelled), 50(PartiallyExecuted) and 60(Executed).
  - ``load_executions`` (``boolean``, *optional*) - Specifies whether to load executed trades for an order. Default value is False.
  - ``max_count`` (``integer``, *optional*) - Maximum number of items returned. Default value is 100.
 
Return value:
"""""""""""""
 Returns a ``dict`` with an element ``'response'`` that has the response object from the Trading API request. When the response HTTP status code is 200, the ``dict`` includes an element ``'data'`` with a list of orders. Each order is a ``dict`` with the following elements:
  - ``orderID`` (``string``)
  - ``price`` (``float``)
  - ``initialQuantity`` (``float``)
  - ``quantity`` (``float``)
  - ``dateCreated`` (``string``)
  - ``offerType`` (``integer``) - Possible values 1 (Bid) and 2 (Ask).
  - ``type`` (``integer``) - Possible values 1 (Limit), 2 (Market) and 3 (Stop).
  - ``status`` (``integer``) - Possible values 10 (Pending), 15 (Failed), 20 (Placed), 30 (Rejected), 40 (Cancelled), 50 (PartiallyExecuted) and 60 (Executed).
  - ``instrumentID`` (``integer``)
  - ``trades`` (a list of trades)
    
 Each trade in the returned list of trades is a dict with the following elements:
  - ``tradeID`` (``string``)
  - ``price`` (``float``)
  - ``totalPrice`` (``float``)
  - ``quantity`` (``float``)
  - ``tradeDate`` (``string``)
  - ``currencyID`` (``integer``)
  - ``quoteCurrencyID`` (``integer``)
  - ``instrumentID`` (``integer``)
  - ``offerType`` (``integer``) - Possible values 1 (Bid) and 2 (Ask).
 
Example:
""""""""
 ``orders = trade_api.get_orders(1, 'Limit', 'Bid', '10,20', 'true', 50)``

 The value of ``orders['data']`` is:
 
 ``[{'orderID': '32667', 'price': 5.2, 'initialQuantity': 0.3, 'quantity': 0.3, 'dateCreated': '2017-11-06T17:32:23.03787+00:00', 'offerType': 1, 'type': 1, 'status': 20, 'instrumentID': 1, 'trades': None}]``
 

``get_market_orders(instrument_id, order_type=None, offer_type=None, status=None, max_count=None)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 Gets the market orders with the ability to apply filters.
 
Arguments:
""""""""""
  - ``instrument_id`` (``integer``, *optional*) - Instrument identifier. Use ``get_partner_instruments()`` to retrieve them.
  - ``order_type`` (``string``, *optional*) - Order type. Possible values 'Limit', 'Market' and 'Stop'.
  - ``offer_type`` (``string``, *optional*) - Offer type. Possible values 'Bid' and 'Ask'.
  - ``status`` (``string``, *optional*) - Order status. A comma separated list of integers with possible values 10 (Pending), 15 (Failed), 20 (Placed), 30 (Rejected), 40 (Cancelled), 50 (PartiallyExecuted) and 60 (Executed).
  - ``max_count`` (``integer``, *optional*) - Maximum number of items returned. Default value is 100.
 
Return value:
"""""""""""""
 Returns a ``dict`` with an element ``'response'`` that has the response object from the Trading API request. When the response HTTP status code is 200, the ``dict`` includes an element ``'data'`` with a list of orders. Each order is a dict with the following elements:
  - ``orderID`` (``string``)
  - ``price`` (``float``)
  - ``initialQuantity`` (``float``)
  - ``quantity`` (``float``)
  - ``dateCreated`` (``string``)
  - ``offerType`` (``integer``) - Possible values 1 (Bid) and 2 (Ask).
  - ``type`` (``integer``) - Possible values 1 (Limit), 2 (Market) and 3 (Stop).
  - ``status`` (``integer``) - Possible values 10 (Pending), 15 (Failed), 20 (Placed), 30 (Rejected), 40 (Cancelled), 50 (PartiallyExecuted) and 60 (Executed).
  - ``instrumentID`` (``integer``)
  - ``trades`` (a list of trades)
 
 Each trade in the returned list of trades is a dict with the following elements:
  - ``tradeID`` (``string``)
  - ``price`` (``float``)
  - ``totalPrice`` (``float``)
  - ``quantity`` (``float``)
  - ``tradeDate`` (``string``)
  - ``currencyID`` (``integer``)
  - ``quoteCurrencyID`` (``integer``)
  - ``instrumentID`` (``integer``)
  - ``offerType`` (``integer``) - Possible values 1 (Bid) and 2 (Ask).

Example:
""""""""
 ``orders = trade_api.get_market_ordersget_market_orders(1, 'Limit', 'Bid', '10,20', 2)``

 The value of ``orders['data']`` is:
 
 ``[{'orderID': '32369', 'price': 2000.22, 'initialQuantity': 0.1, 'quantity': 0.1, 'dateCreated': '2017-07-06T14:11:37.446676+00:00', 'offerType': 1, 'type': 1, 'status': 30, 'instrumentID': 1, 'trades': None}, {'orderID': '32371', 'price': 2000.22, 'initialQuantity': 0.1, 'quantity': 0.1, 'dateCreated': '2017-07-06T14:12:55.680301+00:00', 'offerType': 1, 'type': 1, 'status': 30, 'instrumentID': 1, 'trades': None}]``

Placing/cancelling orders methods
---------------------------------------
``create_order(offer_type, order_type, instrument_id, price, quantity)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 Places an order.

Arguments:
""""""""""
  - ``offer_type`` (``string``) - Offer type. Possible values 'Bid' and 'Ask'.
  - ``order_type`` (``string``) - Order type. Possible values 'Limit', 'Market' and 'Stop'.
  - ``instrument_id`` (``integer``) - Instrument identifier. Use ``get_trader_instruments()`` to retrieve them.
  - ``price`` (``float``) - Price
  - ``quantity`` (``float``) - Quantity

Return value:
"""""""""""""
 Returns a ``dict`` with an element ``'response'`` that has the response object from the Trading API request.
 
Example:
""""""""
 ``trade_api.create_order('Bid', 'Limit', 1, 5.2, 0.3)``

``cancel_order(order_id)``
^^^^^^^^^^^^^^^^^^^^^^^^^^
 Cancels a specific order.

Arguments:
""""""""""
  - ``order_id`` (``integer``) - Order identifier.

Return value:
"""""""""""""
 Returns a ``dict`` with an element ``'response'`` that has the response object from the Trading API request.

Example:
""""""""
 ``trade_api.cancel_order(32598)``

``cancel_all_orders(instrument_id)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 Cancels all the orders of the trader for a specific instrument.
 
Arguments:
""""""""""
  - ``instrument_id`` (``integer``) - Instrument identifier.

Return value:
"""""""""""""
 Returns a ``dict`` with an element ``'response'`` that has the response object from the Trading API request.

Example:
""""""""
 ``trade_api.cancel_all_orders(1)``

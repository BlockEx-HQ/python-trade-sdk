``class BlockExTradeApi``
=========================
 This class consists of the implementation of all the methods needed to access the BlockEx Trading API resources supported by the library. The class is stateful and when an instance of it is logged in the API, it keeps the API access token and uses it for the API requests that are made. In case of API call when the access token has expired, a login is performed and the API request is sent again.

 An object of the class can be created using the constructor:

 ``__init__(api_url, api_id, username, password)``

 and providing the necessary values. An example of instance creation is the following:

 ``trade_api = BlockExTradeApi('https://api.blockex.com/', '5c65fb8e-f258-12ee-aec2-4da5eb77ad21', 'traderusername', 'traderpassword')``

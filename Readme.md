# BlockEx Trading API Library #

## Description ##
BlockEx Trading API Library is a Python client module for the Trading API of BlockEx Digital Asset Platform. Its purpose is to provide an easy integration of Python-based systems with the BlockEx Trading API.

The library consists of client implementations of API resources that can generally be grouped into four categories:

 - Trader authentication
 - Getting instruments
 - Getting orders
 - Placing/cancelling orders

## Installation ##
Installation and usage of BlockEx Trading API Library is an easy and straightforward process. The code of the library can be found in the file `BlockExTradeApi.py`, which is available in the source of this repository. An instance of the class `BlockExTradeApi` must be created and initialized with the URL of the Trade API and the credentials for it. The methods of the created instance can be directly used to make API calls. Details and examples are provided in the documentation and the examples folder.

## Prerequisites ##
1. Python
The library works both on Pyton 2 and Python 3 environments. It is tested on Python 2.7.14 and Python 3.6.2. Python can be downloaded and  installed from http://www.python.org/
2. Six
The Six library is necessary for the compatibility of BlockEx Trading API Library both with Python 2 and 3. Six can be easily installed by running:
```
pip install six
```
3. Mock
In order to run the unit tests, mock library is needed. It can be easily installed by running:
```
pip install mock
```

## Configuration ##
The only part of the library that needs to be configured are the integration tests. They need a running instance of the BlockEx Trading API. The configuration is done in the file `test_integration_config.py`, where the values of four variables must be set:
`api_url` - The API URL, e.g. https://api.blockex.com/
`api_id` - The Partner's API ID
`username` - The Trader's username
`password` - The Trader's password
A missing value of any of the four variables would lead to an exception when running the integration tests.

## Unit and integration tests ##
The library code is covered by unit and integration tests. To be run, they can be found in the files `test_blockExTradeApi.py` and `test_integration_blockExTradeApi.py`. A proper configuration must be done for the integration tests, as described in the configuration section of the current document.
# BlockEx Trade API Library #

## Description ##
BlockEx Trade API Library is a Python client module for the Trade API of BlockEx Digital Asset Platform. Its purpose is to provide an easy integration of Python-based systems with the BlockEx Trade API.

The library consists of client implementations of API resources that can generally be grouped into four categories:

 - Trader authentication
 - Getting instruments
 - Getting orders
 - Placing/cancelling orders

## Installation ##
The code of the library can be found in the file `BlockExTradeApi.py`, which is available in the source of this repository. An instance of the class `BlockExTradeApi` must be created and initialized with the URL of the Trade API and the credentials for it. The methods of the created instance can be directly used to make API calls. Details and examples are provided in the documentation and the examples folder.

## Prerequisites ##
- Python
The library works both on Pyton 2 and Python 3 environments. It is tested on Python 2.7.14 and Python 3.6.2. Python can be downloaded and  installed from http://www.python.org/
- Six
The Six library is necessary for the compatibility of BlockEx Trade API Library both with Python 2 and 3. Six can be easily installed by running:
```
pip install six
```
- Enum
For Python versions prior to 3.4, enum34 must be installed. It can be easily installed by running:
```
pip install enum34
```

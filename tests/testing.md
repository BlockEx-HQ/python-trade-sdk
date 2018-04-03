# BlockEx Trade API Library Tests #

## Description ##
BlockEx Trade API Library is covered by unit and integration tests. This document describes how to get them running.

## Prerequisites ##
- Mock
In order to run the unit tests, mock library is needed. It is needed in addition to the prerequisites for the library itself. Mock can be easily installed by running:
```
pip install mock
```

## Unit and integration tests ##
The tests can be found in the files `test_blockExTradeApi.py` and `test_integration_blockExTradeApi.py`. A proper configuration must be done for the integration tests, as described in the configuration section of the current document.

### Integration tests configuration ###
The integration tests need to be configured. They require a running instance of the BlockEx Trade API. The configuration is done in the file `test_integration_config.py`, where the values of four variables must be set:
`api_url` - The API URL, e.g. https://api.blockex.com/
`api_id` - The Partner's API ID
`username` - The Trader's username
`password` - The Trader's password
A missing value of any of the four variables would lead to an exception when running the integration tests.

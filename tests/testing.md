# BlockEx Trade API Library Tests #

## Description ##
BlockEx Trade API Library is covered by unit and integration tests.
This document describes how to get them running.

## Prerequisites ##
To run the tests locally check out the SDK source and install `test` extra with:
````
pip install .[test]
```

## Unit and integration tests ##
The tests can be found in the files `test_blockExTradeApi.py` and
`test_integration_blockExTradeApi.py`. A proper configuration must be
done for the integration tests, as described in the configuration section
of the current document.

### Integration tests configuration ###
The integration tests need to be configured. They require a running
instance of the BlockEx Trade API. The configuration is done in the
file `test_integration_config.py`, where the values of four variables
must be set:
`api_url` - the API base URL, e.g. https://api.blockex.com/
`api_id` - the target Partner's API ID
`username` - the trader's username
`password` - the trader's password

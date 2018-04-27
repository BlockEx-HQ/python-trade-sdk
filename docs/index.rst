.. title:: BlockEx Trade API SDK

*****
Description
*****

BlockEx Trade API SDK is a Python client package for the Trade API
of BlockEx Digital Asset eXchange Platform. It's purpose is to provide an
easy integration of Python-based systems with the BlockEx Trade API.

The module consists of client implementations of API resources that
can generally be grouped into four categories:

 - Trader authentication
 - Getting instruments
 - Getting open orders
 - Placing/cancelling orders
 - Receiving trade events


*****
Installation
*****

Tested and working on Python 2.7 .. 3.6.4+.

blockex.trade-sdk is `available on PyPI <http://pypi.python.org/pypi/blockex.trade-sdk/>`_


.. code-block:: python

    pip install blockex.trade-sdk

*****
Usage
*****

Below is a set of short example.

.. literalinclude:: examples/example_trading.py

.. automodule:: blockex.tradeapi

This example only shows how to try naive trading.
Take a look at the more examples in the `examples <https://github.com/BlockEx-HQ/blockex.trade-sdk/tree/master/docs/examples/>`_ directory.

Contents:

.. toctree::
   :maxdepth: 2

   tradeapi.rst
   auth.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

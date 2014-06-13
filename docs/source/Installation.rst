.. _installation-label:

Installation
============
Because we do not have the package up on PyPI yet, and also because we don't have a build server,
we will manually maintain the packages on mon1 for the time being. Provided that you have VPN
access, simply execute the following command using your favorite python venv:

.. code-block:: bash

    pip install http://mon1/objectrocket-0.1.0a-py2.py3-none-any.whl

The package name itself follows this convention:
``objectrocket-<version>-<python_compatability>-<abi>-<platform>.whl``.

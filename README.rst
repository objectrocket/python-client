ObjectRocket Python Client
--------------------------
ObjectRocket API bindings for Python.


Examples
~~~~~~~~
To use the bindings, simply do the following:

.. code-block:: python

    import objectrocket
    >>>

    client = objectrocket.ORClient('<user_key>', '<pass_key>')
    >>>

    # To get information on one of your instances.
    client.instances.get('instance1')
    >>> {u'data': {u'name': u'instance1', ...}}

    # To get information on all of your instances.
    client.instances.get()
    >>> {u'data': [{u'name': u'instance1', ...}, ...]}

    # To create a new instance.
    client.instances.create('instance2', 5, 'US-West')
    >>> {u'data': {u'name': u'instance2', ...}}

    # To request instance compaction.
    client.instances.compaction('instance2', request_compaction=True)
    >>> {u'data': {u'state': u'requested', ...}}

    # To see instance compaction state.
    client.instances.compaction('instance2')
    >>> {u'data': {u'state': u'compressing', ...}}


Installation
~~~~~~~~~~~~
Because we do not have the package up on PyPi yet, build the package manually
as mentioned below in `Development Notes`_. E.G., ``tox -e build``. After you
have the ObjectRocket wheel package, install it like so:

.. code-block:: bash

    pip install objectrocket-0.1.0-py27-none-any.whl


Development Notes
~~~~~~~~~~~~~~~~~
Before you push your code, run ``tox`` from the top level directory. If errors
are reported, fix them. If a PEP8 issue is reported, and you do not believe
that it is accurate, place ``# noqa`` at the end of the line.

To build the client, invoke ``tox -e build`` from the top level directory.
Your artifact will appear in the ``dist`` directory, and will look
something like ``objectrocket-<version>-py27-<abi>-<platform>.whl``.

ObjectRocket Python Client
--------------------------
ObjectRocket API bindings for Python.


Examples
~~~~~~~~
To use the bindings, simply do the following:

.. code-block:: python

    import objectrocket
    >>>

    client = objectrocket.Client('<user_key>', '<pass_key>')
    >>>

    # To create a new instance.
    client.instances.create(name='instance0', size=5, zone='US-West', service_type='mongodb', version='2.4.6')
    >>> <objectrocket.instances.Instance at 0x10afeacd0>

    # To get one of your instances as an Instance object.
    client.instances.get('instance0')
    >>> <objectrocket.instances.Instance at 0x1097a8390>

    # To get all of your instances in a list.
    client.instances.get()
    >>> [<objectrocket.instances.Instance at 0x1091f9990>]

    # To see an instance's compaction state.
    client.instances.compaction('instance0')
    >>> {u'data': {u'state': u'compressing', ...}}

    # To request compaction for an instance.
    client.instances.compaction('instance0', request_compaction=True)
    >>> {u'data': {u'state': u'requested', ...}}


Installation
~~~~~~~~~~~~
Because we do not have the package up on PyPI yet, build the package manually
as mentioned below in `Development Notes`_. E.G., ``tox -e build``. After you
have the ObjectRocket wheel package, install it like so:

.. code-block:: bash

    pip install objectrocket-0.1.0-py27-none-any.whl


Development Notes
~~~~~~~~~~~~~~~~~
Running Tests
^^^^^^^^^^^^^
Before you push your code, run ``tox`` from the top level directory. If errors
are reported, fix them. If a PEP8 issue is reported, and you do not believe
that it is accurate, place ``# noqa`` at the end of the line.

Coverage Report
^^^^^^^^^^^^^^^
To receive a test coverage report, run ``tox -e coverage`` from the top level directory.

Building the Client
^^^^^^^^^^^^^^^^^^^
To build the client, invoke ``tox -e build`` from the top level directory.
Your artifact will appear in the ``dist`` directory, and will look
something like ``objectrocket-<version>-py27-<abi>-<platform>.whl``.

Building Documentation
^^^^^^^^^^^^^^^^^^^^^^
To build the documentation, invoke ``tox -e docs`` from the top level directory.
The HTML index can then be found at ``docs/build/html/index.html``.

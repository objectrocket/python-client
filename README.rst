ObjectRocket Python Client
--------------------------
ObjectRocket API bindings for Python. To use the bindings, simply do the following:

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

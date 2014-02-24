ObjectRocket Python Client
--------------------------
ObjectRocket API bindings for Python. To use the bindings, simply do the following:

.. code-block:: python

    import objectrocket
    >>>

    client = objectrocket.ORClient('http://localhost:5050/', '<user_key>', '<pass_key>')
    >>>

    # To get information on all of your instances.
    client.instances.get()
    >>> {u'data': [{u'name': u'testinstance1', ...}, ...]}

    # To get information on one of your instances.
    client.instances.get('testinstance1')
    >>> {u'data': [{u'name': u'testinstance1', ...}]}

    # To create a new instance.
    client.instances.create('testinstance2', 5, 'US-West')
    >>> {u'data': [{u'name': u'testinstance2', ...}]}

    # To request instance compaction.
    client.instances.compact('testinstance2', request_compaction=True)
    >>> {u'data': 'Success'}

    # To see instance compaction state.
    client.instances.compact('testinstance2')
    >>> {u'data': {u'state': u'requested', u'updated': u'2014-02-24 23:14:30.322166'}}

ObjectRocket Python Client
--------------------------
ObjectRocket API bindings for Python. To use the bindings, simply do the following:

.. code-block:: python

    import objectrocket
    >>>

    client = objectrocket.ORClient(<str:api_server>, <str:user_key>, <str:pass_key>)
    >>>

    # To get information on all of your instances.
    client.instances.get()
    >>> {'data': [{u'name': u'testinstance1', ...}, ...]}

    # To get information on one of your instances.
    client.instances.get(<str:instance_name>)
    >>> {'data': [{u'name': u'testinstance1', ...}]}

    # To create a new instance.
    client.instances.create(<str:test_name>, <int:size>, <str:zone>)
    >>> {'data': [{u'name': u'testinstance1', ...}]}

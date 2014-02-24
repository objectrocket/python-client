ObjectRocket Python Client
--------------------------
ObjectRocket API bindings for Python. To use the bindings, simply do the following:

.. code-block:: python

    import objectrocket
    >>>

    client = objectrocket.ORClient('<api_server>', '<user_key>', '<pass_key>')
    >>>

    # To get information on all of your instances.
    client.instances.get()
    >>> {'data': [{u'name': u'testinstance1', ...}, ...]}

    # To get information on one of your instances.
    client.instances.get('<instance_name>')
    >>> {'data': [{u'name': u'testinstance1', ...}]}

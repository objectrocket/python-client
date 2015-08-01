Tutorial
========
And now for a super awesome tutorial. Provided that you've already performed an :ref:`installation-label`, here is an example of how you might want to use the client:

.. code-block:: python

    >>> import objectrocket

    >>> client = objectrocket.Client()
    >>> client.authenticate('<username>', '<password>')

    # To create a new instance:
    >>> client.instances.create(name='mongodb_sharded_0', size=5, zone='US-East-IAD3', service_type='mongodb', instance_type='mongodb_sharded', version='3.0.5')
    <objectrocket.instances.MongodbInstance {...} at 0x10afeacd0>

    # To get all of your instances in a list:
    >>> client.instances.all()
    [<objectrocket.instances.MongodbInstance {...} at 0x1091f9990>]

    # To get one of your instances by name:
    >>> inst = client.instances.get('mongodb_sharded_0')
    >>> inst
    <objectrocket.instances.MongodbInstance {...} at 0x1097a8390>

    # To add a shard to your instance:
    >>> inst.shards(add_shard=True)
    {'data': [{'name': '7a0d6366f80f4a42995fabe01cbaea74', 'plan': 5, ...}, {...}]}

    # To request compaction for your instance:
    >>> inst.compaction(request_compaction=True)
    {'data': {'state': 'requested', 'updated': '2015-01-01 00:00:00.000000'}}

    # To check the compaction state of your instance:
    >>> inst.compaction()
    {'data': {'state': 'requested', 'updated': '2015-01-01 00:00:00.000000'}}

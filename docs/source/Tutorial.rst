Tutorial
========
And now for a super fun tutorial. Provided that you've already performed an
:ref:`installation-label`, here is an example of how you might want to use the client:

.. code-block:: python

    import objectrocket
    >>>

    client = objectrocket.Client('<user_key>', '<pass_key>')
    >>>

    # To create a new instance.
    client.instances.create(name='instance0', size=5, zone='US-West', service_type='mongodb', version='2.4.6')
    >>> <objectrocket.instances.Instance {...} at 0x10afeacd0>

    # To get all of your instances in a list.
    client.instances.get()
    >>> [<objectrocket.instances.Instance {...} at 0x1091f9990>]

    # To get one of your instances as an Instance object.
    inst = client.instances.get('instance0')
    inst
    >>> <objectrocket.instances.Instance {...} at 0x1097a8390>

    # To add a shard to your instance.
    inst.shards(add_shard=True)
    >>> {u'data': [{u'name': u'REPLSET_60001', u'plan': 5, ...}, {...}]}

    # To request compaction for your instance.
    inst.compaction(request_compaction=True)
    >>> {u'data': u'Success'}

    # To check the compaction state of your instance.
    inst.compaction()
    >>> {u'data': {u'state': u'requested', u'updated': u'2025-01-01 00:00:00.000000'}}

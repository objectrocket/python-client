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

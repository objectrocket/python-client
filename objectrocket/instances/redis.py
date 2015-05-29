"""MongoDB instance classes."""
from objectrocket import bases


class RedisInstance(bases.BaseInstance):
    """An ObjectRocket Reids service instance.

    :param dict instance_document: A dictionary representing the instance object.
    :param object client: An instance of :py:class:`objectrocket.client.Client`, most likely coming
        from the :py:class:`objectrocket.instance.Instances` service layer.
    """

    def __init__(self, instance_document, client):
        super(RedisInstance, self).__init__(instance_document=instance_document, client=client)

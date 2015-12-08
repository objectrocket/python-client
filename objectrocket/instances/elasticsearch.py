"""Elasticsearch instance class and logic."""
import logging

from objectrocket import bases

logger = logging.getLogger(__name__)


class ESInstance(bases.BaseInstance, bases.Extensible, bases.InstanceAclsInterface):
    """An ObjectRocket Elasticsearch service instance.

    :param dict instance_document: A dictionary representing the instance object, most likey coming
        from the ObjectRocket API.
    :param objectrocket.instances.Instances instances: An instance of
        :py:class:`objectrocket.instances.Instances`.
    """

    def __init__(self, instance_document, instances):
        super(ESInstance, self).__init__(
            instance_document=instance_document,
            instances=instances
        )

    def get_connection(self, ssl=True):
        """Get a live connection to this instance.

        :param bool ssl: Use SSL/TLS if available for this instance.
        """
        return True

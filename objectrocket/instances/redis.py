"""Redis instance classes and logic."""
from __future__ import absolute_import  # Force absolute imports if running under py2.

import redis

from objectrocket import bases


class RedisInstance(bases.BaseInstance):
    """An ObjectRocket Reids service instance.

    :param dict instance_document: A dictionary representing the instance object.
    :param objectrocket.instances.Instances instances: An instance of
        :py:class:`objectrocket.instances.Instances`.
    """

    def __init__(self, instance_document, instances):
        super(RedisInstance, self).__init__(
            instance_document=instance_document,
            instances=instances
        )

        # Bind required pseudo private attributes from API response document.
        self.__password = instance_document['password']
        self._internal_connect_string = instance_document['servicenet_connect_string']
        self._public_connect_string = instance_document['public_connect_string']

    #####################
    # Public interface. #
    #####################
    @property
    def internal_connect_string(self):
        """The DC internal network connection string."""
        return self._servicenet_connect_string

    def get_connection(self, internal=False):
        """Get a live connection to this instance.

        :param bool internal: Whether or not to use a DC internal network connection.

        :rtype: :py:class:`redis.client.StrictRedis`
        """
        # Determine the connection string to use.
        connect_string = self.connect_string
        if internal:
            connect_string = self.internal_connect_string

        # Stripe Redis protocol prefix coming from the API.
        connect_string = connect_string.strip('redis://')
        host, port = connect_string.split(':')

        # Build and return the redis client.
        return redis.StrictRedis(host=host, port=port, password=self._password)

    ######################
    # Private interface. #
    ######################
    def _password(self):
        """The password that is currently being used for this instance."""
        return self.__password

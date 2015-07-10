"""Redis instance classes and logic."""
import redis

from objectrocket import bases


class RedisInstance(bases.BaseInstance):
    """An ObjectRocket Reids service instance.

    :param dict instance_document: A dictionary representing the instance object.
    :param object base_client: An instance of :py:class:`objectrocket.client.Client`, most likely
        coming from the :py:class:`objectrocket.instance.Instances` service layer.
    """

    def __init__(self, instance_document, base_client):
        super(RedisInstance, self).__init__(
            instance_document=instance_document,
            base_client=base_client
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

        :param bool servicenet: Whether or not to use a DC internal network connection.

        :rtype: :py:class:`redis.client.StrictRedis`
        """
        # Keyword arguments to feed to the redis client.
        kwargs = {'password': self._password}

        # Determine the connection string to use.
        connect_string = self.connect_string
        if internal:
            connect_string = self.internal_connect_string

        # Determine if port kwarg also needs to be supplied.
        if ':' in connect_string:
            host, port = connect_string.split(':')
            kwargs.update({'host': host, 'port': port})

        # Else, just supply host.
        else:
            kwargs.update({'host': connect_string})

        # Build and return the redis client.
        return redis.StrictRedis(host=host, port=port, password=self.password)

    ######################
    # Private interface. #
    ######################
    def _password(self):
        """The password that is currently being used for this instance."""
        return self.__password

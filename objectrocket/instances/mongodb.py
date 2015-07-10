"""MongoDB instance classes and logic."""
import datetime
import json
import logging

import pymongo
import requests

from objectrocket import auth
from objectrocket import bases
from objectrocket import constants
from objectrocket import errors

logger = logging.getLogger(__name__)


class MongodbInstance(bases.BaseInstance):
    """An ObjectRocket MongoDB service instance.

    :param dict instance_document: A dictionary representing the instance object, most likey coming
        from the ObjectRocket API.
    :param object base_client: An instance of :py:class:`objectrocket.client.Client`, most likely
        coming from the :py:class:`objectrocket.instance.Instances` service layer.
    """

    def __init__(self, instance_document, base_client):
        super(MongodbInstance, self).__init__(
            instance_document=instance_document,
            base_client=base_client
        )

        # Bind required pseudo private attributes from API response document.
        # Smallest plans may not have an SSL/TLS connection string.
        self._ssl_connect_string = instance_document.get('ssl_connect_string')

    #####################
    # Public interface. #
    #####################
    @auth.token_auto_auth
    def compaction(self, request_compaction=False):
        """Retrieve a report on, or request compaction for this instance.

        :param bool request_compaction: A boolean indicating whether or not to request compaction.
        """
        url = self._url + self.name + '/compaction/'

        if request_compaction:
            response = requests.post(url, **self._client.default_request_kwargs)
        else:
            response = requests.get(url, **self._client.default_request_kwargs)

        return response.json()

    def get_authenticated_connection(self, user, passwd, db='admin', ssl=True):
        """Get an authenticated connection to this instance.

        :param str user: The username to use for authentication.
        :param str passwd: The password to use for authentication.
        :param str db: The name of the database to authenticate against. Defaults to ``'Admin'``.
        :param bool ssl: Use SSL/TLS if available for this instance. Defaults to ``True``.
        :raises: :py:class:`pymongo.errors.OperationError` if authentication fails.
        """
        # Attempt to establish an authenticated connection.
        try:
            connection = self.get_connection(ssl=ssl)
            connection[db].authenticate(user, passwd)
            return connection

        # Catch exception here for logging, then just re-raise.
        except pymongo.errors.OperationError as ex:
            logger.exception(ex)
            raise

    def get_connection(self, ssl=True):
        """Get a live connection to this instance.

        :param bool ssl: Use SSL/TLS if available for this instance.
        """
        return self._get_connection(ssl=ssl)

    @auth.token_auto_auth
    def shards(self, add_shard=False):
        """Get a list of shards belonging to this instance.

        :param bool add_shard: A boolean indicating whether to add a new shard to the specified
            instance.
        """
        url = self._url + self.name + '/shards/'
        if add_shard:
            response = requests.post(url, **self._client.default_request_kwargs)
        else:
            response = requests.get(url, **self._client.default_request_kwargs)

        return response.json()

    @property
    def ssl_connect_string(self):
        """This instance's SSL connection string."""
        return self._ssl_connect_string

    @auth.token_auto_auth
    def stepdown_window(self):
        """Get information on this instance's stepdown window."""
        url = self._url + self.name + '/stepdown/'
        response = requests.get(url, **self._client.default_request_kwargs)
        return response.json()

    @auth.token_auto_auth
    def set_stepdown_window(self, start, end, enabled=True, scheduled=True, weekly=True):
        """Set the stepdown window for this instance.

        Date times are assumed to be UTC, so use UTC date times.

        :param str start: The start time in string format. Should be of the form:
            :py:const:`objectrocket.constants.TIME_FORMAT`.
        :param str end: The end time in string format. Should be of the form:
            :py:const:`objectrocket.constants.TIME_FORMAT`.
        :param bool enabled: A boolean indicating whether or not stepdown is to be enabled.
        :param bool scheduled: A boolean indicating whether or not to schedule stepdown.
        :param bool weekly: A boolean indicating whether or not to schedule compaction weekly.
        """
        try:
            # Ensure that time strings can be parsed properly.
            datetime.datetime.strptime(start, constants.TIME_FORMAT)
            datetime.datetime.strptime(end, constants.TIME_FORMAT)
        except ValueError as ex:
            raise errors.InstancesException(str(ex) + 'Time strings should be of the following '
                                                      'format: %s' % constants.TIME_FORMAT)

        url = self._url + self.name + '/stepdown/'

        data = {
            'start': start,
            'end': end,
            'enabled': enabled,
            'scheduled': scheduled,
            'weekly': weekly,
        }

        response = requests.post(url, data=json.dumps(data), **self._client.default_request_kwargs)
        return response.json()

    ######################
    # Private interface. #
    ######################
    def _get_connection(self, ssl):
        """Get a live connection to this instance."""

        # Use SSL/TLS if requested and available.
        connect_string = self.connect_string
        if ssl and self.ssl_connect_string:
            connect_string = self.ssl_connect_string

        # Use replica set client if needed.
        if self.type == [constants.MONGODB_REPLICA_SET_INSTANCE, constants.TOKUMX_REPLICA_SET_INSTANCE]:
            return pymongo.MongoReplicaSetClient(connect_string)

        # Else, use standard client.
        return pymongo.MongoClient(connect_string)


class TokumxInstance(MongodbInstance):
    """An ObjectRocket TokuMX service instance.

    :param dict instance_document: A dictionary representing the instance object, most likey coming
        from the ObjectRocket API.
    :param object base_client: An instance of :py:class:`objectrocket.client.Client`, most likely
        coming from the :py:class:`objectrocket.instance.Instances` service layer.
    """

    def __init__(self, instance_document, base_client):
        super(TokumxInstance, self).__init__(
            instance_document=instance_document,
            base_client=base_client
        )

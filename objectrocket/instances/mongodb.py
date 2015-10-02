"""MongoDB instance classes and logic."""
import datetime
import json
import logging

import pymongo
import requests

from objectrocket import bases
from objectrocket import util

logger = logging.getLogger(__name__)


class MongodbInstance(bases.BaseInstance, bases.Extensible):
    """An ObjectRocket MongoDB service instance.

    :param dict instance_document: A dictionary representing the instance object, most likey coming
        from the ObjectRocket API.
    :param objectrocket.instances.Instances instances: An instance of
        :py:class:`objectrocket.instances.Instances`.
    """

    def __init__(self, instance_document, instances):
        super(MongodbInstance, self).__init__(
            instance_document=instance_document,
            instances=instances
        )

        # Bind required pseudo private attributes from API response document.
        # Smallest plans may not have an SSL/TLS connection string.
        self._ssl_connect_string = instance_document.get('ssl_connect_string')

        # Register any extensions for this class.
        self._register_extensions('objectrocket.instances.mongodb.MongodbInstance')

    #####################
    # Public interface. #
    #####################
    @util.token_auto_auth
    def compaction(self, request_compaction=False):
        """Retrieve a report on, or request compaction for this instance.

        :param bool request_compaction: A boolean indicating whether or not to request compaction.
        """
        url = self._service_url + 'compaction/'

        if request_compaction:
            response = requests.post(url, **self._instances._default_request_kwargs)
        else:
            response = requests.get(url, **self._instances._default_request_kwargs)

        return response.json()

    def get_authenticated_connection(self, user, passwd, db='admin', ssl=True):
        """Get an authenticated connection to this instance.

        :param str user: The username to use for authentication.
        :param str passwd: The password to use for authentication.
        :param str db: The name of the database to authenticate against. Defaults to ``'Admin'``.
        :param bool ssl: Use SSL/TLS if available for this instance. Defaults to ``True``.
        :raises: :py:class:`pymongo.errors.OperationFailure` if authentication fails.
        """
        # Attempt to establish an authenticated connection.
        try:
            connection = self.get_connection(ssl=ssl)
            connection[db].authenticate(user, passwd)
            return connection

        # Catch exception here for logging, then just re-raise.
        except pymongo.errors.OperationFailure as ex:
            logger.exception(ex)
            raise

    def get_connection(self, ssl=True):
        """Get a live connection to this instance.

        :param bool ssl: Use SSL/TLS if available for this instance.
        """
        return self._get_connection(ssl=ssl)

    @util.token_auto_auth
    def shards(self, add_shard=False):
        """Get a list of shards belonging to this instance.

        :param bool add_shard: A boolean indicating whether to add a new shard to the specified
            instance.
        """
        url = self._service_url + 'shards/'
        if add_shard:
            response = requests.post(url, **self._instances._default_request_kwargs)
        else:
            response = requests.get(url, **self._instances._default_request_kwargs)

        return response.json()

    @property
    def ssl_connect_string(self):
        """This instance's SSL connection string."""
        return self._ssl_connect_string

    @util.token_auto_auth
    def get_stepdown_window(self):
        """Get information on this instance's stepdown window."""
        url = self._service_url + 'stepdown/'
        response = requests.get(url, **self._instances._default_request_kwargs)
        return response.json()

    @util.token_auto_auth
    def set_stepdown_window(self, start, end, enabled=True, scheduled=True, weekly=True):
        """Set the stepdown window for this instance.

        Date times are assumed to be UTC, so use UTC date times.

        :param datetime.datetime start: The datetime which the stepdown window is to open.
        :param datetime.datetime end: The datetime which the stepdown window is to close.
        :param bool enabled: A boolean indicating whether or not stepdown is to be enabled.
        :param bool scheduled: A boolean indicating whether or not to schedule stepdown.
        :param bool weekly: A boolean indicating whether or not to schedule compaction weekly.
        """
        # Ensure a logical start and endtime is requested.
        if not start < end:
            raise TypeError('Parameter "start" must occur earlier in time than "end".')

        # Ensure specified window is less than a week in length.
        week_delta = datetime.timedelta(days=7)
        if not ((end - start) <= week_delta):
            raise TypeError('Stepdown windows can not be longer than 1 week in length.')

        url = self._service_url + 'stepdown/'
        data = {
            'start': int(start.strftime('%s')),
            'end': int(end.strftime('%s')),
            'enabled': enabled,
            'scheduled': scheduled,
            'weekly': weekly,
        }

        response = requests.post(url, data=json.dumps(data), **self._instances._default_request_kwargs)
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

        return pymongo.MongoClient(connect_string)

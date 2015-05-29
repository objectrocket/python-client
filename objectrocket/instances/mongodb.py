"""MongoDB instance classes."""
import datetime
import json

import pymongo
import requests

from objectrocket import auth
from objectrocket import bases
from objectrocket import constants
from objectrocket import errors


class MongodbInstance(bases.BaseInstance):
    """An ObjectRocket MongoDB service instance.

    :param dict instance_document: A dictionary representing the instance object.
    :param object client: An instance of :py:class:`objectrocket.client.Client`, most likely coming
        from the :py:class:`objectrocket.instance.Instances` service layer.
    """

    def __init__(self, instance_document, client):
        super(MongodbInstance, self).__init__(instance_document=instance_document, client=client)

        # Bind pseudo private attributes from instance_document.
        self._plan = instance_document['plan']
        self._ssl_connect_string = instance_document.get('ssl_connect_string')

        # Lazily-created properties.
        self._connection = None

    @auth.token_auto_auth
    def compaction(self, request_compaction=False):
        """Retrieve a report on, or request compaction for this instance.

        :param bool request_compaction: A boolean indicating whether or not to request compaction.
        """
        url = self.url + self.name + '/compaction/'

        if request_compaction:
            response = requests.post(url, **self.client.default_request_kwargs)
        else:
            response = requests.get(url, **self.client.default_request_kwargs)

        return response.json()

    @property
    def connection(self):
        """A live connection to this instance."""
        if self._connection is None:
            self._connection = self._get_connection()
        return self._connection

    def get_authenticated_connection(self, user, passwd, db='admin'):
        """Establish an authenticated connection to this instance.

        :param str user: The username to use for authentication.
        :param str passwd: The password to use for authentication.
        :param str db: The name of the database to authenticate against. Defaults to 'Admin'.
        """
        try:
            self.connection[db].authenticate(user, passwd)
        except pymongo.errors.OperationError as ex:
            raise errors.InstancesException(str(ex))

        return self.connection

    def _get_connection(self):
        """Establish a live connection to the instance."""
        if self.type == constants.MONGODB_SHARDED_INSTANCE:
            host, port = self.connect_string.split(':')
            port = int(port)
            return pymongo.MongoClient(host=host, port=port)
        elif self.type == constants.MONGODB_REPLICA_SET_INSTANCE:
            replica_set_name, member_list = self.connect_string.split('/')
            member_list = member_list.strip().strip(',')
            return pymongo.MongoReplicaSetClient(hosts_or_uri=member_list)

    @property
    def plan(self):
        """The base plan size of this instance."""
        return self._plan

    @auth.token_auto_auth
    def shards(self, add_shard=False):
        """Get a list of shards belonging to this instance.

        :param bool add_shard: A boolean indicating whether to add a new shard to the specified
            instance.
        """
        url = self.url + self.name + '/shard/'
        if add_shard:
            response = requests.post(url, **self.client.default_request_kwargs)
        else:
            response = requests.get(url, **self.client.default_request_kwargs)

        return response.json()

    @property
    def ssl_connect_string(self):
        """This instance's SSL connection string."""
        return self._ssl_connect_string

    @auth.token_auto_auth
    def stepdown_window(self):
        """Get information on this instance's stepdown window."""
        url = self.url + self.name + '/stepdown/'

        response = requests.get(url, **self.client.default_request_kwargs)
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

        url = self.url + self.name + '/stepdown/'

        data = {
            'start': start,
            'end': end,
            'enabled': enabled,
            'scheduled': scheduled,
            'weekly': weekly,
        }

        response = requests.post(url, data=json.dumps(data), **self.client.default_request_kwargs)
        return response.json()


class TokumxInstance(MongodbInstance):
    """An ObjectRocket TokuMX service instance.

    :param dict instance_document: A dictionary representing the instance object.
    :param object client: An instance of :py:class:`objectrocket.client.Client`, most likely coming
        from the :py:class:`objectrocket.instance.Instances` service layer.
    """

    def __init__(self, instance_document, client):
        super(TokumxInstance, self).__init__(instance_document=instance_document, client=client)

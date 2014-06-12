"""Instances layer."""
import datetime
import json
import sys

import requests
import pymongo

from objectrocket import constants


class Instances(object):
    """Instance operations.

    :param objectrocket.client.Client client_instance: An instance of
        objectrocket.client.Client.
    """

    def __init__(self, client_instance):
        self._client = client_instance
        self._api_instances_url = self._client.api_url + 'instance/'

    def compaction(self, instance_name, request_compaction=False):
        """Retrieve a report on, or request compaction for the given instance.

        :param str instance_name: The name of the instance to operate upon.
        :param bool request_compaction: A boolean indicating whether or not to request compaction.
        """
        url = self._api_instances_url + instance_name + '/compaction/'

        if request_compaction:
            response = requests.post(url, auth=(self._client.user_key, self._client.pass_key))
        else:
            response = requests.get(url, auth=(self._client.user_key, self._client.pass_key))

        return response.json()

    def create(self, name, size, zone, service_type='mongodb', version='2.4.6'):
        """Create an instance.

        :param str name: The name to give to the new instance.
        :param int size: The size in gigabytes of the new instance.
        :param str zone: The zone that the new instance is to exist in.
        :param str service_type: The type of service that the new instance is to provide.
        :param str version: The version of the service the new instance is to provide.
        """
        valid_service_types = ('mongodb', )
        if service_type not in valid_service_types:
            raise self.InstancesException('Invalid value for "service_type". Must be one of "%s".'
                                          % valid_service_types)

        valid_versions = ('2.4.6', )
        if version not in valid_versions:
            raise self.InstancesException('Invalid value for "version". Must be one of "%s".'
                                          % valid_versions)

        url = self._api_instances_url
        data = {
            'name': name,
            'size': size,
            'zone': zone,
            'type': service_type,
            'version': version,
        }

        # Not passing service type ATM. Probably will soon though.
        data.pop('type')

        response = requests.post(url,
                                 auth=(self._client.user_key, self._client.pass_key),
                                 data=json.dumps(data),
                                 headers={'Content-Type': 'application/json'})
        return self._return_instance_objects(response)

    def get(self, instance_name=None):
        """Get details on one or all instances.

        :param str instance_name: The name of the instance to retrieve. If ``None``, then retrieve
            a list of all instances which you have access to.
        """
        url = self._api_instances_url
        if instance_name is not None:
            url += instance_name + '/'

        response = requests.get(url, auth=(self._client.user_key, self._client.pass_key))
        return self._return_instance_objects(response)

    def _return_instance_objects(self, response):
        """Translate response data into :py:class:`objectrocket.instances.Instance` objects.

        :param object response: An object having a ``json`` method which returns a dict with a key
            'data'.
        """
        _json = response.json()
        data = _json['data']
        if isinstance(data, dict):
            return Instance(instance_document=data, client=self._client)
        elif isinstance(data, list):
            return [Instance(instance_document=doc, client=self._client) for doc in data]
        else:
            raise self.InstancesException('response.json()["data"] must be a '
                                          'dict or list of dicts.')

    def shards(self, instance_name, add_shard=False):
        """Get a list of shards belonging to the given instance.

        :param str instance_name: The name of the instance to operate upon.
        :param bool add_shard: A boolean indicating whether to add a new shard to the specified
            instance.
        """
        url = self._api_instances_url + instance_name + '/shard/'
        if add_shard:
            response = requests.post(url, auth=(self._client.user_key, self._client.pass_key))
        else:
            response = requests.get(url, auth=(self._client.user_key, self._client.pass_key))

        return response.json()

    def stepdown_window(self, instance_name):
        """Get information on the instance's stepdown window.

        :param str instance_name: The name of the instance to operate upon.
        """
        url = self._api_instances_url + instance_name + '/stepdown/'

        response = requests.get(url, auth=(self._client.user_key, self._client.pass_key))
        return response.json()

    def set_stepdown_window(self, instance_name, start, end, enabled, scheduled, weekly):
        """Set the stepdown window of the given instance.

        Date times are assumed to be UTC ... so use UTC date times.

        :param str instance_name: The name of the instance to operate upon.
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
            raise self.InstancesException(str(ex) + 'Time strings should be of the following '
                                                    'format: %s' % constants.TIME_FORMAT)

        url = self._api_instances_url + instance_name + '/stepdown/'

        data = {
            'start': start,
            'end': end,
            'enabled': enabled,
            'scheduled': scheduled,
            'weekly': weekly,
        }

        response = requests.post(url,
                                 auth=(self._client.user_key, self._client.pass_key),
                                 data=json.dumps(data),
                                 headers={'Content-Type': 'application/json'})
        return response.json()

    class InstancesException(Exception):
        pass


class Instance(object):
    """The base class of an ObjectRocket service.

    :param dict instance_document: A dictionary representing the instance object.
    :param object client: An instance of :py:class:`objectrocket.client.Client`.
    """

    def __init__(self, instance_document, client):
        self._client = client
        self.instance_document = instance_document

        # Bind pseudo private attributes from instance_document.
        self._api_endpoint = instance_document['api_endpoint']
        self._connect_string = instance_document['connect_string']
        self._created = instance_document['created']
        self._name = instance_document['name']
        self._plan = instance_document['plan']
        self._service = instance_document['service']
        self._ssl_connect_string = instance_document.get('ssl_connect_string')
        self._type = instance_document['type']
        self._version = instance_document['version']

        # Lazily-created properties.
        self._connection = None

    @property
    def api_endpoint(self):
        """The optimal API endpoint for this instance."""
        return self._api_endpoint

    @property
    def connection(self):
        """A live connection to this instance."""
        if self._connection is None:
            self._connection = self._get_connection()
        return self._connection

    @property
    def connect_string(self):
        """This instance's connection string."""
        return self._connect_string

    @property
    def created(self):
        """The date this instance was created."""
        return self._created

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
    def name(self):
        """This instance's name."""
        return self._name

    @property
    def plan(self):
        """This instance's plan."""
        return self._plan

    @property
    def service(self):
        """The service this instance provides."""
        return self._service

    @property
    def ssl_connect_string(self):
        """This instance's SSL connection string."""
        return self._ssl_connect_string

    def to_dict(self):
        """Render this object as a dictionary."""
        return self.instance_document

    @property
    def type(self):
        """The type of service this instance provides."""
        return self._type

    @property
    def version(self):
        """The version of this instance's service."""
        return self._version

    # -------------------
    # CONVENIENCE METHODS
    # -------------------
    @property
    def client(self):
        """An instance of the objectrocket.client.Client."""
        if 'objectorcket.client' not in sys.modules:
            from objectrocket import client
        if not isinstance(self._client, client.Client):
            return None
        return self._client

    def compaction(self, request_compaction=False):
        """Retrieve a report on, or request compaction for this instance.

        :param bool request_compaction: A boolean indicating whether or not to request compaction.
        """
        response = self.client.instances.compaction(instance_name=self.name,
                                                    request_compaction=request_compaction)
        return response

    def stepdown_window(self, instance_name):
        pass

    def set_stepdown_window(self, instance_name, start, end, enabled, scheduled, weekly):
        pass

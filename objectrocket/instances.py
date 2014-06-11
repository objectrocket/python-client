"""Instances layer."""
import datetime
import json

import requests
import pymongo

from functools import wraps

from objectrocket import constants
from objectrocket.utils import Utils


def return_instance_objects(func):
    """Translate responses into :py:class:`objectrocket.instances.Instance` objects."""
    @wraps(func)
    def wrapped(*args, **kwargs):
        response = func(*args, **kwargs)
        if isinstance(response['data'], dict):
            return Instance(response['data'])
        elif isinstance(response['data'], list):
            return [Instance(doc) for doc in response['data']]
        else:
            return response

    return wrapped


class Instances(object):
    """Instance operations.

    :param objectrocket.client.Client client_instance: An instance of
        objectrocket.client.Client.
    """

    def __init__(self, client_instance):
        self._client = client_instance
        self._api_instances_url = self._client.api_url + 'instance/'

    def compaction(self, instance_name, request_compaction=False):
        """Compaction."""
        if not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance of str.')

        url = self._api_instances_url + instance_name + '/compaction/'

        if request_compaction:
            response = requests.post(url, auth=(self._client.user_key, self._client.pass_key))
        else:
            response = requests.get(url, auth=(self._client.user_key, self._client.pass_key))

        return response.json()

    @return_instance_objects
    def create(self, name, size, zone, service_type='mongodb', version='2.4.6'):
        """Create an instance."""
        if not isinstance(name, str):
            raise self.InstancesException('Parameter "name" must be an instance of str.')

        if not isinstance(size, int):
            raise self.InstancesException('Parameter "size" must be an instance of int.')

        if not isinstance(zone, str):
            raise self.InstancesException('Parameter "zone" must be an instance of str.')

        valid_service_types = ('mongodb', )
        if service_type not in valid_service_types:
            raise self.InstancesException('Invalid value for "service_type". Must be one of %s.'
                                          % valid_service_types)

        valid_versions = ('2.4.6', )
        if version not in valid_versions:
            raise self.InstancesException('Invalid value for "version". Must be one of %s.'
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
        return response.json()

    @return_instance_objects
    def get(self, instance_name=None):
        """Get details on one or all instances."""
        if instance_name is not None and not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance of str.')

        url = self._api_instances_url
        if instance_name is not None:
            url += instance_name + '/'

        response = requests.get(url, auth=(self._client.user_key, self._client.pass_key))
        return response.json()

    def stepdown_window(self, instance_name):
        """Get information on the instance's stepdown window."""
        if not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance of str.')

        url = self._api_instances_url + instance_name + '/stepdown/'

        response = requests.get(url, auth=(self._client.user_key, self._client.pass_key))
        return response.json()

    def set_stepdown_window(self, instance_name, start, end, enabled, scheduled, weekly):
        """Use UTC date times."""
        if not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance of str.')
        if not isinstance(start, str):
            raise self.InstancesException('Parameter "start" must be an instance of datetime.')
        if not isinstance(end, str):
            raise self.InstancesException('Parameter "end" must be an instance of datetime.')
        if not isinstance(enabled, bool):
            raise self.InstancesException('Parameter "enabled" must be a boolean.')
        if not isinstance(scheduled, bool):
            raise self.InstancesException('Parameter "scheduled" must be a boolean.')
        if not isinstance(weekly, bool):
            raise self.InstancesException('Parameter "weekly" must be a boolean.')

        try:
            # Ensure that time strings can be parsed properly.
            datetime.datetime.strptime(start, Utils.TIME_FORMAT)
            datetime.datetime.strptime(end, Utils.TIME_FORMAT)
        except ValueError as ex:
            raise self.InstancesException(str(ex) + 'Time strings should be of the following '
                                                    'format: %s' % Utils.TIME_FORMAT)

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
    """

    def __init__(self, instance_document):
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

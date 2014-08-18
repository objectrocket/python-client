"""Instance operations and instances."""
import datetime
import json
import pymongo
import requests

from objectrocket import auth
from objectrocket import constants
from objectrocket import errors
from objectrocket import operations


class Instances(operations.BaseOperationsLayer):
    """Instance operations.

    :param objectrocket.client.Client client_instance: An instance of
        objectrocket.client.Client.
    """

    def __init__(self, client_instance):
        super(Instances, self).__init__(client_instance=client_instance)

    @auth._token_auto_auth
    def compaction(self, instance_name, request_compaction=False):
        """Retrieve a report on, or request compaction for the given instance.

        :param str instance_name: The name of the instance to operate upon.
        :param bool request_compaction: A boolean indicating whether or not to request compaction.
        """
        url = self.url + instance_name + '/compaction/'

        if request_compaction:
            response = requests.post(url, **self.client.default_request_kwargs)
        else:
            response = requests.get(url, **self.client.default_request_kwargs)

        return response.json()

    def _concretize_instance_doc(self, instance_doc):
        """Concretize and instance document into a :py:class:`BaseInstance` subclass."""
        service = instance_doc.setdefault('service', 'unknown')
        cls = BaseInstance

        # If service key is a recognized service type, instantiate its respective instance.
        if service in self._service_class_map:
            cls = self._service_class_map[service]

        return cls(instance_document=instance_doc, client=self.client)

    @auth._token_auto_auth
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
            raise errors.InstancesException('Invalid value for "service_type". Must be one of '
                                            '"%s".' % valid_service_types)

        valid_versions = ('2.4.6', )
        if version not in valid_versions:
            raise errors.InstancesException('Invalid value for "version". Must be one of "%s".'
                                            % valid_versions)

        url = self.url
        data = {
            'name': name,
            'size': size,
            'zone': zone,
            'type': service_type,
            'version': version,
        }

        # Not passing service type ATM. Probably will soon though.
        data.pop('type')

        response = requests.post(url, data=json.dumps(data), **self.client.default_request_kwargs)
        return self._return_instance_objects(response)

    @auth._token_auto_auth
    def get(self, instance_name=None):
        """Get details on one or all instances.

        :param str instance_name: The name of the instance to retrieve. If ``None``, then retrieve
            a list of all instances which you have access to.
        """
        url = self.url
        if instance_name is not None:
            url += instance_name + '/'

        response = requests.get(url, **self.client.default_request_kwargs)
        return self._return_instance_objects(response)

    def _return_instance_objects(self, response):
        """Translate response data into the appropriate :py:class:`BaseInstance` subclass.

        :param object response: a response object from which JSON data might be extracted.
        """
        # If no JSON object could be decoded, simply return the response.
        try:
            _json = response.json()
            data = _json.get('data')
            if data is None:
                return response
        except ValueError:
            return response

        # Translate instance documents to instance objects corresponding to their service.
        if isinstance(data, dict):
            return self._concretize_instance_doc(instance_doc=data)
        elif isinstance(data, list):
            return [self._concretize_instance_doc(instance_doc=doc) for doc in data]
        else:
            return response

    @property
    def _service_class_map(self):
        """A mapping of services to class objects."""
        service_map = {
            'mongodb': MongodbInstance,
            'redis': RedisInstance,
            'tokumx': TokumxInstance,
        }
        return service_map

    @auth._token_auto_auth
    def shards(self, instance_name, add_shard=False):
        """Get a list of shards belonging to the given instance.

        :param str instance_name: The name of the instance to operate upon.
        :param bool add_shard: A boolean indicating whether to add a new shard to the specified
            instance.
        """
        url = self.url + instance_name + '/shard/'
        if add_shard:
            response = requests.post(url, **self.client.default_request_kwargs)
        else:
            response = requests.get(url, **self.client.default_request_kwargs)

        return response.json()

    @auth._token_auto_auth
    def stepdown_window(self, instance_name):
        """Get information on the instance's stepdown window.

        :param str instance_name: The name of the instance to operate upon.
        """
        url = self.url + instance_name + '/stepdown/'

        response = requests.get(url, **self.client.default_request_kwargs)
        return response.json()

    @auth._token_auto_auth
    def set_stepdown_window(self, instance_name, start, end,
                            enabled=True, scheduled=True, weekly=True):
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
            raise errors.InstancesException(str(ex) + 'Time strings should be of the following '
                                                      'format: %s' % constants.TIME_FORMAT)

        url = self.url + instance_name + '/stepdown/'

        data = {
            'start': start,
            'end': end,
            'enabled': enabled,
            'scheduled': scheduled,
            'weekly': weekly,
        }

        response = requests.post(url, data=json.dumps(data), **self.client.default_request_kwargs)
        return response.json()

    @property
    def url(self):
        """The base URL for instance operations."""
        return self.client.url + 'instance/'


class BaseInstance(object):
    """The base class for ObjectRocket service instances.

    :param dict instance_document: A dictionary representing the instance object.
    :param object client: An instance of :py:class:`objectrocket.client.Client`, most likely coming
        from the :py:class:`objectrocket.instance.Instances` service layer.
    """

    def __init__(self, instance_document, client):
        self._client = client
        self._instance_document = instance_document

        # Bind pseudo private attributes from instance_document.
        self._api_endpoint = instance_document['api_endpoint']
        self._connect_string = instance_document['connect_string']
        self._created = instance_document['created']
        self._name = instance_document['name']
        self._service = instance_document['service']
        self._type = instance_document['type']
        self._version = instance_document['version']

    def __repr__(self):
        """Represent this object as a string."""
        _id = hex(id(self))
        rep = '<objectrocket.instances.{!s} {!r} at {!s}>'.format(
            self.__class__.__name__, self.instance_document, _id)
        return rep

    @property
    def api_endpoint(self):
        """The optimal API endpoint for this instance."""
        return self._api_endpoint

    @property
    def client(self):
        """An instance of the objectrocket.client.Client."""
        return self._client

    @property
    def connect_string(self):
        """This instance's connection string."""
        return self._connect_string

    @property
    def created(self):
        """The date this instance was created."""
        return self._created

    @property
    def instance_document(self):
        """The document used to construct this Instance object."""
        return self._instance_document

    @property
    def name(self):
        """This instance's name."""
        return self._name

    @property
    def service(self):
        """The service this instance provides."""
        return self._service

    @property
    def type(self):
        """The type of service this instance provides."""
        return self._type

    @property
    def version(self):
        """The version of this instance's service."""
        return self._version

    def to_dict(self):
        """Render this object as a dictionary."""
        return self.instance_document


class MongodbInstance(BaseInstance):
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

    @property
    def ssl_connect_string(self):
        """This instance's SSL connection string."""
        return self._ssl_connect_string

    #######################
    # CONVENIENCE METHODS #
    #######################
    def compaction(self, request_compaction=False):
        """Retrieve a report on, or request compaction for this instance.

        :param bool request_compaction: A boolean indicating whether or not to request compaction.
        """
        response = self.client.instances.compaction(instance_name=self.name,
                                                    request_compaction=request_compaction)
        return response

    def shards(self, add_shard=False):
        """Get a list of shards belonging to this instance.

        :param bool add_shard: A boolean indicating whether to add a new shard to the specified
            instance.
        """
        response = self.client.instances.shards(instance_name=self.name, add_shard=add_shard)
        return response

    def stepdown_window(self, instance_name):
        pass

    def set_stepdown_window(self, instance_name, start, end, enabled, scheduled, weekly):
        pass


class TokumxInstance(MongodbInstance):
    """An ObjectRocket TokuMX service instance.

    :param dict instance_document: A dictionary representing the instance object.
    :param object client: An instance of :py:class:`objectrocket.client.Client`, most likely coming
        from the :py:class:`objectrocket.instance.Instances` service layer.
    """

    def __init__(self, instance_document, client):
        super(TokumxInstance, self).__init__(instance_document=instance_document, client=client)


class RedisInstance(BaseInstance):
    """An ObjectRocket Reids service instance.

    :param dict instance_document: A dictionary representing the instance object.
    :param object client: An instance of :py:class:`objectrocket.client.Client`, most likely coming
        from the :py:class:`objectrocket.instance.Instances` service layer.
    """

    def __init__(self, instance_document, client):
        super(RedisInstance, self).__init__(instance_document=instance_document, client=client)

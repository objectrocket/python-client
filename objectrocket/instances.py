"""Instance operations and instances."""
import datetime
import json
import logging
import pymongo
import requests

from objectrocket import auth
from objectrocket import constants
from objectrocket import errors
from objectrocket import operations

logger = logging.getLogger(__name__)


class Instances(operations.BaseOperationsLayer):
    """Instance operations.

    :param objectrocket.client.Client client_instance: An instance of objectrocket.client.Client.
    """

    def __init__(self, client_instance):
        super(Instances, self).__init__(client_instance=client_instance)

    def _concrete_instance(self, instance_doc):
        """Concretize an instance document.

        :param dict instance_doc: A document describing an instance. Should come from the API.
        :returns: A subclass of :py:class:`BaseInstance`, or None.
        :rtype: :py:class:`BaseInstance`
        """
        if not isinstance(instance_doc, dict):
            return None

        service = instance_doc.setdefault('service', 'unknown')
        inst = None

        # If service key is a recognized service type, instantiate its respective instance.
        if service in self._service_class_map:
            cls = self._service_class_map[service]
            inst = cls(instance_document=instance_doc, client=self.client)

        # If service is not recognized, log a warning and return None.
        else:
            logger.warning(
                'Could not determine instance service. You probably need to upgrade to a more '
                'recent version of the client. Instance document which generated this '
                'warning: {}'.format(instance_doc)
            )

        return inst

    def _concrete_instance_list(self, instance_docs):
        """Concretize a list of instance documents.

        :param list instance_docs: A list of instance documents. Should come from the API.
        :returns: A list of :py:class:`BaseInstance`s.
        :rtype: list
        """
        if not isinstance(instance_docs, list):
            return []

        return filter(None, [self._concrete_instance(instance_doc=doc) for doc in instance_docs])

    @auth._token_auto_auth
    def create(self, name, size, zone, service_type='mongodb', version='2.4.6'):
        """Create an instance.

        :param str name: The name to give to the new instance.
        :param int size: The size in gigabytes of the new instance.
        :param str zone: The zone that the new instance is to exist in.
        :param str service_type: The type of service that the new instance is to provide.
        :param str version: The version of the service the new instance is to provide.
        """
        # TODO(TheDodd): we can probably have the API return a list of available services if the
        # specified service is not supported.
        valid_service_types = ('mongodb', )
        if service_type not in valid_service_types:
            raise errors.InstancesException('Invalid value for "service_type". Must be one of '
                                            '"%s".' % valid_service_types)

        # TODO(TheDodd): we can probably have the API return a list of available versions for the
        # specified service if the given version is not supported.
        valid_versions = ('2.4.6', )
        if version not in valid_versions:
            raise errors.InstancesException('Invalid value for "version". Must be one of "%s".'
                                            % valid_versions)

        # Build up request data.
        url = self.url
        request_data = {
            'name': name,
            'size': size,
            'zone': zone,
            'type': service_type,
            'version': version,
        }
        request_data.pop('type')  # Not passing service type ATM. Probably will soon though.

        # Call to create an instance.
        response = requests.post(url, data=json.dumps(request_data),
                                 **self.client.default_request_kwargs)

        # Log outcome of instance creation request.
        if response.status_code == 200:
            logger.info('Successfully created a new instance with: {}'.format(request_data))
        else:
            logger.info('Failed to create instance with: {}'.format(request_data))

        data = self._get_response_data(response)
        return self._concrete_instance_list(data)

    @auth._token_auto_auth
    def get(self, instance_name):
        """Get an ObjectRocket instance.

        :param str instance_name: The name of the instance to retrieve.
        :returns: A subclass of :py:class:`BaseInstance`, or None.
        :rtype: :py:class:`BaseInstance`
        """
        url = self.url + instance_name + '/'
        response = requests.get(url, **self.client.default_request_kwargs)
        data = self._get_response_data(response)
        return self._concrete_instance(data)

    @auth._token_auto_auth
    def get_all(self):
        """Get all authorized ObjectRocket instances.

        :returns: A list of :py:class:`BaseInstance` instances.
        :rtype: list
        """
        response = requests.get(self.url, **self.client.default_request_kwargs)
        data = self._get_response_data(response)
        return self._concrete_instance_list(data)

    def _get_response_data(self, response):
        """Return the data from a ``requests.Response`` object.

        :param requests.Response response: The ``Response`` object from which to get the data.
        """
        try:
            _json = response.json()
            data = _json.get('data')
            return data
        except ValueError:
            return None

    @property
    def _service_class_map(self):
        """A mapping of services to class objects."""
        service_map = {
            'mongodb': MongodbInstance,
            'redis': RedisInstance,
            'tokumx': TokumxInstance,
        }
        return service_map

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

    @auth._token_auto_auth
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

    @auth._token_auto_auth
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

    @auth._token_auto_auth
    def stepdown_window(self):
        """Get information on this instance's stepdown window."""
        url = self.url + self.name + '/stepdown/'

        response = requests.get(url, **self.client.default_request_kwargs)
        return response.json()

    @auth._token_auto_auth
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


class RedisInstance(BaseInstance):
    """An ObjectRocket Reids service instance.

    :param dict instance_document: A dictionary representing the instance object.
    :param object client: An instance of :py:class:`objectrocket.client.Client`, most likely coming
        from the :py:class:`objectrocket.instance.Instances` service layer.
    """

    def __init__(self, instance_document, client):
        super(RedisInstance, self).__init__(instance_document=instance_document, client=client)

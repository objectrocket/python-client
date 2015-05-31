"""Instance operations and instances."""
import json
import logging

import requests

from objectrocket import auth
from objectrocket import bases
from objectrocket import errors
from objectrocket.instances.mongodb import MongodbInstance
from objectrocket.instances.mongodb import TokumxInstance
from objectrocket.instances.redis import RedisInstance

logger = logging.getLogger(__name__)


class Instances(bases.BaseOperationsLayer):
    """Instance operations.

    :param objectrocket.client.Client base_client: An instance of objectrocket.client.Client.
    """

    def __init__(self, base_client):
        super(Instances, self).__init__(base_client=base_client)

    #####################
    # Public interface. #
    #####################
    @auth.token_auto_auth
    def all(self):
        """Get all ObjectRocket instances the current client has access to.

        :returns: A list of :py:class:`bases.BaseInstance` instances.
        :rtype: list
        """
        response = requests.get(self._url, **self._default_request_kwargs)
        data = self._get_response_data(response)
        return self._concrete_instance_list(data)

    # TODO(TheDodd): need to add instance_type.
    @auth.token_auto_auth
    def create(self, name, size, zone, service_type='mongodb', version='2.4.6'):
        """Create an ObjectRocket instance.

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
        url = self._url
        request_data = {
            'name': name,
            'size': size,
            'zone': zone,
            'type': service_type,
            'version': version,
        }
        request_data.pop('type')  # Not passing service type ATM. Probably will soon though.

        # Call to create an instance.
        response = requests.post(
            url,
            data=json.dumps(request_data),
            **self._default_request_kwargs
        )

        # Log outcome of instance creation request.
        if response.status_code == 200:
            logger.info('Successfully created a new instance with: {}'.format(request_data))
        else:
            logger.info('Failed to create instance with: {}'.format(request_data))

        data = self._get_response_data(response)
        return self._concrete_instance(data)

    @auth.token_auto_auth
    def get(self, instance_name):
        """Get an ObjectRocket instance by name.

        :param str instance_name: The name of the instance to retrieve.
        :returns: A subclass of :py:class:`bases.BaseInstance`, or None if instance does not exist.
        :rtype: :py:class:`bases.BaseInstance`
        """
        url = self._url + instance_name + '/'
        response = requests.get(url, **self._default_request_kwargs)
        data = self._get_response_data(response)
        return self._concrete_instance(data)

    ######################
    # Private interface. #
    ######################
    def _concrete_instance(self, instance_doc):
        """Concretize an instance document.

        :param dict instance_doc: A document describing an instance. Should come from the API.
        :returns: A subclass of :py:class:`bases.BaseInstance`, or None.
        :rtype: :py:class:`bases.BaseInstance`
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
        :returns: A list of :py:class:`bases.BaseInstance`s.
        :rtype: list
        """
        if not isinstance(instance_docs, list):
            return []

        return filter(None, [self._concrete_instance(instance_doc=doc) for doc in instance_docs])

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
    def _default_request_kwargs(self):
        """The default request keyword arguments to be passed to the requests library."""
        default_kwargs = super(Instances, self)._default_request_kwargs
        default_kwargs.setdefault('headers', {}).update({
            'X-Auth-Token': self.client._token
        })
        return default_kwargs

    @property
    def _service_class_map(self):
        """A mapping of service names to service classes."""
        service_map = {
            'mongodb': MongodbInstance,
            'redis': RedisInstance,
            'tokumx': TokumxInstance,
        }
        return service_map

    @property
    def _url(self):
        """The base URL for instance operations."""
        return self.client._url + 'instances/'

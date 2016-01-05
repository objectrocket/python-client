"""Instance operations and instances."""
import copy
import json
import logging

import requests

from objectrocket import bases
from objectrocket import util
from objectrocket.instances.mongodb import MongodbInstance
from objectrocket.instances.elasticsearch import ESInstance
from objectrocket.instances.redis import RedisInstance

logger = logging.getLogger(__name__)


class Instances(bases.BaseOperationsLayer, bases.Extensible):
    """Instance operations.

    :param objectrocket.client.Client base_client: An instance of objectrocket.client.Client.
    """

    def __init__(self, base_client):
        super(Instances, self).__init__(base_client=base_client)

        # Register any extensions for this class.
        self._register_extensions('objectrocket.instances.Instances')

    #####################
    # Public interface. #
    #####################
    @util.token_auto_auth
    def all(self):
        """Get all ObjectRocket instances the current client has access to.

        :returns: A list of :py:class:`bases.BaseInstance` instances.
        :rtype: list
        """
        response = requests.get(self._url, **self._default_request_kwargs)
        data = self._get_response_data(response)
        return self._concrete_instance_list(data)

    @util.token_auto_auth
    def create(self, name, plan, zone,
               service_type='mongodb', instance_type='mongodb_sharded', version='2.4.6'):
        """Create an ObjectRocket instance.

        :param str name: The name to give to the new instance.
        :param int plan: The plan size of the new instance.
        :param str zone: The zone that the new instance is to exist in.
        :param str service_type: The type of service that the new instance is to provide.
        :param str instance_type: The instance type to create.
        :param str version: The version of the service the new instance is to provide.
        """
        # Build up request data.
        url = self._url
        request_data = {
            'name': name,
            'service': service_type,
            'plan': plan,
            'type': instance_type,
            'version': version,
            'zone': zone
        }

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

    @util.token_auto_auth
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

        # Attempt to instantiate the appropriate class for the given instance document.
        try:
            service = instance_doc['service']
            cls = self._service_class_map[service]
            return cls(instance_document=instance_doc, instances=self)

        # If construction fails, log the exception and return None.
        except Exception as ex:
            logger.exception(ex)
            logger.error(
                'Instance construction failed. You probably need to upgrade to a more '
                'recent version of the client. Instance document which generated this '
                'warning: {}'.format(instance_doc)
            )
            return None

    def _concrete_instance_list(self, instance_docs):
        """Concretize a list of instance documents.

        :param list instance_docs: A list of instance documents. Should come from the API.
        :returns: A list of :py:class:`bases.BaseInstance`s.
        :rtype: list
        """
        if not instance_docs:
            return []

        return list(
            filter(None, [self._concrete_instance(instance_doc=doc) for doc in instance_docs])
        )

    @property
    def _default_request_kwargs(self):
        """The default request keyword arguments to be passed to the requests library."""
        defaults = copy.deepcopy(super(Instances, self)._default_request_kwargs)
        defaults.setdefault('headers', {}).update({
            'X-Auth-Token': self._client.auth._token
        })
        return defaults

    @property
    def _service_class_map(self):
        """A mapping of service names to service classes."""
        service_map = {
            'mongodb': MongodbInstance,
            'elasticsearch': ESInstance,
            'redis': RedisInstance,
        }
        return service_map

    @property
    def _url(self):
        """The base URL for instance operations."""
        return self._client._url + 'instances/'

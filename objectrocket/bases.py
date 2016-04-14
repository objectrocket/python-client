"""Base classes used throughout the library."""
import abc
import logging

import requests
import six

from objectrocket import errors
from objectrocket import util

from stevedore.extension import ExtensionManager

log = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class BaseOperationsLayer(object):
    """A base class for operations layer classes."""

    def __init__(self, base_client):
        self.__client = base_client

    ######################
    # Private interface. #
    ######################
    @property
    def _client(self):
        """An instance of the objectrocket.client.Client."""
        return self.__client

    @abc.abstractproperty
    def _default_request_kwargs(self):
        """The default request keyword arguments to be passed to the requests library."""
        default_kwargs = {
            'headers': {
                'Content-Type': 'application/json'
            },
            'hooks': {
                'response': self._verify_auth
            }
        }
        return default_kwargs

    def _get_response_data(self, response):
        """Return the data from a ``requests.Response`` object.

        :param requests.Response response: The ``Response`` object from which to get the data.
        """
        try:
            _json = response.json()
            data = _json.get('data')
            return data
        except ValueError as ex:
            log.exception(ex)
            return None

    @abc.abstractproperty
    def _url(self):
        """The URL this operations layer is to interface with."""
        pass

    def _verify_auth(self, resp, *args, **kwargs):
        """A callback handler to verify that the given response object did not receive a 401."""
        if resp.status_code == 401:
            raise errors.AuthFailure(
                'Received response code 401 from {} {}.'
                .format(resp.request.method, resp.request.path_url)
            )


class BaseAuthLayer(BaseOperationsLayer):
    """A base class for authentication layer classes."""

    #####################
    # Public interface. #
    #####################
    @abc.abstractmethod
    def authenticate(self):
        """An implementation of this layer's authentication protocol."""
        pass

    ######################
    # Private interface. #
    ######################
    @property
    def _default_request_kwargs(self):
        """The default request keyword arguments to be passed to the requests library."""
        default_kwargs = {
            'headers': {
                'Content-Type': 'application/json'
            },
            'hooks': {}
        }
        return default_kwargs

    @abc.abstractmethod
    def _refresh(self):
        """An implementation of this layer's authentication refresh protocol."""
        pass

    @abc.abstractproperty
    def _url(self):
        """The URL this operations layer is to interface with."""
        pass


@six.add_metaclass(abc.ABCMeta)
class BaseInstance(object):
    """The base class for ObjectRocket service instances.

    :param dict instance_document: A dictionary representing the instance object, most likey coming
        from the ObjectRocket API.
    :param objectrocket.instances.Instances instances: An instance of
        :py:class:`objectrocket.instances.Instances`.
    """

    def __init__(self, instance_document, instances):
        self.__client = instances._client
        self.__instances = instances
        self.__instance_document = instance_document

        if 'connect_string' in instance_document:
            self._connect_string = instance_document['connect_string']
        elif 'connection_strings' in instance_document:
            self._connect_string = instance_document['connection_strings']
        else:
            raise errors.InstancesException('No connection string found.')

        # Bind required pseudo private attributes from API response document.
        self._created = instance_document['created']
        self._id = instance_document['id']
        self._name = instance_document['name']
        self._plan = instance_document['plan']
        self._service = instance_document['service']
        self._type = instance_document['type']
        self._version = instance_document['version']
        self._settings = instance_document.get('settings', [])

    def __repr__(self):
        """Represent this object as a string."""
        _id = hex(id(self))
        rep = (
            '<{!s} name={!s} id={!s} at {!s}>'
            .format(self.__class__.__name__, self.name, self.id, _id)
        )
        return rep

    def acl_sync(self, aws_sync=None, rackspace_sync=None):
        """Adjust Amazon Web Services and/or Rackspace Acl Sync feature for this instance.

        :param bool aws_sync: True/False whether to enable AWS acl sync for this instance.
        :param bool rackspace_sync: True/False whether to enable Rackspace acl sync for this
            instance.
        """
        url = self._url + 'acl_sync'

        data = {"aws_acl_sync_enabled": False, "rackspace_acl_sync_enabled": False}

        # Let's get current status of acl sync for this intance to set proper defaults.
        response = requests.get(url, **self._instances._default_request_kwargs)

        if response.status_code == 200:
            resp_json = response.json()
            current_status = resp_json.get('data', {})
            current_aws_sync_status = current_status.get("aws_acl_sync_enabled", False)
            current_rax_sync_status = current_status.get("rackspace_acl_sync_enabled", False)
            data.update({
                "aws_acl_sync_enabled": current_aws_sync_status,
                "rackspace_acl_sync_enabled": current_rax_sync_status
            })

            if aws_sync is not None:
                data.update({"aws_acl_sync_enabled": aws_sync})

            if rackspace_sync is not None:
                data.update({"rackspace_acl_sync_enabled": rackspace_sync})

            response = requests.put(url, json=data, **self._instances._default_request_kwargs)
            return response.json()

        else:
            raise errors.ObjectRocketException(
                "Couldn't get current status of instance, failing. Error: {}".format(response.text)
            )

    def run_acl_sync(self, aws_sync=False, rackspace_sync=False):
        """Run Acl sync for this instance.

        :param bool aws_sync: True/False whether to run AWS acl sync for this instance immediately.
        :param bool rackspace_sync: True/False whether to run Rackspace acl sync for this instance
            immediately.
        """
        url = self._url + 'acl_sync'

        data = {"aws_acl_sync_enabled": False, "rackspace_acl_sync_enabled": False}

        if aws_sync:
            data.update({"aws_acl_sync_enabled": True})
        if rackspace_sync:
            data.update({"rackspace_acl_sync_enabled": True})

        response = requests.post(url, json=data, **self._instances._default_request_kwargs)
        return response.json()

    @property
    def connect_string(self):
        """This instance's connection string."""
        return self._connect_string

    @property
    def created(self):
        """The date this instance was created."""
        return self._created

    @abc.abstractmethod
    def get_connection(self):
        """Get a live connection to this instance."""
        pass

    @property
    def id(self):
        """This instance's ID."""
        return self._id

    @property
    def name(self):
        """This instance's name."""
        return self._name

    @property
    def plan(self):
        """The base plan size of this instance."""
        return self._plan

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

    @property
    def settings(self):
        """The settings on this instance's service."""
        return self._settings

    def to_dict(self):
        """Render this object as a dictionary."""
        return self._instance_document

    ######################
    # Private interface. #
    ######################
    @property
    def _client(self):
        """An instance of the objectrocket.client.Client."""
        return self.__client

    @property
    def _instances(self):
        """An instance of the objectrocket.instances.Instances."""
        return self.__instances

    @property
    def _instance_document(self):
        """The document used to construct this Instance object."""
        return self.__instance_document

    @property
    def _url(self):
        """The URL of this instance object."""
        return self._instances._url + '{}/'.format(self.name)

    @property
    def _service_url(self):
        """The service specific URL of this instance object."""
        return self._client._url + '{}/{}/'.format(self.service, self.name)


###########
# Mixins. #
###########
class Extensible(object):
    """A mixin to implement support for class extensibility."""

    def _register_extensions(self, namespace):
        """Register any extensions under the given namespace."""

        # Register any extension classes for this class.
        extmanager = ExtensionManager(
            'extensions.classes.{}'.format(namespace),
            propagate_map_exceptions=True
        )

        if extmanager.extensions:
            extmanager.map(util.register_extension_class, base=self)

        # Register any extension methods for this class.
        extmanager = ExtensionManager(
            'extensions.methods.{}'.format(namespace),
            propagate_map_exceptions=True
        )
        if extmanager.extensions:
            extmanager.map(util.register_extension_method, base=self)


class InstanceAclsInterface(object):
    """A mixin implementing support for the instance bound ACLs interface.

    Should only be mixed in with an Instance class.
    """

    _acls = None

    @property
    def acls(self):
        """The instance bound ACLs operations layer."""
        if self._acls is None:
            self._acls = InstanceAcls(instance=self)
        return self._acls


class InstanceAcls(object):
    """An object implementing the ACLs interface bound to a specific instance."""

    def __init__(self, instance):
        self._instance = instance

    def all(self):
        """Get all ACLs for this instance."""
        return self._instance._client.acls.all(self._instance.name)

    def create(self, cidr_mask, description, **kwargs):
        """Create an ACL for this instance.

        See :py:meth:`Acls.create` for call signature.
        """
        return self._instance._client.acls.create(
            self._instance.name,
            cidr_mask,
            description,
            **kwargs
        )

    def get(self, acl):
        """Get the ACL specified by ID belonging to this instance.

        See :py:meth:`Acls.get` for call signature.
        """
        return self._instance._client.acls.get(self._instance.name, acl)

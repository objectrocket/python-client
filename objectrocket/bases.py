"""Base classes used throughout the library."""
import abc

import six

from objectrocket import errors
from objectrocket import util

from stevedore.extension import ExtensionManager


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
        self._name = instance_document['name']
        self._plan = instance_document['plan']
        self._service = instance_document['service']
        self._type = instance_document['type']
        self._version = instance_document['version']

    def __repr__(self):
        """Represent this object as a string."""
        _id = hex(id(self))
        rep = (
            '<{!s} {!r} at {!s}>'
            .format(self.__class__.__name__, self._instance_document, _id)
        )
        return rep

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

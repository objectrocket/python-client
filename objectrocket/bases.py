"""Base classes used throughout the library."""
import abc

import six

from objectrocket import errors


@six.add_metaclass(abc.ABCMeta)
class BaseOperationsLayer(object):
    """A base class for operations layer classes."""

    def __init__(self, base_client):
        self.__client = base_client

    #####################
    # Public interface. #
    #####################
    @property
    def _client(self):
        """An instance of the objectrocket.client.Client."""
        return self.__client

    ######################
    # Private interface. #
    ######################
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
                'Received response code 401 from {} {}. Token used: {}.'
                .format(resp.request.method, resp.request.path_url, self._client._token)
            )


@six.add_metaclass(abc.ABCMeta)
class BaseInstance(object):
    """The base class for ObjectRocket service instances.

    :param dict instance_document: A dictionary representing the instance object, most likey coming
        from the ObjectRocket API.
    :param object base_client: An instance of :py:class:`objectrocket.client.Client`, most likely
        coming from the :py:class:`objectrocket.instance.Instances` service layer.
    """

    def __init__(self, instance_document, base_client):
        self.__client = base_client
        self.__instance_document = instance_document

        # Bind required pseudo private attributes from API response document.
        self._connect_string = instance_document['connect_string']
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
    def _instance_document(self):
        """The document used to construct this Instance object."""
        return self.__instance_document

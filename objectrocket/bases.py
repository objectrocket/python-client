"""Base classes used throughout the library."""
import copy


class BaseOperationsLayer(object):
    """A base class for operations layer classes."""

    def __init__(self, base_client):
        self._client = base_client

    @property
    def client(self):
        """An instance of the objectrocket.client.Client."""
        return self._client

    def _verify_auth(self, resp, *args, **kwargs):
        """A wrapper around :py:meth:`objectrocket.client.Client._verify_auth`."""
        self.client._verify_auth(resp, *args, **kwargs)


class BaseInstance(object):
    """The base class for ObjectRocket service instances.

    :param dict instance_document: A dictionary representing the instance object.
    :param object client: An instance of :py:class:`objectrocket.client.Client`, most likely coming
        from the :py:class:`objectrocket.instance.Instances` service layer.
    """

    def __init__(self, instance_document, client):
        self._client = client
        self._instance_document = copy.deepcopy(instance_document)

        # Bind pseudo private attributes from instance_document.
        self._api_endpoint = instance_document.pop('api_endpoint', None)
        self._connect_string = instance_document.pop('connect_string', None)
        self._created = instance_document.pop('created', None)
        self._name = instance_document.pop('name', None)
        self._service = instance_document.pop('service', None)
        self._type = instance_document.pop('type', None)
        self._version = instance_document.pop('version', None)

        # Bind any additional items as properties.
        for key, val in instance_document.items():
            setattr(self, key, val)

    def __repr__(self):
        """Represent this object as a string."""
        _id = hex(id(self))
        rep = (
            '<objectrocket.instances.{!s} {!r} at {!s}>'
            .format(self.__class__.__name__, self.instance_document, _id)
        )
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

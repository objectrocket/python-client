"""ObjectRocket Python client."""
from objectrocket import auth
from objectrocket import bases
from objectrocket import constants
from objectrocket import instances


class Client(bases.Extensible):
    """The base client for ObjectRocket's Python interface.

    :param str base_url: The base APIv2 URL to interface with.
    """

    def __init__(self, base_url=constants.OR_DEFAULT_API_URL):
        # Private interface attributes.
        self.__url = base_url

        # Public interface attributes.
        self.auth = auth.Auth(base_client=self)
        self.instances = instances.Instances(base_client=self)

        # Register any extensions for this class.
        self._register_extensions('objectrocket.client.Client')

    #####################
    # Public interface. #
    #####################
    def authenticate(self, *args, **kwargs):
        """Conveniently call the underlying :py:meth:`objectrocket.auth.Authenticate` method."""
        return self.auth.authenticate(*args, **kwargs)

    ######################
    # Private interface. #
    ######################
    @property
    def _url(self):
        """The base URL this client is using."""
        return self.__url

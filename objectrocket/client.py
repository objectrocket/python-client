"""ObjectRocket Python client."""
from objectrocket import auth
from objectrocket import instances
from objectrocket import constants

from stevedore.extension import ExtensionManager


class Client(object):
    """The base client for ObjectRocket's Python interface.

    Instantiation of the client will perform API authentication. If API authentication fails,
    client instantiation will also fail.

    :param str username: This is the username to perform basic authentication against the API with.
    :param str password: This is the password to perform basic authentication against the API with.
    :param str alternative_url: (optional) An alternative base URL for the client to use. You
        shouldn't have to worry about this at all.
    """

    def __init__(self, username, password, **kwargs):
        # Client properties.
        self._base_url = kwargs.get('alternative_url') or constants.DEFAULT_API_URL
        self.__username = username
        self.__password = password

        # Lazily-created properties.
        self._auth = None
        self._instances = None
        self.__token = None

        # Perform authentication as part of initialization phase for now.
        self._token  # Accessing this attribute will trigger authentication.

        # Register any additional operations layer extensions.
        extmanager = ExtensionManager('objectrocket', propagate_map_exceptions=True)
        if extmanager.extensions:
            extmanager.map(self._register_operations_extensions)

    #####################
    # Public interface. #
    #####################
    @property
    def auth(self):
        """The authentication operations layer."""
        if self._auth is None:
            self._auth = auth.Auth(base_client=self)
        return self._auth

    @property
    def instances(self):
        """The instances operations layer."""
        if self._instances is None:
            self._instances = instances.Instances(base_client=self)
        return self._instances

    ######################
    # Private interface. #
    ######################
    @property
    def _password(self):
        """The password currently being used by this client."""
        return self.__password

    def _register_operations_extensions(self, extension):
        """Register any operations layer extensions which may be installed."""
        # Bind extension as a public attribute.
        extension_instance = extension.plugin(self)  # Pass self as standard registry process.
        setattr(self, extension.name.lstrip('_'), extension_instance)

    @property
    def _token(self):
        """The API token this client is currently using."""
        if self.__token is None:
            self.__token = self.auth.authenticate(username=self._username, password=self._password)
        return self.__token

    @_token.setter
    def _token(self, new_token):
        """Set the value of this client's API token."""
        self.__token = new_token
        return self.__token

    @property
    def _url(self):
        """The base URL this client is using."""
        return self._base_url

    @property
    def _username(self):
        """The username currently being used by this client."""
        return self.__username

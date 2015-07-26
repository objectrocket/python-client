"""ObjectRocket Python client."""
from objectrocket import auth
from objectrocket import constants
from objectrocket import instances
from objectrocket import util

from stevedore.extension import ExtensionManager


class Client(object):
    """The base client for ObjectRocket's Python interface.

    :param str base_url: The base APIv2 URL to interface with.
    """

    def __init__(self, base_url=constants.DEFAULT_API_URL):
        # Private interface attributes.
        self._base_url = base_url

        # Public interface attributes.
        self.auth = auth.Auth(base_client=self)
        self.instances = instances.Instances(base_client=self)

        # Register any extensions classes for this class.
        extmanager = ExtensionManager(
            'extensions.classes::objectrocket.client.Client',
            propagate_map_exceptions=True
        )
        if extmanager.extensions:
            extmanager.map(util.register_extension_class, base=self)

    #####################
    # Public interface. #
    #####################
    def authenticate(self, username, password):
        """Authenticate with the API and get a token back for client use.

        :param str username: This is the username to perform basic authentication
            against the API with.
        :param str password: This is the password to perform basic authentication
            against the API with.
        """
        self.auth.authenticate(username=username, password=password)

    ######################
    # Private interface. #
    ######################
    @property
    def _url(self):
        """The base URL this client is using."""
        return self._base_url

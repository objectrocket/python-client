"""Client layer."""
from objectrocket import instances
from objectrocket import constants


class Client(object):
    """The base client for ObjectRocket API Python interface.

    :param str user_key: This is the user key to be used for API authentication.
    :param str pass_key: This is the password key to be used for API authentication.
    """

    def __init__(self, user_key, pass_key, api_url='default'):
        if not isinstance(user_key, str) or not isinstance(pass_key, str):
            raise self.ClientException('All parameters should be instances of str.')

        # Client properties.
        self._api_url = constants.API_URL_MAP[api_url]
        self._user_key = user_key
        self._pass_key = pass_key

        # Lazily-created properties.
        self._instances = None

    @property
    def api_url(self):
        """The base API URL the Client is using."""
        return self._api_url

    @property
    def instances(self):
        """The instance operations layer."""
        if self._instances is None:
            self._instances = instances.Instances(self)

        return self._instances

    @property
    def pass_key(self):
        """The password key currently being used by the Client."""
        return self._pass_key

    @property
    def user_key(self):
        """The user key currently being used by the Client."""
        return self._user_key

    class ClientException(Exception):
        pass

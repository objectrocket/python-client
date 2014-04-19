"""Client layer."""
from objectrocket import instances


# TODO(Anthony): api_url should default to our v2 api. Overwrite with a kwarg.
class Client(object):
    """Client."""

    def __init__(self, user_key, pass_key, api_url=None):
        if (not isinstance(user_key, str) or
                not isinstance(pass_key, str)):
            raise self.ClientException('All parameters should be instances of str.')

        if api_url is not None:
            # FIXME(Anthony): Probably shouldn't do this long term.
            api_url = self._check_api_url(api_url)
        else:
            api_url = 'http://localhost:5050/v2/'  # Point this to the LB when deployed.

        # Client properties.
        self._api_url = api_url
        self._user_key = user_key
        self._pass_key = pass_key

        self._instances = None

    @property
    def api_url(self):
        """The base API URL the Client is using."""
        return self._api_url

    def _check_api_url(self, api_url):
        """Ensure that a custom url is somewhat usable."""
        api_url = api_url.strip()
        if not api_url.endswith('/'):
            api_url += '/'

        if not api_url.endswith('/v2/'):
            api_url += 'v2/'

        if not api_url.startswith(('http://', 'https://')):
            api_url = 'https://' + api_url

        return api_url

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

"""ObjectRocket Python client."""
from objectrocket import auth
from objectrocket import instances
from objectrocket import constants
from objectrocket import errors


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
        self._url = kwargs.get('alternative_url') or constants.DEFAULT_API_URL
        self._username = username
        self._password = password

        # Lazily-created properties.
        self._instances = None

        # Authenticate.
        self._auth = auth.Auth(base_client=self)
        self._token = self._auth.authenticate(username=self.username, password=self.password)

    @property
    def auth(self):
        """The authentication operations layer."""
        return self._auth

    # TODO(TheDodd): move this to respective base classes.
    @property
    def default_request_kwargs(self):
        """The default request keyword arguments to be passed to the request library."""
        default_kwargs = {
            'headers': {
                'Content-Type': 'application/json',
                'X-Auth-Token': self.token
            },
            'hooks': {
                'response': self._verify_auth
            }
        }
        return default_kwargs

    @property
    def instances(self):
        """The instance operations layer."""
        if self._instances is None:
            self._instances = instances.Instances(base_client=self)
        return self._instances

    @property
    def password(self):
        """The password currently being used by this client."""
        return self._password

    @property
    def token(self):
        """The API token this client is currently using."""
        return self._token

    @property
    def url(self):
        """The base URL this client is using."""
        return self._url

    @property
    def username(self):
        """The username currently being used by this client."""
        return self._username

    def _verify_auth(self, resp, *args, **kwargs):
        """A callback handler to verify that the given response object did not receive a 401."""
        if resp.status_code == 401:
            raise errors.AuthFailure(
                'Received response code 401 from {} {}. Token used: {}.'
                .format(resp.request.method, resp.request.path_url, self.token)
            )

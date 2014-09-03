"""ObjectRocket Python client."""
from objectrocket import auth
from objectrocket import instances
from objectrocket import constants
from objectrocket import errors


class Client(object):
    """The base client for ObjectRocket's Python interface.

    Instantiation of the client will perform API authentication. If API authentication fails,
    client instantiation will also fail.

    The client will use API tokens by default. If you don't want to use API  tokens, and would
    rather have the client perform basic authentication using your keypair for each request, set
    the ``use_tokens`` parameter to ``False``.

    :param str user_key: This is the user key to be used for API authentication.
    :param str pass_key: This is the password key to be used for API authentication.
    :param bool use_tokens: Instruct the client to use tokens or not.
    :param str alternative_url: (optional) An alternative base URL for the client to use. You
        shouldn't have to worry about this at all.
    """

    def __init__(self, user_key, pass_key, use_tokens=True, **kwargs):
        # Client properties.
        self._url = kwargs.get('alternative_url') or constants.DEFAULT_API_URL
        self._user_key = user_key
        self._pass_key = pass_key
        self._is_using_tokens = use_tokens

        # Lazily-created properties.
        self._instances = None

        # Authenticate.
        self._auth = auth.Auth(client_instance=self)
        self._token = self._auth.authenticate(user_key=self.user_key, pass_key=self.pass_key)

    @property
    def auth(self):
        """The authentication operations layer."""
        return self._auth

    @property
    def default_request_kwargs(self):
        """The default request keyword arguments to be passed to the request library."""
        default_kwargs = {
            'headers': {
                'Content-Type': 'application/json',
            },
            'hooks': {
                'response': self._verify_auth,
            },
        }

        # Configue default authentication method based on clients configuration.
        if self.is_using_tokens:
            default_kwargs['headers']['X-Auth-Token'] = self.token
        else:
            default_kwargs['auth'] = (self.user_key, self.pass_key)

        return default_kwargs

    @property
    def instances(self):
        """The instance operations layer."""
        if self._instances is None:
            self._instances = instances.Instances(client_instance=self)
        return self._instances

    @property
    def is_using_tokens(self):
        """A boolean value indicating whether the client is using token authentication or not."""
        return self._is_using_tokens

    @property
    def pass_key(self):
        """The password key currently being used by this client."""
        return self._pass_key

    @property
    def token(self):
        """The API token this client is currently using."""
        return self._token

    @property
    def url(self):
        """The base URL this client is using."""
        return self._url

    @property
    def user_key(self):
        """The user key currently being used by this client."""
        return self._user_key

    def _verify_auth(self, resp, *args, **kwargs):
        """A callback handler to verify that the given response object did not receive a 401."""
        if resp.status_code == 401:
            raise errors.AuthFailure('Received response code 401 from {} {}. Keypair used: {}:{}'
                                     ''.format(resp.request.method, resp.request.path_url,
                                               self.user_key, self.pass_key))

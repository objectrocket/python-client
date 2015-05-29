"""Authentication operations."""
import functools
import requests

from objectrocket import bases
from objectrocket import errors


def token_auto_auth(func):
    """Wrap class methods with automatic token re-authentication.

    This wrapper will detect authentication failures coming from its wrapped method. When one is
    caught, it will request a new token, and simply replay the original request.

    The one constraint that this wrapper has is that the wrapped method's class must have the
    :py:class:`objectrocket.client.Client` object embedded in it as the property ``client``. Such
    is the design of all current client operations layers.
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            response = func(self, *args, **kwargs)
        except errors.AuthFailure:
            # Re-raise the exception if the client is not using token authentication.
            if not self.client.is_using_tokens:
                raise

            # Request a new token using the keypair originally given to the client.
            self.client._token = self.client.auth.authenticate(self.client.username,
                                                               self.client.password)
            response = func(self, *args, **kwargs)
        return response

    return wrapper


class Auth(bases.BaseOperationsLayer):
    """Authentication operations.

    :param objectrocket.client.Client base_client: An objectrocket.client.Client instance.
    """

    def __init__(self, base_client):
        super(Auth, self).__init__(base_client=base_client)

    def authenticate(self, username, password):
        """Authenticate against the ObjectRocket API.

        :param str username: The username to perform basic authentication against the API with.
        :param str password: The password to perform basic authentication against the API with.

        :returns: A token used for authentication against token protected resources.
        :rtype: str
        """
        resp = requests.get(
            self.url,
            auth=(username, password),
            # TODO(TheDodd): maybe break client.default_request_kwargs.hooks into client prop.
            hooks=dict(response=self.client._verify_auth)
        )

        try:
            data = resp.json()
            token = data['data']['token']
            return token
        except (ValueError, KeyError) as ex:
            raise errors.AuthFailure(str(ex))

    @property
    def url(self):
        """The base URL for authentication operations."""
        return self.client.url + 'tokens/'

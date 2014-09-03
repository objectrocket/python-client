"""Authentication operations."""
import functools
import requests

from objectrocket import operations
from objectrocket import errors


def _token_auto_auth(func):
    """Wrap class methods with automatic token re-authentication.

    This wrapper will detect authentication failures coming from its wrapped method. When one is
    caught, it will request a new token, and simply replay the original request. If the client
    object is not using token authentication, then this wrapper effectively does nothing.

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
            self.client._token = self.client.auth.authenticate(self.client.user_key,
                                                               self.client.pass_key)
            response = func(self, *args, **kwargs)
        return response

    return wrapper


class Auth(operations.BaseOperationsLayer):
    """Authentication operations.

    :param objectrocket.client.Client client_instance: An objectrocket.client.Client instance.
    """

    def __init__(self, client_instance):
        super(Auth, self).__init__(client_instance=client_instance)

    def authenticate(self, user_key, pass_key):
        """Authenticate against the ObjectRocket API.

        :param str user_key: The username key used for basic auth.
        :param str pass_key: The password key used for basic auth.

        :returns: A token used for authentication against token protected resources.
        :rtype: str
        """
        url = self.url + 'token/'
        resp = requests.get(url, auth=(user_key, pass_key),
                            hooks=dict(response=self.client._verify_auth))

        try:
            data = resp.json()
            token = data['data']
            return token
        except (ValueError, KeyError) as ex:
            raise errors.AuthFailure(str(ex))

    @property
    def url(self):
        """The base URL for authentication operations."""
        return self.client.url + 'auth/'

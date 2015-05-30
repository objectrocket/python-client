"""Authentication operations."""
import functools
import logging
import requests

from objectrocket import bases
from objectrocket import errors

logger = logging.getLogger(__name__)


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

        # If auth failure occures, attempt to re-authenticate and replay once at most.
        except errors.AuthFailure:

            # Request and set a new API token.
            new_token = self.client.auth.authenticate(self.client._username, self.client._password)
            self.client._token = new_token
            logger.info('New API token bound to client: "{}".'.format(new_token))

            # Replay original request.
            response = func(self, *args, **kwargs)

        return response

    # TODO(TheDodd): figure out a way to match func call signature and docs.
    return wrapper


class Auth(bases.BaseOperationsLayer):
    """Authentication operations.

    :param objectrocket.client.Client base_client: An objectrocket.client.Client instance.
    """

    def __init__(self, base_client):
        super(Auth, self).__init__(base_client=base_client)

    #####################
    # Public interface. #
    #####################
    def authenticate(self, username, password):
        """Authenticate against the ObjectRocket API.

        :param str username: The username to perform basic authentication against the API with.
        :param str password: The password to perform basic authentication against the API with.

        :returns: A token used for authentication against token protected resources.
        :rtype: str
        """
        resp = requests.get(
            self._url,
            auth=(username, password),
            **self._default_request_kwargs
        )

        try:
            data = resp.json()
            token = data['data']['token']
            return token
        except (ValueError, KeyError) as ex:
            raise errors.AuthFailure(str(ex))

    ######################
    # Private interface. #
    ######################
    @property
    def _default_request_kwargs(self):
        """The default request keyword arguments to be passed to the requests library."""
        return super(Auth, self)._default_request_kwargs

    @property
    def _url(self):
        """The base URL for authentication operations."""
        return self.client._url + 'tokens/'

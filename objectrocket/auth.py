"""Authentication operations."""
import copy
import logging
import requests

from objectrocket import bases
from objectrocket import errors

logger = logging.getLogger(__name__)


class Auth(bases.BaseAuthLayer):
    """Authentication operations.

    :param objectrocket.client.Client base_client: An objectrocket.client.Client instance.
    """

    def __init__(self, base_client):
        self.__username = None
        self.__password = None
        self.__token = None

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
        # Update the username and password bound to this instance for re-authentication needs.
        self._username = username
        self._password = password

        # Attempt to authenticate.
        resp = requests.get(
            self._url,
            auth=(username, password),
            **self._default_request_kwargs
        )

        # Attempt to extract authentication data.
        try:
            json_data = resp.json()
            token = json_data['data']['token']
        except Exception as ex:
            logging.exception(ex)
            raise errors.AuthFailure('{}: {}'.format(ex.__class__.__name__, ex))

        # Update the token bound to this instance for use by other client operations layers.
        self._token = token
        logger.info('New API token received: "{}".'.format(token))
        return token

    ######################
    # Private interface. #
    ######################
    @property
    def _default_request_kwargs(self):
        """The default request keyword arguments to be passed to the requests library."""
        return super(Auth, self)._default_request_kwargs

    @property
    def _password(self):
        """The password currently being used for authentication."""
        return self.__password

    @_password.setter
    def _password(self, new_password):
        """Update the password to be used for authentication."""
        self.__password = new_password

    def _refresh(self):
        """Refresh the API token using the currently bound credentials.

        This is simply a convenience method to be invoked automatically if authentication fails
        during normal client use.
        """
        # Request and set a new API token.
        new_token = self.authenticate(self._username, self._password)
        self._token = new_token
        logger.info('New API token received: "{}".'.format(new_token))
        return self._token

    @property
    def _token(self):
        """The API token this instance is currently using."""
        return self.__token

    @_token.setter
    def _token(self, new_token):
        """Update the API token which this instance is to use."""
        self.__token = new_token
        return self.__token

    @property
    def _url(self):
        """The base URL for authentication operations."""
        return self._client._url + 'tokens/'

    @property
    def _username(self):
        """The username currently being used for authentication."""
        return self.__username

    @_username.setter
    def _username(self, new_username):
        """Update the username to be used for authentication."""
        self.__username = new_username

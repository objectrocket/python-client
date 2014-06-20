"""Base operations logic for interfacing with various API resources."""
from objectrocket import errors


class BaseOperationsLayer(object):
    """A base for operations layer classes; I.E., :py:class:`objectrocket.instances.Instances`."""

    def __init__(self, client_instance):
        self.__client = client_instance

    @property
    def _client(self):
        """This layer's :py:class:`objectrocket.client.Client` instance."""
        return self.__client

    def _verify_auth(self, resp, *args, **kwargs):
        """Verify that the response object did not receive a 401."""
        if resp.status_code == 401:
            raise errors.AuthFailure('Received response code 401 from {} {}. Keypair used: {}:{}'
                                     ''.format(resp.request.method, resp.request.path_url,
                                               self._client.user_key, self._client.pass_key))

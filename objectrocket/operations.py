"""Base operations logic for interfacing with various API resources."""


class BaseOperationsLayer(object):
    """A base class for operations layer classes."""

    def __init__(self, client_instance):
        self._client = client_instance

    @property
    def client(self):
        """An instance of the objectrocket.client.Client."""
        return self._client

    def _verify_auth(self, resp, *args, **kwargs):
        """A wrapper around :py:meth:`objectrocket.client.Client._verify_auth`."""
        self.client._verify_auth(resp, *args, **kwargs)

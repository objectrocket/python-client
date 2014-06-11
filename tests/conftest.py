"""Test configuration for the ObjectRocket Python Client.

Testing
=======
This client interfaces with the ObjectRocket APIv2. On principal - The Law of Demeter - we cannot
simply spin up an APIv2 service and use that for testing purposes. We must test according to the
documented interface. To do so, we will use mocks which will return the expected and documented
response. This will also provide to harden the API interface.
"""
import pytest


@pytest.fixture
def mocked_request(request):
    return


class BaseClientTest(object):
    """Base class for client based testing."""
    pass

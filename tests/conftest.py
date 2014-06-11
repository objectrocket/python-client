"""Test configuration for the ObjectRocket Python Client.

Testing
=======
This client interfaces with the ObjectRocket APIv2. On principal - The Law of Demeter - we cannot
simply spin up an APIv2 service and use that for testing purposes. We must test according to the
documented interface. To do so, we will use mocks which will return the expected and documented
response. This will also provide to harden the API interface.
"""
import datetime

import pytest

from objectrocket.client import Client
from objectrocket import constants


class BaseClientTest(object):
    """Base class for client based testing."""

    @pytest.fixture(autouse=True)
    def _bind_client(self):
        """Automatically construct and bind the client to self."""
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        self.client = Client(user_key, pass_key)


@pytest.fixture
def mocked_request(request):
    return


@pytest.fixture
def instance_document():
    now = datetime.datetime.utcnow()
    instance_document = {
        "api_endpoint": constants.API_URL_MAP['testing'],
        "connect_string": "localhost:50002",
        "created": datetime.datetime.strftime(now, constants.TIME_FORMAT),
        "name": "testinstance",
        "plan": 5,
        "service": "mongodb",
        "ssl_connect_string": "localhost:60002",
        "type": "mongodb_sharded",
        "version": "2.4.6",
    }
    return instance_document

"""Test configuration for the ObjectRocket Python Client."""
import datetime

import mock
import pytest

from objectrocket.client import Client
from objectrocket import instances
from objectrocket import constants

constants.DEFAULT_API_URL = '/v2/'


class ClientHarness(object):
    """A harness for testing client based logic."""

    @pytest.fixture
    def requests_patches(self, request):
        """Return a dict of ``MagicMock``s which patch the requests library in various places.

        :returns: A dict where each key is the name of a module, and its value is the ``MagicMock``
            which is patching the requests library in its respective module.
        """
        patches = {}

        mocked = mock.patch('objectrocket.auth.requests', autospec=True)
        request.addfinalizer(mocked.stop)
        patches['auth'] = mocked.start()

        mocked = mock.patch('objectrocket.instances.requests', autospec=True)
        request.addfinalizer(mocked.stop)
        patches['instances'] = mocked.start()

        return patches

    @pytest.fixture
    def client_basic_auth(self, requests_patches):
        """Build a client configured to use basic auth."""
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        return Client(user_key, pass_key, use_tokens=False)

    @pytest.fixture
    def client_token_auth(self, requests_patches):
        """Build a client configured to use token auth."""
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        return Client(user_key, pass_key, use_tokens=True)


class InstancesHarness(ClientHarness):
    """A harness for testing operations logic."""

    def pytest_generate_tests(self, metafunc):
        """Generate tests for the different instance types."""
        if '_docs' in metafunc.fixturenames:
            metafunc.parametrize('_docs', [
                mongo_replica_doc(),
                mongo_sharded_doc(),
            ])

        if '_instances_and_docs' in metafunc.fixturenames:
            metafunc.parametrize('_instances_and_docs', [
                (self.mongo_replica_instance(mongo_replica_doc()), mongo_replica_doc()),
                (self.mongo_sharded_instance(mongo_sharded_doc()), mongo_sharded_doc()),
            ])

    @pytest.fixture
    def default_create_instance_kwargs(self):
        """Return a dict having default data for calling Instances.create."""
        data = {
            'name': 'instance0',
            'size': 5,
            'zone': 'US-West',
            'service_type': 'mongodb',
            'version': '2.4.6',
        }
        return data

    @pytest.fixture
    def mongo_replica_instance(client_token_auth, mongo_replica_doc):
        return instances.MongodbInstance(instance_document=mongo_replica_doc,
                                         client=client_token_auth)

    @pytest.fixture
    def mongo_sharded_instance(client_token_auth, mongo_sharded_doc):
        return instances.MongodbInstance(instance_document=mongo_sharded_doc,
                                         client=client_token_auth)


class OperationsHarness(ClientHarness):
    """A harness for testing operations logic."""

    # Add operations specific fixtures and such here.
    pass


class GenericFixtures(object):
    """Generic fixtures."""

    @pytest.fixture
    def obj(self):
        """A generic object for testing purposes."""
        class Obj(object):
            pass

        return Obj()


#############################
# INSTANCE RELATED FIXTURES #
#############################
@pytest.fixture
def mongo_replica_doc():
    now = datetime.datetime.utcnow()
    doc = {
        "api_endpoint": 'not_a_real_endpoint',
        "connect_string": "REPLSET_60000/localhost:60000,localhost:60001,localhost:60002",
        "created": datetime.datetime.strftime(now, constants.TIME_FORMAT),
        "name": "testinstance",
        "plan": 1,
        "service": "mongodb",
        "type": "mongodb_replica_set",
        "version": "2.4.6",
    }
    return doc


@pytest.fixture
def mongo_sharded_doc():
    now = datetime.datetime.utcnow()
    doc = {
        "api_endpoint": 'not_a_real_endpoint',
        "connect_string": "localhost:50002",
        "created": datetime.datetime.strftime(now, constants.TIME_FORMAT),
        "name": "testinstance",
        "plan": 5,
        "service": "mongodb",
        "ssl_connect_string": "localhost:60002",
        "type": "mongodb_sharded",
        "version": "2.4.6",
    }
    return doc

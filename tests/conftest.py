"""Test configuration for the ObjectRocket Python Client."""
import datetime

import mock
import pytest

from objectrocket.client import Client
from objectrocket import instances
from objectrocket import constants


class AuthenticationHarness(object):
    """A harness for testing logic coming from :py:module:`objectrocket.auth`."""

    @pytest.fixture
    def auth_requests(self, request):
        """Return a MagicMock which patches objectrocket.auth.requests."""
        mocked = mock.patch('objectrocket.auth.requests', autospec=True)
        request.addfinalizer(mocked.stop)
        return mocked.start()


class ClientHarness(AuthenticationHarness):
    """A harness for testing client based logic."""

    @pytest.fixture
    def client_basic_auth(self, auth_requests):
        """Build a client configured to use basic auth."""
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        return Client(user_key, pass_key, use_tokens=False)

    @pytest.fixture
    def client_token_auth(self, auth_requests):
        """Build a client configured to use token auth."""
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        return Client(user_key, pass_key, use_tokens=True)


class OperationsHarness(ClientHarness):
    """A harness for testing operations logic."""

    pass
    # def pytest_generate_tests(self, metafunc):
    #     """Generate tests for the different client configurations."""

    #     if 'client_instance' in metafunc.fixturenames:
    #         metafunc.parametrize('client_instance', [
    #             self.client_token_auth(self.auth_requests(pytest.fixture.request)),
    #             self.client_basic_auth(self.auth_requests(pytest.fixture.request)),
    #         ])


class GenericFixtures(object):
    """Generic fixtures."""

    @pytest.fixture
    def obj(self):
        """A generic object for testing purposes."""
        class Obj(object):
            pass

        return Obj()


class BaseInstanceTest(object):
    """Base class for testing instance objects."""

    def pytest_generate_tests(self, metafunc):
        """Generate tests for the different instance types."""
        if '_docs' in metafunc.fixturenames:
            metafunc.parametrize('_docs', [
                mongo_replica_doc(),
                mongo_sharded_doc(),
            ])

        if '_instances_and_docs' in metafunc.fixturenames:
            metafunc.parametrize('_instances_and_docs', [
                (mongo_replica_instance(mongo_replica_doc()), mongo_replica_doc()),
                (mongo_sharded_instance(mongo_sharded_doc()), mongo_sharded_doc()),
            ])


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


@pytest.fixture
def mongo_replica_instance(mongo_replica_doc):
    return instances.MongodbInstance(instance_document=mongo_replica_doc,
                                     client=Client('test_user_key', 'test_pass_key'))


@pytest.fixture
def mongo_sharded_instance(mongo_sharded_doc):
    return instances.MongodbInstance(instance_document=mongo_sharded_doc,
                                     client=Client('test_user_key', 'test_pass_key'))

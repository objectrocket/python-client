"""Test configuration for the ObjectRocket Python Client."""
import datetime
import uuid

import mock
import pytest
import requests

from objectrocket.client import Client
from objectrocket import acls
from objectrocket import instances
from objectrocket import constants

from .mock_stats import (SHARD_STATS_THIS_SECOND, INSTANCE_STATS_THIS_SECOND,
                         INSTANCE_STATS_NEXT_SECOND, NEW_RELIC_STATS)

#####################
# Generic fixtures. #
#####################
@pytest.fixture
def client(patched_requests_map):
    """Build a client for use in testing."""
    return Client(base_url='http://localhost:5050/v2/')


@pytest.fixture
def default_create_instance_kwargs():
    """Return a dict having default data for instance creation."""
    data = {
        'name': 'instance0',
        'size': 5,
        'zone': 'US-West',
        'service_type': 'mongodb',
        'version': '2.4.6',
    }
    return data


@pytest.fixture
def obj():
    """A generic object for testing purposes."""
    class Obj(object):
        pass

    return Obj()


##########################
# ACLs related fixtures. #
##########################
@pytest.fixture
def acl_doc():
    now = datetime.datetime.utcnow()
    doc = {
        'id': uuid.uuid4().hex,

        'cidr_mask': '0.0.0.0/1',
        'description': 'testing',
        'instance': 'testinstance',
        'login': 'testuser',
        'port': 27017,

        'date_created': datetime.datetime.strftime(now, constants.TIME_FORMAT),
        'instance_id': uuid.uuid4().hex,
        'instance_type': 'mongodb_sharded',
        'metadata': {},
        'service_type': 'mongodb'
    }
    return doc


@pytest.fixture
def acl(acl_doc, client):
    return acls.Acl(document=acl_doc, acls=client.acls)


##############################
# Instance related fixtures. #
##############################
@pytest.fixture
def mongodb_replica_doc():
    now = datetime.datetime.utcnow()
    doc = {
        'id': uuid.uuid4().hex,
        'api_endpoint': 'not_a_real_endpoint',
        'connect_string': 'REPLSET_60000/localhost:60000,localhost:60001,localhost:60002',
        'created': datetime.datetime.strftime(now, constants.TIME_FORMAT),
        'name': 'testinstance',
        'plan': 1,
        'service': 'mongodb',
        'type': 'mongodb_replica_set',
        'version': '2.4.6',
    }
    return doc


@pytest.fixture
def mongodb_sharded_doc():
    now = datetime.datetime.utcnow()
    doc = {
        'id': uuid.uuid4().hex,
        'api_endpoint': 'not_a_real_endpoint',
        'connect_string': 'localhost:50002',
        'created': datetime.datetime.strftime(now, constants.TIME_FORMAT),
        'name': 'testinstance',
        'plan': 5,
        'service': 'mongodb',
        'ssl_connect_string': 'localhost:60002',
        'type': 'mongodb_sharded',
        'version': '2.4.6',
    }
    return doc


@pytest.fixture
def mongodb_replicaset_instance(client, mongodb_replica_doc):
    return instances.MongodbInstance(instance_document=mongodb_replica_doc,
                                     instances=client.instances)


@pytest.fixture
def mongodb_sharded_instance(client, mongodb_sharded_doc):
    return instances.MongodbInstance(instance_document=mongodb_sharded_doc,
                                     instances=client.instances)


######################
# Patches and mocks. #
######################
@pytest.fixture
def mocked_response(request):
    """Mock a request's response object."""
    return mock.create_autospec(requests.Response)


@pytest.fixture
def patched_requests_map(request):
    """Return a dict of ``MagicMock``s which patch the requests library in various places.

    .. deprecated:: 0.4.0
        Let's go ahead and kill this as we go, and favor the `responses` lib, as it is way better.

    :returns: A dict where each key is the name of a module, and its value is the ``MagicMock``
        which is patching the requests library in its respective module.
    """
    patches = {}

    mocked = mock.patch('objectrocket.instances.requests', autospec=True)
    request.addfinalizer(mocked.stop)
    patches['instances'] = mocked.start()

    mocked = mock.patch('objectrocket.instances.mongodb.requests', autospec=True)
    request.addfinalizer(mocked.stop)
    patches['instances.mongodb'] = mocked.start()

    return patches


@pytest.fixture
def mock_shard_stats():
    """Mock shard stats."""
    return SHARD_STATS_THIS_SECOND


@pytest.fixture
def mock_instance_stats_this_second():
    """Mock shard stats."""
    return INSTANCE_STATS_THIS_SECOND


@pytest.fixture
def mock_instance_stats_next_second():
    """Mock shard stats."""
    return INSTANCE_STATS_NEXT_SECOND


@pytest.fixture
def mock_new_relic_stats():
    """Mock shard stats."""
    return NEW_RELIC_STATS

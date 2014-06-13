"""Tests for the objectrocket.instances module."""
import json
import pytest
import mock

from tests import conftest
from objectrocket import errors
from objectrocket.client import Client
from objectrocket.instances import Instance


class TestInstances(conftest.BaseClientTest):
    """Tests for the objectrocket.instances.Instances operations layer."""

    @pytest.fixture
    def requestsm(self, request):
        """Return a MagicMock which patches objectrocket.instances.requests."""
        mocked = mock.patch('objectrocket.instances.requests', autospec=True)
        request.addfinalizer(mocked.stop)
        return mocked.start()

    @pytest.fixture
    def create_call_data(self):
        """Return a dict having default data for calling Instnaces.create."""
        data = {
            'name': 'instance0',
            'size': 5,
            'zone': 'US-West',
            'service_type': 'mongodb',
            'version': '2.4.6',
        }
        return data

    def test_instances_client(self):
        assert isinstance(self.client.instances._client, Client)

    def test_instances_api_instnaces_url(self):
        assert self.client.instances._api_instances_url == self.client.api_url + 'instance/'

    # ----------------
    # GET METHOD TESTS
    # ----------------
    def test_get_calls_proper_endpoint_with_no_args(self, requestsm):
        requestsm.get.return_value = self._response_object()
        self.client.instances.get()

        expected_endpoint = self.client.api_url + 'instance/'
        requestsm.get.assert_called_once_with(expected_endpoint,
                                              auth=(self.client.user_key, self.client.pass_key))

    def test_get_calls_proper_endpoint_with_args(self, requestsm):
        requestsm.get.return_value = self._response_object()
        self.client.instances.get('instance0')

        expected_endpoint = self.client.api_url + 'instance/instance0/'
        requestsm.get.assert_called_once_with(expected_endpoint,
                                              auth=(self.client.user_key, self.client.pass_key))

    # -------------------
    # CREATE METHOD TESTS
    # -------------------
    def test_create_calls_proper_end_point(self, requestsm, create_call_data):
        requestsm.post.return_value = self._response_object()
        self.client.instances.create(**create_call_data)
        create_call_data.pop('service_type')

        expected_endpoint = self.client.api_url + 'instance/'
        requestsm.post.assert_called_once_with(expected_endpoint,
                                               auth=(self.client.user_key, self.client.pass_key),
                                               data=json.dumps(create_call_data),
                                               headers={'Content-Type': 'application/json'})

    def test_create_fails_with_bad_service_type_value(self, requestsm, create_call_data):
        create_call_data['service_type'] = 'not_a_valid_service'
        with pytest.raises(errors.InstancesException) as exinfo:
            self.client.instances.create(**create_call_data)

        assert exinfo.value.args[0] == ('Invalid value for "service_type". '
                                        'Must be one of "mongodb".')

    def test_create_fails_with_bad_version_value(self, requestsm, create_call_data):
        create_call_data['version'] = 'not_a_valid_version'
        with pytest.raises(errors.InstancesException) as exinfo:
            self.client.instances.create(**create_call_data)

        assert exinfo.value.args[0] == ('Invalid value for "version". '
                                        'Must be one of "2.4.6".')

    # ----------------
    # COMPACTION TESTS
    # ----------------
    def test_compaction_calls_proper_end_point_request_compaction_false(self, requestsm):
        requestsm.get.return_value = self._response_object()
        instance_name = 'instance0'
        self.client.instances.compaction(instance_name=instance_name, request_compaction=False)

        expected_endpoint = self.client.api_url + 'instance/' + instance_name + '/compaction/'
        requestsm.get.assert_called_once_with(expected_endpoint,
                                              auth=(self.client.user_key, self.client.pass_key))

    def test_compaction_calls_proper_end_point_request_compaction_true(self, requestsm):
        requestsm.post.return_value = self._response_object()
        instance_name = 'instance0'
        self.client.instances.compaction(instance_name=instance_name, request_compaction=True)

        expected_endpoint = self.client.api_url + 'instance/' + instance_name + '/compaction/'
        requestsm.post.assert_called_once_with(expected_endpoint,
                                               auth=(self.client.user_key, self.client.pass_key))

    # ------------
    # SHARDS TESTS
    # ------------
    def test_shards_calls_proper_end_point_without_add_shard(self, requestsm):
        requestsm.get.return_value = self._response_object()
        instance_name = 'instance0'
        self.client.instances.shards(instance_name=instance_name, add_shard=False)

        expected_endpoint = self.client.api_url + 'instance/' + instance_name + '/shard/'
        requestsm.get.assert_called_once_with(expected_endpoint,
                                              auth=(self.client.user_key, self.client.pass_key))

    def test_shards_calls_proper_end_point_with_add_shard(self, requestsm):
        requestsm.post.return_value = self._response_object()
        instance_name = 'instance0'
        self.client.instances.shards(instance_name=instance_name, add_shard=True)

        expected_endpoint = self.client.api_url + 'instance/' + instance_name + '/shard/'
        requestsm.post.assert_called_once_with(expected_endpoint,
                                               auth=(self.client.user_key, self.client.pass_key))

    # ------------------------
    # CONVENIENCE METHOD TESTS
    # ------------------------
    def test_instance_compaction_convenience_call_request_compaction_true(self, requestsm,
                                                                          mongo_sharded_instance):
        requestsm.get.return_value = self._response_object()
        mongo_sharded_instance.compaction()

        expected_endpoint = (self.client.api_url + 'instance/' +
                             mongo_sharded_instance.name + '/compaction/')
        requestsm.get.assert_called_once_with(expected_endpoint,
                                              auth=(self.client.user_key, self.client.pass_key))

    def test_instance_compaction_convenience_call_request_compaction_false(self, requestsm,
                                                                           mongo_sharded_instance):
        requestsm.post.return_value = self._response_object()
        mongo_sharded_instance.compaction(request_compaction=True)

        expected_endpoint = (self.client.api_url + 'instance/' +
                             mongo_sharded_instance.name + '/compaction/')
        requestsm.post.assert_called_once_with(expected_endpoint,
                                               auth=(self.client.user_key, self.client.pass_key))

    def test_instance_shards_calls_proper_end_point_without_add_shard(self, requestsm,
                                                                      mongo_sharded_instance):
        requestsm.get.return_value = self._response_object()
        mongo_sharded_instance.shards(add_shard=False)

        expected_endpoint = (self.client.api_url + 'instance/' +
                             mongo_sharded_instance.name + '/shard/')
        requestsm.get.assert_called_once_with(expected_endpoint,
                                              auth=(self.client.user_key, self.client.pass_key))

    def test_instance_shards_calls_proper_end_point_with_add_shard(self, requestsm,
                                                                   mongo_sharded_instance):
        requestsm.post.return_value = self._response_object()
        mongo_sharded_instance.shards(add_shard=True)

        expected_endpoint = (self.client.api_url + 'instance/' +
                             mongo_sharded_instance.name + '/shard/')
        requestsm.post.assert_called_once_with(expected_endpoint,
                                               auth=(self.client.user_key, self.client.pass_key))


class TestInstance(conftest.BaseInstanceTest):
    """Tests for objectrocket.instances.Instance objects with mongodb_sharded input."""

    def _pop_needed_key_and_assert(self, doc, needed_key):
        """Pop needed_key from doc and assert KeyError during constructor run."""
        doc.pop(needed_key)
        with pytest.raises(KeyError) as exinfo:
            Instance(instance_document=doc, client=Client('test_user_key', 'test_pass_key'))

        assert exinfo.value.__class__ == KeyError
        assert exinfo.value.args[0] == needed_key

    # -----------------
    # CONSTRUCTOR TESTS
    # -----------------
    def test_constructor_passes_with_expected_document(self, _docs):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        inst = Instance(instance_document=_docs,
                        client=Client(user_key=user_key, pass_key=pass_key))
        assert isinstance(inst, Instance)

    def test_constructor_fails_with_missing_api_endpoint(self, _docs):
        self._pop_needed_key_and_assert(_docs, 'api_endpoint')

    def test_constructor_fails_with_missing_connect_string(self, _docs):
        self._pop_needed_key_and_assert(_docs, 'connect_string')

    def test_constructor_fails_with_missing_created(self, _docs):
        self._pop_needed_key_and_assert(_docs, 'created')

    def test_constructor_fails_with_missing_name(self, _docs):
        self._pop_needed_key_and_assert(_docs, 'name')

    def test_constructor_fails_with_missing_plan(self, _docs):
        self._pop_needed_key_and_assert(_docs, 'plan')

    def test_constructor_passes_without_ssl_connect_string(self, _docs):
        _docs.pop('ssl_connect_string', None)
        inst = Instance(instance_document=_docs, client=Client('test_user_key', 'test_pass_key'))
        assert isinstance(inst, Instance)

    def test_constructor_fails_with_missing_service(self, _docs):
        self._pop_needed_key_and_assert(_docs, 'service')

    def test_constructor_fails_with_missing_type(self, _docs):
        self._pop_needed_key_and_assert(_docs, 'type')

    def test_constructor_fails_with_missing_version(self, _docs):
        self._pop_needed_key_and_assert(_docs, 'version')

    # -----------------------
    # INSTANCE PROPERTY TESTS
    # -----------------------
    def test_api_endpoint_property(self, _instances_and_docs):
        instance, doc = _instances_and_docs[0], _instances_and_docs[1]
        assert instance.api_endpoint == doc['api_endpoint']

    def test_client_property_with_valid_client(self, _instances_and_docs):
        instance = _instances_and_docs[0]
        assert isinstance(instance.client, Client)

    def test_mongo_sharded_connection_property(self, mongo_sharded_instance, mongo_sharded_doc):
        with mock.patch('pymongo.MongoClient', return_value=None) as client:
            mongo_sharded_instance.connection

        host, port = mongo_sharded_doc['connect_string'].split(':')
        port = int(port)
        client.assert_called_once_with(host=host, port=port)

    def test_mongo_replica_connection_property(self, mongo_replica_instance, mongo_replica_doc):
        with mock.patch('pymongo.MongoReplicaSetClient', return_value=None) as client:
            mongo_replica_instance.connection

        replica_set_name, member_list = mongo_replica_doc['connect_string'].split('/')
        member_list = member_list.strip().strip(',')
        client.assert_called_once_with(hosts_or_uri=member_list)

    def test_connect_string_property(self, _instances_and_docs):
        instance, doc = _instances_and_docs[0], _instances_and_docs[1]
        assert instance.connect_string == doc['connect_string']

    def test_created_property(self, _instances_and_docs):
        instance, doc = _instances_and_docs[0], _instances_and_docs[1]
        assert instance.created == doc['created']

    def test_name_property(self, _instances_and_docs):
        instance, doc = _instances_and_docs[0], _instances_and_docs[1]
        assert instance.name == doc['name']

    def test_plan_property(self, _instances_and_docs):
        instance, doc = _instances_and_docs[0], _instances_and_docs[1]
        assert instance.plan == doc['plan']

    def test_service_property(self, _instances_and_docs):
        instance, doc = _instances_and_docs[0], _instances_and_docs[1]
        assert instance.service == doc['service']

    def test_ssl_connect_string_property(self, _instances_and_docs):
        instance, doc = _instances_and_docs[0], _instances_and_docs[1]
        assert instance.ssl_connect_string == doc.get('ssl_connect_string')

    def test_type_property(self, _instances_and_docs):
        instance, doc = _instances_and_docs[0], _instances_and_docs[1]
        assert instance.type == doc['type']

    def test_version_property(self, _instances_and_docs):
        instance, doc = _instances_and_docs[0], _instances_and_docs[1]
        assert instance.version == doc['version']

    # ---------------------
    # INSTANCE METHOD TESTS
    # ---------------------
    def test_to_dict_method(self, _instances_and_docs):
        instance, doc = _instances_and_docs[0], _instances_and_docs[1]
        assert instance.to_dict() == doc

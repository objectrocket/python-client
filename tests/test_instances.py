"""Tests for the objectrocket.instances module."""
import pytest
import mock

from tests import conftest
from objectrocket.instances import Instances, Instance


# TODO(Anthony): Write tests for this guy.
class TestInstances(conftest.BaseClientTest):
    pass


class TestInstance(conftest.BaseInstanceTest):
    """Tests for objectrocket.instances.Instance objects with mongodb_sharded input."""

    def _pop_needed_key_and_assert(self, doc, needed_key):
        """Pop needed_key from doc and assert KeyError during constructor run."""
        doc.pop(needed_key)
        with pytest.raises(KeyError) as exinfo:
            Instance(instance_document=doc)

        assert exinfo.value.__class__ == KeyError
        assert exinfo.value.args[0] == needed_key

    # -----------------
    # CONSTRUCTOR TESTS
    # -----------------
    def test_constructor_passes_with_expected_document(self, _docs):
        inst = Instance(instance_document=_docs)
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
        inst = Instance(instance_document=_docs)
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

"""Tests for the objectrocket.instances module."""
import pytest

from tests import conftest
from objectrocket.instances import Instances, Instance


class TestInstances(conftest.BaseClientTest):
    pass


class TestInstance(object):
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
    def test_constructor_passes_with_expected_document(self, mongo_sharded_doc):
        inst = Instance(instance_document=mongo_sharded_doc)
        assert isinstance(inst, Instance)

    def test_constructor_fails_with_missing_api_endpoint(self, mongo_sharded_doc):
        self._pop_needed_key_and_assert(mongo_sharded_doc, 'api_endpoint')

    def test_constructor_fails_with_missing_connect_string(self, mongo_sharded_doc):
        self._pop_needed_key_and_assert(mongo_sharded_doc, 'connect_string')

    def test_constructor_fails_with_missing_created(self, mongo_sharded_doc):
        self._pop_needed_key_and_assert(mongo_sharded_doc, 'created')

    def test_constructor_fails_with_missing_name(self, mongo_sharded_doc):
        self._pop_needed_key_and_assert(mongo_sharded_doc, 'name')

    def test_constructor_fails_with_missing_plan(self, mongo_sharded_doc):
        self._pop_needed_key_and_assert(mongo_sharded_doc, 'plan')

    def test_constructor_passes_without_ssl_connect_string(self, mongo_sharded_doc):
        mongo_sharded_doc.pop('ssl_connect_string')
        inst = Instance(instance_document=mongo_sharded_doc)
        assert isinstance(inst, Instance)

    def test_constructor_fails_with_missing_service(self, mongo_sharded_doc):
        self._pop_needed_key_and_assert(mongo_sharded_doc, 'service')

    def test_constructor_fails_with_missing_type(self, mongo_sharded_doc):
        self._pop_needed_key_and_assert(mongo_sharded_doc, 'type')

    def test_constructor_fails_with_missing_version(self, mongo_sharded_doc):
        self._pop_needed_key_and_assert(mongo_sharded_doc, 'version')

    # -----------------------
    # INSTANCE PROPERTY TESTS
    # -----------------------
    def test_api_endpoint_property(self, mongo_sharded_instance, mongo_sharded_doc):
        assert mongo_sharded_instance.api_endpoint == mongo_sharded_doc['api_endpoint']

    def test_connection_property(self, mongo_sharded_instance, mongo_sharded_doc):
        assert mongo_sharded_instance.api_endpoint == mongo_sharded_doc['api_endpoint']

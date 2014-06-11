"""Tests for the objectrocket.instances module."""
import pytest

from tests import conftest
from objectrocket.instances import Instances, Instance


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
    # def test_api_endpoint_property(self, instance, doc):
    #     assert instance.api_endpoint == doc['api_endpoint']

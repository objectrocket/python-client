"""Tests for the objectrocket.instances module."""
import pytest

from tests import conftest
from objectrocket.instances import Instances, Instance


class TestInstances(conftest.BaseClientTest):
    pass


class TestInstance(object):
    """Tests for objectrocket.instances.Instance objects."""

    def _pop_needed_key_and_assert(self, doc, needed_key):
        """Pop needed_key from doc and assert KeyError during constructor run."""
        doc.pop(needed_key)
        with pytest.raises(KeyError) as exinfo:
            Instance(instance_document=doc)

        assert exinfo.value.__class__ == KeyError
        assert exinfo.value.args[0] == needed_key

    # ---------------
    # __init__ tests.
    # ---------------
    def test_constructor_passes_with_expected_document(self, instance_document):
        inst = Instance(instance_document=instance_document)
        assert isinstance(inst, Instance)

    def test_constructor_fails_with_missing_api_endpoint(self, instance_document):
        self._pop_needed_key_and_assert(instance_document, 'api_endpoint')

    def test_constructor_fails_with_missing_connect_string(self, instance_document):
        self._pop_needed_key_and_assert(instance_document, 'connect_string')

    def test_constructor_fails_with_missing_created(self, instance_document):
        self._pop_needed_key_and_assert(instance_document, 'created')

    def test_constructor_fails_with_missing_name(self, instance_document):
        self._pop_needed_key_and_assert(instance_document, 'name')

    def test_constructor_fails_with_missing_plan(self, instance_document):
        self._pop_needed_key_and_assert(instance_document, 'plan')

    def test_constructor_passes_without_ssl_connect_string(self, instance_document):
        instance_document.pop('ssl_connect_string')
        inst = Instance(instance_document=instance_document)
        assert isinstance(inst, Instance)

    def test_constructor_fails_with_missing_service(self, instance_document):
        self._pop_needed_key_and_assert(instance_document, 'service')

    def test_constructor_fails_with_missing_type(self, instance_document):
        self._pop_needed_key_and_assert(instance_document, 'type')

    def test_constructor_fails_with_missing_version(self, instance_document):
        self._pop_needed_key_and_assert(instance_document, 'version')

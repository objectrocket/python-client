"""Tests for the objectrocket.instances module."""
from objectrocket.instances.mongodb import MongodbInstance


##########################################
# Tests for Instances private interface. #
##########################################
def test_concrete_instance_returns_none_if_dict_not_given(client):
    output = client.instances._concrete_instance([])
    assert output is None


def test_concrete_instance_returns_none_if_doc_is_missing_needed_field(client, mongodb_sharded_doc):
    mongodb_sharded_doc.pop('name')  # Will cause a constructor error.
    output = client.instances._concrete_instance(mongodb_sharded_doc)
    assert output is None


def test_concrete_instance_returns_expected_instance_object(client, mongodb_sharded_doc):
    output = client.instances._concrete_instance(mongodb_sharded_doc)
    assert isinstance(output, MongodbInstance)
    assert output._instance_document is mongodb_sharded_doc


def test_concrete_instance_list_returns_empty_list_if_empty_list_provided(client):
    output = client.instances._concrete_instance_list([])
    assert output == []


def test_concrete_instance_list_returns_empty_list_if_constructor_error_for_doc(client, mongodb_sharded_doc):
    mongodb_sharded_doc.pop('name')  # Will cause a constructor error.
    output = client.instances._concrete_instance_list([mongodb_sharded_doc])
    assert output == []


def test_concrete_instance_list_returns_expected_list(client, mongodb_sharded_doc):
    output = client.instances._concrete_instance_list([mongodb_sharded_doc])
    assert isinstance(output, list)
    assert len(output) == 1
    assert output[0]._instance_document is mongodb_sharded_doc

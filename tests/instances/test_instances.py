"""Tests for the objectrocket.instances module."""
import responses

from objectrocket.instances.mongodb import MongodbInstance
from objectrocket.acls import Acl


##########################################
# Tests for Instances private interface. #
##########################################
def test_concrete_instance_returns_none_if_dict_not_given(client):
    output = client.instances._concrete_instance([])
    assert output is None


def test_concrete_instance_returns_none_if_doc_is_missing_needed_field(
        client,
        mongodb_sharded_doc):
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


def test_concrete_instance_list_returns_empty_list_if_constructor_error_for_doc(
        client,
        mongodb_sharded_doc):
    mongodb_sharded_doc.pop('name')  # Will cause a constructor error.
    output = client.instances._concrete_instance_list([mongodb_sharded_doc])
    assert output == []


def test_concrete_instance_list_returns_expected_list(client, mongodb_sharded_doc):
    output = client.instances._concrete_instance_list([mongodb_sharded_doc])
    assert isinstance(output, list)
    assert len(output) == 1
    assert output[0]._instance_document is mongodb_sharded_doc


#######################################
# Tests for Instances ACLs interface. #
#######################################
@responses.activate
def test_instance_acls_all_makes_expected_call(mongodb_sharded_instance):
    inst = mongodb_sharded_instance
    expected_url = 'http://localhost:5050/v2/instances/{}/acls/'.format(inst.name)
    responses.add(
        responses.GET,
        expected_url,
        status=200,
        json={'data': []},
        content_type="application/json",
    )

    output = inst.acls.all()

    assert output == []


@responses.activate
def test_instance_acls_all_returns_expected_acl_object(mongodb_sharded_instance, acl):
    inst = mongodb_sharded_instance
    expected_url = 'http://localhost:5050/v2/instances/{}/acls/'.format(inst.name)
    responses.add(
        responses.GET,
        expected_url,
        status=200,
        json={'data': [acl._document]},
        content_type="application/json",
    )

    output = inst.acls.all()

    assert isinstance(output[0], Acl)
    assert output[0].id == acl.id


@responses.activate
def test_instance_acls_create_makes_expected_call(mongodb_sharded_instance, acl):
    inst = mongodb_sharded_instance
    expected_url = 'http://localhost:5050/v2/instances/{}/acls/'.format(inst.name)
    responses.add(
        responses.POST,
        expected_url,
        status=200,
        json={'data': acl._document},
        content_type="application/json",
    )

    output = inst.acls.create(cidr_mask=acl.cidr_mask, description=acl.description)

    assert isinstance(output, Acl)
    assert output.id == acl.id

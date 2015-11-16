"""Tests for the objectrocket.acls module."""
import responses

from objectrocket.acls import Acl


####################################
# Tests for Acls public interface. #
####################################
# Tests for all. #
@responses.activate
def test_all_makes_expected_api_request(client):
    instance_name = 'test_instance'
    expected_url = 'http://localhost:5050/v2/instances/{}/acls/'.format(instance_name)
    responses.add(
        responses.GET,
        expected_url,
        status=200,
        json={'data': []},
        content_type="application/json",
    )

    output = client.acls.all(instance_name)

    assert output == []


@responses.activate
def test_all_concretizes_returned_acl_doc(client, acl_doc):
    instance_name = 'test_instance'
    expected_acl_object = Acl(acl_doc, client.acls)
    expected_url = 'http://localhost:5050/v2/instances/{}/acls/'.format(instance_name)
    responses.add(
        responses.GET,
        expected_url,
        status=200,
        json={'data': [acl_doc]},
        content_type="application/json",
    )

    output = client.acls.all(instance_name)

    assert len(output) == 1
    assert output[0].id == expected_acl_object.id
    assert isinstance(output[0], Acl)


# Tests for create. #
@responses.activate
def test_create_makes_expected_api_request(client, acl_doc):
    cidr_mask = '0.0.0.0/1'
    description = 'testing'
    instance_name = 'test_instance'
    expected_acl_object = Acl(acl_doc, client.acls)
    expected_url = 'http://localhost:5050/v2/instances/{}/acls/'.format(instance_name)
    responses.add(
        responses.POST,
        expected_url,
        status=200,
        json={'data': acl_doc},
        content_type="application/json",
    )

    output = client.acls.create(instance_name, cidr_mask, description)

    assert output.id == expected_acl_object.id
    assert isinstance(output, Acl)


# Tests for get. #
@responses.activate
def test_get_makes_expected_api_request(client, acl_doc):
    instance_name = 'test_instance'
    expected_acl_object = Acl(acl_doc, client.acls)
    expected_url = 'http://localhost:5050/v2/instances/{}/acls/{}/'.format(
        instance_name,
        expected_acl_object.id
    )
    responses.add(
        responses.GET,
        expected_url,
        status=200,
        json={'data': acl_doc},
        content_type="application/json",
    )

    output = client.acls.get(instance_name, expected_acl_object.id)

    assert output.id == expected_acl_object.id
    assert isinstance(output, Acl)


#####################################
# Tests for Acls private interface. #
#####################################
# Tests for _concrete_acl. #
def test_concrete_acl_returns_none_if_dict_not_given(client):
    output = client.acls._concrete_acl([])
    assert output is None


def test_concrete_acl_returns_none_if_doc_is_missing_needed_field(acl_doc, client):
    acl_doc.pop('cidr_mask')  # Will cause a constructor error.
    output = client.acls._concrete_acl(acl_doc)
    assert output is None


def test_concrete_acl_returns_expected_acl_object(acl_doc, client):
    output = client.acls._concrete_acl(acl_doc)
    assert isinstance(output, Acl)
    assert output._document is acl_doc


# Tests for _concrete_acl_list. #
def test_concrete_acl_list_returns_empty_list_if_empty_list_provided(client):
    output = client.acls._concrete_acl_list([])
    assert output == []


def test_concrete_acl_list_returns_empty_list_if_constructor_error_for_doc(acl_doc, client):
    acl_doc.pop('cidr_mask')  # Will cause a constructor error.
    output = client.acls._concrete_acl_list([acl_doc])
    assert output == []


def test_concrete_acl_list_returns_expected_list(acl_doc, client):
    output = client.acls._concrete_acl_list([acl_doc])
    assert isinstance(output, list)
    assert len(output) == 1
    assert output[0]._document is acl_doc

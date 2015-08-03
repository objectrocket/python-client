"""Tests for the objectrocket.acls module."""
from objectrocket.acls import Acl


####################################
# Tests for Acls public interface. #
####################################
# def test_authenticate_makes_expected_request(client, mocked_response, patched_requests_map):
#     username, password, return_token = 'tester', 'testpass', 'return_token'
#     patched_requests_map['auth'].get.return_value = mocked_response
#     mocked_response.json.return_value = {'data': {'token': return_token}}

#     output = client.auth.authenticate(username, password)

#     assert output == return_token
#     patched_requests_map['auth'].get.assert_called_with(
#         client.auth._url,
#         auth=(username, password),
#         **client.auth._default_request_kwargs
#     )


# def test_authenticate_binds_given_credentials(client, mocked_response, patched_requests_map):
#     username, password, return_token = 'tester', 'testpass', 'return_token'
#     patched_requests_map['auth'].get.return_value = mocked_response
#     mocked_response.json.return_value = {'data': {'token': return_token}}
#     orig_username, orig_password = client.auth._username, client.auth._password

#     client.auth.authenticate(username, password)

#     assert orig_username is None
#     assert orig_password is None
#     assert client.auth._username == username
#     assert client.auth._password == password


# def test_authenticate_binds_auth_token_properly(client, mocked_response, patched_requests_map):
#     username, password, return_token = 'tester', 'testpass', 'return_token'
#     patched_requests_map['auth'].get.return_value = mocked_response
#     mocked_response.json.return_value = {'data': {'token': return_token}}
#     orig_token = client.auth._token

#     client.auth.authenticate(username, password)

#     assert orig_token is None
#     assert client.auth._token == return_token


# def test_authenticate_raises_when_no_data_returned(client, mocked_response, patched_requests_map):
#     username, password = 'tester', 'testpass'
#     auth = Auth(base_client=client)
#     patched_requests_map['auth'].get.return_value = mocked_response
#     mocked_response.json.return_value = {}

#     with pytest.raises(errors.AuthFailure) as exinfo:
#         auth.authenticate(username, password)

#     assert exinfo.value.args == ("KeyError: 'data'",)


# def test_authenticate_raises_when_no_token_returned(client, mocked_response, patched_requests_map):
#     username, password = 'tester', 'testpass'
#     auth = Auth(base_client=client)
#     patched_requests_map['auth'].get.return_value = mocked_response
#     mocked_response.json.return_value = {'data': {}}

#     with pytest.raises(errors.AuthFailure) as exinfo:
#         auth.authenticate(username, password)

#     assert exinfo.value.args == ("KeyError: 'token'",)


#####################################
# Tests for Acls private interface. #
#####################################
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

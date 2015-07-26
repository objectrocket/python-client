"""Tests for the objectrocket.auth module."""
import mock
import pytest

from objectrocket import errors
from objectrocket.auth import Auth


####################################
# Tests for Auth public interface. #
####################################
def test_authenticate_makes_expected_request(client, mocked_response, patched_requests_map):
    username, password, return_token = 'tester', 'testpass', 'return_token'
    patched_requests_map['auth'].get.return_value = mocked_response
    mocked_response.json.return_value = {'data': {'token': return_token}}

    output = client.auth.authenticate(username, password)

    assert output == return_token
    patched_requests_map['auth'].get.assert_called_with(
        client.auth._url,
        auth=(username, password),
        **client.auth._default_request_kwargs
    )


def test_authenticate_binds_given_credentials(client, mocked_response, patched_requests_map):
    username, password, return_token = 'tester', 'testpass', 'return_token'
    patched_requests_map['auth'].get.return_value = mocked_response
    mocked_response.json.return_value = {'data': {'token': return_token}}
    orig_username, orig_password = client.auth._username, client.auth._password

    client.auth.authenticate(username, password)

    assert orig_username is None
    assert orig_password is None
    assert client.auth._username == username
    assert client.auth._password == password


def test_authenticate_binds_auth_token_properly(client, mocked_response, patched_requests_map):
    username, password, return_token = 'tester', 'testpass', 'return_token'
    patched_requests_map['auth'].get.return_value = mocked_response
    mocked_response.json.return_value = {'data': {'token': return_token}}
    orig_token = client.auth._token

    client.auth.authenticate(username, password)

    assert orig_token is None
    assert client.auth._token == return_token


def test_authenticate_raises_when_no_data_returned(client, mocked_response, patched_requests_map):
    username, password = 'tester', 'testpass'
    auth = Auth(base_client=client)
    patched_requests_map['auth'].get.return_value = mocked_response
    mocked_response.json.return_value = {}

    with pytest.raises(errors.AuthFailure) as exinfo:
        auth.authenticate(username, password)

    assert exinfo.value.args == ("KeyError: 'data'",)


def test_authenticate_raises_when_no_token_returned(client, mocked_response, patched_requests_map):
    username, password = 'tester', 'testpass'
    auth = Auth(base_client=client)
    patched_requests_map['auth'].get.return_value = mocked_response
    mocked_response.json.return_value = {'data': {}}

    with pytest.raises(errors.AuthFailure) as exinfo:
        auth.authenticate(username, password)

    assert exinfo.value.args == ("KeyError: 'token'",)


#####################################
# Tests for Auth private interface. #
#####################################
def test_default_request_kwargs_match_base(client):
    auth = Auth(base_client=client)
    auth_kwargs = auth._default_request_kwargs
    base_kwargs = super(Auth, auth)._default_request_kwargs
    assert auth_kwargs == base_kwargs


def test_auth_url_points_to_expected_endpoint(client):
    auth = Auth(base_client=client)
    assert auth._url == client._url + 'tokens/'


def test_auth_password_setter(client):
    orig_val = client.auth._password
    testval = 'testing-password'
    client.auth._password = testval
    assert client.auth._password is testval
    assert orig_val is not testval


def test_auth_refresh_simply_invokes_authenticate_with_current_creds(client, mocked_response, patched_requests_map):
    # Assemble.
    username, password, return_token = 'tester', 'testpass', 'return_token'
    patched_requests_map['auth'].get.return_value = mocked_response
    mocked_response.json.return_value = {'data': {'token': return_token}}

    auth_output = client.auth.authenticate(username, password)
    bound_username, bound_password = client.auth._username, client.auth._password

    # Action.
    with mock.patch.object(client.auth, 'authenticate', return_value=return_token) as patched_auth:
        refresh_output = client.auth._refresh()

    # Assert.
    assert auth_output is refresh_output
    patched_auth.assert_called_once_with(bound_username, bound_password)


def test_auth_token_setter(client):
    orig_val = client.auth._token
    testval = 'testing-token'
    client.auth._token = testval
    assert client.auth._token is testval
    assert orig_val is not testval


def test_auth_username_setter(client):
    orig_val = client.auth._username
    testval = 'testing-username'
    client.auth._username = testval
    assert client.auth._username is testval
    assert orig_val is not testval

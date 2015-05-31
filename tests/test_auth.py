"""Tests for the objectrocket.auth module."""
import pytest

from objectrocket import errors
from objectrocket.auth import Auth


####################################
# Tests for Auth public interface. #
####################################
def test_authenticate_makes_expected_request(client, mocked_response, patched_requests_map):
    username, password, return_token = 'tester', 'testpass', 'return_token'
    auth = Auth(base_client=client)
    patched_requests_map['auth'].get.return_value = mocked_response
    mocked_response.json.return_value = {'data': {'token': return_token}}

    output = auth.authenticate(username, password)

    assert output == return_token
    patched_requests_map['auth'].get.assert_called_with(
        client.auth._url,
        auth=(username, password),
        **auth._default_request_kwargs
    )


def test_authenticate_raises_when_no_data_returned(client, mocked_response, patched_requests_map):
    username, password = 'tester', 'testpass'
    auth = Auth(base_client=client)
    patched_requests_map['auth'].get.return_value = mocked_response
    mocked_response.json.return_value = {}

    with pytest.raises(errors.AuthFailure) as exinfo:
        auth.authenticate(username, password)

    assert isinstance(exinfo.value.args[0], KeyError)
    assert exinfo.value.args[0].args == ('data',)


def test_authenticate_raises_when_no_token_returned(client, mocked_response, patched_requests_map):
    username, password = 'tester', 'testpass'
    auth = Auth(base_client=client)
    patched_requests_map['auth'].get.return_value = mocked_response
    mocked_response.json.return_value = {'data': {}}

    with pytest.raises(errors.AuthFailure) as exinfo:
        auth.authenticate(username, password)

    assert isinstance(exinfo.value.args[0], KeyError)
    assert exinfo.value.args[0].args == ('token',)


#####################################
# Tests for Auth private interface. #
#####################################
def test_default_request_kwargs_match_base_operations(client):
    auth = Auth(base_client=client)
    auth_kwargs = auth._default_request_kwargs
    base_kwargs = super(Auth, auth)._default_request_kwargs
    assert auth_kwargs == base_kwargs


def test_auth_url_points_to_expected_endpoint(client):
    auth = Auth(base_client=client)
    assert auth._url == client._url + 'tokens/'

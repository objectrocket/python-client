"""Tests for the objectrocket.auth module."""
import base64
import json
import mock
import pytest
import responses

from objectrocket import errors
from objectrocket.auth import Auth
from objectrocket.client import Client


@pytest.fixture
def auth_url(mongodb_sharded_instance):
    return "https://sjc-api.objectrocket.com/v2/tokens/"


@pytest.yield_fixture(autouse=True)
def ensure_auth_production_url(auth_url):
    """Fixture that ensures that the proper production URLs are used in tests,
    instead of the potentially overridden ones from environment variables.

    See objectrocket.constants.OR_DEFAULT_API_URL
    """
    with mock.patch.object(Auth, '_url', new_callable=mock.PropertyMock) as mock_auth_url:
        type(mock_auth_url).return_value = auth_url
        with mock.patch.object(Client, '_url', new_callable=mock.PropertyMock) as mock_client_url:
            type(mock_client_url).return_value = auth_url.replace('tokens/', '')
            yield


@pytest.fixture()
def base64_basic_auth_header():
    """Just returns a properly formatted basic author header for testing"""
    user_passwd = '{}:{}'.format('tester', 'testpass').encode()
    b64string = base64.encodestring(user_passwd).decode().replace('\n', '')
    return 'Basic {}'.format(b64string)


####################################
# Tests for Auth public interface. #
####################################
@responses.activate
def test_authenticate_makes_expected_request(client, mocked_response, auth_url,
                                             base64_basic_auth_header):
    username, password, return_token = 'tester', 'testpass', 'return_token'
    responses.add(responses.GET, auth_url, status=200,
                  body=json.dumps({'data': {'token': return_token}}),
                  content_type="application/json")

    output = client.auth.authenticate(username, password)

    assert output == return_token

    assert responses.calls[0].request.headers.get('Authorization') == base64_basic_auth_header
    assert responses.calls[0].request.headers.get('Content-Type') == 'application/json'


@responses.activate
def test_authenticate_binds_given_credentials(client, mocked_response, auth_url):
    username, password, return_token = 'tester', 'testpass', 'return_token'
    responses.add(responses.GET, auth_url, status=200,
                  body=json.dumps({'data': {'token': return_token}}),
                  content_type="application/json")
    orig_username, orig_password = client.auth._username, client.auth._password

    client.auth.authenticate(username, password)

    assert orig_username is None
    assert orig_password is None
    assert client.auth._username == username
    assert client.auth._password == password


@responses.activate
def test_authenticate_binds_auth_token_properly(client, mocked_response, auth_url):
    username, password, return_token = 'tester', 'testpass', 'return_token'
    responses.add(responses.GET, auth_url, status=200,
                  body=json.dumps({'data': {'token': return_token}}),
                  content_type="application/json")
    orig_token = client.auth._token

    client.auth.authenticate(username, password)

    assert orig_token is None
    assert client.auth._token == return_token


@responses.activate
def test_authenticate_raises_when_no_data_returned(client, mocked_response, auth_url):
    username, password = 'tester', 'testpass'
    auth = Auth(base_client=client)
    responses.add(responses.GET, auth_url, status=200,
                  body=json.dumps({}),
                  content_type="application/json")

    with pytest.raises(errors.AuthFailure) as exinfo:
        auth.authenticate(username, password)

    assert exinfo.value.args == ("KeyError: 'data'",)


@responses.activate
def test_authenticate_raises_when_no_token_returned(client, mocked_response, auth_url):
    username, password = 'tester', 'testpass'
    auth = Auth(base_client=client)
    responses.add(responses.GET, auth_url, status=200,
                  body=json.dumps({'data': {}}),
                  content_type="application/json")

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


@responses.activate
def test_auth_refresh_simply_invokes_authenticate_with_current_creds(client, mocked_response,
                                                                     auth_url):
    # Assemble.
    username, password, return_token = 'tester', 'testpass', 'return_token'
    responses.add(
        responses.GET, auth_url,
        status=200,
        body=json.dumps({'data': {'token': return_token}}),
        content_type="application/json"
    )

    auth_output = client.auth.authenticate(username, password)
    bound_username, bound_password = client.auth._username, client.auth._password

    # Action.
    with mock.patch.object(client.auth, 'authenticate', return_value=return_token) as patched_auth:
        refresh_output = client.auth._refresh()

    # Assert.
    assert auth_output == refresh_output
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

"""Tests for the objectrocket.client module."""
import pytest

from objectrocket import auth
from objectrocket import constants
from objectrocket import errors
from objectrocket import instances
from objectrocket.client import Client
from tests import conftest


class TestClient(conftest.AuthenticationHarness, conftest.GenericFixtures):
    """Tests for objectrocket.client.Client object."""

    def test_client_has_correct_default_url(self, auth_requests):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key)
        assert client.url == constants.DEFAULT_API_URL

    def test_client_assigns_alternative_url_properly(self, auth_requests):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key, alternative_url='testing')
        assert client.url == 'testing'

    def test_client_has_proper_user_and_pass_key_properties(self, auth_requests):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key)
        assert client.user_key == user_key
        assert client.pass_key == pass_key

    def test_client_binds_proper_value_for_is_using_tokens_when_true(self, auth_requests):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key, use_tokens=True)
        assert client.is_using_tokens is True

    def test_client_binds_proper_value_for_is_using_tokens_when_false(self, auth_requests):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key, use_tokens=False)
        assert client.is_using_tokens is False

    def test_client_makes_auth_request_upon_instantiation(self, auth_requests):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key, alternative_url='testing')
        auth_requests.get.assert_called_once_with(client.auth.url + 'token/',
                                                  auth=(user_key, pass_key),
                                                  hooks=dict(response=client._verify_auth))

    def test_client_binds_auth_token_properly(self, auth_requests, obj):
        user_key, pass_key = 'test_user_key', 'test_pass_key'

        obj.json = lambda: {'data': 'testing_token'}
        auth_requests.get.return_value = obj

        client = Client(user_key, pass_key)
        assert client.token == 'testing_token'

    def test_client_default_request_kwargs_with_tokens_enables(self, auth_requests):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key, use_tokens=True)
        assert client.default_request_kwargs == {
            'headers': {
                'Content-Type': 'application/json',
                'X-Auth-Token': client.token,
            },
            'hooks': {
                'response': client._verify_auth,
            },
        }

    def test_client_default_request_kwargs_with_tokens_disabled(self, auth_requests):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key, use_tokens=False)
        assert client.default_request_kwargs == {
            'auth': (client.user_key, client.pass_key),
            'headers': {
                'Content-Type': 'application/json',
            },
            'hooks': {
                'response': client._verify_auth,
            },
        }

    def test_client_verify_auth_hook_raises_with_code_401(self, auth_requests):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key)

        resp = type('response', (object,), {'status_code': 401})
        resp.request = type('request', (object,), {'method': 'GET', 'path_url': 'testing'})

        with pytest.raises(errors.AuthFailure) as exinfo:
            client._verify_auth(resp)

        assert len(exinfo.value.args) == 1
        assert exinfo.value.args[0] == ('Received response code 401 from {} {}. '
                                        'Keypair used: {}:{}'.format(resp.request.method,
                                                                     resp.request.path_url,
                                                                     user_key, pass_key))

    def test_client_verify_auth_hook_does_not_raise_with_code_200(self, auth_requests):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key)

        resp = type('response', (object,), {'status_code': 200})
        client._verify_auth(resp)

    #########################
    # TEST EMBEDDED CLASSES #
    #########################
    def test_client_has_embedded_auth_class(self, auth_requests):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key)
        assert isinstance(client.auth, auth.Auth)

    def test_client_has_embedded_instances_class(self, auth_requests):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key)
        assert isinstance(client.instances, instances.Instances)

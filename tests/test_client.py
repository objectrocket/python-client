"""Tests for the objectrocket.client module."""
from pytest import raises

from objectrocket.client import Client
from objectrocket.instances import Instances


class TestClient(object):
    """Tests for objectrocket.client.Client object."""

    def test_client_constructor_fails_with_bad_user_key(self):
        user_key_of_wrong_type = 123
        with raises(Client.ClientException) as exinfo:
            Client(user_key_of_wrong_type, 'test_pass_key')

        assert exinfo.value.args[0] == 'All parameters should be instances of str.'

    def test_client_constructor_fails_with_bad_pass_key(self):
        pass_key_of_wrong_type = 123
        with raises(Client.ClientException) as exinfo:
            Client('test_user_key', pass_key_of_wrong_type)

        assert exinfo.value.args[0] == 'All parameters should be instances of str.'

    def test_client_has_correct_default_api_url(self):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key)
        assert client.api_url == 'http://localhost:5050/v2/'

    def test_client_has_proper_user_and_pass_key_properties(self):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key)
        assert client.user_key == user_key
        assert client.pass_key == pass_key

    def test_client_has_embedded_instances_object(self):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key)
        assert isinstance(client.instances, Instances)

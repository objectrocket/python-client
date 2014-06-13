"""Tests for the objectrocket.client module."""
from objectrocket.client import Client
from objectrocket.instances import Instances


class TestClient(object):
    """Tests for objectrocket.client.Client object."""

    def test_client_has_correct_default_api_url(self):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key)
        assert client.api_url == 'http://localhost:5050/v2/'

    def test_client_has_correct_testing_api_url(self):
        user_key, pass_key = 'test_user_key', 'test_pass_key'
        client = Client(user_key, pass_key, api_url='testing')
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

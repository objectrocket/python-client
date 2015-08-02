"""Tests for the objectrocket.client module."""
import mock

from objectrocket import auth
from objectrocket import constants
from objectrocket import instances
from objectrocket.client import Client


#################################
# Tests for Client constructor. #
#################################
def test_client_binds_correct_default_url(patched_requests_map):
    client = Client()
    assert client._url == constants.OR_DEFAULT_API_URL


def test_client_binds_alternative_url_properly(patched_requests_map):
    client = Client(base_url='testURL')
    assert client._url == 'testURL'


######################################
# Tests for Client public interface. #
######################################
def test_client_auth_invokes_auth_authenticate(client):
    username, password = 'username', 'password'
    with mock.patch.object(client.auth, 'authenticate') as patched_auth:
        client.authenticate(username, password)

    patched_auth.assert_called_once_with(username, password)


def test_client_has_embedded_auth_class(client):
    assert isinstance(client.auth, auth.Auth)


def test_client_has_embedded_instances_class(client):
    assert isinstance(client.instances, instances.Instances)

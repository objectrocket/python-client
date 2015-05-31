"""Tests for the objectrocket.operations module."""
import pytest

from objectrocket import errors
from objectrocket import client
from objectrocket.operations import BaseOperationsLayer


def test_class_instantiation(self, client_token_auth, obj):
    assert BaseOperationsLayer(client_instance=client_token_auth)


def test_client_is_properly_embedded(self, client_token_auth):
    inst = BaseOperationsLayer(client_instance=client_token_auth)
    assert isinstance(inst.client, client.Client)


def test_verify_auth_returns_none_with_status_code_200(self, client_token_auth, obj):
    obj.status_code = 200
    inst = BaseOperationsLayer(client_instance=client_token_auth)
    assert inst._verify_auth(obj) is None


def test_verify_auth_raises_with_status_code_401(self, client_token_auth, obj):
    obj.status_code = 401
    obj.request = self.obj()
    obj.request.method = 'TEST'
    obj.request.path_url = '/TEST/PATH/'
    inst = BaseOperationsLayer(client_token_auth)

    with pytest.raises(errors.AuthFailure) as exinfo:
        inst._verify_auth(obj)

    assert exinfo.value.args[0] == ('Received response code 401 from TEST /TEST/PATH/. '
                                    'Keypair used: {}:{}'.format(client_token_auth.user_key,
                                                                 client_token_auth.pass_key))

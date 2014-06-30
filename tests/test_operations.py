"""Tests for the objectrocket.operations module."""
import pytest

from objectrocket import errors
from objectrocket.client import Client
from objectrocket.operations import BaseOperationsLayer
from tests import conftest


class TestBaseOperationsLayer(conftest.BaseClientTest):
    """Tests for objectrocket.operations.BaseOperationsLayer object."""

    @pytest.fixture
    def obj(self):
        class Obj(object):
            pass

        return Obj()

    def test_instantiation(self, obj):
        assert BaseOperationsLayer(self.client)

    def test_client_is_given_client(self):
        inst = BaseOperationsLayer(self.client)
        assert isinstance(inst._client, Client)

    def test_client_returns_none_when_client_is_invalid(self):
        inst = BaseOperationsLayer('not_a_valid_client')
        assert inst._client is None

    def test_verify_auth_returns_none(self, obj):
        obj.status_code = 200
        inst = BaseOperationsLayer(self.client)
        assert inst._verify_auth(obj) is None

    def test_verify_auth_raises_if_401_status_code(self, obj):
        obj.status_code = 401
        obj.request = self.obj()
        obj.request.method = 'TEST'
        obj.request.path_url = '/TEST/PATH/'
        inst = BaseOperationsLayer(self.client)

        with pytest.raises(errors.AuthFailure) as exinfo:
            inst._verify_auth(obj) is obj

        assert exinfo.value.args[0] == ('Received response code 401 from TEST /TEST/PATH/. '
                                        'Keypair used: {}:{}'
                                        ''.format(self.client.user_key, self.client.pass_key))

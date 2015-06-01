"""Tests for the objectrocket.bases module."""
import pytest

from objectrocket import errors
# from objectrocket.client import Client
from objectrocket.bases import BaseOperationsLayer


class OpsLayer(BaseOperationsLayer):
    """A class for testing the :py:class:`objectrocket.bases.BaseOperationsLayer`."""

    @property
    def _default_request_kwargs(self):
        return super(OpsLayer, self)._default_request_kwargs

    @property
    def _url(self):
        pass


##################################
# Tests for BaseOperationsLayer. #
##################################
def test_client_is_properly_embedded(client):
    inst = OpsLayer(base_client=client)
    assert client is inst.client


def test_default_request_kwargs(client):
    inst = OpsLayer(base_client=client)
    assert inst._default_request_kwargs == {
        'headers': {
            'Content-Type': 'application/json'
        },
        'hooks': {
            'response': inst._verify_auth
        }
    }


def test_url(client):
    inst = OpsLayer(base_client=client)
    assert inst._url is None


def test_verify_auth_returns_none_with_status_code_200(client, mocked_response, obj):
    mocked_response.status_code = 200
    mocked_response.request = obj
    mocked_response.request.method = 'TEST'
    mocked_response.request.path_url = '/TEST/PATH/'
    inst = OpsLayer(base_client=client)
    assert inst._verify_auth(mocked_response) is None


def test_verify_auth_raises_with_status_code_401(client, mocked_response, obj):
    mocked_response.status_code = 401
    mocked_response.request = obj
    mocked_response.request.method = 'TEST'
    mocked_response.request.path_url = '/TEST/PATH/'
    inst = OpsLayer(base_client=client)

    with pytest.raises(errors.AuthFailure) as exinfo:
        inst._verify_auth(mocked_response)

    assert exinfo.value.args[0] == (
        'Received response code 401 from TEST /TEST/PATH/. Token used: {}.'
        .format(client._token))

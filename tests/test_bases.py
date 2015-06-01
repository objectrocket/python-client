"""Tests for the objectrocket.bases module."""
import pytest

from objectrocket import errors
from objectrocket.bases import BaseInstance
from objectrocket.bases import BaseOperationsLayer

REQUIRED_INSTANCE_FIELDS = [
    'connect_string',
    'created',
    'name',
    'plan',
    'service',
    'type',
    'version'
]


class OpsLayerPrototype(BaseOperationsLayer):
    """A class for testing the :py:class:`objectrocket.bases.BaseOperationsLayer`."""

    @property
    def _default_request_kwargs(self):
        """Base requires this to be implemented."""
        return super(OpsLayerPrototype, self)._default_request_kwargs

    @property
    def _url(self):
        """Base requires this to be implemented."""
        pass


class InstancePrototype(BaseInstance):
    """A class for testing the :py:class:`objectrocket.bases.BaseOperationsLayer`."""

    @property
    def get_connection(self):
        """Base requires this to be implemented."""
        return super(BaseInstance, self).get_connection()


###########################
# Tests for BaseInstance. #
###########################
def test_client_is_properly_embedded_in_base_instance(client, mongodb_sharded_doc):
    inst = InstancePrototype(instance_document=mongodb_sharded_doc, base_client=client)
    assert inst.client is client


def test_instance_doc_is_properly_embedded_in_base_instance(client, mongodb_sharded_doc):
    inst = InstancePrototype(instance_document=mongodb_sharded_doc, base_client=client)
    assert inst.instance_document is mongodb_sharded_doc


@pytest.mark.parametrize('needed_field', REQUIRED_INSTANCE_FIELDS)
def test_instance_creation_fails_with_missing_field(client, mongodb_sharded_doc, needed_field):
    mongodb_sharded_doc.pop(needed_field, None)

    with pytest.raises(KeyError) as exinfo:
        InstancePrototype(instance_document=mongodb_sharded_doc, base_client=client)

    assert exinfo.value.args == (needed_field,)


def test_instance_repr_is_as_expected(client, mongodb_sharded_doc):
    inst = InstancePrototype(instance_document=mongodb_sharded_doc, base_client=client)
    inst_id = hex(id(inst))
    expected_repr = (
        '<{!s} {!r} at {!s}>'
        .format(inst.__class__.__name__, inst.instance_document, inst_id)
    )

    assert repr(inst) == expected_repr


##################################
# Tests for BaseOperationsLayer. #
##################################
def test_client_is_properly_embedded_in_base_ops(client):
    inst = OpsLayerPrototype(base_client=client)
    assert client is inst.client


def test_default_request_kwargs(client):
    inst = OpsLayerPrototype(base_client=client)
    assert inst._default_request_kwargs == {
        'headers': {
            'Content-Type': 'application/json'
        },
        'hooks': {
            'response': inst._verify_auth
        }
    }


def test_url(client):
    inst = OpsLayerPrototype(base_client=client)
    assert inst._url is None


def test_verify_auth_returns_none_with_status_code_200(client, mocked_response, obj):
    mocked_response.status_code = 200
    mocked_response.request = obj
    mocked_response.request.method = 'TEST'
    mocked_response.request.path_url = '/TEST/PATH/'
    inst = OpsLayerPrototype(base_client=client)
    assert inst._verify_auth(mocked_response) is None


def test_verify_auth_raises_with_status_code_401(client, mocked_response, obj):
    mocked_response.status_code = 401
    mocked_response.request = obj
    mocked_response.request.method = 'TEST'
    mocked_response.request.path_url = '/TEST/PATH/'
    inst = OpsLayerPrototype(base_client=client)

    with pytest.raises(errors.AuthFailure) as exinfo:
        inst._verify_auth(mocked_response)

    assert exinfo.value.args[0] == (
        'Received response code 401 from TEST /TEST/PATH/. Token used: {}.'
        .format(client._token))

import copy
import json
import mock
import pytest
import responses

from objectrocket.bases import BaseInstance

@pytest.yield_fixture(autouse=True)
def ensure_production_url(mongodb_sharded_instance, instance_acl_url):
    """Fixture that ensures that the proper production URLs are used in tests,
    instead of the potentially overridden ones from environment variables.

    See objectrocket.constants.OR_DEFAULT_API_URL
    """
    inst = mongodb_sharded_instance
    with mock.patch.object(BaseInstance, '_url', new_callable=mock.PropertyMock) as mock_url:
        type(mock_url).return_value = instance_acl_url.replace('acl_sync', '')
        yield

@pytest.fixture
def instance_acl_url(mongodb_sharded_instance):
    return "https://sjc-api.objectrocket.com/v2/instances/{}/acl_sync".format(mongodb_sharded_instance.name)

class TestSetGetAclSync:

    @responses.activate
    def test_acl_sync_disables(self, client, mongodb_sharded_instance, instance_acl_url):
        inst = mongodb_sharded_instance
        responses.add(responses.PUT, instance_acl_url,
                      status=200,
                      body=json.dumps({'data': {'aws_acl_sync_enabled': False,
                                       'rackspace_acl_sync_enabled': False}}),
                      content_type="application/json")
        responses.add(responses.GET, instance_acl_url, status=200,
                      body=json.dumps({'data': {'aws_acl_sync_enabled': True,
                                       'rackspace_acl_sync_enabled': True}}),
                      content_type="application/json")

        response = inst.acl_sync(aws_sync=False, rackspace_sync=False)

        assert isinstance(response, dict) is True
        assert response.get('data', {}).get('aws_acl_sync_enabled', True) is False
        assert response.get('data', {}).get('rackspace_acl_sync_enabled', True) is False

    @responses.activate
    def test_acl_sync_enables(self, client, mongodb_sharded_instance, instance_acl_url):
        inst = mongodb_sharded_instance
        responses.add(responses.PUT, instance_acl_url,
                      status=200,
                      body=json.dumps({'data': {'aws_acl_sync_enabled': True,
                                       'rackspace_acl_sync_enabled': True}}),
                      content_type="application/json")
        responses.add(responses.GET, instance_acl_url, status=200,
                      body=json.dumps({'data': {'aws_acl_sync_enabled': False,
                                       'rackspace_acl_sync_enabled': False}}),
                      content_type="application/json")

        response = inst.acl_sync(aws_sync=False, rackspace_sync=False)

        assert isinstance(response, dict) is True
        assert response.get('data', {}).get('aws_acl_sync_enabled', False) is True
        assert response.get('data', {}).get('rackspace_acl_sync_enabled', False) is True

    @responses.activate
    def test_acl_sync_just_returns_status(self, client, mongodb_sharded_instance, instance_acl_url):
        inst = mongodb_sharded_instance
        responses.add(responses.GET, instance_acl_url, status=200,
                      body=json.dumps({'data': {'aws_acl_sync_enabled': True,
                                       'rackspace_acl_sync_enabled': True}}),
                      content_type="application/json")
        responses.add(responses.PUT, instance_acl_url,
                      status=200,
                      body=json.dumps({'data': {'aws_acl_sync_enabled': False,
                                       'rackspace_acl_sync_enabled': False}}),
                      content_type="application/json")

        response = inst.acl_sync()

        assert isinstance(response, dict) is True
        assert response.get('data', {}).get('aws_acl_sync_enabled', True) is False
        assert response.get('data', {}).get('rackspace_acl_sync_enabled', True) is False

    @responses.activate
    def test_acl_sync_raises(self, client, mongodb_sharded_instance, instance_acl_url):
        inst = mongodb_sharded_instance
        exception = Exception('Test Exception')
        responses.add(responses.GET, instance_acl_url, status=500,
                      body=exception)

        with pytest.raises(Exception) as exinfo:
            response = inst.acl_sync()

        assert exinfo is not None
        assert exinfo.value.args[0] == 'Test Exception'

class TestRunAclSync:

    @responses.activate
    def test_run_sync_without_args_is_unchanged(self, client, mongodb_sharded_instance, instance_acl_url):
        inst = mongodb_sharded_instance
        responses.add(responses.POST, instance_acl_url,
                      status=200,
                      body=json.dumps({'data': {'aws_acl_sync_state': 'unchanged',
                                       'rackspace_acl_sync_state': 'unchanged'}}),
                      content_type="application/json")

        response = inst.run_acl_sync()

        assert isinstance(response, dict) is True
        assert response.get('data', {}).get('aws_acl_sync_state', None) == 'unchanged'
        assert response.get('data', {}).get('rackspace_acl_sync_state', None) == 'unchanged'

    @responses.activate
    def test_run_sync_starts(self, client, mongodb_sharded_instance, instance_acl_url):
        inst = mongodb_sharded_instance
        responses.add(responses.POST, instance_acl_url,
                      status=200,
                      body=json.dumps({'data': {'aws_acl_sync_state': 'started',
                                       'rackspace_acl_sync_state': 'started'}}),
                      content_type="application/json")

        response = inst.run_acl_sync(aws_sync=True, rackspace_sync=True)

        assert isinstance(response, dict) is True
        assert response.get('data', {}).get('aws_acl_sync_state', None) == 'started'
        assert response.get('data', {}).get('rackspace_acl_sync_state', None) == 'started'

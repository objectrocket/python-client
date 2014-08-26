"""Tests for the objectrocket.instances module."""
import json
import pytest
import mock

from tests import conftest
from objectrocket import errors
from objectrocket.client import Client
from objectrocket import instances


class TestInstances(conftest.InstancesHarness, conftest.GenericFixtures):
    """Tests for the objectrocket.instances.Instances operations layer."""

    def _response_object(self, data=[]):
        """Return an object with a single method ``json``.

        :param data: The value of the key 'data' in the returned json.
        """
        class response(object):
            def json(self):
                return {'data': data}

        return response()

    def test_instances_client(self, client_token_auth):
        assert isinstance(client_token_auth.instances._client, Client)

    def test_instances_api_instnaces_url(self, client_token_auth):
        assert client_token_auth.instances.url == client_token_auth.url + 'instance/'

    ####################
    # GET METHOD TESTS #
    ####################
    def test_get_calls_proper_endpoint_with_no_args(self, requests_patches, client_token_auth, obj):
        requests_patches['instances'].get.return_value = self._response_object()
        rv = client_token_auth.instances.get()

        expected_endpoint = client_token_auth.url + 'instance/'
        requests_patches['instances'].get.assert_called_once_with(
            expected_endpoint,
            **client_token_auth.default_request_kwargs)
        assert rv == []

    def test_get_calls_proper_endpoint_with_args(self, requests_patches, client_token_auth):
        requests_patches['instances'].get.return_value = self._response_object()
        rv = client_token_auth.instances.get('instance0')

        expected_endpoint = client_token_auth.url + 'instance/instance0/'
        requests_patches['instances'].get.assert_called_once_with(
            expected_endpoint,
            **client_token_auth.default_request_kwargs)
        assert rv == []

    #######################
    # CREATE METHOD TESTS #
    #######################
    def test_create_calls_proper_end_point(self, requests_patches, client_token_auth,
                                           default_create_instance_kwargs):
        requests_patches['instances'].post.return_value = self._response_object()
        rv = client_token_auth.instances.create(**default_create_instance_kwargs)
        default_create_instance_kwargs.pop('service_type')

        expected_endpoint = client_token_auth.url + 'instance/'
        requests_patches['instances'].post.assert_called_once_with(
            expected_endpoint,
            data=json.dumps(default_create_instance_kwargs),
            **client_token_auth.default_request_kwargs
        )
        assert rv == []

    def test_create_fails_with_bad_service_type_value(self, client_token_auth,
                                                      default_create_instance_kwargs):
        default_create_instance_kwargs['service_type'] = 'not_a_valid_service'
        with pytest.raises(errors.InstancesException) as exinfo:
            client_token_auth.instances.create(**default_create_instance_kwargs)

        assert exinfo.value.args[0] == ('Invalid value for "service_type". '
                                        'Must be one of "mongodb".')

    def test_create_fails_with_bad_version_value(self, client_token_auth,
                                                 default_create_instance_kwargs):
        default_create_instance_kwargs['version'] = 'not_a_valid_version'
        with pytest.raises(errors.InstancesException) as exinfo:
            client_token_auth.instances.create(**default_create_instance_kwargs)

        assert exinfo.value.args[0] == ('Invalid value for "version". '
                                        'Must be one of "2.4.6".')

    ####################
    # COMPACTION TESTS #
    ####################
    def test_compaction_calls_proper_end_point_request_compaction_false(self,
                                                                        requests_patches,
                                                                        client_token_auth):
        requests_patches['instances'].get.return_value = self._response_object()
        instance_name = 'instance0'
        rv = client_token_auth.instances.compaction(instance_name=instance_name,
                                                    request_compaction=False)

        expected_endpoint = client_token_auth.url + 'instance/' + instance_name + '/compaction/'
        requests_patches['instances'].get.assert_called_once_with(
            expected_endpoint,
            **client_token_auth.default_request_kwargs)
        assert rv == {'data': []}

    def test_compaction_calls_proper_end_point_request_compaction_true(self,
                                                                       requests_patches,
                                                                       client_token_auth):
        requests_patches['instances'].post.return_value = self._response_object()
        instance_name = 'instance0'
        rv = client_token_auth.instances.compaction(instance_name=instance_name,
                                                    request_compaction=True)

        expected_endpoint = client_token_auth.url + 'instance/' + instance_name + '/compaction/'
        requests_patches['instances'].post.assert_called_once_with(
            expected_endpoint,
            **client_token_auth.default_request_kwargs)
        assert rv == {'data': []}

    ################
    # SHARDS TESTS #
    ################
    def test_shards_calls_proper_end_point_without_add_shard(self,
                                                             requests_patches,
                                                             client_token_auth):
        requests_patches['instances'].get.return_value = self._response_object()
        instance_name = 'instance0'
        rv = client_token_auth.instances.shards(instance_name=instance_name, add_shard=False)

        expected_endpoint = client_token_auth.url + 'instance/' + instance_name + '/shard/'
        requests_patches['instances'].get.assert_called_once_with(
            expected_endpoint,
            **client_token_auth.default_request_kwargs)
        assert rv == {'data': []}

    def test_shards_calls_proper_end_point_with_add_shard(self,
                                                          requests_patches,
                                                          client_token_auth):
        requests_patches['instances'].post.return_value = self._response_object()
        instance_name = 'instance0'
        rv = client_token_auth.instances.shards(instance_name=instance_name, add_shard=True)

        expected_endpoint = client_token_auth.url + 'instance/' + instance_name + '/shard/'
        requests_patches['instances'].post.assert_called_once_with(
            expected_endpoint,
            **client_token_auth.default_request_kwargs)
        assert rv == {'data': []}

    ############################
    # CONVENIENCE METHOD TESTS #
    ############################
    # def test_instance_compaction_convenience_call_request_compaction_true(self,
    #                                                                       requests_patches,
    #                                                                       client_token_auth,
    #                                                                       mongo_sharded_instance):
    #     requests_patches['instances'].get.return_value = self._response_object()
    #     rv = mongo_sharded_instance.compaction()

    #     expected_endpoint = (client_token_auth.url + 'instance/' +
    #                          mongo_sharded_instance.name + '/compaction/')
    #     defaults = client_token_auth.default_request_kwargs
    #     defaults.update({'hooks': {'response': client_token_auth._verify_auth}})
    #     requests_patches['instances'].get.assert_called_once_with(expected_endpoint, **defaults)
    #     assert rv == {'data': []}

    # def test_instance_compaction_convenience_call_request_compaction_false(self,
    #                                                                        requests_patches,
    #                                                                        client_token_auth,
    #                                                                        mongo_sharded_instance):
    #     requests_patches['instances'].post.return_value = self._response_object()
    #     rv = mongo_sharded_instance.compaction(request_compaction=True)

    #     expected_endpoint = (client_token_auth.url + 'instance/' +
    #                          mongo_sharded_instance.name + '/compaction/')
    #     defaults = client_token_auth.default_request_kwargs
    #     defaults.update({'hooks': {'response': client_token_auth._verify_auth}})
    #     requests_patches['instances'].post.assert_called_once_with(expected_endpoint, **defaults)
    #     assert rv == {'data': []}

    # def test_instance_shards_calls_proper_end_point_without_add_shard(self,
    #                                                                   requests_patches,
    #                                                                   client_token_auth,
    #                                                                   mongo_sharded_instance):
    #     requests_patches['instances'].get.return_value = self._response_object()
    #     rv = mongo_sharded_instance.shards(add_shard=False)

    #     expected_endpoint = (client_token_auth.url + 'instance/' +
    #                          mongo_sharded_instance.name + '/shard/')
    #     defaults = client_token_auth.default_request_kwargs
    #     defaults.update({'hooks': {'response': client_token_auth._verify_auth}})
    #     requests_patches['instances'].get.assert_called_once_with(expected_endpoint, **defaults)
    #     assert rv == {'data': []}

    # def test_instance_shards_calls_proper_end_point_with_add_shard(self,
    #                                                                requests_patches,
    #                                                                client_token_auth,
    #                                                                mongo_sharded_instance):
    #     requests_patches['instances'].post.return_value = self._response_object()
    #     rv = mongo_sharded_instance.shards(add_shard=True)

    #     expected_endpoint = (client_token_auth.url + 'instance/' +
    #                          mongo_sharded_instance.name + '/shard/')
    #     defaults = client_token_auth.default_request_kwargs
    #     defaults.update({'hooks': {'response': client_token_auth._verify_auth}})
    #     requests_patches['instances'].post.assert_called_once_with(expected_endpoint, **defaults)
    #     assert rv == {'data': []}


# class TestInstance(conftest.InstancesHarness):
#     """Tests for objectrocket.instances.Instance objects with mongodb_sharded input."""

#     def _pop_needed_key_and_assert(self, doc, needed_key):
#         """Pop needed_key from doc and assert KeyError during constructor run."""
#         doc.pop(needed_key)
#         with pytest.raises(KeyError) as exinfo:
#             instances.BaseInstance(instance_document=doc, client=Client('test_user_key',
#                                                                         'test_pass_key'))

#         assert exinfo.value.__class__ == KeyError
#         assert exinfo.value.args[0] == needed_key

#     #####################
#     # CONSTRUCTOR TESTS #
#     #####################
#     def test_constructor_passes_with_expected_document(self, requests_patches, _docs):
#         user_key, pass_key = 'test_user_key', 'test_pass_key'
#         inst = instances.BaseInstance(instance_document=_docs,
#                                       client=Client(user_key=user_key, pass_key=pass_key))
#         assert isinstance(inst, instances.BaseInstance)

#     def test_constructor_fails_with_missing_api_endpoint(self, requests_patches, _docs):
#         self._pop_needed_key_and_assert(_docs, 'api_endpoint')

#     def test_constructor_fails_with_missing_connect_string(self, requests_patches, _docs):
#         self._pop_needed_key_and_assert(_docs, 'connect_string')

#     def test_constructor_fails_with_missing_created(self, requests_patches, _docs):
#         self._pop_needed_key_and_assert(_docs, 'created')

#     def test_constructor_fails_with_missing_name(self, requests_patches, _docs):
#         self._pop_needed_key_and_assert(_docs, 'name')

#     def test_constructor_fails_with_missing_plan(self, requests_patches, _docs):
#         self._pop_needed_key_and_assert(_docs, 'plan')

#     def test_constructor_passes_without_ssl_connect_string(self, requests_patches, _docs):
#         _docs.pop('ssl_connect_string', None)
#         inst = instances.BaseInstance(instance_document=_docs, client=Client('test_user_key',
#                                                                              'test_pass_key'))
#         assert isinstance(inst, instances.BaseInstance)

#     def test_constructor_fails_with_missing_service(self, requests_patches, _docs):
#         self._pop_needed_key_and_assert(_docs, 'service')

#     def test_constructor_fails_with_missing_type(self, requests_patches, _docs):
#         self._pop_needed_key_and_assert(_docs, 'type')

#     def test_constructor_fails_with_missing_version(self, requests_patches, _docs):
#         self._pop_needed_key_and_assert(_docs, 'version')

#     ###########################
#     # INSTANCE PROPERTY TESTS #
#     ###########################
#     def test_api_endpoint_property(self, _instances_and_docs):
#         instance, doc = _instances_and_docs[0], _instances_and_docs[1]
#         assert instance.api_endpoint == doc['api_endpoint']

#     def test_client_property_with_valid_client(self, _instances_and_docs):
#         instance = _instances_and_docs[0]
#         assert isinstance(instance.client, Client)

#     def test_mongo_sharded_connection_property(self, mongo_sharded_instance, mongo_sharded_doc):
#         with mock.patch('pymongo.MongoClient', return_value=None) as client:
#             mongo_sharded_instance.connection

#         host, port = mongo_sharded_doc['connect_string'].split(':')
#         port = int(port)
#         client.assert_called_once_with(host=host, port=port)

#     def test_mongo_replica_connection_property(self, mongo_replica_instance, mongo_replica_doc):
#         with mock.patch('pymongo.MongoReplicaSetClient', return_value=None) as client:
#             mongo_replica_instance.connection

#         replica_set_name, member_list = mongo_replica_doc['connect_string'].split('/')
#         member_list = member_list.strip().strip(',')
#         client.assert_called_once_with(hosts_or_uri=member_list)

#     def test_connect_string_property(self, _instances_and_docs):
#         instance, doc = _instances_and_docs[0], _instances_and_docs[1]
#         assert instance.connect_string == doc['connect_string']

#     def test_created_property(self, _instances_and_docs):
#         instance, doc = _instances_and_docs[0], _instances_and_docs[1]
#         assert instance.created == doc['created']

#     def test_name_property(self, _instances_and_docs):
#         instance, doc = _instances_and_docs[0], _instances_and_docs[1]
#         assert instance.name == doc['name']

#     def test_plan_property(self, _instances_and_docs):
#         instance, doc = _instances_and_docs[0], _instances_and_docs[1]
#         assert instance.plan == doc['plan']

#     def test_service_property(self, _instances_and_docs):
#         instance, doc = _instances_and_docs[0], _instances_and_docs[1]
#         assert instance.service == doc['service']

#     def test_ssl_connect_string_property(self, _instances_and_docs):
#         instance, doc = _instances_and_docs[0], _instances_and_docs[1]
#         assert instance.ssl_connect_string == doc.get('ssl_connect_string')

#     def test_type_property(self, _instances_and_docs):
#         instance, doc = _instances_and_docs[0], _instances_and_docs[1]
#         assert instance.type == doc['type']

#     def test_version_property(self, _instances_and_docs):
#         instance, doc = _instances_and_docs[0], _instances_and_docs[1]
#         assert instance.version == doc['version']

#     #########################
#     # INSTANCE METHOD TESTS #
#     #########################
#     def test_to_dict_method(self, _instances_and_docs):
#         instance, doc = _instances_and_docs[0], _instances_and_docs[1]
#         assert instance.to_dict() == doc

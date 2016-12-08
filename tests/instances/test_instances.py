"""Tests for the objectrocket.instances module."""
import sys
import responses

import pytest

from objectrocket.instances.mongodb import MongodbInstance
from objectrocket.acls import Acl

from ..utils import comparable_dictionaries


##########################################
# Tests for Instances private interface. #
##########################################
def test_concrete_instance_returns_none_if_dict_not_given(client):
    output = client.instances._concrete_instance([])
    assert output is None


def test_concrete_instance_returns_none_if_doc_is_missing_needed_field(
        client,
        mongodb_sharded_doc):
    mongodb_sharded_doc.pop('name')  # Will cause a constructor error.
    output = client.instances._concrete_instance(mongodb_sharded_doc)
    assert output is None


def test_concrete_instance_returns_expected_instance_object(client, mongodb_sharded_doc):
    output = client.instances._concrete_instance(mongodb_sharded_doc)
    assert isinstance(output, MongodbInstance)
    assert output._instance_document is mongodb_sharded_doc


def test_concrete_instance_list_returns_empty_list_if_empty_list_provided(client):
    output = client.instances._concrete_instance_list([])
    assert output == []


def test_concrete_instance_list_returns_empty_list_if_constructor_error_for_doc(
        client,
        mongodb_sharded_doc):
    mongodb_sharded_doc.pop('name')  # Will cause a constructor error.
    output = client.instances._concrete_instance_list([mongodb_sharded_doc])
    assert output == []


def test_concrete_instance_list_returns_expected_list(client, mongodb_sharded_doc):
    output = client.instances._concrete_instance_list([mongodb_sharded_doc])
    assert isinstance(output, list)
    assert len(output) == 1
    assert output[0]._instance_document is mongodb_sharded_doc


#######################################
# Tests for Instances ACLs interface. #
#######################################
@responses.activate
def test_instance_acls_all_makes_expected_call(mongodb_sharded_instance):
    inst = mongodb_sharded_instance
    expected_url = 'http://localhost:5050/v2/instances/{}/acls/'.format(inst.name)
    responses.add(
        responses.GET,
        expected_url,
        status=200,
        json={'data': []},
        content_type="application/json",
    )

    output = inst.acls.all()

    assert output == []


@responses.activate
def test_instance_acls_all_returns_expected_acl_object(mongodb_sharded_instance, acl):
    inst = mongodb_sharded_instance
    expected_url = 'http://localhost:5050/v2/instances/{}/acls/'.format(inst.name)
    responses.add(
        responses.GET,
        expected_url,
        status=200,
        json={'data': [acl._document]},
        content_type="application/json",
    )

    output = inst.acls.all()

    assert isinstance(output[0], Acl)
    assert output[0].id == acl.id


@responses.activate
def test_instance_acls_create_makes_expected_call(mongodb_sharded_instance, acl):
    inst = mongodb_sharded_instance
    expected_url = 'http://localhost:5050/v2/instances/{}/acls/'.format(inst.name)
    responses.add(
        responses.POST,
        expected_url,
        status=200,
        json={'data': acl._document},
        content_type="application/json",
    )

    output = inst.acls.create(cidr_mask=acl.cidr_mask, description=acl.description)

    assert isinstance(output, Acl)
    assert output.id == acl.id


@responses.activate
def test_instance_new_relic_stats(mongodb_replicaset_instance,):
    inst = mongodb_replicaset_instance
    expected_url = 'http://localhost:5050/v2/instances/{}/new-relic-stats'.format(inst.name)
    responses.add(
        responses.GET,
        expected_url,
        status=200,
        body={},
        content_type="application/json",
    )

    assert hasattr(mongodb_replicaset_instance, 'new_relic_stats')
    assert mongodb_replicaset_instance.new_relic_stats == {}


@pytest.mark.skipif(sys.version_info[0] >= 3, reason=('long and unincode use in objectrocket.utils.sum_values'
                                                      'should be cleaned up before running this test on python 3'))
def test_instance_rollup_shard_stats_to_instance_stats(mongodb_sharded_instance,
                                                       mock_shard_stats,
                                                       mock_instance_stats_this_second):

    rolled_up_instance_stats = mongodb_sharded_instance._rollup_shard_stats_to_instance_stats(mock_shard_stats)
    # we check just the keys because some rolled up values won't be the same every time even if the same set
    # of shard stats were to be rolled up to instance level.
    assert comparable_dictionaries(rolled_up_instance_stats, mock_instance_stats_this_second)


def test_compile_new_relic_stats(mongodb_sharded_instance, mock_instance_stats_this_second,
                                 mock_instance_stats_next_second, mock_new_relic_stats):

    new_relic_stats = mongodb_sharded_instance._compile_new_relic_stats(
        mock_instance_stats_this_second, mock_instance_stats_next_second)
    assert comparable_dictionaries(new_relic_stats, mock_new_relic_stats)

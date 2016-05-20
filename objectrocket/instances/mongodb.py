"""MongoDB instance classes and logic."""
import datetime
import json
import logging
import time

import pymongo
import requests

from concurrent import futures

from objectrocket import bases
from objectrocket import util

logger = logging.getLogger(__name__)


class MongodbInstance(bases.BaseInstance, bases.Extensible, bases.InstanceAclsInterface):
    """An ObjectRocket MongoDB service instance.

    :param dict instance_document: A dictionary representing the instance object, most likey coming
        from the ObjectRocket API.
    :param objectrocket.instances.Instances instances: An instance of
        :py:class:`objectrocket.instances.Instances`.
    """

    def __init__(self, instance_document, instances):
        super(MongodbInstance, self).__init__(
            instance_document=instance_document,
            instances=instances
        )

        # Bind required pseudo private attributes from API response document.
        # Smallest plans may not have an SSL/TLS connection string.
        self._ssl_connect_string = instance_document.get('ssl_connect_string')

        # Register any extensions for this class.
        self._register_extensions('objectrocket.instances.mongodb.MongodbInstance')

        # on demand initialization of new_relic_stats
        # TODO: (kmagge) we can get rid of this when we have newer version of stats
        self._new_relic_stats = None

    #####################
    # Public interface. #
    #####################
    @util.token_auto_auth
    def compaction(self, request_compaction=False):
        """Retrieve a report on, or request compaction for this instance.

        :param bool request_compaction: A boolean indicating whether or not to request compaction.
        """
        url = self._service_url + 'compaction/'

        if request_compaction:
            response = requests.post(url, **self._instances._default_request_kwargs)
        else:
            response = requests.get(url, **self._instances._default_request_kwargs)

        return response.json()

    def get_authenticated_connection(self, user, passwd, db='admin', ssl=True):
        """Get an authenticated connection to this instance.

        :param str user: The username to use for authentication.
        :param str passwd: The password to use for authentication.
        :param str db: The name of the database to authenticate against. Defaults to ``'Admin'``.
        :param bool ssl: Use SSL/TLS if available for this instance. Defaults to ``True``.
        :raises: :py:class:`pymongo.errors.OperationFailure` if authentication fails.
        """
        # Attempt to establish an authenticated connection.
        try:
            connection = self.get_connection(ssl=ssl)
            connection[db].authenticate(user, passwd)
            return connection

        # Catch exception here for logging, then just re-raise.
        except pymongo.errors.OperationFailure as ex:
            logger.exception(ex)
            raise

    def get_connection(self, ssl=True):
        """Get a live connection to this instance.

        :param bool ssl: Use SSL/TLS if available for this instance.
        """
        return self._get_connection(ssl=ssl)

    @util.token_auto_auth
    def shards(self, add_shard=False):
        """Get a list of shards belonging to this instance.

        :param bool add_shard: A boolean indicating whether to add a new shard to the specified
            instance.
        """
        url = self._service_url + 'shards/'
        if add_shard:
            response = requests.post(url, **self._instances._default_request_kwargs)
        else:
            response = requests.get(url, **self._instances._default_request_kwargs)

        return response.json()

    def get_aggregate_database_stats(self):
        return requests.get(self._service_url + 'aggregate_database_stats/',
                            **self._instances._default_request_kwargs).json()['data']

    @property
    @util.token_auto_auth
    def new_relic_stats(self):
        """
        Get stats for this instance.
        """
        if self._new_relic_stats is None:
            # if this is a sharded instance, fetch shard stats in parallel
            if self.type == 'mongodb_sharded':
                shards = [Shard(self.name, self._service_url + 'shards/',
                                self._client, shard_doc)
                          for shard_doc in self.shards().get('data')]
                fs = []
                with futures.ThreadPoolExecutor(len(shards)) as executor:
                    for shard in shards:
                        fs.append(executor.submit(shard.get_shard_stats))
                    futures.wait(fs, timeout=None, return_when=futures.ALL_COMPLETED)
                stats_this_second = self._rollup_shard_stats_to_instance_stats(
                    {shard.name: future.result() for (shard, future) in zip(shards, fs)})
                # power nap
                time.sleep(1)
                # fetch again
                fs = []
                with futures.ThreadPoolExecutor(len(shards)) as executor:
                    for shard in shards:
                        fs.append(executor.submit(shard.get_shard_stats))
                    futures.wait(fs, timeout=None, return_when=futures.ALL_COMPLETED)
                stats_next_second = self._rollup_shard_stats_to_instance_stats(
                    {shard.name: future.result() for (shard, future) in zip(shards, fs)})
                self._new_relic_stats = self._compile_new_relic_stats(stats_this_second, stats_next_second)
            else:
                # fetch stats like we did before (by hitting new_relic_stats API resource)
                response = requests.get('{}{}'.format(self._url,
                                        'new-relic-stats'),
                                        **self._instances._default_request_kwargs)
                self._new_relic_stats = json.loads(response.content).get(
                    'data') if response.status_code == 200 else {}
        return self._new_relic_stats

    def _rollup_shard_stats_to_instance_stats(self, shard_stats):
        """
        roll up all shard stats to instance level stats

        :param shard_stats: dict of {shard_name: shard level stats}
        """
        instance_stats = {}
        opcounters_per_node = []

        # aggregate replication_lag
        instance_stats['replication_lag'] = max(map(lambda s: s['replication_lag'], shard_stats.values()))

        aggregate_server_statistics = {}
        for shard_name, stats in shard_stats.items():
            for statistic_key in stats.get('shard_stats'):
                if statistic_key != 'connections' and statistic_key in aggregate_server_statistics:
                    aggregate_server_statistics[statistic_key] = util.sum_values(aggregate_server_statistics[statistic_key],
                                                                                 stats.get('shard_stats')[statistic_key])
                else:
                    aggregate_server_statistics[statistic_key] = stats.get('shard_stats')[statistic_key]

            # aggregate per_node_stats into opcounters_per_node
            opcounters_per_node.append({shard_name: {member: node_stats['opcounters']
                                                     for member, node_stats in stats.get('per_node_stats').items()}})

        instance_stats['opcounters_per_node'] = opcounters_per_node
        instance_stats['aggregate_server_statistics'] = aggregate_server_statistics
        return instance_stats

    def _compile_new_relic_stats(self, stats_this_second, stats_next_second):
        """
        from instance 'stats_this_second' and instance 'stats_next_second', compute some per
        second stats metrics and other aggregated metrics

        :param dict stats_this_second:
        :param dict stats_next_second:
        :return: compiled instance stats that has metrics

        {'opcounters_per_node_per_second': {...},
         'server_statistics_per_second': {...},
         'aggregate_server_statistics': {...},
         'replication_lag': 0.0,
         'aggregate_database_statistics': {}
         }
        """
        server_statistics_per_second = {}
        opcounters_per_node_per_second = []
        for subdoc in ["opcounters", "network"]:
            first_doc = stats_this_second['aggregate_server_statistics'][subdoc]
            second_doc = stats_next_second['aggregate_server_statistics'][subdoc]
            keys = set(first_doc.keys()) | set(second_doc.keys())
            server_statistics_per_second[subdoc] = {key: int(second_doc[key]) - int(first_doc[key]) for key in keys}
        for node1, node2 in zip(stats_this_second['opcounters_per_node'], stats_next_second['opcounters_per_node']):
            node_opcounters_per_second = {}
            for repl, members in node2.items():
                node_opcounters_per_second[repl] = {}
                for member, ops in members.items():
                    node_opcounters_per_second[repl][member] = {}
                    for op, count in ops.items():
                        node_opcounters_per_second[repl][member][op] = count - node1[repl][member][op]
            opcounters_per_node_per_second.append(node_opcounters_per_second)

        return {'opcounters_per_node_per_second': opcounters_per_node_per_second,
                'server_statistics_per_second': server_statistics_per_second,
                'aggregate_server_statistics': stats_next_second.get('aggregate_server_statistics'),
                'replication_lag': stats_next_second.get('replication_lag'),
                'aggregate_database_statistics': self.get_aggregate_database_stats()}

    @property
    def ssl_connect_string(self):
        """This instance's SSL connection string."""
        return self._ssl_connect_string

    @util.token_auto_auth
    def get_stepdown_window(self):
        """Get information on this instance's stepdown window."""
        url = self._service_url + 'stepdown/'
        response = requests.get(url, **self._instances._default_request_kwargs)
        return response.json()

    @util.token_auto_auth
    def set_stepdown_window(self, start, end, enabled=True, scheduled=True, weekly=True):
        """Set the stepdown window for this instance.

        Date times are assumed to be UTC, so use UTC date times.

        :param datetime.datetime start: The datetime which the stepdown window is to open.
        :param datetime.datetime end: The datetime which the stepdown window is to close.
        :param bool enabled: A boolean indicating whether or not stepdown is to be enabled.
        :param bool scheduled: A boolean indicating whether or not to schedule stepdown.
        :param bool weekly: A boolean indicating whether or not to schedule compaction weekly.
        """
        # Ensure a logical start and endtime is requested.
        if not start < end:
            raise TypeError('Parameter "start" must occur earlier in time than "end".')

        # Ensure specified window is less than a week in length.
        week_delta = datetime.timedelta(days=7)
        if not ((end - start) <= week_delta):
            raise TypeError('Stepdown windows can not be longer than 1 week in length.')

        url = self._service_url + 'stepdown/'
        data = {
            'start': int(start.strftime('%s')),
            'end': int(end.strftime('%s')),
            'enabled': enabled,
            'scheduled': scheduled,
            'weekly': weekly,
        }

        response = requests.post(
            url,
            data=json.dumps(data),
            **self._instances._default_request_kwargs
        )
        return response.json()

    ######################
    # Private interface. #
    ######################
    def _get_connection(self, ssl):
        """Get a live connection to this instance."""

        # Use SSL/TLS if requested and available.
        connect_string = self.connect_string
        if ssl and self.ssl_connect_string:
            connect_string = self.ssl_connect_string

        return pymongo.MongoClient(connect_string)


class Shard(bases.Extensible):
    """An ObjectRocket MongoDB instance shard.

    :param dict instance_name: Name of the instance the shard belongs to
    :param string stats_base_url: Base url to fetch information and stats for this shard.
    :param objectrocket.client.Client or_client: handle to talk to OR API
    :param dict shard_document: a dictionary representing a mongodb shard
    """

    def __init__(self, instance_name, stats_base_url, or_client, shard_document):
        self._instance_name = instance_name
        self._shardstr = shard_document['shardstr']
        self._plan = shard_document['plan']
        self._id = shard_document['id']
        self._name = shard_document['name']
        self._stats_base_url = stats_base_url
        self._client = or_client

    @property
    def instance_name(self):
        """
        :return: name of parent instance
        """
        return self._instance_name

    @property
    def shard_string(self):
        """
        :return: shard string
        """
        return self._shardstr

    @property
    def plan(self):
        """
        :return: Objectrocket plan that the parent instance is on
        """
        return self._plan

    @property
    def name(self):
        """
        :return: shard's name
        """
        return self._name

    @property
    def id(self):
        """
        :return: shard's unique ID
        """
        return self._id

    def get_shard_stats(self):
        """
        :return: get stats for this mongodb shard
        """
        return requests.get(self._stats_url, params={'include_stats': True},
                            headers={'X-Auth-Token': self._client.auth._token}
                            ).json()['data']['stats']

    @property
    def _stats_url(self):
        """
        :return: Objectrocket API endpoint to send shard stats request to
        """
        return '%s%s/' % (self._stats_base_url, self.name)

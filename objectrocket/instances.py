"""Instances layer."""
import datetime
import json
import requests

from objectrocket.utils import Utils


class Instances(object):
    """Instance operations.

    :param objectrocket.client.Client client_instance: An instance of
        objectrocket.client.Client.
    """

    def __init__(self, client_instance):
        self._client = client_instance
        self._api_instances_url = self.client.api_url + 'instance/'

    @property
    def api_instances_url(self):
        """The base URL for instance operations."""
        return self._api_instances_url

    @property
    def client(self):
        """The Client instance object."""
        return self._client

    def compaction(self, instance_name, request_compaction=False):
        """Compaction."""
        if not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance of str.')

        url = self.api_instances_url + instance_name + '/compaction/'

        if request_compaction:
            response = requests.post(url, auth=(self.client.user_key, self.client.pass_key))
        else:
            response = requests.get(url, auth=(self.client.user_key, self.client.pass_key))

        return response.json()

    def create(self, name, size, zone, service_type='mongodb', version='2.4.6'):
        """Create an instance."""
        if not isinstance(name, str):
            raise self.InstancesException('Parameter "name" must be an instance of str.')

        if not isinstance(size, int):
            raise self.InstancesException('Parameter "size" must be an instance of int.')

        if not isinstance(zone, str):
            raise self.InstancesException('Parameter "zone" must be an instance of str.')

        valid_service_types = ('mongodb', )
        if service_type not in valid_service_types:
            raise self.InstancesException('Invalid value for "service_type". Must be one of %s.'
                                          % valid_service_types)

        valid_versions = ('2.4.6', )
        if version not in valid_versions:
            raise self.InstancesException('Invalid value for "version". Must be one of %s.'
                                          % valid_versions)

        url = self.api_instances_url
        data = {
            'name': name,
            'size': size,
            'zone': zone,
            'type': service_type,
            'version': version,
        }

        # Not passing service type ATM. Probably will soon though.
        data.pop('type')

        response = requests.post(url,
                                 auth=(self.client.user_key, self.client.pass_key),
                                 data=json.dumps(data),
                                 headers={'Content-Type': 'application/json'})
        return response.json()

    def get(self, instance_name=None):
        """Get details on one or all instances."""
        if instance_name is not None and not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance of str.')

        url = self.api_instances_url
        if instance_name is not None:
            url += instance_name + '/'

        response = requests.get(url, auth=(self.client.user_key, self.client.pass_key))
        return response.json()

    def stepdown_window(self, instance_name):
        """Get information on the instance's stepdown window."""
        if not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance of str.')

        url = self.api_instances_url + instance_name + '/stepdown/'

        response = requests.get(url, auth=(self.client.user_key, self.client.pass_key))
        return response.json()

    def set_stepdown_window(self, instance_name, start, end, enabled, scheduled, weekly):
        """Use UTC date times."""
        if not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance of str.')
        if not isinstance(start, str):
            raise self.InstancesException('Parameter "start" must be an instance of datetime.')
        if not isinstance(end, str):
            raise self.InstancesException('Parameter "end" must be an instance of datetime.')
        if not isinstance(enabled, bool):
            raise self.InstancesException('Parameter "enabled" must be a boolean.')
        if not isinstance(scheduled, bool):
            raise self.InstancesException('Parameter "scheduled" must be a boolean.')
        if not isinstance(weekly, bool):
            raise self.InstancesException('Parameter "weekly" must be a boolean.')

        try:
            # Ensure that time strings can be parsed properly.
            datetime.datetime.strptime(start, Utils.TIME_FORMAT)
            datetime.datetime.strptime(end, Utils.TIME_FORMAT)
        except ValueError as ex:
            raise self.InstancesException(str(ex))

        url = self.api_instances_url + instance_name + '/stepdown/'

        data = {
            'start': start,
            'end': end,
            'enabled': enabled,
            'scheduled': scheduled,
            'weekly': weekly,
        }

        response = requests.post(url,
                                 auth=(self.client.user_key, self.client.pass_key),
                                 data=json.dumps(data),
                                 headers={'Content-Type': 'application/json'})
        return response.json()

    class InstancesException(Exception):
        pass

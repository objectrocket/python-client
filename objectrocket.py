"""
"""
import datetime
import json
import requests


# TODO(Anthony): api_url should default to our v2 api. Overwrite with a kwarg.
class ORClient(object):
    def __init__(self, user_key, pass_key, api_url=None):
        if (not isinstance(user_key, str) or
                not isinstance(pass_key, str)):
            raise self.ORClientException('All parameters should be instances of str.')

        if api_url is not None:
            # FIXME(Anthony): Probably shouldn't do this long term.
            api_url = self._check_api_url(api_url)
        else:
            api_url = 'http://localhost:5050/v2/'  # Point this to the LB when deployed.

        # ORClient properties.
        self._api_url = api_url
        self._user_key = user_key
        self._pass_key = pass_key

        self._instances = None

    @property
    def api_url(self):
        return self._api_url

    def _check_api_url(self, api_url):
        api_url = api_url.strip()
        if not api_url.endswith('/'):
            api_url += '/'

        if not api_url.endswith('/v2/'):
            api_url += 'v2/'

        if not api_url.startswith(('http://', 'https://')):
            api_url = 'https://' + api_url

        return api_url

    @property
    def instances(self):
        if self._instances is None:
            self._instances = Instances(self)

        return self._instances

    @property
    def pass_key(self):
        return self._pass_key

    @property
    def user_key(self):
        return self._user_key

    class ORClientException(Exception):
        pass


class Instances(object):
    def __init__(self, client):
        if not isinstance(client, ORClient):
            raise self.InstancesException('Parameter "client" must be an instance of ORClient.')

        self._client = client
        self._api_instances_url = self.client.api_url + 'instance/'

    @property
    def api_instances_url(self):
        return self._api_instances_url

    @property
    def client(self):
        return self._client

    def compact(self, instance_name, request_compaction=False):
        if not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance of str.')

        url = self.api_instances_url + instance_name + '/compact/'

        if request_compaction:
            request = requests.post(url, data={}, auth=(self.client.user_key, self.client.pass_key))
        else:
            request = requests.get(url, auth=(self.client.user_key, self.client.pass_key))

        return request.json()

    def create(self, name, size, zone, service_type='mongodb', version='2.4.6'):
        if not isinstance(name, str):
            raise self.InstancesException('Parameter "name" must be an instance of str.')

        if not isinstance(size, int):
            raise self.InstancesException('Parameter "size" must be an instance of int.')

        if not isinstance(zone, str):
            raise self.InstancesException('Parameter "zone" must be an instance of str.')

        valid_service_types = ('mongodb', )
        if service_type not in valid_service_types:
            raise self.InstancesException('Invalid value for "service_type". Must be one of %s.' % valid_service_types)

        valid_versions = ('2.4.6', )
        if version not in valid_versions:
            raise self.InstancesException('Invalid value for "version". Must be one of %s.' % valid_versions)

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

        # FIXME(Anthony): Make this POST data as JSON.
        request = requests.post(url, data=json.dumps(data), auth=(self.client.user_key, self.client.pass_key))
        return request.json()

    def get(self, instance_name=None):
        if instance_name is not None and not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance of str.')

        url = self.api_instances_url
        if instance_name is not None:
            url += instance_name + '/'

        request = requests.get(url, auth=(self.client.user_key, self.client.pass_key))
        return request.json()

    def stepdown_window(self, instance_name):
        if not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance of str.')

        url = self.api_instances_url + instance_name + '/stepdown/'

        request = requests.get(url, auth=(self.client.user_key, self.client.pass_key))
        return request.json()

    def set_stepdown_window(self, instance_name, start, end, enabled, scheduled, weekly):
        # TODO: Finish this type checking.
        if not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance of str.')
        if not isinstance(start, datetime.datetime):
            raise self.InstancesException('Parameter "start" must be an instance of datetime.')
        if not isinstance(end, datetime.datetime):
            raise self.InstancesException('Parameter "end" must be an instance of datetime.')
        if not isinstance(enabled, bool):
            raise self.InstancesException('Parameter "enabled" must be a boolean.')
        if not isinstance(scheduled, bool):
            raise self.InstancesException('Parameter "scheduled" must be a boolean.')
        if not isinstance(weekly, bool):
            raise self.InstancesException('Parameter "weekly" must be a boolean.')

        url = self.api_instances_url + instance_name + '/stepdown/'

        data = {
            'start': start.strftime('%s'),
            'end': end.strftime('%s'),
            'enabled': enabled,
            'scheduled': scheduled,
            'weekly': weekly,
        }

        request = requests.post(url, data=data, auth=(self.client.user_key, self.client.pass_key))
        return request.json()

    class InstancesException(Exception):
        pass


class ClientUtils(object):
    def construct_datetime(self, dtstr):
        form = '%Y-%m-%d %H:%M:%S.%f'

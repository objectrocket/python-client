"""
"""
import requests


# TODO: api_url should default to our v2 api. Overwrite with a kwarg.
class ORClient(object):
    def __init__(self, api_url, user_key, pass_key):
        if (not isinstance(api_url, str) or
                not isinstance(user_key, str) or
                not isinstance(pass_key, str)):
            raise self.ORClientException('All parameters should be an instance or subclass of str.')

        api_url = api_url.strip()
        if not api_url.endswith('/'):
            api_url += '/'

        if not api_url.endswith('/v2/'):
            api_url += 'v2/'

        # ORClient properties.
        self._api_url = api_url
        self._user_key = user_key
        self._pass_key = pass_key

        self._instances = None

    @property
    def api_url(self):
        return self._api_url

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
            raise self.InstancesException('Parameter "client" must be an instance or subclass of ORClient.')

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
            raise self.InstancesException()

        url = self.api_instances_url + instance_name + '/compact/'

        if request_compaction:
            request = requests.post(url, data={}, auth=(self.client.user_key, self.client.pass_key))
        else:
            request = requests.get(url, auth=(self.client.user_key, self.client.pass_key))

        return request.json()

    def create(self, name, size, zone, service_type='mongodb', version='2.4.6'):
        if not isinstance(name, str):
            raise self.InstancesException()

        if not isinstance(zone, str):
            raise self.InstancesException()

        if not isinstance(size, int):
            raise self.InstancesException()

        if service_type not in ('mongodb',):
            raise self.InstancesException()

        if version not in ('2.4.6',):
            raise self.InstancesException()

        url = self.api_instances_url
        data = {
            'name': name,
            'size': size,
            'zone': zone,
            'type': service_type,
            'version': version,
        }

        request = requests.post(url, data=data, auth=(self.client.user_key, self.client.pass_key))
        return request.json()

    def get(self, instance_name=None):
        if instance_name is not None and not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance or subclass of str.')

        url = self.api_instances_url
        if instance_name is not None:
            url = self.api_instances_url + instance_name + '/'

        request = requests.get(url, auth=(self.client.user_key, self.client.pass_key))
        return request.json()

    def stepdown_window(self, instance_name):
        if not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance or subclass of str.')

        url = self.api_instances_url + instance_name + '/stepdown/'

        request = requests.get(url, auth=(self.client.user_key, self.client.pass_key))
        return request.json()

    def set_stepdown_window(self, instance_name, start, end, enabled, scheduled, weekly):
        # TODO: Finish this type checking.
        if not isinstance(instance_name, str):
            raise self.InstancesException('Parameter "instance_name" must be an instance or subclass of str.')
        if not isinstance(start, float):
            raise self.InstancesException()
        if not isinstance(end, float):
            raise self.InstancesException()
        if not isinstance(enabled, bool):
            raise self.InstancesException()
        if not isinstance(scheduled, bool):
            raise self.InstancesException()
        if not isinstance(weekly, bool):
            raise self.InstancesException()

        url = self.api_instances_url + instance_name + '/stepdown/'

        data = {
            'start': start,
            'end': end,
            'enabled': enabled,
            'scheduled': scheduled,
            'weekly': weekly,
        }

        request = requests.post(url, data=data, auth=(self.client.user_key, self.client.pass_key))
        return request.json()

    class InstancesException(Exception):
        pass

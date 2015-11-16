"""ACL operations and objects."""
import copy
import json
import logging

import requests

from objectrocket import bases
from objectrocket import util

logger = logging.getLogger(__name__)


class Acls(bases.BaseOperationsLayer):
    """ACL operations.

    :param objectrocket.client.Client base_client: An instance of objectrocket.client.Client.
    """

    def __init__(self, base_client):
        super(Acls, self).__init__(base_client=base_client)

    #####################
    # Public interface. #
    #####################
    @util.token_auto_auth
    def all(self, instance):
        """Get all ACLs associated with the instance specified by name.

        :param str instance: The name of the instance from which to fetch ACLs.
        :returns: A list of :py:class:`Acl` objects associated with the specified instance.
        :rtype: list
        """
        url = self._url.format(instance=instance)
        response = requests.get(url, **self._default_request_kwargs)
        data = self._get_response_data(response)
        return self._concrete_acl_list(data)

    @util.token_auto_auth
    def create(self, instance, cidr_mask, description, **kwargs):
        """Create an ACL entry for the specified instance.

        :param str instance: The name of the instance to associate the new ACL entry with.
        :param str cidr_mask: The IPv4 CIDR mask for the new ACL entry.
        :param str description: A short description for the new ACL entry.
        :param collector kwargs: (optional) Additional key=value pairs to be supplied to the
            creation payload. **Caution:** fields unrecognized by the API will cause this request
            to fail with a 400 from the API.
        """
        # Build up request data.
        url = self._url.format(instance=instance)
        request_data = {
            'cidr_mask': cidr_mask,
            'description': description
        }
        request_data.update(kwargs)

        # Call to create an instance.
        response = requests.post(
            url,
            data=json.dumps(request_data),
            **self._default_request_kwargs
        )

        # Log outcome of instance creation request.
        if response.status_code == 200:
            logger.info('Successfully created a new ACL for instance {} with: {}.'
                        .format(instance, request_data))
        else:
            logger.info('Failed to create a new ACL for instance {} with: {}.'
                        .format(instance, request_data))

        data = self._get_response_data(response)
        return self._concrete_acl(data)

    @util.token_auto_auth
    def get(self, instance, acl):
        """Get an ACL by ID belonging to the instance specified by name.

        :param str instance: The name of the instance from which to fetch the ACL.
        :param str acl: The ID of the ACL to fetch.
        :returns: An :py:class:`Acl` object, or None if ACL does not exist.
        :rtype: :py:class:`Acl`
        """
        base_url = self._url.format(instance=instance)
        url = '{base}{aclid}/'.format(base=base_url, aclid=acl)
        response = requests.get(url, **self._default_request_kwargs)
        data = self._get_response_data(response)
        return self._concrete_acl(data)

    ######################
    # Private interface. #
    ######################
    def _concrete_acl(self, acl_doc):
        """Concretize an ACL document.

        :param dict acl_doc: A document describing an ACL entry. Should come from the API.
        :returns: An :py:class:`Acl`, or None.
        :rtype: :py:class:`bases.BaseInstance`
        """
        if not isinstance(acl_doc, dict):
            return None

        # Attempt to instantiate an Acl object with the given dict.
        try:
            return Acl(document=acl_doc, acls=self)

        # If construction fails, log the exception and return None.
        except Exception as ex:
            logger.exception(ex)
            logger.error('Could not instantiate ACL document. You probably need to upgrade to a '
                         'recent version of the client. Document which caused this error: {}'
                         .format(acl_doc))
            return None

    def _concrete_acl_list(self, acl_docs):
        """Concretize a list of ACL documents.

        :param list acl_docs: A list of ACL documents. Should come from the API.
        :returns: A list of :py:class:`ACL` objects.
        :rtype: list
        """
        if not acl_docs:
            return []

        return list(filter(None, [self._concrete_acl(acl_doc=doc) for doc in acl_docs]))

    @property
    def _default_request_kwargs(self):
        """The default request keyword arguments to be passed to the requests library."""
        defaults = copy.deepcopy(super(Acls, self)._default_request_kwargs)
        defaults.setdefault('headers', {}).update({
            'X-Auth-Token': self._client.auth._token
        })
        return defaults

    @property
    def _url(self):
        """The base URL for ACL operations."""
        base_url = self._client._url.rstrip('/')
        return '{}/instances/{{instance}}/acls/'.format(base_url)


class Acl(object):
    """An Access Control List entry object.

    :param document dict: The dict representing this object.
    :param Acls acls: The Acls operations layer instance from which this object came.
    """

    def __init__(self, document, acls):
        self.__client = acls._client
        self.__acls = acls
        self.__document = document

        # Bind required pseudo private attributes from API response document.
        self._cidr_mask = document['cidr_mask']
        self._description = document['description']
        self._id = document['id']
        self._instance_name = document['instance']
        self._login = document['login']
        self._port = document['port']

        # Bind attributes which may be present in API response document.
        self._date_created = document.get('date_created', None)
        self._instance = document.get('instance_id', None)
        self._instance_type = document.get('instance_type', None)
        self._metadata = document.get('metadata', {})
        self._service_type = document.get('service_type', None)

    def __repr__(self):
        """Represent this object as a string."""
        _id = hex(id(self))
        rep = (
            '<{!s} cidr={!s} port={!s} instance={!s} id={!s} at {!s}>'
            .format(self.__class__.__name__, self.cidr_mask, self.port,
                    self.instance_name, self.id, _id)
        )
        return rep

    @property
    def cidr_mask(self):
        """This ACL entry's CIDR mask."""
        return self._cidr_mask

    @property
    def date_created(self):
        """The date which this ACL entry was created on."""
        return self._date_created

    @property
    def description(self):
        """This ACL entry's description."""
        return self._description

    @property
    def _document(self):
        """This ACL entry's document."""
        return self.__document

    @property
    def id(self):
        """This ACL entry's ID."""
        return self._id

    @property
    def instance(self):
        """The ID of the instance to which this ACL entry is associated."""
        return self._instance

    @property
    def instance_name(self):
        """The name of the instance to which this ACL entry is associated."""
        return self._instance_name

    @property
    def instance_type(self):
        """The type of the instance to which this ACL entry is associated."""
        return self._instance_type

    @property
    def login(self):
        """The login of the user to which this ACL entry belongs."""
        return self._login

    @property
    def metadata(self):
        """This ACL entry's metadata."""
        return self._metadata

    @property
    def port(self):
        """This ACL entry's port number."""
        return self._port

    @property
    def service_type(self):
        """The service of the instance to which this ACL entry is associated."""
        return self._service_type

    def to_dict(self):
        """Render this object as a dictionary."""
        return self._document

    ######################
    # Private interface. #
    ######################
    @property
    def _client(self):
        """An instance of the objectrocket.client.Client."""
        return self.__client

    @property
    def _url(self):
        """The URL of this ACL object."""
        base_url = self._client._url.rstrip('/')
        return '{}/instances/{}/acls/{}/'.format(base_url, self.instance_name, self.id)

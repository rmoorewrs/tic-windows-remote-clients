# Copyright 2011 Nebula, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import logging
import warnings

from keystoneclient.auth.identity import v2 as v2_auth
from keystoneclient import exceptions
from keystoneclient import httpclient
from keystoneclient.i18n import _
from keystoneclient.v2_0 import certificates
from keystoneclient.v2_0 import ec2
from keystoneclient.v2_0 import endpoints
from keystoneclient.v2_0 import extensions
from keystoneclient.v2_0 import roles
from keystoneclient.v2_0 import services
from keystoneclient.v2_0 import tenants
from keystoneclient.v2_0 import tokens
from keystoneclient.v2_0 import users

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3 import disable_warnings as urllib3_disable_warnings

_logger = logging.getLogger(__name__)


class Client(httpclient.HTTPClient):
    """Client for the OpenStack Keystone v2.0 API.

    :param string username: Username for authentication. (optional)
    :param string password: Password for authentication. (optional)
    :param string token: Token for authentication. (optional)
    :param string tenant_id: Tenant id. (optional)
    :param string tenant_name: Tenant name. (optional)
    :param string auth_url: Keystone service endpoint for authorization.
    :param string region_name: Name of a region to select when choosing an
                               endpoint from the service catalog.
    :param string endpoint: A user-supplied endpoint URL for the keystone
                            service.  Lazy-authentication is possible for API
                            service calls if endpoint is set at
                            instantiation.(optional)
    :param integer timeout: Allows customization of the timeout for client
                            http requests. (optional)
    :param string original_ip: The original IP of the requesting user
                               which will be sent to Keystone in a
                               'Forwarded' header. (optional)
    :param string cert: Path to the Privacy Enhanced Mail (PEM) file which
                        contains the corresponding X.509 client certificate
                        needed to established two-way SSL connection with
                        the identity service. (optional)
    :param string key: Path to the Privacy Enhanced Mail (PEM) file which
                       contains the unencrypted client private key needed
                       to established two-way SSL connection with the
                       identity service. (optional)
    :param string cacert: Path to the Privacy Enhanced Mail (PEM) file which
                          contains the trusted authority X.509 certificates
                          needed to established SSL connection with the
                          identity service. (optional)
    :param boolean insecure: Does not perform X.509 certificate validation
                             when establishing SSL connection with identity
                             service. default: False (optional)
    :param dict auth_ref: To allow for consumers of the client to manage their
                          own caching strategy, you may initialize a client
                          with a previously captured auth_reference (token)
    :param boolean debug: Enables debug logging of all request and responses
                          to keystone. default False (option)

    .. warning::

        If debug is enabled, it may show passwords in plain text as a part of
        its output.

    .. warning::

        Constructing an instance of this class without a session is
        deprecated as of the 1.7.0 release and will be removed in the
        2.0.0 release.

    The client can be created and used like a user or in a strictly
    bootstrap mode. Normal operation expects a username, password, auth_url,
    and tenant_name or id to be provided. Other values will be lazily loaded
    as needed from the service catalog.

    Example::

        >>> from keystoneauth1.identity import v2
        >>> from keystoneauth1 import session
        >>> from keystoneclient.v2_0 import client
        >>> auth = v2.Password(auth_url=KEYSTONE_URL,
        ...                    username=USER,
        ...                    password=PASS,
        ...                    tenant_name=TENANT_NAME)
        >>> sess = session.Session(auth=auth)
        >>> keystone = client.Client(session=sess)
        >>> keystone.tenants.list()
        ...
        >>> user = keystone.users.get(USER_ID)
        >>> user.delete()

    Once authenticated, you can store and attempt to re-use the
    authenticated token. the auth_ref property on the client
    returns as a dictionary-like-object so that you can export and
    cache it, re-using it when initiating another client::

        >>> from keystoneauth1.identity import v2
        >>> from keystoneauth1 import session
        >>> from keystoneclient.v2_0 import client
        >>> auth = v2.Password(auth_url=KEYSTONE_URL,
        ...                    username=USER,
        ...                    password=PASS,
        ...                    tenant_name=TENANT_NAME)
        >>> sess = session.Session(auth=auth)
        >>> keystone = client.Client(session=sess)
        >>> auth_ref = keystone.auth_ref
        >>> # pickle or whatever you like here
        >>> new_client = client.Client(auth_ref=auth_ref)

    Alternatively, you can provide the administrative token configured in
    keystone and an endpoint to communicate with directly. See
    (``admin_token`` in ``keystone.conf``) In this case, authenticate()
    is not needed, and no service catalog will be loaded.

    Example::

        >>> from keystoneauth1.identity import v2
        >>> from keystoneauth1 import session
        >>> from keystoneclient.v2_0 import client
        >>> auth = v2.Token(auth_url='http://localhost:35357/v2.0',
        ...                 token='12345secret7890')
        >>> sess = session.Session(auth=auth)
        >>> keystone = client.Client(session=sess)
        >>> keystone.tenants.list()

    """

    version = 'v2.0'

    def __init__(self, **kwargs):
        """Initialize a new client for the Keystone v2.0 API."""
        if not kwargs.get('session'):
            warnings.warn(
                'Constructing an instance of the '
                'keystoneclient.v2_0.client.Client class without a session is '
                'deprecated as of the 1.7.0 release and may be removed in '
                'the 2.0.0 release.', DeprecationWarning)

        # NOTE(knasim-wrs): As per US76645, the Keystone adminURL
        # is no longer an internal address since it needs to be
        # accessible via remote Openstack client. Things get
        # complicated with HTTPS where the internal keystone client
        # gets this adminURL and cannot connect to Keystone server
        # as it cannot verify the SSL certificate.
        # We will check for this condition here, if OS_ENDPOINT_TYPE
        # is not publicURL then this is an internal access scenario and
        # Keystone client will be set to SSL insecure mode
        if os.environ.get('OS_ENDPOINT_TYPE') == 'internalURL':
            kwargs['insecure'] = True
            # disable verbose insecurity warnings
            urllib3_disable_warnings(InsecureRequestWarning)

        super(Client, self).__init__(**kwargs)

        self.certificates = certificates.CertificatesManager(self._adapter)
        self.endpoints = endpoints.EndpointManager(self._adapter)
        self.extensions = extensions.ExtensionManager(self._adapter)
        self.roles = roles.RoleManager(self._adapter)
        self.services = services.ServiceManager(self._adapter)
        self.tokens = tokens.TokenManager(self._adapter)
        self.users = users.UserManager(self._adapter, self.roles)

        self.tenants = tenants.TenantManager(self._adapter,
                                             self.roles, self.users)

        # extensions
        self.ec2 = ec2.CredentialsManager(self._adapter)

        # DEPRECATED: if session is passed then we go to the new behaviour of
        # authenticating on the first required call.
        if not kwargs.get('session') and self.management_url is None:
            self.authenticate()

    def get_raw_token_from_identity_service(self, auth_url, username=None,
                                            password=None, tenant_name=None,
                                            tenant_id=None, token=None,
                                            project_name=None, project_id=None,
                                            trust_id=None,
                                            **kwargs):
        """Authenticate against the v2 Identity API.

        If a token is provided it will be used in preference over username and
        password.

        :returns: access.AccessInfo if authentication was successful.
        :raises keystoneclient.exceptions.AuthorizationFailure: if unable to
            authenticate or validate the existing authorization token
        """
        try:
            if auth_url is None:
                raise ValueError(_("Cannot authenticate without an auth_url"))

            new_kwargs = {'trust_id': trust_id,
                          'tenant_id': project_id or tenant_id,
                          'tenant_name': project_name or tenant_name}

            if token:
                plugin = v2_auth.Token(auth_url, token, **new_kwargs)
            elif username and password:
                plugin = v2_auth.Password(auth_url, username, password,
                                          **new_kwargs)
            else:
                msg = _('A username and password or token is required.')
                raise exceptions.AuthorizationFailure(msg)

            return plugin.get_auth_ref(self.session)
        except (exceptions.AuthorizationFailure, exceptions.Unauthorized):
            _logger.debug("Authorization Failed.")
            raise
        except exceptions.EndpointNotFound:
            msg = (
                _('There was no suitable authentication url for this request'))
            raise exceptions.AuthorizationFailure(msg)
        except Exception as e:
            raise exceptions.AuthorizationFailure(
                _("Authorization Failed: %s") % e)

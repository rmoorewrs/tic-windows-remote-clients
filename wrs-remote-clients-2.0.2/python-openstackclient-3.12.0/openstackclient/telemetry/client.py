#   Copyright 2012-2018 OpenStack Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
#  Copyright (c) 2013-2018 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#

# WRS extension


from osc_lib import utils
from openstackclient.i18n import _

import logging
LOG = logging.getLogger(__name__)

DEFAULT_API_VERSION = '2'
API_VERSION_OPTION = 'telemetry_api_version'
API_NAME = "telemetry"
API_VERSIONS = {
    "2": "ceilometerclient.v2.client.Client",
}


def make_client(instance):
    """Returns an ceilometer service client"""
    ceilometer_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)
    LOG.debug('Instantiating ceilometer client: %s', ceilometer_client)

    # Remember interface only if interface is set
    kwargs = utils.build_kwargs_dict('endpoint_type', instance.interface)

    client = ceilometer_client(
        session=instance.session,
        region_name=instance.region_name,
        **kwargs
    )

    return client


def build_option_parser(parser):
    """Hook to add global options"""
    parser.add_argument(
        '--os-telemetry-api-version',
        metavar='<telemetry-api-version>',
        default=utils.env('TELEMETRY_API_VERSION'),
        help=_('Ceilometer API version, default=%s (Env: TELEMETRY_API_VERSION)') %
        DEFAULT_API_VERSION,
    )
    return parser

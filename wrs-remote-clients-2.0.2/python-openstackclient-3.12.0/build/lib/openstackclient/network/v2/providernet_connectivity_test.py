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
# Copyright (c) 2016 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#

"""Providernet connectivity test action implementations"""

import itertools
from osc_lib import exceptions
from osc_lib import utils
from openstackclient.network import common
from openstackclient.network import sdk_utils

_formatters = {
}


def _get_columns(item):
    column_map = {}
    invisible_columns = ["host_id", "host_name", "id", "message", "name",
                         "providernet_id", "providernet_name",
                         "segmentation_id", "status", "type", "updated_at"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           invisible_columns)


def _get_attrs(client_manager, parsed_args, client):
    attrs = {key: parsed_args[key] for key in
             ["providernet", "host", "segmentation_id", "audit_uuid"]
             if key in parsed_args and parsed_args[key] is not None}
    if "providernet" in attrs:
        providernet = client.find_providernet(attrs.pop("providernet"),
                                              ignore_missing=False)
        attrs["providernet_id"] = providernet.id
    if "host" in attrs:
        host = client.find_host(attrs.pop("host"), ignore_missing=False)
        attrs["host_id"] = host.id
    return attrs


# copied from neutron client and modified to fit data formats here
def _list_segments(segments):
        """Takes a list of segments, and outputs them as a string"""
        msg = ", ".join([str(x or "*") for x in sorted(segments)])
        return msg


# copied from neutron client and modified to fit data formats here
def _group_segmentation_id_list(segmentation_ids):
    """Takes a list of integers and groups them into ranges"""
    if len(segmentation_ids) < 1:
        return ""
    try:
        sorted_segmentation_ids = sorted(
            [int(segmentation_id) for segmentation_id in segmentation_ids]
        )
    except Exception:
        return _list_segments(segmentation_ids)
    grouped_ids = [tuple(g[1]) for g in itertools.groupby(
        enumerate(sorted_segmentation_ids), lambda (i, n): i - n
    )]
    msg = ", ".join(
        [(("%s-%s" % (g[0][1], g[-1][1])) if g[0][1] != g[-1][1]
         else ("%s" % g[0][1])) for g in grouped_ids]
    )
    return msg


# copied from neutron client and modified to fit data formats here
def _format_connectivity_results(data):
    """Takes a list of results, and formats them for reporting

       order assumed: providernet_id, providernet_name, type, host_name,
                      segmentation_id, status, message
    """

    parsed_results = {}
    has_message = False
    for result in data:
        providernet_id = result.providernet_id
        providernet_name = result.providernet_name
        providernet_type = result.type
        hostname = result.host_name
        if hasattr(result, "segmentation_id"):
            segmentation_id = result.segmentation_id
        else:
            segmentation_id = None
        status = result.status
        message = result.message
        if message:
            has_message = True
        test = (providernet_id, providernet_name, providernet_type,
                hostname, status, message)
        if test not in parsed_results:
            parsed_results[test] = []
        parsed_results[test].append(segmentation_id)

    formatted_results = []
    for test, results in parsed_results.iteritems():
        (providernet_id, providernet_name, providernet_type,
         hostname, status, message) = test
        formatted_segmentation_ids = \
            _group_segmentation_id_list(results)

        if has_message:
            formatted_result = (providernet_id,
                                providernet_name,
                                providernet_type,
                                hostname,
                                formatted_segmentation_ids,
                                status,
                                message
                                )
        else:
            formatted_result = (providernet_id,
                                providernet_name,
                                providernet_type,
                                hostname,
                                formatted_segmentation_ids,
                                status
                                )
        formatted_results.append(formatted_result)

    return tuple(formatted_results), has_message


class ListProvidernetConnectivityTest(common.NetworkAndComputeLister):
    """List providernet connectivity tests"""

    def update_parser_common(self, parser):
        parser.add_argument(
            '--audit-uuid',
            dest='audit_uuid', default=None,
            help='List only for this audit-uuid')
        parser.add_argument(
            '--providernet',
            dest='providernet', default=None,
            help='List only for this providernet')
        parser.add_argument(
            '--host',
            dest='host', default=None,
            help='List only for this host')
        parser.add_argument(
            '--segmentation-id',
            dest='segmentation_id', default=None,
            help='List only for this segmentation-id')
        return parser

    def take_action_network(self, client, parsed_args):
        column_headers = (
            'Providernet ID',
            'Providernet Name',
            'Type',
            'Host Name',
            'Segmentation IDs',
            'Status'
        )
        args = _get_attrs(self.app.client_manager, vars(parsed_args), client)

        data = client.providernet_connectivity_tests(**args)
        formatted_data, has_message = _format_connectivity_results(data)

        # replicate behavior from neutron command:
        # dont show message column if it does not exist
        if has_message:
            column_headers = column_headers + ('Message',)

        return (column_headers,
                formatted_data)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class CreateProvidernetConnectivityTest(common.NetworkAndComputeShowOne):
    """Create new providernet connectivity test"""

    def update_parser_common(self, parser):
        parser.add_argument(
            '--providernet',
            dest='providernet', default=None,
            help=('Schedule audit for given providernet'))
        parser.add_argument(
            '--host',
            dest='host', default=None,
            help='Schedule audits for all providernets on host')
        parser.add_argument(
            '--segmentation-id',
            dest='segmentation_id', default=None,
            help='Schedule for this segmentation ID')

        return parser

    def take_action_network(self, client, parsed_args):
        attrs = _get_attrs(self.app.client_manager, vars(parsed_args), client)
        obj = client.create_providernet_connectivity_test(**attrs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return

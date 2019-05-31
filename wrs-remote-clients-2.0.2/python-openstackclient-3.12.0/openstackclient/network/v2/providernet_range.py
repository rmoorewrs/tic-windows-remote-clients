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

"""Providernet range action implementations"""

import argparse
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from openstackclient.i18n import _
from openstackclient.identity import common as identity_common
from openstackclient.network import common
from openstackclient.network import sdk_utils

_formatters = {
    'vxlan': utils.format_dict
}


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def _get_attrs(client_manager, parsed_args):
    attrs = {key: parsed_args[key] for key in
             ["shared", "description", "name", "group", "ttl", "port", "mode",
              "providernet_id", "providernet_range_id"]
             if key in parsed_args}
    if "range" in parsed_args and parsed_args["range"] is not None:
        attrs["maximum"] = parsed_args["range"]["maximum"]
        attrs["minimum"] = parsed_args["range"]["minimum"]
    if "port" in attrs and attrs["port"] is None:
        del attrs["port"]
    if "ttl" in attrs and attrs["ttl"] is None:
        del attrs["ttl"]
    if "group" in attrs and attrs["group"] is None:
        del attrs["group"]
    if "mode" in attrs and attrs["mode"] is None:
        del attrs["mode"]
    if 'project' in parsed_args and parsed_args["project"] is not None:
        identity_client = client_manager.identity
        project_id = identity_common.find_project(
            identity_client,
            parsed_args["project"]
        ).id
        # TODO(dtroyer): Remove tenant_id when we clean up the SDK refactor
        attrs['tenant_id'] = project_id
        attrs['project_id'] = project_id

    return attrs


def _id_range_value(value):
    range_list = value.split('-')
    if (len(range_list) != 2):
        raise argparse.ArgumentTypeError(
            'Expecting MIN_VALUE-MAX_VALUE in range list')
    return {'minimum': range_list[0],
            'maximum': range_list[1]}


class ListProvidernetRange(common.NetworkAndComputeLister):
    """List providernet ranges"""

    def update_parser_common(self, parser):
        parser.add_argument(
            '--project',
            metavar='<project>',
            help=_("Owner's project (name or ID)")
        )
        return parser

    def take_action_network(self, client, parsed_args):
        columns = (
            'id',
            'name',
            'providernet_name',
            'providernet_type',
            'minimum',
            'maximum',
            'vxlan'
        )
        column_headers = (
            'ID',
            'Name',
            'Providernet',
            'Type',
            'Minimum',
            'Maximum',
            'Attributes'
        )

        args = _get_attrs(self.app.client_manager, vars(parsed_args))

        data = client.providernet_ranges(**args)

        return (column_headers,
                (utils.get_item_properties(
                    s, columns,
                    formatters=_formatters,
                ) for s in data))

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class ShowProvidernetRange(common.NetworkAndComputeShowOne):
    """Show providernet range details"""

    def update_parser_common(self, parser):
        parser.add_argument(
            'providernet_range',
            metavar="<providernet range>",
            help=("Providernet range to display (name or ID)")
        )
        return parser

    def take_action_network(self, client, parsed_args):
        obj = client.find_providernet_range(parsed_args.providernet_range,
                                            ignore_missing=False)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class CreateProvidernetRange(common.NetworkAndComputeShowOne):
    """Create new providernet range"""

    def update_parser_common(self, parser):
        parser.add_argument(
            '--shared',
            dest='shared', action='store_true', default=False,
            help=('Set whether a provider network segmentation id range '
                  'may be shared between tenants'))
        parser.add_argument(
            '--project',
            metavar='<project>',
            help=_("Owner's project (name or ID)")
        )
        identity_common.add_project_domain_option_to_parser(parser)
        parser.add_argument(
            '--description',
            dest='description',
            help='Set user-defined description field for a provider network')
        parser.add_argument(
            '--range', metavar='MIN_VALUE-MAX_VALUE', required=True,
            dest='range', type=_id_range_value,
            help='Segmentation id value range')
        parser.add_argument(
            '--name', required=True,
            dest='name',
            help=('Set user-defined name for a provider network '
                  'segmentation id range'))
        parser.add_argument(
            '--group',
            dest='group',
            help='Multicast IP addresses for VXLAN endpoints')
        parser.add_argument(
            '--ttl', dest='ttl', type=int,
            help='Time-to-live value for VXLAN provider networks')
        parser.add_argument(
            '--port', dest='port', type=int,
            help=('Destination UDP port value to use for '
                  'VXLAN provider networks'))
        parser.add_argument(
            '--mode',
            dest='mode', default='dynamic',
            choices=['dynamic', 'static', 'evpn'],
            help='Set vxlan learning mode')
        parser.add_argument(
            'providernet_id', metavar='PROVIDERNET',
            help='Provider network this segmentation id range belongs to')

        return parser

    def take_action_network(self, client, parsed_args):
        attrs = _get_attrs(self.app.client_manager, vars(parsed_args))
        obj = client.find_providernet(parsed_args.providernet_id,
                                      ignore_missing=False)
        attrs["providernet_id"] = obj.id
        obj = client.create_providernet_range(**attrs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class DeleteProvidernetRange(common.NetworkAndComputeDelete):
    """Delete providernet range"""

    # Used by base class to find resources in parsed_args.
    resource = 'providernet_range'
    r = None

    def update_parser_common(self, parser):
        parser.add_argument(
            'providernet_range',
            metavar="<providernet_range>",
            nargs="+",
            help=("Providernet to Delete (name or ID)")
        )
        return parser

    def take_action_network(self, client, parsed_args):
        obj = client.find_providernet_range(self.r)
        client.delete_providernet_range(obj)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class UpdateProvidernetRange(command.Command):
    """Set providernet range properties"""

    def get_parser(self, prog_name):
        parser = super(UpdateProvidernetRange, self).get_parser(prog_name)
        parser.add_argument(
            '--description',
            dest='description',
            help='Set user-defined description field for a provider network')
        parser.add_argument(
            '--range', metavar='MIN_VALUE-MAX_VALUE',
            dest='range', type=_id_range_value,
            help='Segmentation id value range')
        parser.add_argument(
            'providernet_range_id', metavar='PROVIDERNET_RANGE',
            help='Name or ID of this providernet range')
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.network
        obj = client.find_providernet_range(parsed_args.providernet_range_id,
                                            ignore_missing=False)

        attrs = _get_attrs(self.app.client_manager, vars(parsed_args))
        del attrs['providernet_range_id']

        if attrs == {}:
            msg = "Nothing specified to be set"
            raise exceptions.CommandError(msg)
        client.update_providernet_range(obj, **attrs)
        return

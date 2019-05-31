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

"""Providernet action implementations"""

import argparse

from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from openstackclient.network import common
from openstackclient.network import sdk_utils


def add_boolean_argument(parser, name, **kwargs):
    for keyword in ('metavar', 'choices'):
        kwargs.pop(keyword, None)
    default = kwargs.pop('default', argparse.SUPPRESS)
    parser.add_argument(
        name,
        metavar='{True,False}',
        choices=['True', 'true', 'False', 'false'],
        default=default,
        **kwargs)


def _format_ranges(item):
    item = utils.format_list_of_dicts(item)
    # we want to remove some fields
    # to match the output to neutron providernet-list
    separator = ', '
    item = item.split(separator)
    item = [s for s in item if "name" in s or "maximum" in s or "minimum" in s]

    return separator.join(item)

# the providernet list command does not display some values in the ranges field
_filtered_ranges_formatters = {
    'ranges': _format_ranges
}

_formatters = {
    'ranges': utils.format_list_of_dicts
}

_net_list_on_providernet_formatters = {
    'vxlan': utils.format_dict
}


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def _get_attrs(client_manager, parsed_args):
    attrs = {key: parsed_args[key] for key in
             ["name", "type", "vlan_transparent", "description", "mtu"]
             if key in parsed_args}
    if "mtu" in attrs and attrs["mtu"] is None:
        del attrs["mtu"]

    return attrs


class ListProvidernet(common.NetworkAndComputeLister):
    """List providernets"""

    def update_parser_common(self, parser):
        parser.add_argument(
            '--type',
            dest='type',
            help='List all providernets of type')
        return parser

    def take_action_network(self, client, parsed_args):
        columns = (
            'id',
            'name',
            'type',
            'mtu',
            'ranges'
        )
        column_headers = (
            'ID',
            'Name',
            'Type',
            'MTU',
            'Ranges'
        )

        args = _get_attrs(self.app.client_manager, vars(parsed_args))

        data = client.providernets(**args)

        return (column_headers,
                (utils.get_item_properties(
                    s, columns,
                    formatters=_filtered_ranges_formatters,
                ) for s in data))

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class ShowProvidernet(common.NetworkAndComputeShowOne):
    """Show providernet details"""

    def update_parser_common(self, parser):
        parser.add_argument(
            'providernet',
            metavar="<providernet>",
            help=("Providernet to display (name or ID)")
        )
        return parser

    def take_action_network(self, client, parsed_args):
        obj = client.find_providernet(parsed_args.providernet,
                                      ignore_missing=False)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class CreateProvidernet(common.NetworkAndComputeShowOne):
    """Create new providernet"""

    def update_parser_common(self, parser):
        parser.add_argument(
            '--description',
            dest='description',
            help='Set user-defined description field for a provider network')
        parser.add_argument(
            '--type', required=True,
            dest='type', default='flat',
            choices=['flat', 'vlan', 'vxlan'],
            help='Set network type for a provider network')
        parser.add_argument(
            '--mtu', dest='mtu', type=int,
            help='Maximum transmit unit on provider network')
        add_boolean_argument(
            parser,
            '--vlan-transparent',
            default='False',
            help='Allow VLAN tagged packets on tenant networks')
        parser.add_argument(
            'name', metavar='NAME',
            help='Set user-defined name for a provider network')

        return parser

    def take_action_network(self, client, parsed_args):
        attrs = _get_attrs(self.app.client_manager, vars(parsed_args))
        obj = client.create_providernet(**attrs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class DeleteProvidernet(common.NetworkAndComputeDelete):
    """Delete providernet"""

    # Used by base class to find resources in parsed_args.
    resource = 'providernet'
    r = None

    def update_parser_common(self, parser):
        parser.add_argument(
            'providernet',
            metavar="<providernet>",
            nargs="+",
            help=("Providernet to delete (name or ID)")
        )
        return parser

    def take_action_network(self, client, parsed_args):
        obj = client.find_providernet(self.r)
        client.delete_providernet(obj)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class UpdateProvidernet(command.Command):
    """Set providernet properties"""

    def get_parser(self, prog_name):
        parser = super(UpdateProvidernet, self).get_parser(prog_name)
        parser.add_argument(
            '--description',
            dest='description',
            help='Set user-defined description field for a provider network')
        parser.add_argument(
            '--mtu', dest='mtu', type=int,
            help='Maximum transmit unit on provider network')
        add_boolean_argument(
            parser,
            '--vlan-transparent',
            help='Allow VLAN tagged packets on tenant networks')
        parser.add_argument(
            'providernet', metavar='PROVIDERNET',
            help='Set user-defined name for a provider network')

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.network

        obj = client.find_providernet(parsed_args.providernet,
                                      ignore_missing=False)
        attrs = _get_attrs(self.app.client_manager, vars(parsed_args))
        if attrs == {}:
            msg = "Nothing specified to be set"
            raise exceptions.CommandError(msg)

        client.update_providernet(obj, **attrs)
        return


class NetListOnProvidernet(common.NetworkAndComputeLister):
    """List the networks on a provider network."""

    def update_parser_common(self, parser):
        parser.add_argument(
            'providernet',
            metavar="<providernet>",
            help=("Providernet to display (name or ID)")
        )
        return parser

    def take_action_network(self, client, parsed_args):
        obj = client.find_providernet(parsed_args.providernet,
                                      ignore_missing=False)
        providernet_id = obj.id

        columns = (
            'id',
            'name',
            'vlan_id',
            'providernet_type',
            'segmentation_id',
            'vxlan',
        )
        column_headers = (
            'ID',
            'Name',
            'VLAN ID',
            'Providernet Type',
            'Segmentation ID',
            'Providernet Attributes'
        )

        args = {}

        # cheated a bit here, doing the same request as a providernet list,
        # except using providernet_id/providernet-bindings
        # as the base path. Openstack client framwork does not support what
        # we need in terms of editing the address at the
        # time of implementing this
        data = client.net_list_on_providernet(providernet_id +
                                              "/providernet-bindings", **args)

        return (column_headers,
                (utils.get_item_properties(
                    s, columns,
                    formatters=_net_list_on_providernet_formatters,
                ) for s in data))

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return

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

"""Host action implementations"""

from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from openstackclient.network import common
from openstackclient.network import sdk_utils

_showhost_formatters = {
    'agents': utils.format_list_of_dicts
}

_listhost_formatters = {
    'agents': len
}


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def _get_attrs(client_manager, parsed_args):
    attrs = {key: parsed_args[key] for key in ['availability', 'id', 'name']
             if key in parsed_args and parsed_args[key] is not None}
    return attrs


class ListHost(common.NetworkAndComputeLister):
    """List host"""

    def update_parser_common(self, parser):
        return parser

    def take_action_network(self, client, parsed_args):
        columns = (
            'id',
            'name',
            'availability',
            'agents',
            'subnets',
            'routers',
            'ports'
        )
        column_headers = (
            'Id',
            'Name',
            'Availability',
            'Agents',
            'Subnets',
            'Routers',
            'Ports'
        )

        args = {}

        data = client.hosts(**args)

        return (column_headers,
                (utils.get_item_properties(
                    s, columns,
                    formatters=_listhost_formatters,
                ) for s in data))

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class ShowHost(common.NetworkAndComputeShowOne):
    """Show host details"""

    def update_parser_common(self, parser):
        parser.add_argument(
            'host',
            metavar="<HOST>",
            help=("ID or name of host to look up")
        )
        return parser

    def take_action_network(self, client, parsed_args):
        obj = client.find_host(parsed_args.host, ignore_missing=False)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns,
                                         formatters=_showhost_formatters)
        return (display_columns, data)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class CreateHost(common.NetworkAndComputeShowOne):
    """Create a host record"""

    def update_parser_common(self, parser):
        parser.add_argument('--availability', metavar="availability",
                            help='Set host availability status to up or down',
                            required=False)
        parser.add_argument('--id', metavar="id",
                            help='Create a new host record',
                            required=False)
        parser.add_argument('name', metavar='NAME',
                            help='System hostname of given host')
        return parser

    def take_action_network(self, client, parsed_args):
        attrs = _get_attrs(self.app.client_manager, vars(parsed_args))

        # the neutron equivalent command defaults to availability=down
        # when not specified
        if "availability" not in attrs:
            attrs['availability'] = "down"

        obj = client.create_host(**attrs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns,
                                         formatters=_listhost_formatters)
        return (display_columns, data)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class DeleteHost(common.NetworkAndComputeDelete):
    """Delete host"""

    # Used by base class to find resources in parsed_args.
    resource = 'name'
    r = None

    def update_parser_common(self, parser):
        parser.add_argument('name', metavar='NAME', nargs="+",
                            help='System hostname of given host')
        return parser

    def take_action_network(self, client, parsed_args):
        obj = client.find_host(self.r)
        client.delete_host(obj)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class UpdateHost(command.Command):
    """Set host properties"""

    def get_parser(self, prog_name):
        parser = super(UpdateHost, self).get_parser(prog_name)
        parser.add_argument('--availability', metavar="availability",
                            help='Set host availability status to up or down',
                            required=False)
        parser.add_argument('host', metavar='HOST',
                            help='System hostname of given host')
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.network
        obj = client.find_host(parsed_args.host, ignore_missing=False)
        attrs = _get_attrs(self.app.client_manager, vars(parsed_args))

        if attrs == {}:
            msg = "Nothing specified to be set"
            raise exceptions.CommandError(msg)
        client.update_host(obj, **attrs)
        return

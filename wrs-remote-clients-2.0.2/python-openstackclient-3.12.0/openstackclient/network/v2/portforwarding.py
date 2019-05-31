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

"""Port forwarding action implementations"""

import argparse
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from openstackclient.i18n import _
from openstackclient.identity import common as identity_common
from openstackclient.network import common
from openstackclient.network import sdk_utils

_formatters = {}


def _get_columns(item):
    column_map = {}
    invisible_columns = ["name"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           invisible_columns)


def _get_attrs(client_manager, parsed_args):
    attr_names = ['inside_addr', 'inside_port', 'outside_port',
                  'protocol', 'description', 'router_id']
    attrs = {key: parsed_args[key] for key in attr_names
             if key in parsed_args and parsed_args[key] is not None}

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


class ListPortforwarding(common.NetworkAndComputeLister):
    """List portforwarding"""

    def update_parser_common(self, parser):
        parser.add_argument(
            '--project',
            metavar='<project>',
            help=_("Owner's project (name or ID)")
        )
        parser.add_argument(
            '--router-id',
            metavar='<router_id>',
            help=_("Router's ID")
        )
        return parser

    def take_action_network(self, client, parsed_args):
        columns = (
            'id',
            'router_id',
            'inside_addr',
            'inside_port',
            'outside_port',
            'protocol',
        )
        column_headers = (
            'ID',
            'Router ID',
            'Inside Address',
            'Inside Port',
            'Outside Port',
            'Protocol'
        )

        args = _get_attrs(self.app.client_manager, vars(parsed_args))

        data = client.portforwardings(**args)

        return (column_headers,
                (utils.get_item_properties(
                    s, columns,
                    formatters=_formatters,
                ) for s in data))

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class ShowPortforwarding(common.NetworkAndComputeShowOne):
    """Show portforwarding details"""

    def update_parser_common(self, parser):
        parser.add_argument(
            'portforwarding',
            metavar="<portforwarding>",
            help=("Portforwarding to display (ID)")
        )
        return parser

    def take_action_network(self, client, parsed_args):
        obj = client.find_portforwarding(parsed_args.portforwarding,
                                         ignore_missing=False)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class CreatePortforwarding(common.NetworkAndComputeShowOne):
    """Create new portforwarding"""

    def update_parser_common(self, parser):
        parser.add_argument(
            '--inside-addr',
            help='Private IP address.')
        parser.add_argument(
            '--inside_addr',
            help=argparse.SUPPRESS)
        parser.add_argument(
            '--inside-port',
            help='Private layer4 protocol port.')
        parser.add_argument(
            '--inside_port',
            help=argparse.SUPPRESS)
        parser.add_argument(
            '--outside-port',
            help='Public layer4 protocol port.')
        parser.add_argument(
            '--outside_port',
            help=argparse.SUPPRESS)
        parser.add_argument(
            '--protocol',
            help='Layer4 protocol port number.')
        parser.add_argument(
            '--project',
            metavar='<project>',
            help=_("Owner's project (name or ID)")
        )
        identity_common.add_project_domain_option_to_parser(parser)
        parser.add_argument(
            '--description',
            help='User specified text description')
        parser.add_argument(
            'router_id', metavar='ROUTERID',
            help='Router instance identifier.')

        return parser

    def take_action_network(self, client, parsed_args):
        attrs = _get_attrs(self.app.client_manager, vars(parsed_args))
        router = client.find_router(attrs['router_id'], ignore_missing=False)
        attrs['router_id'] = router.id
        obj = client.create_portforwarding(**attrs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class DeletePortforwarding(common.NetworkAndComputeDelete):
    """Delete portforwarding"""

    # Used by base class to find resources in parsed_args.
    resource = 'portforwarding'
    r = None

    def update_parser_common(self, parser):
        parser.add_argument(
            'portforwarding',
            metavar="<portforwarding>",
            nargs="+",
            help=("Portforwarding to delete (ID)")
        )
        return parser

    def take_action_network(self, client, parsed_args):
        obj = client.find_portforwarding(self.r)
        client.delete_portforwarding(obj)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class UpdatePortforwarding(command.Command):
    """Set portforwarding properties"""

    def get_parser(self, prog_name):
        parser = super(UpdatePortforwarding, self).get_parser(prog_name)
        parser.add_argument(
            '--inside-addr',
            help='Private IP address.')
        parser.add_argument(
            '--inside_addr',
            help=argparse.SUPPRESS)
        parser.add_argument(
            '--inside-port',
            help='Private layer4 protocol port.')
        parser.add_argument(
            '--inside_port',
            help=argparse.SUPPRESS)
        parser.add_argument(
            '--outside-port',
            help='Public layer4 protocol port.')
        parser.add_argument(
            '--outside_port',
            help=argparse.SUPPRESS)
        parser.add_argument(
            '--protocol',
            help='Layer4 protocol port number.')
        parser.add_argument(
            '--description',
            help='User specified text description')
        parser.add_argument(
            'portforwarding', metavar='PORTFORWARDING',
            help='Portforwarding to delete (ID)')
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.network
        obj = client.find_portforwarding(parsed_args.portforwarding,
                                         ignore_missing=False)
        attrs = _get_attrs(self.app.client_manager, vars(parsed_args))

        if attrs == {}:
            msg = "Nothing specified to be set"
            raise exceptions.CommandError(msg)
        client.update_portforwarding(obj, **attrs)
        return

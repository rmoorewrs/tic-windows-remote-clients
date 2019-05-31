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

"""QOS action implementations"""

import argparse
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from openstackclient.i18n import _
from openstackclient.identity import common as identity_common
from openstackclient.network import common
from openstackclient.network import sdk_utils

_formatters = {}

TYPE_QOS_DSCP = "dscp"
TYPE_QOS_RATELIMIT = "ratelimit"
TYPE_QOS_SCHEDULER = "scheduler"


def _get_columns(item):
    column_map = {}
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def _args2body_policies(qos, type, policies):
    qos['policies'][type] = {}
    for parg in policies:
        if parg.count('=') != 1:
            raise exceptions.CommandError("Policies must be specified"
                                          " in the format a=b")
        args = parg.split('=')
        qos['policies'][type][args[0]] = args[1]


def _get_attrs(client_manager, parsed_args):
    attrs = {key: parsed_args[key] for key in
             ["name", "description"] if key in parsed_args}
    if "description" in attrs and attrs["description"] is None:
        del attrs["description"]
    attrs['policies'] = {}
    if "dscp" in parsed_args and parsed_args["dscp"] is not None:
        _args2body_policies(attrs, TYPE_QOS_DSCP,
                            parsed_args['dscp'])

    if "ratelimit" in parsed_args and parsed_args["ratelimit"] is not None:
        _args2body_policies(attrs, TYPE_QOS_RATELIMIT,
                            parsed_args['ratelimit'])

    if "scheduler" in parsed_args and parsed_args["scheduler"] is not None:
        _args2body_policies(attrs, TYPE_QOS_SCHEDULER,
                            parsed_args['scheduler'])

    if "project" in parsed_args and parsed_args["project"] is not None:
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


class ListQos(common.NetworkAndComputeLister):
    """List qos"""

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
            'description'
        )
        column_headers = (
            'ID',
            'Name',
            'Description'
        )

        args = _get_attrs(self.app.client_manager, vars(parsed_args))

        data = client.qoses(**args)

        return (column_headers,
                (utils.get_item_properties(
                    s, columns,
                    formatters=_formatters,
                ) for s in data))

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class ShowQos(common.NetworkAndComputeShowOne):
    """Show qos details"""

    def update_parser_common(self, parser):
        parser.add_argument(
            'qos',
            metavar="<QOS>",
            help=("Qos to display (name or ID)")
        )
        return parser

    def take_action_network(self, client, parsed_args):
        obj = client.find_qos(parsed_args.qos, ignore_missing=False)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class CreateQos(common.NetworkAndComputeShowOne):
    """Create new qos"""

    def update_parser_common(self, parser):
        parser.add_argument('--name', metavar='NAME',
                            help='Name of QoS policy')
        parser.add_argument(
            '--project',
            metavar='<project>',
            help=_("Owner's project (name or ID)")
        )
        identity_common.add_project_domain_option_to_parser(parser)
        parser.add_argument('--description', metavar='DESCRIPTION',
                            help="Description of QoS policy", required=False)
        parser.add_argument('--dscp', metavar="POLICY",
                            help='Set of policies for dscp',
                            nargs='+', required=False)
        parser.add_argument('--ratelimit', metavar="POLICY",
                            help='Set of policies for ratelimit',
                            nargs='+', required=False)
        parser.add_argument('--scheduler', metavar="POLICY",
                            help='Set of policies for scheduler',
                            nargs='+', required=False)
        return parser

    def take_action_network(self, client, parsed_args):
        attrs = _get_attrs(self.app.client_manager, vars(parsed_args))
        obj = client.create_qos(**attrs)
        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class DeleteQos(common.NetworkAndComputeDelete):
    """Delete qos"""

    # Used by base class to find resources in parsed_args.
    resource = 'qos'
    r = None

    def update_parser_common(self, parser):
        parser.add_argument(
            'qos',
            metavar="<qos>",
            nargs="+",
            help=("QOS to delete (name or ID)")
        )
        return parser

    def take_action_network(self, client, parsed_args):
        obj = client.find_qos(self.r)
        client.delete_qos(obj)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class UpdateQos(command.Command):
    """Set qos properties"""

    def get_parser(self, prog_name):
        parser = super(UpdateQos, self).get_parser(prog_name)
        parser.add_argument('--name', metavar='NAME',
                            help='Name of QoS policy')
        parser.add_argument('--description', metavar='DESCRIPTION',
                            help="Description of QoS policy", required=False)
        parser.add_argument('--dscp', metavar="POLICY",
                            help='Set of policies for dscp',
                            nargs='+', required=False)
        parser.add_argument('--ratelimit', metavar="POLICY",
                            help='Set of policies for ratelimit',
                            nargs='+', required=False)
        parser.add_argument('--scheduler', metavar="POLICY",
                            help='Set of policies for scheduler',
                            nargs='+', required=False)
        parser.add_argument(
            'qos',
            metavar="<qos>",
            help=("QOS to delete (name or ID)")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.network
        obj = client.find_qos(parsed_args.qos, ignore_missing=False)
        attrs = _get_attrs(self.app.client_manager, vars(parsed_args))

        if attrs == {}:
            msg = "Nothing specified to be set"
            raise exceptions.CommandError(msg)
        client.update_qos(obj, **attrs)
        return

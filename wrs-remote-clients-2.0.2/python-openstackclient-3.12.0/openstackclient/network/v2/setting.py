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

"""Settings action implementations"""

from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils
from openstackclient.i18n import _
from openstackclient.identity import common as identity_common
from openstackclient.network import common
from openstackclient.network import sdk_utils

_formatters = {}


def _get_columns(item):
    column_map = {"id": "project_id"}
    invisible_columns = ["name"]
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           invisible_columns)


def _get_attrs(client_manager, parsed_args):
    attrs = {key: parsed_args[key] for key in ["mac_filtering"]
             if key in parsed_args}

    if 'project' in parsed_args and parsed_args["project"] is not None:
        identity_client = client_manager.identity
        project_id = identity_common.find_project(
            identity_client,
            parsed_args["project"]
        ).id
        attrs['project_id'] = project_id

    return attrs


class ListSetting(common.NetworkAndComputeLister):
    """List settings of all projects who have non-default setting values"""

    def update_parser_common(self, parser):
        return parser

    def take_action_network(self, client, parsed_args):
        columns = (
            'mac_filtering',
            'project_id'
        )
        column_headers = (
            'Mac Filtering',
            'Project ID'
        )

        args = {}

        data = client.settings(**args)

        return (column_headers,
                (utils.get_item_properties(
                    s, columns,
                    formatters=_formatters,
                ) for s in data))

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


class ShowSetting(common.NetworkAndComputeShowOne):
    """Show settings of a given project"""

    def update_parser_common(self, parser):
        parser.add_argument(
            '--project',
            metavar='<project>',
            help=_("Owner's project (name or ID)"),
            required=False
        )
        return parser

    def take_action_network(self, client, parsed_args):
        client = self.app.client_manager.network
        # if no project id is specified, operate on current project
        args = _get_attrs(self.app.client_manager, vars(parsed_args))
        if not "project_id" in args:
            args["project_id"] = client.find_tenant().project_id
        project_id = args["project_id"]

        obj = client.find_setting(project_id, ignore_missing=False)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters=_formatters)
        return (display_columns, data)

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return


# this one uses NetworkAndComputeCommand because settings can be deleted
# without a project id
class DeleteSetting(common.NetworkAndComputeCommand):
    """Delete setting"""

    def update_parser_common(self, parser):
        parser.add_argument(
            '--project',
            metavar='<project>',
            help=_("Owner's project (name or ID)"),
            required=False
        )
        return parser

    def take_action_network(self, client, parsed_args):
        client = self.app.client_manager.network
        # if no project id is specified, operate on current project
        args = _get_attrs(self.app.client_manager, vars(parsed_args))
        if not "project_id" in args:
            args["project_id"] = client.find_tenant().project_id
        project_id = args["project_id"]

        client.delete_setting(project_id)
        return

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs "
                                      "access to a network endpoint.")
        return


class UpdateSetting(command.Command):
    """Set setting properties"""

    def get_parser(self, prog_name):
        parser = super(UpdateSetting, self).get_parser(prog_name)
        parser.add_argument(
            '--project',
            metavar='<project>',
            help=_("Owner's project (name or ID)"),
            required=False
        )
        parser.add_argument('--mac-filtering', metavar='mac_filtering',
                            help="Enable/Disable source MAC filtering"
                                 " on all ports",
                            required=True)
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.network
        # if no project id is specified, operate on current project
        args = _get_attrs(self.app.client_manager, vars(parsed_args))
        if not "project_id" in args:
            args["project_id"] = client.find_tenant().project_id
        project_id = args["project_id"]
        del args['project_id']

        client.find_setting(project_id, ignore_missing=False)

        if args == {}:
            msg = "Nothing specified to be set"
            raise exceptions.CommandError(msg)

        client.update_setting(project_id, **args)
        return

#   Copyright 2016 Huawei, Inc. All rights reserved.
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

"""Compute v2 Server Group action implementations"""

import logging

from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils

from openstackclient.i18n import _
from novaclient import api_versions


LOG = logging.getLogger(__name__)


_formatters = {
    'policies': utils.format_list,
    'members': utils.format_list,
}


def _get_columns(info):
    columns = list(info.keys())
    return tuple(sorted(columns))

#WRS:extension
def _extract_metadata(args):
    metadata = {}
    for server_group in args.metadata:
        for metadatum in server_group:
            if metadatum.find('=') > -1:
                (key, value) = metadatum.split('=', 1)
            else:
                key = metadatum
                value = None
            metadata[key] = value
    return metadata

# WRS:extension - type checking for key-value pair
# returns text instead of tuple like above
def _key_value_type(text):
    try:
        (k, v) = text.split('=', 1)
        return text
    except ValueError:
        msg = "%r is not in the format of key=value" % text
        raise argparse.ArgumentTypeError(msg)


# WRS:extension - type checking for CSV key-value pairs
def _csv_key_value_type(text):
    try:
        return map(_key_value_type, text.split(','))
    except Exception as e:
        raise exceptions.CommandError(
            "Invalid csv key-value argument '%s'. %s" % (text, unicode(e)))


class CreateServerGroup(command.ShowOne):
    _description = _("Create a new server group.")

    def get_parser(self, prog_name):
        parser = super(CreateServerGroup, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_("New server group name")
        )
        # WRS:extension
        parser.add_argument(
            '--metadata',
            metavar='<key1=value1[,key2=value2...>',
            action='append',
            default=[],
            type=_csv_key_value_type,
            help=_("Metadata for this server group")
        )
        parser.add_argument(
            '--policy',
            metavar='<policy>',
            choices=['affinity', 'anti-affinity'],
            default='affinity',
            help=_("Add a policy to <name> "
                   "('affinity' or 'anti-affinity', "
                   "default to 'affinity')")
        )
        return parser

    def take_action(self, parsed_args):
        compute_client = self.app.client_manager.compute
        info = {}

        #WRS:extension
        meta = _extract_metadata(parsed_args)
        compute_client.api_version = api_versions.APIVersion("2.53")
        server_group = compute_client.server_groups.create(
            name=parsed_args.name,
            metadata=meta,
            policies=[parsed_args.policy])

        info.update(server_group._info)
        columns = _get_columns(info)
        data = utils.get_dict_properties(info, columns,
                                         formatters=_formatters)
        return columns, data

class DeleteServerGroup(command.Command):
    _description = _("Delete existing server group(s).")

    def get_parser(self, prog_name):
        parser = super(DeleteServerGroup, self).get_parser(prog_name)
        parser.add_argument(
            'server_group',
            metavar='<server-group>',
            nargs='+',
            help=_("server group(s) to delete (name or ID)")
        )
        return parser

    def take_action(self, parsed_args):
        compute_client = self.app.client_manager.compute
        result = 0
        for group in parsed_args.server_group:
            try:
                group_obj = utils.find_resource(compute_client.server_groups,
                                                group)
                compute_client.server_groups.delete(group_obj.id)
            # Catch all exceptions in order to avoid to block the next deleting
            except Exception as e:
                result += 1
                LOG.error(e)

        if result > 0:
            total = len(parsed_args.server_group)
            msg = _("%(result)s of %(total)s server groups failed to delete.")
            raise exceptions.CommandError(
                msg % {"result": result,
                       "total": total}
            )


class ListServerGroup(command.Lister):
    _description = _("List all server groups.")

    def get_parser(self, prog_name):
        parser = super(ListServerGroup, self).get_parser(prog_name)
        parser.add_argument(
            '--all-projects',
            action='store_true',
            default=False,
            help=_("Display information from all projects (admin only)")
        )
        parser.add_argument(
            '--long',
            action='store_true',
            default=False,
            help=_("List additional fields in output")
        )
        return parser

    def take_action(self, parsed_args):
        compute_client = self.app.client_manager.compute

        #WRS:extension
        compute_client.api_version = api_versions.APIVersion("2.53")

        data = compute_client.server_groups.list(parsed_args.all_projects)

        #WRS:extension list project_id, user_id fields and metadata fields
        if parsed_args.long:
            column_headers = columns = (
                'ID',
                'Name',
                'Policies',
                'Members',
                'Project Id',
                'User Id',
                'Metadata',
            )
        else:
            column_headers = columns = (
                'ID',
                'Name',
                'Policies',
                'Metadata',
            )

        return (column_headers,
                (utils.get_item_properties(
                    s, columns,
                    formatters={
                        'Policies': utils.format_list,
                        'Members': utils.format_list,
                    }
                ) for s in data))


class ShowServerGroup(command.ShowOne):
    _description = _("Display server group details.")

    def get_parser(self, prog_name):
        parser = super(ShowServerGroup, self).get_parser(prog_name)
        parser.add_argument(
            'server_group',
            metavar='<server-group>',
            help=_("server group to display (name or ID)")
        )
        return parser

    def take_action(self, parsed_args):
        compute_client = self.app.client_manager.compute
        #WRS:extension
        compute_client.api_version = api_versions.APIVersion("2.53")

        group = utils.find_resource(compute_client.server_groups,
                                    parsed_args.server_group)

        info = {}
        info.update(group._info)
        columns = _get_columns(info)
        data = utils.get_dict_properties(info, columns,
                                         formatters=_formatters)
        return columns, data

#WRS:extension
class SetServerGroupMetadata(command.Command):
    _description = _("Set metadata of a server group")

    def get_parser(self, prog_name):
        parser = super(SetServerGroupMetadata, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=_("Unique ID of the server group")
        )
        parser.add_argument(
            'metadata',
            metavar='<key1=value1[,key2=value2...]>',
            action='append',
            default=[],
            type=_csv_key_value_type,
            help=_("Metadata to set/unset")
        )
        return parser

    def take_action(self, parsed_args):
        compute_client = self.app.client_manager.compute
        metadata = _extract_metadata(parsed_args)
        compute_client.api_version = api_versions.APIVersion("2.53")       
        compute_client.server_groups.set_metadata(parsed_args.id, metadata)


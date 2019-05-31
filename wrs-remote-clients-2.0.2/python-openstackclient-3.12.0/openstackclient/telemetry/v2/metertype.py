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
#   Copyright (c) 2013-2018 Wind River Systems, Inc.
#
#   The right to copy, distribute, modify, or otherwise make use
#   of this software may be licensed only pursuant to the terms
#   of an applicable Wind River license agreement.
#
#  Copyright (c) 2013-2018 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#
# WRS extension

from osc_lib.command import command
from osc_lib import utils

from openstackclient.i18n import _


class ListMetertype(command.Lister):
    """List the user's meter types."""

    def get_parser(self, prog_name):
        parser = super(ListMetertype, self).get_parser(prog_name)
        parser.add_argument(
            "-q", "--query",
            metavar="<QUERY>",
            help=_("key[op]data_type::value; list. data_type is optional, "
                  "but if supplied must be string, integer, float, or boolean.")
        )
        parser.add_argument(
            "-l", "--limit",
            metavar="<NUMBER>",
            help=_("Maximum number of meters to return.")
        )
        return parser

    def take_action(self, parsed_args):
        ceilometer_client = self.app.client_manager.telemetry

        columns = (
            "Name",
            "Type",
            "Unit",
        )

        metertypes = ceilometer_client.metertypes.list()

        return (columns,
                (utils.get_item_properties(
                    s, columns,
                ) for s in metertypes))

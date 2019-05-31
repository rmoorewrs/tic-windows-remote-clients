#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
# Copyright (c) 2015-2017 Wind River Systems, Inc.
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#


"""Compute v2 wrs_providernet action implementations"""

from osc_lib.cli import parseractions
from osc_lib.command import command
import six

from openstackclient.i18n import _

      
class ShowProvidernetPci(command.ShowOne):
    """Show details of a given provider network"""

    def get_parser(self, prog_name):
        parser = super(ShowProvidernetPci, self).get_parser(prog_name)
        parser.add_argument(
            "providernet",
            metavar="<providernet_id>",
            help=_("Id of the provider network")
        )
        return parser

    def take_action(self, parsed_args):
        compute_client = self.app.client_manager.compute

        providernet = compute_client.wrs_providernets.get(parsed_args.providernet)
        stats = providernet._info.copy() 
        return zip(*sorted(six.iteritems(stats)))

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


"""Compute v2 wrs_pci action implementations"""

from osc_lib.cli import parseractions
from osc_lib.command import command
from osc_lib import utils
import six

from openstackclient.i18n import _


class ListPciDevices(command.Lister):
    """List pci device"""

    def get_parser(self, prog_name):
        parser = super(ListPciDevices, self).get_parser(prog_name)
        parser.add_argument(
            "--device",
            metavar="<device>",
            help=_("PCI devices matching a particular device id or alias.")
        )
        return parser

    def take_action(self, parsed_args):
        compute_client = self.app.client_manager.compute

        columns = (
            "PCI Alias", 
            "Device Id", 
            "Vendor Id", 
            "Class Id",
            "pci_pfs_configured", 
            "pci_pfs_used", 
            "pci_vfs_configured",
            "pci_vfs_used"
        )

        data = compute_client.wrs_pci.list(parsed_args.device)
  
        return (columns, 
                (utils.get_item_properties(
                    s, columns, 
                ) for s in data))

      
class ShowPciDevices(command.ShowOne):
    """Show details of a given PCI device."""

    def get_parser(self, prog_name):
        parser = super(ShowPciDevices, self).get_parser(prog_name)
        parser.add_argument(
            "device",
            metavar="<device>",
            help=_("Device alias or device id of the PCI device.")
        )
        parser.add_argument(
            "--host",
            metavar="<hostname>",
            help=_("Limit matches to PCI devices from a particular host")
        )
        return parser

    def take_action(self, parsed_args):
        compute_client = self.app.client_manager.compute
        deviceInfo = compute_client.wrs_pci.get(parsed_args.device, 
                                             parsed_args.host)
    
        data = deviceInfo._info.copy()
        return zip(*sorted(six.iteritems(data)))


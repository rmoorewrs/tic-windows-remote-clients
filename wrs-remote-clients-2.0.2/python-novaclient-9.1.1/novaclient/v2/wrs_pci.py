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

from six.moves.urllib import parse

from novaclient import base


class PciDevicesManager(base.Manager):
    resource_class = base.Resource

    def list(self, host=None, device=None):
        """
        Get PCI device usage statistics.

        :param host: Name of the compute host to collect PCI statistics for
        :param device: Device id or name to collect PCI statistics for
        :rtype: :class:`PciDevice`
        """
        opts = {}
        if host:
            opts['host'] = host
        if device:
            opts['device'] = device

        # Transform the dict to a sequence of two-element tuples in fixed
        # order, then the encoded string will be consistent in Python 2&3.
        new_opts = sorted(opts.items(), key=lambda x: x[0])

        query_string = "?%s" % parse.urlencode(new_opts) if new_opts else ""

        return self._list("/wrs-pci%s" % query_string, "pci_device_usage")

    def get(self, device, host=None):
        """
        Get PCI device usage statistics for a specific device.

        :param device: Name of the :class:`PciDevice` to get.
        :rtype: :class:`PciDevice`
        """
        opts = {}
        if host:
            opts['host'] = host

        # Transform the dict to a sequence of two-element tuples in fixed
        # order, then the encoded string will be consistent in Python 2&3.
        new_opts = sorted(opts.items(), key=lambda x: x[0])

        query_string = "?%s" % parse.urlencode(new_opts) if new_opts else ""

        return self._list("/wrs-pci/%s%s" % (device, query_string),
                          "pci_device_usage")

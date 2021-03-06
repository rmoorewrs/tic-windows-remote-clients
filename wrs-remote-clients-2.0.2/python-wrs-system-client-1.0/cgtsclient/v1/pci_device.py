#
# Copyright (c) 2015 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#

# -*- encoding: utf-8 -*-
#

from cgtsclient.common import base
from cgtsclient import exc


class PciDevice(base.Resource):
    def __repr__(self):
        return "<PciDevice %s>" % self._info


class PciDeviceManager(base.Manager):
    resource_class = PciDevice

    def list(self, ihost_id):
        path = '/v1/ihosts/%s/pci_devices' % ihost_id
        return self._list(path, "pci_devices")

    def list_all(self):
        path = '/v1/pci_devices'
        return self._list(path, "pci_devices")

    def get(self, pci_id):
        path = '/v1/pci_devices/%s' % pci_id
        try:
            return self._list(path)[0]
        except IndexError:
            return None

    def update(self, pci_id, patch):
        path = '/v1/pci_devices/%s' % pci_id
        return self._update(path, patch)


def get_pci_device_display_name(p):
    if p.name:
        return p.name
    else:
        return '(' + str(p.uuid)[-8:] + ')'
    
#
# Copyright (c) 2013-2014 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#

# -*- encoding: utf-8 -*-
#

from cgtsclient.common import base
from cgtsclient import exc

CREATION_ATTRIBUTES = ['ihost_uuid', 'memtotal_mib', 'memavail_mib',
                       'platform_reserved_mib', 'hugepages_configured',
                       'avs_hugepages_size_mib', 'avs_hugepages_reqd',
                       'avs_hugepages_nr', 'avs_hugepages_avail',
                       'vm_hugepages_nr_2M_pending', 'vm_hugepages_nr_1G_pending',
                       'vm_hugepages_nr_2M', 'vm_hugepages_avail_2M',
                       'vm_hugepages_nr_1G', 'vm_hugepages_avail_1G',
                       'vm_hugepages_avail_1G', 'vm_hugepages_use_1G',
                       'vm_hugepages_possible_2M', 'vm_hugepages_possible_1G',
                       'capabilities', 'numa_node', 'minimum_platform_reserved_mib']

class imemory(base.Resource):
    def __repr__(self):
        return "<imemory %s>" % self._info


class imemoryManager(base.Manager):
    resource_class = imemory

    @staticmethod
    def _path(id=None):
        return '/v1/imemorys/%s' % id if id else '/v1/imemorys'

    def list(self, ihost_id):
        path = '/v1/ihosts/%s/imemorys' % ihost_id
        return self._list(path, "imemorys")

    def get(self, imemory_id):
        path = '/v1/imemorys/%s' % imemory_id
        try:
            return self._list(path)[0]
        except IndexError:
            return None
    
    def update(self, imemory_id, patch):
        return self._update(self._path(imemory_id), patch)

    def create(self, **kwargs):
        path = '/v1/imemorys'
        new = {}
        for (key, value) in kwargs.items():
            if key in CREATION_ATTRIBUTES:
                new[key] = value
            else:
                raise exc.InvalidAttribute('%s' % key)
        return self._create(path, new)

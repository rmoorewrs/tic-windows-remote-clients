# -*- encoding: utf-8 -*-
#
# Copyright (c) 2015-2016 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#


from cgtsclient.common import base
from cgtsclient import exc


CREATION_ATTRIBUTES = ['software_version', 'compatible_version',
                       'required_patches']
IMPORT_ATTRIBUTES = ['path_to_iso', 'path_to_sig']


class Load(base.Resource):
    def __repr__(self):
        return "<loads %s>" % self._info


class LoadManager(base.Manager):
    resource_class = Load

    def list(self):
        return self._list('/v1/loads/', "loads")

    def get(self, load_id):
        path = '/v1/loads/%s' % load_id
        try:
            return self._list(path)[0]
        except IndexError:
            return None

    def create(self, **kwargs):
        path = '/v1/loads/'
        new = {}
        for (key, value) in kwargs.items():
            if key in CREATION_ATTRIBUTES:
                new[key] = value
            else:
                raise exc.InvalidAttribute(key)
        return self._create(path, new)

    def import_load(self, **kwargs):
        path = '/v1/loads/import_load'
        new = {}
        for (key, value) in kwargs.items():
            if key in IMPORT_ATTRIBUTES:
                new[key] = value
            else:
                raise exc.InvalidAttribute(key)
        res, body = self.api.json_request('POST', path, body=new)
        return body

    def delete(self, load_id):
        path = '/v1/loads/%s' % load_id
        return self._delete(path)

    def update(self, load_id, patch):
        path = '/v1/loads/%s' % load_id
        return self._update(path, patch)

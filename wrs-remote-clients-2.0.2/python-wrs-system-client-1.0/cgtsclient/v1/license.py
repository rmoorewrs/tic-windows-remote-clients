#
# Copyright (c) 2017 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#

# -*- encoding: utf-8 -*-
#

from cgtsclient.common import base
from cgtsclient import exc


class License(base.Resource):
    def __repr__(self):
        return "<license %s>" % self._info


class LicenseManager(base.Manager):
    resource_class = License

    @staticmethod
    def _path(id=None):
        return '/v1/license/%s' % id if id else '/v1/license'

    def list(self):
        return self._list(self._path(), "licenses")

    def install_license(self, file):
        path = self._path("install_license")
        return self._upload(path, file)

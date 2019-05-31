# -*- encoding: utf-8 -*-
#
# Copyright (c) 2015-2016 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#


from cgtsclient.common import base


class HealthManager(base.Manager):

    def get(self):
        path = '/v1/health/'
        resp, body = self.api.json_request('GET', path)
        return body

    def get_upgrade(self):
        path = '/v1/health/upgrade'
        resp, body = self.api.json_request('GET', path)
        return body

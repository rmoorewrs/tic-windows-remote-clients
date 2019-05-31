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

CREATION_ATTRIBUTES = ['firewall_path']


class FirewallRules(base.Resource):
    def __repr__(self):
        return "<firewallrules %s>" % self._info


class FirewallRulesManager(base.Manager):
    resource_class = FirewallRules

    @staticmethod
    def _path(id=None):
        return '/v1/firewallrules/%s' % id if id else '/v1/firewallrules'

    def list(self):
        return self._list(self._path(), "firewallrules")

    def get(self, firewallrules_id):
        try:
            return self._list(self._path(firewallrules_id))[0]
        except IndexError:
            return None

    def import_firewall_rules(self, file):
        path = self._path("import_firewall_rules")
        return self._upload(path, file)

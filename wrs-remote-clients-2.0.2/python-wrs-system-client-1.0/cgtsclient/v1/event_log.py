#!/usr/bin/env python
# Copyright (c) 2016 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.

from cgtsclient.common import base
from ceilometerclient.v2 import options



class EventLog(base.Resource):
    def __repr__(self):
                return "<EventLog %s>" % self._info


class EventLogManager(base.Manager):
    resource_class = EventLog

    @staticmethod
    def _path(id=None):
        return '/v1/event_log/%s' % id if id else '/v1/event_log'

    def list(self, q=None, limit=None, marker=None, alarms=False, logs=False, include_suppress=False):
        params = []
        if limit:
            params.append('limit=%s' % str(limit))
        if marker:
            params.append('marker=%s' % str(marker))
        if include_suppress:
            params.append('include_suppress=True')
        if   alarms==True and logs==False:
           params.append('alarms=True')
        elif alarms==False and logs==True:
           params.append('logs=True')

        restAPIURL = options.build_url(self._path(), q, params)

        l = self._list(restAPIURL, 'event_log')
        return l

    def get(self, iid):
        try:
            return self._list(self._path(iid))[0]
        except IndexError:
            return None


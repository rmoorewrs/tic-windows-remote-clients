#!/usr/bin/env python
#
# Copyright (c) 2016 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#

# vim: tabstop=4 shiftwidth=4 softtabstop=4
# All Rights Reserved.
#


def do_health_query(cc, args):
    """Run the Health Check."""
    print cc.health.get()


def do_health_query_upgrade(cc, args):
    """Run the Health Check for an Upgrade."""
    print cc.health.get_upgrade()

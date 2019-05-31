#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
# Copyright (c) 2016 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#

"""Providernet type action implementations"""

from osc_lib import exceptions
from osc_lib import utils
from openstackclient.network import common
from openstackclient.network import sdk_utils

_formatters = {
}


class ListProvidernetType(common.NetworkAndComputeLister):
    """List providernet types"""

    def update_parser_common(self, parser):
        return parser

    def take_action_network(self, client, parsed_args):
        columns = (
            'type',
            'description'
        )
        column_headers = (
            'Type',
            'Description'
        )

        args = {}

        data = client.providernet_types(**args)

        return (column_headers,
                (utils.get_item_properties(
                    s, columns,
                    formatters=_formatters,
                ) for s in data))

    def take_action_compute(self, client, parsed_args):
        raise exceptions.CommandError("This command needs access to"
                                      " a network endpoint.")
        return

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# Copyright (c) 2016 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#

from openstack.network import network_service
from openstack import resource2 as resource


class Setting(resource.Resource):
    resource_key = 'setting'
    resources_key = 'settings'
    base_path = '/wrs-tenant/settings'
    service = network_service.NetworkService()

    # capabilities
    allow_create = False
    allow_get = True
    allow_update = True
    allow_delete = True
    allow_list = True

    # Properties
    mac_filtering = resource.Body('mac_filtering', type=bool)
    project_id = resource.Body('tenant_id')

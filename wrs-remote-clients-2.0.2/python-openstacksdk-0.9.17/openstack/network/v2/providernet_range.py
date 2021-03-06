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


class ProvidernetRange(resource.Resource):
    resource_key = 'providernet_range'
    resources_key = 'providernet_ranges'
    base_path = '/wrs-provider/providernet-ranges'
    service = network_service.NetworkService()

    # capabilities
    allow_create = True
    allow_get = True
    allow_update = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'type', 'project_id',
    )

    # Properties
    minimum = resource.Body('minimum', type=int)
    name = resource.Body('name')
    providernet_id = resource.Body('providernet_id')
    project_id = resource.Body('tenant_id')
    shared = resource.Body('shared', type=bool)
    providernet_name = resource.Body('providernet_name')
    providernet_type = resource.Body('providernet_type')
    id = resource.Body('id')
    maximum = resource.Body('maximum', type=int)
    description = resource.Body('description')
    ttl = resource.Body('ttl', type=int)
    port = resource.Body('port', type=int)
    group = resource.Body('group')
    mode = resource.Body('mode')

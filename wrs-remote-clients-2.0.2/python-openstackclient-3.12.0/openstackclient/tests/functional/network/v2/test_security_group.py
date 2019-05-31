#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import uuid

from openstackclient.tests.functional.network.v2 import common


class SecurityGroupTests(common.NetworkTests):
    """Functional tests for security group"""
    HEADERS = ['Name']
    FIELDS = ['name']

    @classmethod
    def setUpClass(cls):
        common.NetworkTests.setUpClass()
        if cls.haz_network:
            cls.NAME = uuid.uuid4().hex
            cls.OTHER_NAME = uuid.uuid4().hex

            opts = cls.get_opts(cls.FIELDS)
            raw_output = cls.openstack(
                'security group create ' +
                cls.NAME +
                opts
            )
            expected = cls.NAME + '\n'
            cls.assertOutput(expected, raw_output)

    @classmethod
    def tearDownClass(cls):
        try:
            if cls.haz_network:
                # Rename test
                raw_output = cls.openstack(
                    'security group set --name ' +
                    cls.OTHER_NAME + ' ' +
                    cls.NAME
                )
                cls.assertOutput('', raw_output)
                # Delete test
                raw_output = cls.openstack(
                    'security group delete ' +
                    cls.OTHER_NAME
                )
                cls.assertOutput('', raw_output)
        finally:
            super(SecurityGroupTests, cls).tearDownClass()

    def setUp(self):
        super(SecurityGroupTests, self).setUp()
        # Nothing in this class works with Nova Network
        if not self.haz_network:
            self.skipTest("No Network service present")

    def test_security_group_list(self):
        opts = self.get_opts(self.HEADERS)
        raw_output = self.openstack('security group list' + opts)
        self.assertIn(self.NAME, raw_output)

    def test_security_group_set(self):
        raw_output = self.openstack(
            'security group set --description NSA ' + self.NAME
        )
        self.assertEqual('', raw_output)

        opts = self.get_opts(['description'])
        raw_output = self.openstack('security group show ' + self.NAME + opts)
        self.assertEqual("NSA\n", raw_output)

    def test_security_group_show(self):
        opts = self.get_opts(self.FIELDS)
        raw_output = self.openstack('security group show ' + self.NAME + opts)
        self.assertEqual(self.NAME + "\n", raw_output)

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


class SecurityGroupRuleTests(common.NetworkTests):
    """Functional tests for security group rule"""
    SECURITY_GROUP_RULE_ID = None
    NAME_FIELD = ['name']
    ID_FIELD = ['id']
    ID_HEADER = ['ID']

    @classmethod
    def setUpClass(cls):
        common.NetworkTests.setUpClass()
        if cls.haz_network:
            cls.SECURITY_GROUP_NAME = uuid.uuid4().hex

            # Create the security group to hold the rule
            opts = cls.get_opts(cls.NAME_FIELD)
            raw_output = cls.openstack(
                'security group create ' +
                cls.SECURITY_GROUP_NAME +
                opts
            )
            expected = cls.SECURITY_GROUP_NAME + '\n'
            cls.assertOutput(expected, raw_output)

            # Create the security group rule.
            opts = cls.get_opts(cls.ID_FIELD)
            raw_output = cls.openstack(
                'security group rule create ' +
                cls.SECURITY_GROUP_NAME + ' ' +
                '--protocol tcp --dst-port 80:80 ' +
                '--ingress --ethertype IPv4 ' +
                opts
            )
            cls.SECURITY_GROUP_RULE_ID = raw_output.strip('\n')

    @classmethod
    def tearDownClass(cls):
        try:
            if cls.haz_network:
                raw_output = cls.openstack(
                    'security group rule delete ' +
                    cls.SECURITY_GROUP_RULE_ID
                )
                cls.assertOutput('', raw_output)
                raw_output = cls.openstack(
                    'security group delete ' +
                    cls.SECURITY_GROUP_NAME
                )
                cls.assertOutput('', raw_output)
        finally:
            super(SecurityGroupRuleTests, cls).tearDownClass()

    def setUp(self):
        super(SecurityGroupRuleTests, self).setUp()
        # Nothing in this class works with Nova Network
        if not self.haz_network:
            self.skipTest("No Network service present")

    def test_security_group_rule_list(self):
        opts = self.get_opts(self.ID_HEADER)
        raw_output = self.openstack('security group rule list ' +
                                    self.SECURITY_GROUP_NAME +
                                    opts)
        self.assertIn(self.SECURITY_GROUP_RULE_ID, raw_output)

    def test_security_group_rule_show(self):
        opts = self.get_opts(self.ID_FIELD)
        raw_output = self.openstack('security group rule show ' +
                                    self.SECURITY_GROUP_RULE_ID +
                                    opts)
        self.assertEqual(self.SECURITY_GROUP_RULE_ID + "\n", raw_output)

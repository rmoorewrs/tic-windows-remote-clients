# Copyright (c) 2016, Intel Corporation.
# All Rights Reserved.
#
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


class NetworkQosRuleTestsMinimumBandwidth(common.NetworkTests):
    """Functional tests for QoS minimum bandwidth rule"""
    RULE_ID = None
    MIN_KBPS = 2800
    MIN_KBPS_MODIFIED = 7500
    DIRECTION = '--egress'
    HEADERS = ['ID']
    FIELDS = ['id']
    TYPE = 'minimum-bandwidth'

    @classmethod
    def setUpClass(cls):
        common.NetworkTests.setUpClass()
        if cls.haz_network:
            cls.QOS_POLICY_NAME = 'qos_policy_' + uuid.uuid4().hex

            opts = cls.get_opts(cls.FIELDS)
            cls.openstack(
                'network qos policy create ' +
                cls.QOS_POLICY_NAME
            )
            cls.RULE_ID = cls.openstack(
                'network qos rule create ' +
                '--type ' + cls.TYPE + ' ' +
                '--min-kbps ' + str(cls.MIN_KBPS) + ' ' +
                cls.DIRECTION + ' ' +
                cls.QOS_POLICY_NAME +
                opts
            )
            cls.assertsOutputNotNone(cls.RULE_ID)

    @classmethod
    def tearDownClass(cls):
        try:
            if cls.haz_network:
                raw_output = cls.openstack(
                    'network qos rule delete ' +
                    cls.QOS_POLICY_NAME + ' ' +
                    cls.RULE_ID
                )
                cls.openstack(
                    'network qos policy delete ' +
                    cls.QOS_POLICY_NAME
                )
                cls.assertOutput('', raw_output)
        finally:
            super(NetworkQosRuleTestsMinimumBandwidth, cls).tearDownClass()

    def setUp(self):
        super(NetworkQosRuleTestsMinimumBandwidth, self).setUp()
        # Nothing in this class works with Nova Network
        if not self.haz_network:
            self.skipTest("No Network service present")

    def test_qos_rule_list(self):
        opts = self.get_opts(self.HEADERS)
        raw_output = self.openstack('network qos rule list '
                                    + self.QOS_POLICY_NAME + opts)
        self.assertIn(self.RULE_ID, raw_output)

    def test_qos_rule_show(self):
        opts = self.get_opts(self.FIELDS)
        raw_output = self.openstack('network qos rule show ' +
                                    self.QOS_POLICY_NAME + ' ' + self.RULE_ID +
                                    opts)
        self.assertEqual(self.RULE_ID, raw_output)

    def test_qos_rule_set(self):
        self.openstack('network qos rule set --min-kbps ' +
                       str(self.MIN_KBPS_MODIFIED) + ' ' +
                       self.QOS_POLICY_NAME + ' ' + self.RULE_ID)
        opts = self.get_opts(['min_kbps'])
        raw_output = self.openstack('network qos rule show ' +
                                    self.QOS_POLICY_NAME + ' ' + self.RULE_ID +
                                    opts)
        self.assertEqual(str(self.MIN_KBPS_MODIFIED) + "\n", raw_output)


class NetworkQosRuleTestsDSCPMarking(common.NetworkTests):
    """Functional tests for QoS DSCP marking rule"""
    RULE_ID = None
    QOS_POLICY_NAME = 'qos_policy_' + uuid.uuid4().hex
    DSCP_MARK = 8
    DSCP_MARK_MODIFIED = 32
    HEADERS = ['ID']
    FIELDS = ['id']
    TYPE = 'dscp-marking'

    @classmethod
    def setUpClass(cls):
        common.NetworkTests.setUpClass()
        if cls.haz_network:
            opts = cls.get_opts(cls.FIELDS)
            cls.openstack(
                'network qos policy create ' +
                cls.QOS_POLICY_NAME
            )
            cls.RULE_ID = cls.openstack(
                'network qos rule create ' +
                '--type ' + cls.TYPE + ' ' +
                '--dscp-mark ' + str(cls.DSCP_MARK) + ' ' +
                cls.QOS_POLICY_NAME +
                opts
            )
            cls.assertsOutputNotNone(cls.RULE_ID)

    @classmethod
    def tearDownClass(cls):
        try:
            if cls.haz_network:
                raw_output = cls.openstack(
                    'network qos rule delete ' +
                    cls.QOS_POLICY_NAME + ' ' +
                    cls.RULE_ID
                )
                cls.openstack(
                    'network qos policy delete ' + cls.QOS_POLICY_NAME)
                cls.assertOutput('', raw_output)
        finally:
            super(NetworkQosRuleTestsDSCPMarking, cls).tearDownClass()

    def setUp(self):
        super(NetworkQosRuleTestsDSCPMarking, self).setUp()
        # Nothing in this class works with Nova Network
        if not self.haz_network:
            self.skipTest("No Network service present")

    def test_qos_rule_list(self):
        opts = self.get_opts(self.HEADERS)
        raw_output = self.openstack('network qos rule list '
                                    + self.QOS_POLICY_NAME + opts)
        self.assertIn(self.RULE_ID, raw_output)

    def test_qos_rule_show(self):
        opts = self.get_opts(self.FIELDS)
        raw_output = self.openstack('network qos rule show ' +
                                    self.QOS_POLICY_NAME + ' ' + self.RULE_ID +
                                    opts)
        self.assertEqual(self.RULE_ID, raw_output)

    def test_qos_rule_set(self):
        self.openstack('network qos rule set --dscp-mark ' +
                       str(self.DSCP_MARK_MODIFIED) + ' ' +
                       self.QOS_POLICY_NAME + ' ' + self.RULE_ID)
        opts = self.get_opts(['dscp_mark'])
        raw_output = self.openstack('network qos rule show ' +
                                    self.QOS_POLICY_NAME + ' ' + self.RULE_ID +
                                    opts)
        self.assertEqual(str(self.DSCP_MARK_MODIFIED) + "\n", raw_output)


class NetworkQosRuleTestsBandwidthLimit(common.NetworkTests):
    """Functional tests for QoS bandwidth limit rule"""
    RULE_ID = None
    QOS_POLICY_NAME = 'qos_policy_' + uuid.uuid4().hex
    MAX_KBPS = 10000
    MAX_KBPS_MODIFIED = 15000
    MAX_BURST_KBITS = 1400
    MAX_BURST_KBITS_MODIFIED = 1800
    RULE_DIRECTION = 'egress'
    RULE_DIRECTION_MODIFIED = 'ingress'
    HEADERS = ['ID']
    FIELDS = ['id']
    TYPE = 'bandwidth-limit'

    @classmethod
    def setUpClass(cls):
        common.NetworkTests.setUpClass()
        if cls.haz_network:
            opts = cls.get_opts(cls.FIELDS)
            cls.openstack(
                'network qos policy create ' +
                cls.QOS_POLICY_NAME
            )
            cls.RULE_ID = cls.openstack(
                'network qos rule create ' +
                '--type ' + cls.TYPE + ' ' +
                '--max-kbps ' + str(cls.MAX_KBPS) + ' ' +
                '--max-burst-kbits ' + str(cls.MAX_BURST_KBITS) + ' ' +
                '--' + cls.RULE_DIRECTION + ' ' +
                cls.QOS_POLICY_NAME +
                opts
            )
            cls.assertsOutputNotNone(cls.RULE_ID)

    @classmethod
    def tearDownClass(cls):
        try:
            if cls.haz_network:
                raw_output = cls.openstack(
                    'network qos rule delete ' +
                    cls.QOS_POLICY_NAME + ' ' +
                    cls.RULE_ID
                )
                cls.openstack(
                    'network qos policy delete ' + cls.QOS_POLICY_NAME)
                cls.assertOutput('', raw_output)
        finally:
            super(NetworkQosRuleTestsBandwidthLimit, cls).tearDownClass()

    def setUp(self):
        super(NetworkQosRuleTestsBandwidthLimit, self).setUp()
        # Nothing in this class works with Nova Network
        if not self.haz_network:
            self.skipTest("No Network service present")

    def test_qos_rule_list(self):
        opts = self.get_opts(self.HEADERS)
        raw_output = self.openstack('network qos rule list '
                                    + self.QOS_POLICY_NAME + opts)
        self.assertIn(self.RULE_ID, raw_output)

    def test_qos_rule_show(self):
        opts = self.get_opts(self.FIELDS)
        raw_output = self.openstack('network qos rule show ' +
                                    self.QOS_POLICY_NAME + ' ' + self.RULE_ID +
                                    opts)
        self.assertEqual(self.RULE_ID, raw_output)

    def test_qos_rule_set(self):
        self.openstack('network qos rule set --max-kbps ' +
                       str(self.MAX_KBPS_MODIFIED) + ' --max-burst-kbits ' +
                       str(self.MAX_BURST_KBITS_MODIFIED) + ' ' +
                       '--' + self.RULE_DIRECTION_MODIFIED + ' ' +
                       self.QOS_POLICY_NAME + ' ' + self.RULE_ID)
        opts = self.get_opts(['direction', 'max_burst_kbps', 'max_kbps'])
        raw_output = self.openstack('network qos rule show ' +
                                    self.QOS_POLICY_NAME + ' ' + self.RULE_ID +
                                    opts)
        expected = (str(self.RULE_DIRECTION_MODIFIED) + "\n" +
                    str(self.MAX_BURST_KBITS_MODIFIED) + "\n" +
                    str(self.MAX_KBPS_MODIFIED) + "\n")
        self.assertEqual(expected, raw_output)

#
# Copyright (c) 2013-2014 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#

import setuptools

setuptools.setup(
    name='cgtsclient',
    description='CGCS System Client and CLI',
    version='1.0.0',
    license='windriver',
    packages=['cgtsclient', 'cgtsclient.v1', 'cgtsclient.openstack',
              'cgtsclient.openstack.common',
              'cgtsclient.openstack.common.config',
              'cgtsclient.openstack.common.rootwrap',
              'cgtsclient.common'],
    entry_points={
         'console_scripts': [
             'system = cgtsclient.shell:main'
         ]}
)

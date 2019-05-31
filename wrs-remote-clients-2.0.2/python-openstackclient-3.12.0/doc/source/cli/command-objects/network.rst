=======
network
=======

A **network** is an isolated Layer 2 networking segment. There are two types
of networks, project and provider networks. Project networks are fully isolated
and are not shared with other projects. Provider networks map to existing
physical networks in the data center and provide external network access for
servers and other resources. Only an OpenStack administrator can create
provider networks. Networks can be connected via routers.

Compute v2, Network v2

network create
--------------

Create new network

.. program:: network create
.. code:: bash

    openstack network create
        [--project <project> [--project-domain <project-domain>]]
        [--enable | --disable]
        [--share | --no-share]
        [--description <description>]
        [--availability-zone-hint <availability-zone>]
        [--enable-port-security | --disable-port-security]
        [--external [--default | --no-default] | --internal]
        [--provider-network-type <provider-network-type>]
        [--provider-physical-network <provider-physical-network>]
        [--provider-segment <provider-segment>]
        [--qos-policy <qos-policy>]
        [--transparent-vlan | --no-transparent-vlan]
        [--tag <tag> | --no-tag]
        <name>

.. option:: --project <project>

    Owner's project (name or ID)

    *Network version 2 only*

.. option:: --project-domain <project-domain>

    Domain the project belongs to (name or ID).
    This can be used in case collisions between project names exist.

    *Network version 2 only*

.. option:: --enable

    Enable network (default)

    *Network version 2 only*

.. option:: --disable

    Disable network

    *Network version 2 only*

.. option:: --share

    Share the network between projects

.. option:: --no-share

    Do not share the network between projects

.. option:: --description <description>

    Set network description

    *Network version 2 only*

.. option:: --availability-zone-hint <availability-zone>

    Availability Zone in which to create this network
    (Network Availability Zone extension required,
    repeat option to set multiple availability zones)

    *Network version 2 only*

.. option:: --enable-port-security

    Enable port security by default for ports created on
    this network (default)

    *Network version 2 only*

.. option:: --disable-port-security

    Disable port security by default for ports created on
    this network

    *Network version 2 only*

.. option:: --subnet <subnet>

    IPv4 subnet for fixed IPs (in CIDR notation)

    *Compute version 2 only*

.. option:: --external

    Set this network as an external network
    (external-net extension required)

    *Network version 2 only*

.. option:: --internal

    Set this network as an internal network (default)

    *Network version 2 only*

.. option:: --default

    Specify if this network should be used as
    the default external network

    *Network version 2 only*

.. option:: --no-default

    Do not use the network as the default external network
    (default)

    *Network version 2 only*

.. option:: --provider-network-type <provider-network-type>

    The physical mechanism by which the virtual network is implemented.
    The supported options are: flat, geneve, gre, local, vlan, vxlan.

    *Network version 2 only*

.. option:: --provider-physical-network <provider-physical-network>

    Name of the physical network over which the virtual network is implemented

    *Network version 2 only*

.. option:: --provider-segment <provider-segment>

    VLAN ID for VLAN networks or Tunnel ID for GENEVE/GRE/VXLAN networks

    *Network version 2 only*

.. option:: --qos-policy <qos-policy>

    QoS policy to attach to this network (name or ID)

    *Network version 2 only*

.. option:: --transparent-vlan

    Make the network VLAN transparent

    *Network version 2 only*

.. option:: --no-transparent-vlan

    Do not make the network VLAN transparent

    *Network version 2 only*

.. option:: --tag <tag>

    Tag to be added to the network (repeat option to set multiple tags)

    *Network version 2 only*

.. option:: --no-tag

    No tags associated with the network

    *Network version 2 only*

.. _network_create-name:
.. describe:: <name>

    New network name

network delete
--------------

Delete network(s)

.. program:: network delete
.. code:: bash

    openstack network delete
        <network> [<network> ...]

.. _network_delete-network:
.. describe:: <network>

    Network(s) to delete (name or ID)

network list
------------

List networks

.. program:: network list
.. code:: bash

    openstack network list
        [--external | --internal]
        [--long]
        [--name <name>]
        [--enable | --disable]
        [--project <project> [--project-domain <project-domain>]]
        [--share | --no-share]
        [--status <status>]
        [--provider-network-type <provider-network-type>]
        [--provider-physical-network <provider-physical-network>]
        [--provider-segment <provider-segment>]
        [--agent <agent-id>]
        [--tags <tag>[,<tag>,...]] [--any-tags <tag>[,<tag>,...]]
        [--not-tags <tag>[,<tag>,...]] [--not-any-tags <tag>[,<tag>,...]]

.. option:: --external

    List external networks

    *Network version 2 only*

.. option:: --internal

    List internal networks

    *Network version 2 only*

.. option:: --long

    List additional fields in output

    *Network version 2 only*

.. option:: --name <name>

    List networks according to their name

    *Network version 2 only*

.. option:: --enable

    List enabled networks

    *Network version 2 only*

.. option:: --disable

    List disabled networks

    *Network version 2 only*

.. option:: --project <project>

    List networks according to their project (name or ID)

    *Network version 2 only*

.. option:: --project-domain <project-domain>

    Domain the project belongs to (name or ID).
    This can be used in case collisions between project names exist.

    *Network version 2 only*

.. option:: --share

    List networks shared between projects

    *Network version 2 only*

.. option:: --no-share

    List networks not shared between projects

    *Network version 2 only*

.. option:: --status <status>

    List networks according to their status
    ('ACTIVE', 'BUILD', 'DOWN', 'ERROR')

.. option:: --provider-network-type <provider-network-type>

    List networks according to their physical mechanisms.
    The supported options are: flat, geneve, gre, local, vlan, vxlan.

    *Network version 2 only*

.. option:: --provider-physical-network <provider-physical-network>

    List networks according to name of the physical network

    *Network version 2 only*

.. option:: --provider-segment <provider-segment>

    List networks according to VLAN ID for VLAN networks
    or Tunnel ID for GENEVE/GRE/VXLAN networks

    *Network version 2 only*

.. option:: --agent <agent-id>

    List networks hosted by agent (ID only)

    *Network version 2 only*

.. option:: --tags <tag>[,<tag>,...]

    List networks which have all given tag(s)

    *Network version 2 only*

.. option:: --any-tags <tag>[,<tag>,...]

    List networks which have any given tag(s)

    *Network version 2 only*

.. option:: --not-tags <tag>[,<tag>,...]

    Exclude networks which have all given tag(s)

    *Network version 2 only*

.. option:: --not-any-tags <tag>[,<tag>,...]

    Exclude networks which have any given tag(s)

    *Network version 2 only*

network set
-----------

Set network properties

*Network version 2 only*

.. program:: network set
.. code:: bash

    openstack network set
        [--name <name>]
        [--enable | --disable]
        [--share | --no-share]
        [--description <description>]
        [--enable-port-security | --disable-port-security]
        [--external [--default | --no-default] | --internal]
        [--provider-network-type <provider-network-type>]
        [--provider-physical-network <provider-physical-network>]
        [--provider-segment <provider-segment>]
        [--qos-policy <qos-policy> | --no-qos-policy]
        [--tag <tag>] [--no-tag]
        <network>

.. option:: --name <name>

    Set network name

.. option:: --enable

    Enable network

.. option:: --disable

    Disable network

.. option:: --share

    Share the network between projects

.. option:: --no-share

    Do not share the network between projects

.. option:: --description <description>

    Set network description

.. option:: --enable-port-security

    Enable port security by default for ports created on
    this network

.. option:: --disable-port-security

    Disable port security by default for ports created on
    this network

.. option:: --external

    Set this network as an external network.
    (external-net extension required)

.. option:: --internal

    Set this network as an internal network

.. option:: --default

    Set the network as the default external network

.. option:: --no-default

    Do not use the network as the default external network.

.. option:: --provider-network-type <provider-network-type>

    The physical mechanism by which the virtual network is implemented.
    The supported options are: flat, gre, local, vlan, vxlan.

.. option:: --provider-physical-network <provider-physical-network>

    Name of the physical network over which the virtual network is implemented

.. option:: --provider-segment <provider-segment>

    VLAN ID for VLAN networks or Tunnel ID for GRE/VXLAN networks

.. option:: --qos-policy <qos-policy>

    QoS policy to attach to this network (name or ID)

.. option:: --no-qos-policy

    Remove the QoS policy attached to this network

.. option:: --tag <tag>

    Tag to be added to the network (repeat option to set multiple tags)

.. option:: --no-tag

    Clear tags associated with the network. Specify both --tag
    and --no-tag to overwrite current tags

.. _network_set-network:
.. describe:: <network>

    Network to modify (name or ID)

network show
------------

Display network details

.. program:: network show
.. code:: bash

    openstack network show
        <network>

.. _network_show-network:
.. describe:: <network>

    Network to display (name or ID)

network unset
-------------

Unset network properties

*Network version 2 only*

.. program:: network unset
.. code:: bash

    openstack network unset
        [--tag <tag> | --all-tag]
        <network>

.. option:: --tag <tag>

    Tag to be removed from the network
    (repeat option to remove multiple tags)

.. option:: --all-tag

    Clear all tags associated with the network

.. _network_unset-network:
.. describe:: <network>

    Network to modify (name or ID)

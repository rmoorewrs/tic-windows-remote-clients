=================
identity provider
=================

Identity v3

`Requires: OS-FEDERATION extension`

identity provider create
------------------------

Create new identity provider

.. program:: identity provider create
.. code:: bash

    openstack identity provider create
        [--remote-id <remote-id> [...] | --remote-id-file <file-name>]
        [--description <description>]
        [--domain <domain>]
        [--enable | --disable]
        <name>

.. option:: --remote-id <remote-id>

    Remote IDs to associate with the Identity Provider
    (repeat option to provide multiple values)

.. option:: --remote-id-file <file-name>

    Name of a file that contains many remote IDs to associate with the identity
    provider, one per line

.. option:: --description

    New identity provider description

.. option:: --domain

    Name or ID of the domain to associate with the identity provider. If not
    specified, one will be created automatically

.. option:: --enable

    Enable the identity provider (default)

.. option:: --disable

    Disable the identity provider

.. describe:: <name>

    New identity provider name (must be unique)

identity provider delete
------------------------

Delete identity provider(s)

.. program:: identity provider delete
.. code:: bash

    openstack identity provider delete
        <identity-provider> [<identity-provider> ...]

.. describe:: <identity-provider>

    Identity provider(s) to delete

identity provider list
----------------------

List identity providers

.. program:: identity provider list
.. code:: bash

    openstack identity provider list

identity provider set
---------------------

Set identity provider properties

.. program:: identity provider set
.. code:: bash

    openstack identity provider set
        [--remote-id <remote-id> [...] | --remote-id-file <file-name>]
        [--description <description>]
        [--enable | --disable]
        <identity-provider>

.. option:: --remote-id <remote-id>

    Remote IDs to associate with the Identity Provider
    (repeat option to provide multiple values)

.. option:: --remote-id-file <file-name>

    Name of a file that contains many remote IDs to associate with the identity
    provider, one per line

.. option:: --description

    Set identity provider description

.. option:: --enable

    Enable the identity provider

.. option:: --disable

    Disable the identity provider

.. describe:: <identity-provider>

    Identity provider to modify

identity provider show
----------------------

Display identity provider details

.. program:: identity provider show
.. code:: bash

    openstack identity provider show
        <identity-provider>

.. describe:: <identity-provider>

    Identity provider to display

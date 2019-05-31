.. _plugin-commands:

===============
Plugin Commands
===============

.. list-plugins:: openstack.cli.extension

aodh
----

.. list-plugins:: openstack.alarming.v2
   :detailed:

barbican
--------

.. list-plugins:: openstack.key_manager.v1
   :detailed:

congress
--------

.. list-plugins:: openstack.congressclient.v1
   :detailed:

.. cue
.. # cueclient is not in global-requirements
.. # list-plugins:: openstack.mb.v1
.. #   :detailed:

designate
---------

.. list-plugins:: openstack.dns.v1
   :detailed:

gnocchi
-------
.. list-plugins:: openstack.metric.v1
   :detailed:

heat
----

.. list-plugins:: openstack.orchestration.v1
   :detailed:

ironic
------

.. list-plugins:: openstack.baremetal.v1
   :detailed:

ironic-inspector
----------------

.. list-plugins:: openstack.baremetal_introspection.v1
   :detailed:

.. karbor
.. ------
.. bug 1705258: Exclude karborclient 0.4.0 until a fixed version is released.
.. .. list-plugins:: openstack.data_protection.v1
..    :detailed:

mistral
-------

.. list-plugins:: openstack.workflow_engine.v2
   :detailed:

.. murano
.. # the murano docs cause warnings and a broken docs build
.. # .. list-plugins:: openstack.application_catalog.v1
.. #   :detailed:

neutron
-------

.. list-plugins:: openstack.neutronclient.v2
   :detailed:

octavia
-------

.. list-plugins:: openstack.load_balancer.v2
   :detailed:

sahara
------

.. list-plugins:: openstack.data_processing.v1
   :detailed:

searchlight
-----------

.. list-plugins:: openstack.search.v1
   :detailed:

senlin
------

.. list-plugins:: openstack.clustering.v1
   :detailed:

.. tripleo
.. # tripleoclient is not in global-requirements
.. # list-plugins:: openstack.tripleoclient.v1
.. #   :detailed:

trove
------

.. list-plugins:: openstack.database.v1
   :detailed:

.. watcher
.. # watcherclient is not in global-requirements
.. # list-plugins:: openstack.infra_optim.v1
.. #  :detailed:

zaqar
-----

.. list-plugins:: openstack.messaging.v2
   :detailed:

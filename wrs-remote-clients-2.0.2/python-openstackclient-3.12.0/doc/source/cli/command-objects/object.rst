======
object
======

Object Storage v1

object create
-------------

Upload object to container

.. program:: object create
.. code:: bash

    openstack object create
        [--name <name>]
        <container>
        <filename> [<filename> ...]

.. option:: --name <name>

    Upload a file and rename it. Can only be used when uploading a single object

.. describe:: <container>

    Container for new object

.. describe:: <filename>

    Local filename(s) to upload

object delete
-------------

Delete object from container

.. program:: object delete
.. code:: bash

    openstack object delete
        <container>
        <object> [<object> ...]

.. describe:: <container>

    Delete object(s) from <container>

.. describe:: <object>

    Object(s) to delete

object list
-----------

List objects

.. program object list
.. code:: bash

    openstack object list
        [--prefix <prefix>]
        [--delimiter <delimiter>]
        [--marker <marker>]
        [--end-marker <end-marker>]
        [--limit <num-objects>]
        [--long]
        [--all]
        <container>

.. option:: --prefix <prefix>

    Filter list using <prefix>

.. option:: --delimiter <delimiter>

    Roll up items with <delimiter>

.. option:: --marker <marker>

    Anchor for paging

.. option:: --end-marker <end-marker>

    End anchor for paging

.. option:: --limit <num-objects>

    Limit number of objects returned

.. option:: --long

    List additional fields in output

.. option:: --all

    List all objects in <container> (default is 10000)

.. describe:: <container>

    Container to list

object save
-----------

Save object locally

.. program:: object save
.. code:: bash

    openstack object save
        [--file <filename>]
        <container>
        <object>

.. option:: --file <filename>

    Destination filename (defaults to object name);
    using - as the filename will print the file to stdout

.. describe:: <container>

    Download <object> from <container>

.. describe:: <object>

    Object to save

object set
----------

Set object properties

.. program:: object set
.. code:: bash

    openstack object set
        [--property <key=value> [...] ]
        <container>
        <object>

.. option:: --property <key=value>

    Set a property on this object (repeat option to set multiple properties)

.. describe:: <container>

    Modify <object> from <container>

.. describe:: <object>

    Object to modify

object show
-----------

Display object details

.. program:: object show
.. code:: bash

    openstack object show
        <container>
        <object>

.. describe:: <container>

    Display <object> from <container>

.. describe:: <object>

    Object to display

object unset
------------

Unset object properties

.. program:: object unset
.. code:: bash

    openstack object unset
        [--property <key>]
        <container>
        <object>

.. option:: --property <key>

    Property to remove from object (repeat option to remove multiple properties)

.. describe:: <container>

    Modify <object> from <container>

.. describe:: <object>

    Object to modify

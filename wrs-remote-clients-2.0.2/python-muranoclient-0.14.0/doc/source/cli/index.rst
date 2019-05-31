=================
Murano API Client
=================

In order to use the python api directly, you must first obtain an auth token
and identify which endpoint you wish to speak to. Once you have done so,
you can use the API like so::

    >>> from muranoclient import Client
    >>> murano = Client('1', endpoint=MURANO_URL, token=OS_AUTH_TOKEN)
    ...


Command-line Tool
=================

In order to use the CLI, you must provide your OpenStack username,
password, tenant, and auth endpoint. Use the corresponding configuration
options (:option:``--os-username``, :option:``--os-password``,
:option:``--os-tenant-id``, and :option:``--os-auth-url``) or
set them in environment variables::

    export OS_USERNAME=user
    export OS_PASSWORD=pass
    export OS_TENANT_ID=b363706f891f48019483f8bd6503c54b
    export OS_AUTH_URL=http://auth.example.com:5000/v2.0

The command line tool will attempt to reauthenticate using your provided
credentials for every request. You can override this behavior by manually
supplying an auth token using :option:``--os-image-url`` and
:option:``--os-auth-token``. You can alternatively set these environment
variables::

    export MURANO_URL=http://murano.example.org:8082/
    export OS_AUTH_TOKEN=3bcc3d3a03f44e3d8377f9247b0ad155

Once you've configured your authentication parameters, you can run
:command:`murano help` to see a complete listing of available commands.

.. toctree::

   murano

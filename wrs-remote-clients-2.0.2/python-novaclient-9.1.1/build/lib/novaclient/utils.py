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

import contextlib
import json
import os
import re
import textwrap
import time
import uuid

from oslo_serialization import jsonutils
from oslo_utils import encodeutils
import prettytable
import six
from six.moves.urllib import parse

from datetime import datetime
import dateutil
from dateutil import parser

from novaclient import exceptions
from novaclient.i18n import _


VALID_KEY_REGEX = re.compile(r"[\w\.\- :]+$", re.UNICODE)


def env(*args, **kwargs):
    """Returns the first environment variable set.

    If all are empty, defaults to '' or keyword arg `default`.
    """
    for arg in args:
        value = os.environ.get(arg)
        if value:
            return value
    return kwargs.get('default', '')


def get_service_type(f):
    """Retrieves service type from function."""
    return getattr(f, 'service_type', None)


def unauthenticated(func):
    """Adds 'unauthenticated' attribute to decorated function.

    Usage:

    >>> @unauthenticated
    ... def mymethod(f):
    ...     pass
    """
    func.unauthenticated = True
    return func


def isunauthenticated(func):
    """Checks if the function does not require authentication.

    Mark such functions with the `@unauthenticated` decorator.

    :returns: bool
    """
    return getattr(func, 'unauthenticated', False)


def arg(*args, **kwargs):
    """Decorator for CLI args.

    Example:

    >>> @arg("name", help="Name of the new entity")
    ... def entity_create(args):
    ...     pass
    """
    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func
    return _decorator


def add_arg(func, *args, **kwargs):
    """Bind CLI arguments to a shell.py `do_foo` function."""

    if not hasattr(func, 'arguments'):
        func.arguments = []

    # NOTE(sirp): avoid dups that can occur when the module is shared across
    # tests.
    if (args, kwargs) not in func.arguments:
        # Because of the semantics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        func.arguments.insert(0, (args, kwargs))


def service_type(stype):
    """Adds 'service_type' attribute to decorated function.
    Usage:
    .. code-block:: python
       @service_type('volume')
       def mymethod(f):
       ...
    """
    def inner(f):
        f.service_type = stype
        return f
    return inner


def add_resource_manager_extra_kwargs_hook(f, hook):
    """Add hook to bind CLI arguments to ResourceManager calls.

    The `do_foo` calls in shell.py will receive CLI args and then in turn pass
    them through to the ResourceManager. Before passing through the args, the
    hooks registered here will be called, giving us a chance to add extra
    kwargs (taken from the command-line) to what's passed to the
    ResourceManager.
    """
    if not hasattr(f, 'resource_manager_kwargs_hooks'):
        f.resource_manager_kwargs_hooks = []

    names = [h.__name__ for h in f.resource_manager_kwargs_hooks]
    if hook.__name__ not in names:
        f.resource_manager_kwargs_hooks.append(hook)


def get_resource_manager_extra_kwargs(f, args, allow_conflicts=False):
    """Return extra_kwargs by calling resource manager kwargs hooks."""
    hooks = getattr(f, "resource_manager_kwargs_hooks", [])
    extra_kwargs = {}
    for hook in hooks:
        hook_kwargs = hook(args)
        hook_name = hook.__name__
        conflicting_keys = set(hook_kwargs.keys()) & set(extra_kwargs.keys())
        if conflicting_keys and not allow_conflicts:
            msg = (_("Hook '%(hook_name)s' is attempting to redefine "
                     "attributes '%(conflicting_keys)s'") %
                   {'hook_name': hook_name,
                    'conflicting_keys': conflicting_keys})
            raise exceptions.NoUniqueMatch(msg)

        extra_kwargs.update(hook_kwargs)

    return extra_kwargs


def pretty_choice_list(l):
    return ', '.join("'%s'" % i for i in l)


def pretty_choice_dict(d):
    """Returns a formatted dict as 'key=value'."""
    return pretty_choice_list(['%s=%s' % (k, d[k]) for k in sorted(d.keys())])


def parse_date(string_data):
    """Parses a date-like input string into a timezone aware Python
    datetime.
    """
    if not isinstance(string_data, six.string_types):
        return string_data

    pattern = r'(\d{4}-\d{2}-\d{2}[T ])?\d{2}:\d{2}:\d{2}(\.\d{6})?Z?'

    def convert_date(matchobj):
        formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d %H:%M:%S.%f",
                   "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S",
                   "%Y-%m-%dT%H:%M:%SZ", "%H:%M:%S"]
        datestring = matchobj.group(0)
        if datestring:
            for format in formats:
                try:
                    datetime.strptime(datestring, format)
                    datestring += "+0000"
                    parsed = parser.parse(datestring)
                    converted = parsed.astimezone(dateutil.tz.tzlocal())
                    converted = datetime.strftime(converted, format)
                    return converted
                except Exception:
                    pass
        return datestring

    return re.sub(pattern, convert_date, string_data)


def print_list(objs, fields, formatters={}, sortby_index=None):
    if sortby_index is None:
        sortby = None
    else:
        sortby = fields[sortby_index]
    mixed_case_fields = ['serverId']
    pt = prettytable.PrettyTable([f for f in fields], caching=False)
    pt.align = 'l'

    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                row.append(parse_date(formatters[field](o)))
            else:
                if field in mixed_case_fields:
                    field_name = field.replace(' ', '_')
                else:
                    field_name = field.lower().replace(' ', '_')
                data = getattr(o, field_name, '')
                if data is None:
                    data = '-'
                # '\r' would break the table, so remove it.
                data = six.text_type(data).replace("\r", "")
                data = parse_date(data)
                row.append(data)
        pt.add_row(row)

    if sortby is not None:
        result = encodeutils.safe_encode(pt.get_string(sortby=sortby))
    else:
        result = encodeutils.safe_encode(pt.get_string())

    if six.PY3:
        result = result.decode()

    print(result)


def _flatten(data, prefix=None):
    """Flatten a dict, using name as a prefix for the keys of dict.

    >>> _flatten('cpu_info', {'arch':'x86_64'})
    [('cpu_info_arch': 'x86_64')]

    """
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = '%s_%s' % (prefix, key) if prefix else key
            if isinstance(value, (dict, list)) and value:
                for item in _flatten(value, new_key):
                    yield item
            else:
                yield new_key, value
    else:
        yield prefix, data


def flatten_dict(data):
    """Return a new dict whose sub-dicts have been merged into the
    original.  Each of the parents keys are prepended to the child's
    to prevent collisions.  Any string elements will be JSON parsed
    before flattening.

    >>> flatten_dict({'service': {'host':'cloud9@compute-068', 'id': 143}})
    {'service_host': colud9@compute-068', 'service_id': 143}

    """
    data = data.copy()
    # Try and decode any nested JSON structures.
    for key, value in data.items():
        if isinstance(value, six.string_types):
            try:
                data[key] = json.loads(value)
            except ValueError:
                pass

    return dict(_flatten(data))


def print_dict(d, dict_property="Property", dict_value="Value", wrap=0):
    pt = prettytable.PrettyTable([dict_property, dict_value], caching=False)
    pt.align = 'l'
    for k, v in sorted(d.items()):
        # convert dict to str to check length
        if isinstance(v, (dict, list)):
            v = jsonutils.dumps(v, ensure_ascii=False)
        if wrap > 0:
            v = textwrap.fill(six.text_type(v), wrap)
        # if value has a newline, add in multiple rows
        # e.g. fault with stacktrace
        v = parse_date(v)
        if v and isinstance(v, six.string_types) and (r'\n' in v or '\r' in v):
            # '\r' would break the table, so remove it.
            if '\r' in v:
                v = v.replace('\r', '')
            lines = v.strip().split(r'\n')
            col1 = k
            for line in lines:
                pt.add_row([col1, line])
                col1 = ''
        else:
            if v is None:
                v = '-'
            pt.add_row([k, v])

    result = encodeutils.safe_encode(pt.get_string())

    if six.PY3:
        result = result.decode()

    print(result)


def find_resource(manager, name_or_id, wrap_exception=True, **find_args):
    """Helper for the _find_* methods."""
    # for str id which is not uuid (for Flavor, Keypair and hypervsior in cells
    # environments search currently)
    if getattr(manager, 'is_alphanum_id_allowed', False):
        try:
            return manager.get(name_or_id)
        except exceptions.NotFound:
            pass

    # first try to get entity as uuid
    try:
        tmp_id = encodeutils.safe_encode(name_or_id)

        if six.PY3:
            tmp_id = tmp_id.decode()

        uuid.UUID(tmp_id)
        return manager.get(tmp_id)
    except (TypeError, ValueError, exceptions.NotFound):
        pass

    # then try to get entity as name
    try:
        try:
            resource = getattr(manager, 'resource_class', None)
            name_attr = resource.NAME_ATTR if resource else 'name'
            kwargs = {name_attr: name_or_id}
            kwargs.update(find_args)
            return manager.find(**kwargs)
        except exceptions.NotFound:
            pass

        # then try to find entity by human_id
        try:
            return manager.find(human_id=name_or_id, **find_args)
        except exceptions.NotFound:
            pass
    except exceptions.NoUniqueMatch:
        msg = (_("Multiple %(class)s matches found for '%(name)s', use an ID "
                 "to be more specific.") %
               {'class': manager.resource_class.__name__.lower(),
                'name': name_or_id})
        if wrap_exception:
            raise exceptions.CommandError(msg)
        raise exceptions.NoUniqueMatch(msg)

    # finally try to get entity as integer id
    try:
        return manager.get(int(name_or_id))
    except (TypeError, ValueError, exceptions.NotFound):
        msg = (_("No %(class)s with a name or ID of '%(name)s' exists.") %
               {'class': manager.resource_class.__name__.lower(),
                'name': name_or_id})
        if wrap_exception:
            raise exceptions.CommandError(msg)
        raise exceptions.NotFound(404, msg)


def format_servers_list_networks(server):
    output = []
    for (network, addresses) in server.networks.items():
        if len(addresses) == 0:
            continue
        addresses_csv = ', '.join(addresses)
        group = "%s=%s" % (network, addresses_csv)
        output.append(group)

    return '; '.join(output)


def _format_servers_list_addresses(server):
    output = []
    unsorted_nics = getattr(server, 'wrs-if:nics', [])
    # Each entry in the nics list is a single key dictionary where the key is
    # the name of the nic (e.g., nic0) and the value is a dictionary of the nic
    # attributes.  For example,
    #         nics = [{'nic0': {'network': 'net1', 'vif-model': 'virtio'...}},
    #                 {'nic1': {'network': 'net2', 'vif-model': 'avp'...}}]
    #
    for entry in sorted(unsorted_nics, key=lambda nic: nic.keys()[0]):
        nic = entry.values()[0]
        addresses = []
        for address in server.addresses.get(nic['network'], []):
            if address['addr'] is None:
                continue
            if address['OS-EXT-IPS-MAC:mac_addr'] == nic['mac_address']:
                addresses.append(address['addr'])
        addresses_csv = ', '.join([a for a in addresses] or ["No Address"])
        group = "%s=%s" % (nic['network'], addresses_csv)
        output.append(group)
    return '; '.join(output)


def format_security_groups(groups):
    return ', '.join(group['name'] for group in groups)


def _format_field_name(attr):
    """Format an object attribute in a human-friendly way."""
    # Split at ':' and leave the extension name as-is.
    parts = attr.rsplit(':', 1)
    name = parts[-1].replace('_', ' ')
    # Don't title() on mixed case
    if name.isupper() or name.islower():
        name = name.title()
    parts[-1] = name
    return ': '.join(parts)


def make_field_formatter(attr, filters=None):
    """
    Given an object attribute, return a formatted field name and a
    formatter suitable for passing to print_list.

    Optionally pass a dict mapping attribute names to a function. The function
    will be passed the value of the attribute and should return the string to
    display.
    """
    filter_ = None
    if filters:
        filter_ = filters.get(attr)

    def get_field(obj):
        field = getattr(obj, attr, '')
        if field and filter_:
            field = filter_(field)
        return field

    name = _format_field_name(attr)
    formatter = get_field
    return name, formatter


def safe_issubclass(*args):
    """Like issubclass, but will just return False if not a class."""

    try:
        if issubclass(*args):
            return True
    except TypeError:
        pass

    return False


def do_action_on_many(action, resources, success_msg, error_msg):
    """Helper to run an action on many resources."""
    failure_flag = False

    for resource in resources:
        try:
            action(resource)
            print(success_msg % resource)
        except Exception as e:
            failure_flag = True
            print(encodeutils.safe_encode(six.text_type(e)))

    if failure_flag:
        raise exceptions.CommandError(error_msg)


def is_integer_like(val):
    """Returns validation of a value as an integer."""
    try:
        int(val)
        return True
    except (TypeError, ValueError, AttributeError):
        return False


def validate_flavor_metadata_keys(keys):
    for key in keys:
        valid_name = VALID_KEY_REGEX.match(key)
        if not valid_name:
            msg = _('Invalid key: "%s". Keys may only contain letters, '
                    'numbers, spaces, underscores, periods, colons and '
                    'hyphens.')
            raise exceptions.CommandError(msg % key)


@contextlib.contextmanager
def record_time(times, enabled, *args):
    """Record the time of a specific action.

    :param times: A list of tuples holds time data.
    :type times: list
    :param enabled: Whether timing is enabled.
    :type enabled: bool
    :param *args: Other data to be stored besides time data, these args
                  will be joined to a string.
    """
    if not enabled:
        yield
    else:
        start = time.time()
        yield
        end = time.time()
        times.append((' '.join(args), start, end))


def prepare_query_string(params):
    """Convert dict params to query string"""
    params = sorted(params.items(), key=lambda x: x[0])
    return '?%s' % parse.urlencode(params) if params else ''

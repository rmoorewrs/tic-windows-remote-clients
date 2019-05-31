#   Copyright 2012-2018 OpenStack Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
#   Copyright (c) 2013-2018 Wind River Systems, Inc.
#
#   The right to copy, distribute, modify, or otherwise make use
#   of this software may be licensed only pursuant to the terms
#   of an applicable Wind River license agreement.
#

#   WRS extension

from osc_lib.command import command
from osc_lib import utils
import six

from openstackclient.i18n import _

from oslo_utils import strutils
from ceilometerclient import exc
from ceilometerclient.common import utils as ceilometer_utils


class ListPipeline(command.Lister):
    """List the pipelines ."""

    def get_parser(self, prog_name):
        parser = super(ListPipeline, self).get_parser(prog_name)
        parser.add_argument(
            "-q", "--query", 
            metavar="<QUERY>",
            help=_("key[op]value; list.")
        )
        return parser

    def take_action(self, parsed_args):
        ceilometer_client = self.app.client_manager.telemetry

        columns = (
            "Name",
            "Enabled",
            "Location",
            "Max Bytes",
            "Backup Count",
            "Compress",
        )

        pipelines = ceilometer_client.pipelines.list()

        return (columns,
                (utils.get_item_properties(
                    s, columns,
                ) for s in pipelines))


class ShowPipeline(command.ShowOne):
    """Show details of a given pipeline."""

    def get_parser(self, prog_name):
        parser = super(ShowPipeline, self).get_parser(prog_name)
        parser.add_argument(
            "-n", "--name",
            metavar="<PIPELINE_NAME>",
            help=_("Name of the pipeline to show.")
        )
        return parser

    def take_action(self, parsed_args):
        ceilometer_client = self.app.client_manager.telemetry
        pipelines = ceilometer_client.pipelines.get(parsed_args.name)
        data = pipelines._info.copy()
        return zip(*sorted(six.iteritems(data)))


def _show_pipeline(pipeline):
    fields = ['name', 'enabled', 'location', 'max_bytes',
              'backup_count', 'compress']
    data = dict([(f, getattr(pipeline, f, '')) for f in fields])
    ceilometer_utils.print_dict(data, wrap=72)
       

class UpdatePipeline(command.Command):
    """Update output values for an existing csv pipeline"""

    def get_parser(self, prog_name):
        parser = super(UpdatePipeline, self).get_parser(prog_name)
        parser.add_argument(
            "-n", "--name",
            required=True,
            metavar="<PIPELINE_NAME>",
            help=_("Name of the pipeline to update.")
        )
        parser.add_argument(
            "--enabled", 
            type=strutils.bool_from_string,
            metavar="{True|False}",
            help=_("True if enabling this pipeline")
        )
        parser.add_argument(
            "--location", 
            metavar="<LOCATION>",
            help=_("Full Path of the output file.")
        )
        parser.add_argument(
            "--backup_count",
            type=int,
            metavar="<BACKUP_COUNT>",
            help=_("Number of backup files to keep.")
        )
        parser.add_argument(
            "--max_bytes",
            type=int,
            metavar="<MAX_BYTES>",
            help=_("Maximum size of the file in bytes.")
        )
        parser.add_argument(
            "--compress",
            type=strutils.bool_from_string,
            metavar="{True|False}",
            help=_("True if compressing backups.")
        )        
        return parser

    def take_action(self, parsed_args):
        """Update output values for an existing csv pipeline."""
        ceilometer_client = self.app.client_manager.telemetry
             
        fields = dict(filter(lambda x: not (x[1] is None), vars(parsed_args).items()))
        fields = ceilometer_utils.key_with_slash_to_nested_dict(fields)
        fields.pop('name')
        try:
            pipeline = ceilometer_client.pipelines.update(parsed_args.name, **fields)
        except exc.HTTPNotFound:
            raise exc.CommandError('Pipeline not found: %s' % parsed_args.name)
        _show_pipeline(pipeline)

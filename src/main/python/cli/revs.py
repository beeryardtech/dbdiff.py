#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

import gettext
import json
import logging
import pydash as _
import os
from os.path import dirname, realpath # for library path manipulation
import sys

sys.path.insert(0, '{}/libs'.format(dirname(realpath(__file__))))
from libs import auth, pathutils

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

__log__  = logging.getLogger(__name__)


def add_args(parser):
    """Add my arguments to the given argparse parser."""
    parser.add_argument(
        "local_file",
        help = _("Path to file. This will be parsed to see find path relative to Dropbox dir"),
    )

    parser.add_argument(
        "--format",
        default = "json",
        help = _("Which formatter function to use")
    )


def run(config):
    """
    Gets the revisions for a given dropbox file. If set, produces the revs in
    different formats.
    """
    # Get client
    client, config = auth.build_client(config)

    # Get the remote path for the given file
    pathutils.get_db_basepath()
    remote_path = pathutils.find_remote_db_path(config.get("local_file"))

    # Now get the revisions of the given file
    revs = client.revisions(remote_path)

def select_formatter(name):
    """"
    Selects which formatter function to use based on the string `name`. Pulls
    from a list (map). If `format_name` is not in map, logs a warning and defaults to json
    """
    name = str(name).lower()

FORMATTER_MAP = {
    "json": _.partial(json.dumps)
}

if __name__ == '__main__':
    run(sys.argv)

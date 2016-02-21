#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

from dropbox import rest as dbrest
import logging
import sys
from libs import auth, pathutils

__author__ = "Travis Goldie and Janie Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

__log__ = logging.getLogger(__name__)


def add_args(parser):
    """Add my arguments to the given argparse parser."""
    parser.add_argument(
        "local_file",
        help = "Path to local file. This will be parsed to see find path relative to Dropbox dir",
    )

    parser.add_argument(
        "dest",
        help = "Path to destination inside of Dropbox.",
    )
    return 


def run(config):
    """
    Puts file into destination within Dropbox
    """
    # Get client
    client, config = auth.build_client(config)

    local_path = config.get("local_file")
    dest_path = pathutils.find_remote_db_path(config.get("dest"))

    put_file = __do_put(local_path, dest_path, client, config)

    return put_file


def __do_put(local_path, dest_path, client, config):
    """
    This puts file into Dropbox using the client.
    """
    with open(local_path) as local_fp:
        try:
            put_response = client.put_file(dest_path, local_fp)

        except dbrest.ErrorResponse as err:
            __log__.exception(
                "Failed to put file {} at dest {}. Message: {}".format(
                    local_path,
                    dest_path,
                    err.message
                )
            )

    return put_response

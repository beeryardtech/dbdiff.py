#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

from dropbox import rest as dbrest
import logging
import sys
from libs import authutils, pathutils

__author__ = "Travis Goldie"
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
        "-d",
        "--dest",
        default = "STDOUT",
        help = "Output destination filepath. Defaults to STDOUT"
    )

    parser.add_argument(
        "-i"
        "--index",
        default = None,
        help = "Which revision position to use. 0 is the newest revision"
    )

    parser.add_argument(
        "-r"
        "--rev",
        default = None,
        help = "The hash of a given revision for the file."
    )

    # TODO Create a arg for getting by date


def run(config):
    """
    Gets a copy of the file from dropbox store. If specified gets
    """
    # Get client
    client, config = authutils.build_client(config)

    # Get the remote path for the given file
    remote_path = pathutils.find_remote_db_path(config.get("local_file"))

    try:
        get_file = __do_output(remote_path, client, config)
    except dbrest.ErrorResponse as err:
        __log__.error("Failed to output file! Message: {}".format(err.message))

    return get_file


def __do_output(remote_path, client, config):
    """
    Outputs the fetched `remote_path` to either a file or to STDOUT
    """
    dest = config.get("dest", "STDOUT")

    __log__.debug("Outputting remote file '{}' to '{}'".format(remote_path, dest))

    # XXX Note that no control over bitsize done here. If needed can
    # implement a while loop to load file in blocks
    with client.get_file(remote_path, rev = config.get("rev")) as get_file:
        if dest == "STDOUT":
            sys.stdout.write(get_file.read())
        else:
            dest = pathutils.normpath(dest)
            __output_to_file(dest, get_file)

    return get_file


def __output_to_file(dest, get_file):
    """ Opens file handler and outputs to a file"""
    try:
        with open(dest, "w+") as dest_fp:
            dest_fp.write(get_file.read())

    except OSError as err:
        __log__.exception("Failed to write to destination {}. Mesage: {}".format(dest, err.message))

    return

if __name__ == '__main__':
    pass

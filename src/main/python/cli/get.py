#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

import logging
import sys
from libs import auth, pathutils

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
        "-r"
        "--rev",
        help = "Which given revision position to use. 0 is the newest revision"
    )

    # TODO Create a arg for getting by date


def run(config):
    """
    Gets a copy of the file from dropbox store. If specified gets
    """
    # Get client
    authutils = reload(auth)
    __log__.info("here {}".format(config))
    client, config = authutils.build_client(config)

    # Get the remote path for the given file
    # remote_path = pathutils.find_remote_db_path(config.get("local_file"))
    # __log__.info("remote " + remote_path)

    # get_file = __do_output(remote_path, client, config)
    # return get_file
    return


def __do_output(remote_path, client, config):
    """
    Outputs the fetched `remote_path` to either a file or to STDOUT
    """
    dest = config.get("dest", "STDOUT")

    __log__.debug("Outputting remote file '{}' to '{}'".format(remote_path, dest))

    with client.get_file(remote_path) as get_file:
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

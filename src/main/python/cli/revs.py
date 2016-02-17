#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import print_function, with_statement

import logging
import pprint
import json
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
        help = "Path to local file. This will be parsed to see find path relative to Dropbox dir",
    )

    parser.add_argument(
        "-d",
        "--dest",
        default = "print",
        help = "Output destination. Defaults to print."
    )

    parser.add_argument(
        "-f",
        "--format",
        default = "json",
        help = "Which formatter function to use"
    )

    parser.add_argument(
        "-r",
        "--rev_num",
        default = None,
        help = "Outputs only the rev at the given position. Can be negative numbers." +
                "If not given, then outputs all revs"
    )


def run(config):
    """
    Gets the revisions for a given dropbox file. If set, produces the revs in
    different formats.
    """
    # Get client
    client, config = auth.build_client(config)

    # Get the remote path for the given file
    remote_path = pathutils.find_remote_db_path(config.get("local_file"))

    # Now get the revisions of the given file
    revs = client.revisions(remote_path)

    # Which version to use?
    revVal = __get_rev(revs, config)

    # Get the formatter function
    formatter = __get_formatter(config.get("format"))

    # TODO Needs a way to control where to send output
    output = formatter(revVal)
    __do_output(output, config)

    return output


def __get_formatter(name):
    """"
    Selects which formatter function to use based on the string `name`. Pulls
    from a list (map). If `format_name` is not in map, logs a warning and defaults to json
    """
    name = name.lower() if name else "json"
    return FORMATTER_MAP.get(name, FORMATTER_MAP["json"])


def __do_output(output, config):
    """
    Sends `output` to a given change based on `config["revs_dest"]` option.
    Default to `print`.
    """
    dest_str = config.get("revs_dest", "print").lower()
    dest_func = REVS_DEST_MAP.get(dest_str)

    # Now do output
    dest_func(output)
    return


def __get_rev(revs, config):
    """
    Either get a single revision, if `rev_num` is set or return all
    """
    if config.get("rev_num") is not None:
        __log__.debug("Rev num set. {}".format(config.get("rev_num")))
        try:
            if int(config.get("rev_num")) < len(revs):
                pos = int(config.get("rev_num"))
                revToUse = revs[pos]
                __log__.debug("Pos set. New rev is {}".format(revToUse))

        except:
            pass
    else:
        revToUse = revs

    return revToUse


# Maps string to a formatter function. Typically use partial funcs to config the formatters
FORMATTER_MAP = {
    "json": _.partial(json.dumps, indent = 2, sort_keys = True)
}

REVS_DEST_MAP = {
    "print": print,
    "pprint": pprint.pprint
}

if __name__ == '__main__':
    run(sys.argv)

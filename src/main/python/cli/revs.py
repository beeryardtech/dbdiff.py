#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import print_function, with_statement

import json
from libs import authutils, pathutils, vimutils
import pprint
import logging
from pydash import py_ as _
import sys


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
        "-o",
        "--output",
        default = "print",
        help = "Output method. Defaults to print. \n Possible values: {}".format(
            ", ".join(_.map(OUTPUT_MAP.keys(), lambda val: "'{}'".format(val)))
        )
    )

    parser.add_argument(
        "-f",
        "--formatter",
        default = "json",
        help = "Which formatter function to use. Possible values: {}".format(
            ", ".join(_.map(FORMATTER_MAP.keys(), lambda val: "'{}'".format(val)))
        )
    )

    parser.add_argument(
        "-r",
        "--rev_num",
        default = None,
        help = "Outputs only the rev at the given position. Can be negative numbers." +
               "If not given, then outputs all revs"
    )

    parser.add_argument(
        "-R",
        "--rev_list",
        action = "store_true",
        default = None,
        help = "Outputs a list of all the rev hashes."
    )

    return


def run(config):
    """
    Gets the revisions for a given dropbox file. If set, produces the revs in
    different formats.
    """
    # Get client
    client, config = authutils.build_client(config)

    # Get the remote path for the given file
    remote_path = pathutils.find_remote_db_path(config.get("local_file"))

    # Now get the revisions of the given file
    revs = client.revisions(remote_path)

    # Which revision to use?
    revVal = __get_rev(revs, config)

    # Get the formatter function
    formatter = __get_formatter(config.get("formatter"))

    # TODO Needs a way to control where to send output
    output = formatter(revVal)
    if config.get("output"):
        __do_output(output, config)

    if config.get("state_machine"):
        config.get("state_machine").setup(revVal, output)

    return output


def __get_formatter(name):
    """"
    Selects which formatter function to use based on the string `name`. Pulls
    from a list (map). If `format_name` is not in map, logs a warning and defaults to json
    """
    if name:
        formatter = FORMATTER_MAP.get(name.lower(), FORMATTER_MAP["idenity"])
    else:
        __log__.warning("Invalid name for formatter! Name: {}".format(name))
        formatter = FORMATTER_MAP.get("json")

    return formatter


def __do_output(outputVal, config):
    """
    Sends `outputVal` to a given change based on `config["output"]` option.
    Default to `print`.
    """
    outputStr = config.get("output", "print").lower()
    outputFunc = OUTPUT_MAP.get(outputStr)

    # Now do output
    return outputFunc(outputVal)


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

        except Exception as err:
            __log__.debug("Error getting specific rev. Returing all: {}".format(err.message))

    elif config.get("rev_list"):
        __log__.debug("Rev list set. Getting list of revs")
        revToUse = _.pluck(revs, "rev")

    else:
        revToUse = revs

    return revToUse


def hashes_json(output):
    """
    Formatter function to pluck out the revision hashes from the output, then formats it as json
    """
    return _(output).pluck("rev").thru(
        lambda val: json.dumps(val, indent = 2, sort_keys = True)
    ).value()


# Maps string to a formatter function. Typically use partial funcs to config the formatters
FORMATTER_MAP = {
    "json": _.partial(json.dumps, indent = 2, sort_keys = True),
    "hashes": hashes_json,
    "idenity": _.identity,
    "menu": vimutils.build_rev_menu,
}

OUTPUT_MAP = {
    "print": print,
    "pprint": pprint.pprint
}

if __name__ == '__main__':
    run(sys.argv)

#!/usr/bin/python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

import argparse
import ConfigParser
import gettext
import logging
import os
from os.path import dirname, realpath  # for library path manipulation
import sys

# For translations
i18n = gettext.translation('', '{}/../i18n'.format(dirname(realpath(__file__))), fallback = True)
_ = i18n.lgettext

# Setup sys path and the i18n directory
sys.path.insert(0, '{}/cli'.format(dirname(realpath(__file__))))
import cli

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

__log__ = logging.getLogger(__name__)


def main(args):
    """ Create the argparser. """
    parser = add_args(args)

    # Add the args from any cli subcommands under the parser named after
    # the desired name from the cli module
    subparsers = parser.add_subparsers(
        title = _("subcommands"),
        description = _("available subcommands"),
        dest = _("subcommand")
    )

    for sc in cli.subcommands:
        subparser = subparsers.add_parser(
            sc,
            help = _("subcommand for {} operations.").format(sc)
        )
        cli.subcommands[sc].add_args(subparser)

    # Parse the args and be ready to send to each subcommand"s run() method
    opts = parser.parse_args(args[1:])

    opts = merge_opts(opts, opts.config)

    # Disable logging in quit mode. Otherwise enable basic config
    if opts.quiet:
        logging.basicConfig(level = logging.CRITICAL)
    else:
        logging.basicConfig(level = logging.INFO)

    # Debug mode? (turn this on first, in case we want to debug below)
    if opts.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # now, let"s see which subcommand was given and pass everything along to it
    if opts.subcommand:
        cli.subcommands[opts.subcommand].run(opts)
    else:
        parser.print_usage()


def add_args(args):
    """ Add arguments to parser. Return new parser """
    parser = argparse.ArgumentParser(prog = args[0], prefix_chars = '-')

    parser.add_argument(
        "-d",
        "--debug",
        action = "store_true",
        help = _("add debug information to the output, default  =  False"),
        required = False,
    )

    parser.add_argument(
        "--config",
        default = "dbdiff.ini",
        help = _("Path to config file."),
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action = "store_true",
        default = False,
        help = _("Stop all logging. Only output data."),
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action = "store_true",
        help = _("make the output more verbose, default  =  False"),
        required = False,
    )

    return parser


def merge_opts(config_path, parsed_opts):
    """ Merges config file options with command line args """
    config = ConfigParser.SafeConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
    else:
        __log__.critical("Config File does not exist!", config_path)
        raise OSError




    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main(sys.argv)

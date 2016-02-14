#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

import gettext
import logging
from os.path import dirname, realpath  # for library path manipulation
import sys

# For translations
current_dir = dirname(realpath(__file__))
i18n = gettext.translation('', '{}/../i18n'.format(current_dir), fallback = True)
_ = i18n.lgettext

# Setup sys path and the i18n directory
sys.path.insert(0, '{}/cli'.format(dirname(realpath(__file__))))
import cli

sys.path.insert(0, '{}/libs'.format(dirname(realpath(__file__))))
from libs import configutils

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

__log__ = logging.getLogger(__name__)


def main(args):
    """ Create the argparser. """
    parser = configutils.add_args(current_dir, args)

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

    config = configutils.merge_configs(opts.config, opts)

    # Disable logging in quit mode. Otherwise enable basic config
    if config.get("quiet"):
        logging.basicConfig(level = logging.CRITICAL)
    else:
        logging.basicConfig(level = logging.INFO)

    # Handle warnings from urllib3
    # import urllib3
    # urllib3.disable_warnings()
    logging.captureWarnings(True)

    # Debug mode? (turn this on first, in case we want to debug below)
    if config.get("verbose"):
        logging.getLogger().setLevel(logging.DEBUG)

    # Now, let's see which subcommand was given and pass everything along to it
    if opts.subcommand:
        cli.subcommands[opts.subcommand].run(config)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main(sys.argv)

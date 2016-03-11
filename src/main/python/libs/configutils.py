#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

import argparse
import ConfigParser
import logging
import os
import sys
import urllib3

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

__log__ = logging.getLogger(__name__)


def main(args):
    pass


def add_args(current_dir, args):
    """ Add arguments to parser. Return new parser """
    parser = argparse.ArgumentParser(prog = args[0], prefix_chars = '-')

    default_config = "{}/dbdiff.ini".format(current_dir)
    parser.add_argument(
        "--config",
        # XXX This is the only default defined here
        default = default_config,
        help = "Path to config file.\n Default is {}".format(default_config),
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action = "store_true",
        default = None,
        help = "Stop all logging. Only output data.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action = "store_true",
        default = None,
        help = "make the output more verbose, default = False",
        required = False,
    )

    return parser


def merge(configopts, argopts):
    """
    Merges the config options from the file and command line argumetns
    """
    config = {}
    for sect_name in configopts.sections():
        # secct_items is a list of tuples
        sect_items = dict(configopts.items(sect_name))
        config.update(sect_items)

    # Merge in argopts values
    for arg_key, arg_val in vars(argopts).items():
        config[arg_key] = arg_val

    return config


def merge_configs(config_path, argopts):
    """
    Loads and merges the configs
    """
    configopts = load_config_parser(config_path)
    merge_result = merge(configopts, argopts)

    return merge_result


def load_config_parser(config_path):
    """
    Create config parser from the file at `config_path`.
    """
    config_parser = ConfigParser.ConfigParser()

    # Get config file
    if os.path.exists(config_path):
        config_parser.read(config_path)
    else:
        __log__.debug("config_path does not exist! {}".format(config_path))

    return config_parser


def setup_logger(config):
    """
    Sets up the `logging` config. If `quiet` config is set, logging level
    is `CRITICAL`, otherwise defaults to `INFO`.
    """
    # Disable logging in quit mode. Otherwise enable basic config
    if config.get("quiet"):
        logging.basicConfig(level = logging.CRITICAL)
    else:
        logging.basicConfig(level = logging.INFO)

    # Debug mode? (turn this on first, in case we want to debug below)
    if config.get("verbose") or config.get("debug"):
        print("")
        logging.getLogger().setLevel(logging.DEBUG)

    # Handle warnings from urllib3
    urllib3.disable_warnings()
    logging.captureWarnings(True)

    return


if __name__ == '__main__':
    main(sys.argv)

#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

import argparse
import ConfigParser
import logging
import os
import sys

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


def vim_build_config(*sources):
    """
    XXX This should only be used with VIM (say plugin)

    Builds the config object using VIM variables. The `sources` are
    merged in with the created config object.
    """
    varsToKeys = {
        "app_code": "g:dbdiff_config_auth_app_code",
        "app_key": "g:dbdiff_config_auth_app_key",
        "app_secret": "g:dbdiff_config_auth_app_secret",
        "app_token": "g:dbdiff_config_auth_app_token",
        "quit": "g:dbdiff_config_system_quit",
    }
    # Build the config object
    config = vim_eval_var_keys(varsToKeys)

    # Now merge in any additional `sources` to `config`
    for source in sources:
        if isinstance(source, dict):
            config.update(source)
        else:
            __log__.error("Source is not a dict! Type: {} Value: {}".format(type(source), source))

    return config


def vim_eval_var_keys(varsToKeys):
    """
    Evals each value and returns a dict with the given keys.
    """
    import vim

    result = {}
    for keyVal, varName in varsToKeys.items():
        try:
            result[keyVal] = vim.eval(varName)
        except vim.error as err:
            __log__.exception("Issue with eval'ing key. Message: {}".format(err.message))

    return result

if __name__ == '__main__':
    main(sys.argv)

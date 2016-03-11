#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

import logging
from libs import authutils
import vim

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"
__log__ = logging.getLogger(__name__)


###
# UTILS FOR VIM PLUGIN
###
def build_config_with_client(*sources):
    """
    Builds the config dict using `build_config`, and then creates the auth client.
    """
    config = build_config(*sources)
    client, config = authutils.build_client(config)

    return config


def build_config(*sources):
    """
    XXX This should only be used with VIM (as a plugin)

    Builds the config object using VIM variables. The `sources` are
    merged in with the created config object.
    """
    # Build the config object
    config = eval_var_keys(VIM_VARS_TO_KEYS)

    # Now merge in any additional `sources` to `config`
    for source in sources:
        if isinstance(source, dict):
            config.update(source)
        else:
            __log__.error("Source is not a dict! Type: {} Value: {}".format(type(source), source))

    return config


def eval_var_keys(varsToKeys):
    """
    Evals each value and returns a dict with the given keys.
    """
    result = {}
    for keyVal, varVal in varsToKeys.items():
        try:
            varValToUse = eval_or_convert(varVal)

        except vim.error as err:
            # Could not eval value. So just use it in its raw form
            varValToUse = varVal
            __log__.debug(
                "Issue with eval'ing key. Key: {}, Val: {} Message: {}".format(
                    keyVal,
                    varVal,
                    err.message
                )
            )

        # Now set value onto the dict
        result[keyVal] = varValToUse

    return result


def eval_or_convert(varVal):
    """
    Use VIM's eval on `varVal` to get value. If it can be
    converted (value is in `convertMap`), then use that. Otherwise return
    the eval'd value.
    """
    if isinstance(varVal, int) or varVal is None:
        val = varVal
    else:
        # Only eval if safe
        val = vim.eval(varVal)

    return TYPE_CONVERT_MAP.get(val, val)


def scratch_buffer():
    """
    Create a scratch buffer (in a new tab)
    """
    vim.command("tabe | setlocal buftype=nofile bufhidden=hide noswapfile")
    scratchBuffer = vim.current.buffer
    return scratchBuffer


def put_to_scratch_buffer(output):
    """
    Create a new scratch buffer and output the `output` string to it.
    """
    scratch = scratch_buffer()

    for line in output.split("\n"):
        scratch.append(line)

    return scratch


TYPE_CONVERT_MAP = {
    None: False,
    "0": False,
    "1": True,
}

VIM_VARS_TO_KEYS = {
    "app_code": "g:dbdiff_config_auth_app_code",
    "app_key": "g:dbdiff_config_auth_app_key",
    "app_secret": "g:dbdiff_config_auth_app_secret",
    "auth_token": "g:dbdiff_config_auth_auth_token",
    "debug": "g:dbdiff_config_system_debug",
    "input_disabled": "g:dbdiff_config_system_input_disabled",
    "quit": "g:dbdiff_config_system_quit",
    "verbose": "g:dbdiff_config_system_verbose",
}

if __name__ == '__main__':
    pass

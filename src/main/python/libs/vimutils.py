#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

from datetime import datetime
from libs import authutils
import logging
from pydash import py_ as _

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"
__log__ = logging.getLogger(__name__)

try:
    import vim
except ImportError as err:
    __log__.debug("Failed to import vim module, skipping")


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


def put_to_scratch_buffer(output, buffer_type):
    """
    Create a new scratch buffer and output the `output` string to it.
    """
    scratch = scratch_buffer(buffer_type)

    for line in output.split("\n"):
        scratch.append(line)

    return scratch


def scratch_buffer(buffer_type):
    """
    Create a scratch buffer in either a horizontal split ("split"), a vertical split ("vsplit"), or
    a new tab ("tab").
    """
    buffer_type_cmd = BUFFER_TYPE_MAP.get(buffer_type)
    if buffer_type_cmd is None:
        __log__.debug("Buffer type cmd not defined!, buffer type: {}", buffer_type)

    vim.command("{} | setlocal buftype=nofile bufhidden=hide noswapfile".format(buffer_type_cmd))
    scratchBuffer = vim.current.buffer
    return scratchBuffer


def build_rev_menu(rev_list):
    """
    Create the VIM menu from the list of revisions. The result will be an
    array of strings, with each element representing each row in the menu.
    """
    def menu_mapper(revVal, revKey):
        index = len(rev_list) - revKey
        modifiedTime = datetime.strptime(
            revVal.get("modified").replace(" +0000", ""),
            "%a, %d %b %Y %H:%M:%S"
        ).strftime("%b %d, %H:%M:%S")
        return "{} - {} ({})".format(index, modifiedTime, revVal.get("rev"))

    return "{}\n{}\n".format(
        REV_MENU_HEADER,
        _(rev_list).map(menu_mapper).join("\n").value()
    )


##
# Properties
##
BUFFER_TYPE_MAP = {
    "split": "new",
    "tab": "tabe",
    "vsplit": "topleft vnew",
}

# TODO Use a string formatter to add name of file
REV_MENU_HEADER = """
" DBDiff for VIM
" j/k  - Move through the list of revisions
" <CR> - Open diff for the given revision
"""

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
    "buffer_type": "g:dbdiff_config_system_buffer_type",
    "debug": "g:dbdiff_config_system_debug",
    "input_disabled": "g:dbdiff_config_system_input_disabled",
    "quit": "g:dbdiff_config_system_quit",
    "verbose": "g:dbdiff_config_system_verbose",
}

if __name__ == '__main__':
    pass

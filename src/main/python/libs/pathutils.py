#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

import logging
import json
import os

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"
__log__ = logging.getLogger(__name__)


def find_remote_db_path(filepath, db_basepath = None):
    if not db_basepath:
        db_basepath = get_db_basepath()

    # Return the remote half of the path
    path = abspath(filepath)
    return path.split(db_basepath)[1]


def is_local_db_path(filepath, db_basepath = None):
    if not db_basepath:
        db_basepath = get_db_basepath()

    return db_basepath in normpath(filepath)


def normpath(filepath):
    """
    Normalize `filepath`. It will call os.path.norm path,
    and expand user/vars
    """
    return os.path.normpath(
        os.path.expandvars(
            os.path.expanduser(filepath)
        )
    )


def abspath(filepath):
    """ Get the normalized path of `filepath`"""
    return normpath(os.path.abspath(filepath))


def get_db_basepath():
    """
    Tries to read from the info.json file for the base path.
    """
    default_path = os.path.expanduser("~/Dropbox")
    info_path = os.path.expanduser("~/.dropbox/info.json")

    if not os.path.exists(info_path):
        __log__.warn("Info.json file does not exist at {}".format(info_path))
        return default_path

    try:
        with open(info_path) as info_fp:
            info_data = json.load(info_fp)

    except ValueError as err:
        __log__.warn("ValueError: Invalid json at {}. Message: {}".format(info_path, err.message))
        return default_path

    except OSError as err:
        __log__.warn("OSError at path {}. Message: {}".format(info_path, err.message))
        return default_path

    # Now have a valid JSON object, lets get the path
    try:
        path = info_data["personal"]["path"]

    except KeyError as err:
        __log__.warn("Path key not in info data! Message: {}".format(err.message))
        return default_path

    if os.path.exists(path):
        # Everything looks good! Finished!
        __log__.debug("Got path {}".format(path))
        return path

    else:
        __log__.warn("Path in info.json, but it does not exist! {}".format(path))
        return default_path


if __name__ == '__main__':
    pass

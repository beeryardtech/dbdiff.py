#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

from dropbox import rest as dbrest
from functools import partial
import logging
import os
from os.path import dirname, realpath # for library path manipulation
import sys
import tempfile


sys.path.insert(0, '{}/libs'.format(dirname(realpath(__file__))))
from libs import auth

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

__log__  = logging.getLogger(__name__)


def add_args(parser):
    """Add my arguments to the given argparse parser."""
    pass


def run(config):
    """
    Verifies dropbox is properly configured.

    Attempts to:
        - Test authentication by creating a connection.
        - List the root dir
        - Puts a tmp file on dropbox
        - Gets that tmp file from dropbox
        - Checks that there is revisions available
        - Deletes that file
    """
    client, config = auth.build_client(config)

    __log__.info("START checking connection!")

    # Create file properties
    db_filepath = "/test.txt"
    tmpfile = __build_tmp_file()

    # Build each check func as partials
    partial_funcs = [
        partial(check_root, client, config),
        partial(check_put, client, config, db_filepath, tmpfile),
        partial(check_get, client, config, db_filepath),
        partial(check_rev, client, config, db_filepath),
        partial(check_delete, client, config, db_filepath),
    ]

    # Execute the partials and collect their results
    check_results = True
    for func in partial_funcs:
        name = func.func.__name__
        result = func()
        if result:
            __log__.info("Result: {}: SUCCESS".format(name))
        else:
            __log__.warn("Result: {}: FAILED".format(name))
            check_results = False

    # Don't forget to close the tmpfile and delete it from disk!
    tmpfile.close()
    os.remove(tmpfile.name)

    __log__.info("END checking connection! Result {}".format(check_results))
    return check_results


def check_root(client, config):
    """
    Checks if client can access the root directory and that it is non-empty
    """
    result = True

    try:
        root_meta = client.metadata('/')
        result = root_meta["contents"] and len(root_meta["contents"])

    except dbrest.ErrorResponse as err:
        result = False

    return result


def check_put(client, config, db_filepath, tmpfile):
    """
    Checks if client can put `tmpfile` onto dropbox dir at `db_filepath`
    """
    result = True

    put_response = None
    try:
        put_response = client.put_file(db_filepath, tmpfile, overwrite = True)
        result = put_response.get("bytes") > 0

    except dbrest.ErrorResponse as err:
        result = False

    return result


def check_get(client, config, db_filepath):
    """
    Checks if client can get the file at `db_filepath` and
    that file is not empty.
    """
    result = True

    try:
        with client.get_file(db_filepath) as get_file:
            if not get_file.read():
                result = False

    except dbrest.ErrorResponse as err:
        result = False

    return result


def check_rev(client, config, db_filepath):
    """
    Checks that the file at `db_filepath` has at least one "revision".
    """
    result = True
    try:
        revs = client.revisions(db_filepath)
        result = len(revs) > 0

    except dbrest.ErrorResponse as err:
        result = False

    return result


def check_delete(client, config, db_filepath):
    """
    Checks that the file at `db_filepath` is deleted. That is the metadata says
    it has a size of 0 and has the `is_deleted` flag set.
    """
    result = True

    try:
        del_response = client.file_delete(db_filepath)
        result = del_response.get("bytes") == 0 and del_response.get("is_deleted")

    except dbrest.ErrorResponse as err:
        result = False

    return result

def __build_tmp_file():
    """
    Creates the tmp file used for checking put and get operations
    """
    tmpfile = open(__random_filename(), "w+")
    tmpfile.write("Temp data: {}".format(tmpfile.name))
    tmpfile.flush()
    tmpfile.seek(0, 0)

    return tmpfile

def __random_filename():
    """ Generate randome file name"""
    import random
    import string

    chars = string.ascii_uppercase + string.digits
    return "/tmp/{}".format("".join(
        random.choice(chars) for index in range(6)
    ))


if __name__ == '__main__':
    run(sys.argv)

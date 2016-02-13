#!/usr/bin/python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

import logging

# import the subcommands
from . import check

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

__log__ = logging.getLogger(__name__)

# Exposed to Parser. List of subcommands
subcommands = {
    "check": check,
    # "diff": diff,
    # "get": get,
    # "revs": revs,
    # "update": update,
}

if __name__ == '__main__':
    pass

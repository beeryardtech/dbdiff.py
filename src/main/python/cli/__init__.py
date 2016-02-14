#!/usr/bin/python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

# import the subcommands
from . import check
from . import revs

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

# Exposed to Parser. List of subcommands
subcommands = {
    "check": check,
    "revs": revs,
    # "diff": diff,
    # "get": get,
    # "update": update,
}

if __name__ == '__main__':
    pass

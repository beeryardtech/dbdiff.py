#!/usr/bin/python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

# import the subcommands
from . import check
from . import get
from . import put
from . import revs

__author__ = "Travis Goldie and Janie Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

# Exposed to Parser. List of subcommands
subcommands = {
    "check": check,
    "get": get,
    "put": put,
    "revs": revs,
    # "diff": diff,
    # "update": update,
}

if __name__ == '__main__':
    pass

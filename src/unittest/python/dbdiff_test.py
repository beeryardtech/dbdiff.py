#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

from os.path import dirname, realpath
import sys

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

current_dir = dirname(realpath(__file__))
sys.path.insert(0, '{}/cli'.format(current_dir))
sys.path.insert(0, '{}/libs'.format(current_dir))

if __name__ == '__main__':
    pass

#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

import logging
# from mockito import mock
from os.path import dirname, realpath
import sys
import unittest

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"
__log__ = logging.getLogger(__name__)

# current_dir = dirname(realpath(__file__))
current_dir = dirname(realpath("../../../main/python"))
sys.path.insert(0, '{}/cli'.format(current_dir))
sys.path.insert(0, '{}/libs'.format(current_dir))

from libs import pathutils


class pathutils_test(unittest.TestCase):
    def test_normpath(self):
        path = "~/tmp"
        normedPath = "/home/tgoldie/tmp"

        self.assertEqual(pathutils.normpath(path), normedPath)


if __name__ == '__main__':
    unittest.main()

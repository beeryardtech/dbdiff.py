#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

import gettext
import logging
from mockito import mock, verify
import os
from os.path import dirname, realpath # for library path manipulation
import sys
import unittest

# For translations
i18n = gettext.translation('', '{}/../i18n'.format(dirname(realpath(__file__))), fallback = True)
_ = i18n.lgettext

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

__log__  = logging.getLogger(__name__)

from libs import pathutils

class PathutilsTest(unittest.TestCase):
    def test_normpath(self):
        out = mock()


if __name__ == '__main__':
    pass

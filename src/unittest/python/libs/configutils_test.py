#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

import ConfigParser
import gettext
import logging
from os.path import dirname, realpath  # for library path manipulation
import unittest

# For translations
i18n = gettext.translation('', '{}/../i18n'.format(dirname(realpath(__file__))), fallback = True)
_ = i18n.lgettext

__author__ = "Travis Goldie"
__email__ = "tgoldie@gmail.com"
__copyright__ = "(c) Beeryard Tech 2016"

__log__ = logging.getLogger(__name__)


class TestStringMethods(unittest.TestCase):
    def test_merge_configs(self):
        pass

    def test_load_config(self):
        self.assertIsInstance(ConfigParser.ConfigParser())


if __name__ == '__main__':
    unittest.main()

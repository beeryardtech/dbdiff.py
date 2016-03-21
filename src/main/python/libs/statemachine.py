#!/usr/bin/env python
# vim: tabstop=4:shiftwidth=4:expandtab:
from __future__ import with_statement

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


class StateMachine:
    """
    Holds statefulness of the revision menu. Each time the line changes, update
    the properties of this class.
    """
    def __init__(self):
        __log__.error("here!!")
        self.current_line = 0
        self.current_rev = ""

        # Consts
        self.HEADER_OFFSET = 3 + 2
        return

    def setup(self, rev_list, output):
        """
        Setup the internal state of a given instance.
        """
        self.output = output
        self.rev_list = rev_list
        self.line_map = self.__build_line_map(self.rev_list)
        return

    def move(self, line_num = None):
        if not line_num:
            line_num = vim.eval("getline('.')")

        self.current_rev = (
            _(self.line_map)
            .get(str(line_num), {})
            .get("rev", "")
            .value()
        )
        self.current_line = line_num
        return self.current_rev

    def __build_line_map(self, rev_list):
        """
        """
        def line_mapper(mapVal, mapKey):
            return [
                str(mapKey + self.HEADER_OFFSET),
                _.pick(mapVal, "rev", "modified")
            ]

        return (
            _(rev_list)
            .map(line_mapper)
            .zip_object()
            .value()
        )


if __name__ == '__main__':
    pass

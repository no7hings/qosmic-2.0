# coding=utf-8
import sys
# qt
from ...core.wrap import *


class QtNodeActionCommand(QtWidgets.QUndoCommand):
    def __init__(self, data):
        super(QtNodeActionCommand, self).__init__()
        self._data = data

    def undo(self):
        for i, i_coord, i_last_coord, i_size, i_last_size in self._data:
            i._pull_basic_coord_(*i_last_coord)
            # i._pull_basic_size_(*i_last_size)
            sys.stdout.write(
                'node move: name="{}", coord=({}, {})\n'.format(i._get_name_text_(), *i_last_coord)
            )

    def redo(self):
        for i, i_coord, i_last_coord, i_size, i_last_size in self._data:
            i._pull_basic_coord_(*i_coord)
            # i._pull_basic_size_(*i_size)
            sys.stdout.write(
                'node move: name="{}", coord=({}, {})\n'.format(i._get_name_text_(), *i_coord)
            )

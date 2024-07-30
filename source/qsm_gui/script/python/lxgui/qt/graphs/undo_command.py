# coding=utf-8
# qt
import sys

from ..core.wrap import *


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


class QtTimetrackActionCommand(QtWidgets.QUndoCommand):
    def __init__(self, data):
        super(QtTimetrackActionCommand, self).__init__()
        self._data = data
        self._graph = None

    def undo(self):
        for i, i_model, i_last_model in self._data:
            i._pull_track_model_(i_last_model)
            sys.stdout.write(
                'timetrack change: name="{}", model={}\n'.format(i._get_name_text_(), i_last_model)
            )
            self._graph._update_stage_()

    def redo(self):
        for i, i_model, i_last_model in self._data:
            i._pull_track_model_(i_model)
            sys.stdout.write(
                'timetrack change: name="{}", model={}\n'.format(i._get_name_text_(), i_model)
            )

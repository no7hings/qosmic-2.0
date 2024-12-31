# coding=utf-8
import sys
# qt
from ...core.wrap import *


class QtTimetrackActionCommand(QtWidgets.QUndoCommand):
    def __init__(self, data):
        super(QtTimetrackActionCommand, self).__init__()
        self._data = data
        self._graph = None

    def undo(self):
        for i_node, i_model, i_last_model, i_flag in self._data:
            if i_flag == 'transformation':
                i_node._pull_track_geometry_(i_last_model)
                sys.stdout.write(
                    'timetrack change: name="{}", model={}\n'.format(i_model.key, i_last_model)
                )
            self._graph._update_stage_()

    def redo(self):
        for i_node, i_model, i_last_model, i_flag in self._data:
            if i_flag == 'transformation':
                i_node._pull_track_geometry_(i_model)
                sys.stdout.write(
                    'timetrack change: name="{}", model={}\n'.format(i_model.key, i_model)
                )
            self._graph._update_stage_()

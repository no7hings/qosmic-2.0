# coding=utf-8
import sys
# qt
from ...core.wrap import *


class QtTrackActionCommand(QtWidgets.QUndoCommand):
    def __init__(self, data):
        super(QtTrackActionCommand, self).__init__()
        self._data = data
        self._graph = None

    def undo(self):
        for i_node, i_flag, i_data in self._data:
            if i_flag in {'move', 'trim', 'scale', 'layout'}:
                i_model, i_last_model = i_data
                self._graph._graph_node_update_transformation_fnc_(i_last_model)
                sys.stdout.write(
                    'track {}: name="{}", model={}\n'.format(i_flag, i_model.key, i_last_model)
                )
            elif i_flag == 'bypass':
                i_model, i_bypass_flag = i_data
                self._graph._graph_bypass_node_fnc_(i_model, not i_bypass_flag)
            elif i_flag == 'trash':
                i_model, i_trash_flag = i_data
                self._graph._graph_node_trash_fnc_(i_model, not i_trash_flag)

            self._graph._update_stage_()

    def redo(self):
        for i_node, i_flag, i_data in self._data:
            if i_flag in {'move', 'trim', 'scale', 'layout'}:
                i_model, i_last_model = i_data
                self._graph._graph_node_update_transformation_fnc_(i_model)
                sys.stdout.write(
                    'track {}: name="{}", model={}\n'.format(i_flag, i_model.key, i_model)
                )
            elif i_flag == 'bypass':
                # is a tuple, (i_model, )
                i_model, i_bypass_flag = i_data
                self._graph._graph_bypass_node_fnc_(i_model, i_bypass_flag)
            elif i_flag == 'trash':
                # is a tuple, (i_model, )
                i_model, i_trash_flag = i_data
                self._graph._graph_node_trash_fnc_(i_model, i_trash_flag)

            self._graph._update_stage_()

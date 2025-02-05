# coding=utf-8
# qt
from ...core.wrap import *


class QtTrackActionCommand(QtWidgets.QUndoCommand):
    def __init__(self, data):
        super(QtTrackActionCommand, self).__init__()
        self._data = data
        self._graph = None

    def undo(self):
        for i_flag, i_data in self._data:
            if i_flag in {'move', 'trim', 'scale', 'layout'}:
                i_track_model, i_last_track_model = i_data
                self._graph._graph_node_update_track_model_fnc_(i_last_track_model)
            elif i_flag == 'bypass':
                i_track_model, i_flag = i_data
                self._graph._graph_node_bypass_fnc_(i_track_model, not i_flag)
            elif i_flag == 'trash':
                i_track_model, i_flag = i_data
                self._graph._graph_node_trash_fnc_(i_track_model, not i_flag)
            elif i_flag == 'paste_copy':
                i_track_model, i_flag = i_data
                self._graph._graph_node_paste_copy_fnc_(i_track_model, not i_flag)
            elif i_flag == 'paste_cut':
                i_track_model, i_last_track_model = i_data
                self._graph._graph_node_paste_cut_fnc_(i_last_track_model)
            elif i_flag == 'blend':
                i_track_model, i_last_track_model = i_data
                self._graph._graph_node_update_blend_fnc_(i_last_track_model)

        self._graph._update_stage_()

    def redo(self):
        for i_flag, i_data in self._data:
            if i_flag in {'move', 'trim', 'scale', 'layout'}:
                i_track_model, i_last_track_model = i_data
                self._graph._graph_node_update_track_model_fnc_(i_track_model)
            elif i_flag == 'bypass':
                i_track_model, i_flag = i_data
                self._graph._graph_node_bypass_fnc_(i_track_model, i_flag)
            elif i_flag == 'trash':
                i_track_model, i_flag = i_data
                self._graph._graph_node_trash_fnc_(i_track_model, i_flag)
            elif i_flag == 'paste_copy':
                i_track_model, i_flag = i_data
                self._graph._graph_node_paste_copy_fnc_(i_track_model, i_flag)
            elif i_flag == 'paste_cut':
                i_track_model, i_last_track_model = i_data
                self._graph._graph_node_paste_cut_fnc_(i_track_model)
            elif i_flag == 'blend':
                i_track_model, i_last_track_model = i_data
                self._graph._graph_node_update_blend_fnc_(i_track_model)

        self._graph._update_stage_()

# coding=utf-8
import sys
# qt
from ...core.wrap import *


class QtNodeGeneralActionCommand(QtWidgets.QUndoCommand):
    def __init__(self, data):
        super(QtNodeGeneralActionCommand, self).__init__()
        self._data = data
        self._graph = None

    def undo(self):
        for i_flag, i_data in self._data:
            if i_flag == 'selection':
                i_node_widget, i_boolean = i_data

                i_node_widget._set_selected_(not i_boolean)
                if i_boolean is True:
                    self._graph._graph_selection_nodes.remove(i_node_widget)
                else:
                    self._graph._graph_selection_nodes.append(i_node_widget)
            elif i_flag in {'move', 'layout'}:
                i_node_widget, i_basic_coord, i_basic_last_coord = i_data
                i_node_widget._pull_basic_coord_(*i_basic_last_coord)

    def redo(self):
        for i_flag, i_data in self._data:
            if i_flag == 'selection':
                i_node_widget, i_boolean = i_data

                i_node_widget._set_selected_(i_boolean)
                if i_boolean is False:
                    self._graph._graph_selection_nodes.remove(i_node_widget)
                else:
                    self._graph._graph_selection_nodes.append(i_node_widget)
            elif i_flag in {'move', 'layout'}:
                i_node_widget, i_basic_coord, i_basic_last_coord = i_data
                i_node_widget._pull_basic_coord_(*i_basic_coord)

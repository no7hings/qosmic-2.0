# coding:utf-8
import lxbasic.core as bsc_core

from lxgui.qt.core.wrap import *


class _SbjGuiBase:
    ENTITY_TYPE = None

    MODEL_CLS = None


class _QtColors:
    NodeBorder = QtGui.QColor(103, 103, 103, 255)
    NodeBackground = QtGui.QColor(95, 95, 95, 255)
    NodeBackgroundBypass = QtGui.QColor(71, 71, 71, 255)

    NodeImagingBorder = QtGui.QColor(71, 71, 71, 255)
    NodeImagingBackground = QtGui.QColor(63, 63, 63, 255)

    BackdropBorder = QtGui.QColor(95, 95, 95, 255)
    BackdropBackground = QtGui.QColor(63, 63, 127, 31)
    BackdropName = QtGui.QColor(95, 95, 95, 255)

    Port = QtGui.QColor(71, 71, 71, 255)
    AddInput = QtGui.QColor(111, 111, 111, 255)

    Connection = QtGui.QColor(95, 95, 95, 255)
    ConnectionNew = QtGui.QColor(255, 255, 0, 255)

    TypeText = QtGui.QColor(191, 191, 191, 255)
    Text = QtGui.QColor(223, 223, 223)
    TextHover = QtGui.QColor(255, 255, 255)

    Transparent = QtGui.QColor(0, 0, 0, 0)


class _NodeGroup(object):
    def __init__(self, root_model, data):
        self._root_model = root_model
        self._data = data

    def generate_create_data(self):
        node_args = []
        connection_args = []

        if self._data:
            xs = []
            ys = []
            for i in self._data:
                xs.append(i['options']['position']['x'])
                ys.append(i['options']['position']['y'])

            x_min = min(xs)
            y_min = min(ys)

            point = QtGui.QCursor().pos()
            p = self._root_model._gui._map_from_global(point)
            p_x, p_y = p.x(), p.y()

            path_set = self._root_model.get_node_path_set()
            for i in self._data:
                i_x = i['options']['position']['x']
                i_y = i['options']['position']['y']
                i['options']['position']['x'] = p_x+(i_x-x_min)
                i['options']['position']['y'] = p_y+(i_y-y_min)

                i_name = i['name']
                i_new_path = self._root_model._find_next_node_path(
                    path_set, i_name
                )
                path_set.add(i_new_path)
                i_new_name = bsc_core.BscNodePath.to_dag_name(i_new_path)
                i['path'] = i_new_path
                i['name'] = i_new_name
                node_args.append(i)

        return node_args, connection_args

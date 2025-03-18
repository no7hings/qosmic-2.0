# coding:utf-8
import os

import pkgutil

import importlib
# gui
import lxgui.core as gui_core

from lxgui.qt.core.wrap import *

import lxgui.qt.core as gui_qt_core

from .core import base as _base

from .core import gui as _gui

from . import node_type as _node_type


def register_node_types_from(module):
    dir_path = os.path.dirname(module.__file__)

    all_names = os.listdir(dir_path)

    for i in all_names:
        if i.startswith('__init__'):
            continue
        if i.endswith('.pyc'):
            continue

        i_module_name = '{}.{}'.format(module.__name__, os.path.splitext(i)[0])
        if pkgutil.find_loader(i_module_name):
            i_module = importlib.import_module(i_module_name)
            if 'register' in i_module.__dict__:
                i_module.__dict__['register']()


class QtNodeGraphWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtNodeGraphWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setPalette(gui_qt_core.GuiQtDcc.generate_qt_palette())

        self._mrg = 4

        self._grid_lot = QtWidgets.QGridLayout(self)
        self._grid_lot.setContentsMargins(*[self._mrg]*4)
        self._grid_lot.setSpacing(2)

        self._root_node_gui = _gui.QtRootNode()
        self._grid_lot.addWidget(self._root_node_gui, 0, 0, 1, 1)
        self._root_node_gui.setFocusProxy(self)
        self._model = self._root_node_gui._model

        self._scene = _gui.QtScene()
        self._root_node_gui.setScene(self._scene)
        self._scene._set_model(self._model)
        self._scene.setSceneRect(-5000, -5000, 10000, 10000)

        register_node_types_from(_node_type)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        mrg = self._mrg
        x, y, w, h = 0, 0, self.width(), self.height()

        f_x, f_y, f_w, f_h = x+1, y+1, w-2, h-2
        is_focus = self.hasFocus()

        pen = QtGui.QPen(QtGui.QColor(*[(71, 71, 71, 255), (95, 95, 95, 255)][is_focus]))
        pen_width = [1, 2][is_focus]

        pen.setWidth(pen_width)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(*gui_core.GuiRgba.Dim))
        painter.drawRect(f_x, f_y, f_w, f_h)


class QtParametersWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtParametersWidget, self).__init__(*args, **kwargs)

        self._mrg = 4

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self._layout.setContentsMargins(*[self._mrg]*4)
        self._layout.setSpacing(2)

        self._param_root_gui_stack = _gui.ParamRootStackGui()
        self._layout.addWidget(self._param_root_gui_stack)

        self._root_node_gui = None
        self._model = None

    def _set_root_node_gui(self, root_node):
        self._root_node_gui = root_node
        self._model = self._root_node_gui._model
        self._root_node_gui.node_edited_changed.connect(self._load_node_path)
        self._root_node_gui.event_sent.connect(self._event_filter)

    def _load_node_path(self, path):
        self._load_node(self._model.get_node(path))

    def _event_filter(self, data):
        event_type = data['event_type']
        if event_type == _base.EventTypes.ParamSetValue:
            node_path = data['node']
            param_root_gui = self._param_root_gui_stack._get_one(node_path)
            if param_root_gui:
                param_path = data['param']
                param_root_gui._get_parameter(param_path)._refresh()

    def _load_node(self, node):
        self._param_root_gui_stack._load_node(node)

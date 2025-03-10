# coding:utf-8
import os

import pkgutil

import importlib
# gui
import lxgui.core as gui_core

from lxgui.qt.core.wrap import *

import lxgui.qt.core as gui_qt_core

from .core import gui as _gui

from . import nodes as _nodes


def register_nodes_from(module):
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


class QtSceneGraphWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtSceneGraphWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setPalette(gui_qt_core.GuiQtDcc.generate_qt_palette())

        self._mrg = 4

        self._grid_lot = QtWidgets.QGridLayout(self)
        self._grid_lot.setContentsMargins(*[self._mrg]*4)
        self._grid_lot.setSpacing(2)

        self._root = _gui._QtRootNode()
        self._grid_lot.addWidget(self._root, 0, 0, 1, 1)
        self._root.setFocusProxy(self)
        self._model = self._root._model

        self._scene = _gui._QtScene()
        self._root.setScene(self._scene)
        self._scene._set_model(self._model)
        self._scene.setSceneRect(-5000, -5000, 10000, 10000)

        register_nodes_from(_nodes)

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

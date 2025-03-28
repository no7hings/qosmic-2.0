# coding=utf-8
import copy

import lxbasic.web as bsc_web

from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts


class QtDockerWidget(QtWidgets.QDockWidget):
    def __init__(self, *args, **kwargs):
        super(QtDockerWidget, self).__init__(*args)


class QtDockerWindow(
    QtWidgets.QMainWindow,
    _qt_abstracts.AbsQtMainWindowDef,
):
    def __init__(self, *args, **kwargs):
        super(QtDockerWindow, self).__init__(*args, **kwargs)

        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # todo: do not use WA_TranslucentBackground mode, GL bug
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setPalette(_qt_core.GuiQtDcc.generate_qt_palette())
        self.setAutoFillBackground(True)
        self.setStyleSheet(
            _qt_core.QtStyle.get('QDockerWindow')
        )

        self.setFont(_qt_core.QtFonts.NameNormal)

        _qt_core.QtUtil.assign_qt_shadow(self, radius=2)

        self._init_window_base_def_(self)

    def _create_center_widget(self, widget):
        # dock = QtDockerWidget(name, self)
        # dock.setWidget(widget)
        # dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        # self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock)
        self.setCentralWidget(widget)

    def _create_left_docker(self, name, widget):
        dock = QtDockerWidget(name, self)
        dock.setWidget(widget)
        dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        return dock

    def _create_right_docker(self, name, widget):
        dock = QtDockerWidget(name, self)
        dock.setWidget(widget)
        dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        return dock

    def _accept_corner(self):
        self.setCorner(QtCore.Qt.TopLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.TopRightCorner, QtCore.Qt.RightDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomRightCorner, QtCore.Qt.RightDockWidgetArea)

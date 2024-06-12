# coding=utf-8
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts
# qt widgets
from . import base as gui_qt_wgt_base

from . import utility as gui_qt_wgt_utility

from . import item as gui_qt_wgt_item

from . import view as gui_qt_wgt_view


class _QtWindow(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtFrameBaseDef,
):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFont(gui_qt_core.QtFont.generate())
        #
        self._qt_main_layout = gui_qt_wgt_base.QtVBoxLayout(self)
        self._qt_main_layout.setContentsMargins(0, 0, 0, 0)
        self._qt_main_layout.setSpacing(0)
        #
        self._init_frame_base_def_(self)
        #
        self._frame_background_color = 63, 63, 63, 255
        self._hovered_frame_background_color = 63, 63, 63, 255
        #
        self._menu_bar = gui_qt_wgt_view._QtMenuBar()
        self._qt_main_layout.addWidget(self._menu_bar)

    def _set_widget_geometries_update_(self):
        pos_x, pos_y = 0, 0
        width, height = self.width(), self.height()
        self._set_frame_draw_rect_(
            pos_x, pos_y, width, height
        )

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        #
        self._set_widget_geometries_update_()
        #
        painter._draw_frame_by_rect_(
            self._rect_frame_draw,
            background_color=self._frame_background_color,
            border_color=self._frame_border_color
        )

    # def closeEvent(self, event):
    #     d = QtWidgets.QDialog(self)
    #     print 'AAAA'
    #     super(_QtWindow, self).closeEvent(event)


class _QtFramelessWindow(
    QtWidgets.QWidget
):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(_QtFramelessWindow, self).__init__(*args, **kwargs)
        #
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        #
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        self._qt_main_layout = gui_qt_wgt_base.QtVBoxLayout(self)
        self._qt_main_layout.setContentsMargins(0, 0, 0, 0)
        self._qt_main_layout.setSpacing(0)
        self._header = gui_qt_wgt_item._QtWindowHead()
        self._qt_main_layout.addWidget(self._header)
        #
        self._qt_main_widget = gui_qt_wgt_utility.QtWidget()
        self._qt_main_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        self._qt_main_layout.addWidget(self._qt_main_widget)

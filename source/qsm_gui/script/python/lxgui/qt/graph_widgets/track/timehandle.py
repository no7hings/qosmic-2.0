# coding=utf-8
# gui
from .... import core as _gui_core
# qt
from ...core.wrap import *

from ... import core as _qt_core


class QtTimeHandle(
    QtWidgets.QWidget
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y, w, h = 0, 0, self.width(), self.height()
        self._rect.setRect(
            x+int(w/2)-1, y, 1, h
        )

    def _update_from_graph_(self):

        self._refresh_widget_all_()

    def __init__(self, *args, **kwargs):
        super(QtTimeHandle, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self._rect = QtCore.QRect()

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            event.ignore()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)
        painter._set_antialiasing_(False)

        painter._set_border_color_(_gui_core.GuiRgba.LightAzureBlue)
        painter._set_background_color_(_gui_core.GuiRgba.LightAzureBlue)
        painter.drawRect(self._rect)


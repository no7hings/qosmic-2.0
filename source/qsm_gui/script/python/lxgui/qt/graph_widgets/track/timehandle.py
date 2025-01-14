# coding=utf-8
# gui
from .... import core as _gui_core
# qt
from ...core.wrap import *

from ... import core as _qt_core

from ... import abstracts as _qt_abstracts


class QtTimeHandle(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtActionBaseDef,
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

    def _do_press_move_(self, event):
        p = event.pos()

        p_0 = self.mapToParent(p)
        x = p_0.x()

        frame = self._graph._track_model_stage._time_coord_model.compute_unit_index_loc(x)
        self._graph._track_timeline._set_current_timeframe_(frame)

    def __init__(self, *args, **kwargs):
        super(QtTimeHandle, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self._init_action_base_def_(self)

        self._rect = QtCore.QRect()

        self._graph = None

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Enter:
                self._set_action_flag_(self.ActionFlag.TimeMove)
            elif event.type() == QtCore.QEvent.Leave:
                self._clear_all_action_flags_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.PressClick)
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.NoButton:
                    pass
                elif event.buttons() == QtCore.Qt.LeftButton:
                    self._do_press_move_(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._clear_all_action_flags_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)
        painter._set_antialiasing_(False)

        painter.setPen(_qt_core.QtRgba.LightPurple)
        painter.setBrush(_qt_core.QtRgba.LightPurple)
        painter.drawRect(self._rect)

    def _set_graph_(self, widget):
        self._graph = widget


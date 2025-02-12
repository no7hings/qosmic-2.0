# coding=utf-8
import lxbasic.model as bsc_model
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from .. import abstracts as _qt_abstracts

from .. import graph_models as _graph_models


class QtChartAsTimeWrap(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtActionBaseDef,
):
    HEIGHT = 48

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y, w, h = 0, 0, self.width(), self.height()

        tml_frm_h = self.HEIGHT
        self._timeline_frame_rect.setRect(x, y+h-tml_frm_h, w, tml_frm_h)

        self._coord_model.update(
            self._graph_model.tx, self._graph_model.sx, w
        )

    def _do_hover_move_(self, event):
        pass

    def _do_press_click_(self, event):
        pass

    def _do_press_move_(self, event):
        pass

    def _do_graph_track_start_(self, event):
        self._graph_model.on_track_start(event.pos())

    def _do_graph_track_move_(self, event):
        self._graph_model.on_track_move(event.pos())

    def _do_graph_track_end_(self, event):
        self._graph_model.on_track_end(event.pos())

    def _do_graph_zoom_(self, event):
        self._graph_model.on_zoom(event.pos(), event.angleDelta().y())

    def __init__(self, *args, **kwargs):
        super(QtChartAsTimeWrap, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self._init_action_base_def_(self)

        self._graph_model = _graph_models.ModelForBaseGraph(self)

        self._translate_x = 0
        self._scale_x = 0.01

        self._start_frame = 1
        self._end_frame = 48

        self._timeline_frame_rect = qt_rect()

        self._coord_model = bsc_model.CoordModel()
        self._coord_model.setup(100)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            # track
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.PressClick)
                    self._do_press_click_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._set_action_flag_(
                        self.ActionFlag.NGGraphTrackClick
                    )
                    self._do_graph_track_start_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.NoButton:
                    self._do_hover_move_(event)
                elif event.buttons() == QtCore.Qt.LeftButton:
                    self._do_press_move_(event)
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    self._set_action_flag_(
                        self.ActionFlag.NGGraphTrackMove
                    )
                    self._do_graph_track_move_(event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    pass
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._do_graph_track_end_(event)
                else:
                    event.ignore()
                self._clear_all_action_flags_()
            # zoom
            elif event.type() == QtCore.QEvent.Wheel:
                self._do_graph_zoom_(event)
        return False
    
    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)
        _qt_core.PainterFnc.draw_timeline(painter, self._coord_model, self._timeline_frame_rect)

    def _draw_timeline_basic_(self, painter):

        painter.fillRect(
            self._timeline_frame_rect, QtGui.QColor(255, 0, 0)
        )



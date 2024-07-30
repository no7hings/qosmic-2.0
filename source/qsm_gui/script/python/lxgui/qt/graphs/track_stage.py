# coding=utf-8
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts

from . import model as _model


class QtTrackStage(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtActionBaseDef,
):
    timehandle_offset_accepted = qt_signal(int)

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y, w, h = 0, 0, self.width(), self.height()

        self._frame_rect.setRect(
            x, y, w, h
        )

        start_x = self._stage_model.compute_start_x()
        track_w = self._stage_model.compute_width()
        txt_w = self._text_w
        txt_h = h/2

        self._track_start_rect.setRect(
            start_x-txt_w, y, txt_w, h
        )

        self._track_end_rect.setRect(
            start_x+track_w, y, txt_w, h
        )
        # trim
        self._left_trim_rect.setRect(
            x, y, max(start_x, 0), h
        )
        self._right_trim_rect.setRect(
            start_x+track_w, y, max(w-start_x+track_w, 0), h
        )

    def _update_stage_(self):
        self._stage_model.update()

        self._refresh_widget_all_()

    def __init__(self, *args, **kwargs):
        super(QtTrackStage, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(48)

        self._init_action_base_def_(self)

        self._frame_rect = QtCore.QRect()

        self._text_w = 48

        self._track_start_rect = QtCore.QRect()
        self._track_end_rect = QtCore.QRect()

        self._left_trim_rect = QtCore.QRect()
        self._right_trim_rect = QtCore.QRect()

        self._graph = None
        
        self._stage_model = _model.TrackStageModel()

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
                    # self._do_press_click_(event)
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._graph.eventFilter(self._graph, event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.NoButton:
                    pass
                    # self._do_hover_move_(event)
                elif event.buttons() == QtCore.Qt.LeftButton:
                    pass
                    # self._do_press_move_(event)
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    self._graph.eventFilter(self._graph, event)
                else:
                    event.ignore()
            # zoom
            elif event.type() == QtCore.QEvent.Wheel:
                self._graph.eventFilter(self._graph, event)
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)
        painter._set_antialiasing_(False)

        bottom_line = QtCore.QLine(self._frame_rect.bottomLeft(), self._frame_rect.bottomRight())

        painter._set_border_color_(_gui_core.GuiRgba.Dark)
        painter._set_background_color_(_gui_core.GuiRgba.Dark)
        painter.drawRect(self._frame_rect)
        # trim
        painter._draw_alternating_colors_by_rect_(
            self._left_trim_rect, [_gui_core.GuiRgba.Dim, _gui_core.GuiRgba.Transparent]
        )
        painter._draw_alternating_colors_by_rect_(
            self._right_trim_rect, [_gui_core.GuiRgba.Dim, _gui_core.GuiRgba.Transparent]
        )
        # line
        painter._set_border_color_(_gui_core.GuiRgba.Gray)
        painter.drawLine(bottom_line)
        left_line = QtCore.QLine(self._track_start_rect.topRight(), self._track_start_rect.bottomRight())
        painter.drawLine(left_line)
        right_line = QtCore.QLine(self._track_end_rect.topLeft(), self._track_end_rect.bottomLeft())
        painter.drawLine(right_line)

        painter._set_border_color_(_gui_core.GuiRgba.LightGray)
        painter._set_font_(_qt_core.QtFont.generate(size=10))

        painter.drawText(
            self._track_start_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            str(self._stage_model.track_start)
        )
        painter.drawText(
            self._track_end_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            str(self._stage_model.track_end)
        )

        self._draw_track_frame_ranges_(painter)

    def _draw_track_frame_ranges_(self, painter):
        h = self.height()
        track_models = self._stage_model.get_all()
        for i_track_model in track_models:
            i_frame_ranges = i_track_model.valid_frame_ranges
            for j in i_track_model.valid_frame_ranges:
                if isinstance(j, tuple):
                    j_start, j_end = j
                elif isinstance(j, int):
                    j_start = j_end = j
                else:
                    raise RuntimeError()

                j_count = j_end-j_start+1
                j_start_x = self._stage_model.compute_start_x_at(j_start)
                j_count_w = self._stage_model.compute_width_for(j_count)
                j_rect = QtCore.QRect(j_start_x, 0, j_count_w, h)
                painter._set_background_color_(i_track_model.rgb)
                painter._set_border_color_(i_track_model.rgb)
                painter.drawRect(j_rect)

    def _set_graph_(self, widget):
        self._graph = widget

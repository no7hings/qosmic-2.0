# coding=utf-8
# gui
import sys

from .... import core as _gui_core
# qt
from ...core.wrap import *

from ... import core as _qt_core

from ... import abstracts as _qt_abstracts


class QtTrackTimeline(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtActionBaseDef,
):
    frame_accepted = qt_signal(int)

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._update_to_timehandle_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        frm_w, frm_h = self.width(), self.height()

        self._unit_current_coord = self._coord_model.compute_offset_at(self._timeframe_current)

        #
        self._timeframe_start, self._timeframe_end = self._coord_model.unit_index_range

        # timehandle
        txt_w = QtGui.QFontMetrics(self._text_font).width(str(self._timeframe_current))+16

        d = self._timeframe_current_handle_w/2
        txt_h = frm_h-d
        self._timehandle_text_rect.setRect(
            self._unit_current_coord-(txt_w/2), y+d, txt_w, txt_h
        )
        self._timehandle_path = _qt_core.QtPainterPath()
        self._timehandle_path._add_points_(
            [
                (self._unit_current_coord-d, y+d),
                (self._unit_current_coord, y),
                (self._unit_current_coord+d, y+d),

                (self._unit_current_coord+d, y+frm_h),
                (self._unit_current_coord-d, y+frm_h),

                (self._unit_current_coord-d, y+d),
            ]
        )

        bub_h = frm_h/2
        bub_gap = (frm_h-bub_h)/2

        self._timeframe_bubble_flag = False

        # left hide
        if self._timeframe_start > self._timeframe_current:
            self._timeframe_bubble_flag = True

            self._timeframe_bubble_rect.setRect(
                x+bub_gap, y+bub_gap, txt_w, bub_h
            )

        # right hide
        elif self._timeframe_end < self._timeframe_current:
            self._timeframe_bubble_flag = True

            self._timeframe_bubble_rect.setRect(
                x+frm_w-txt_w-bub_gap, y+bub_gap, txt_w, bub_h
            )

    def _update_from_graph_(self, rect, translate, scale):
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

        self._coord_model.update(translate, scale, w)

        frm_h = self.height()

        self._timeline_frame_rect.setRect(x, y, w, frm_h)

        self._refresh_widget_all_()

    def _do_hover_move_(self, event):
        p = event.pos()

        if self._timehandle_path.contains(p):
            self._set_action_flag_(
                self.ActionFlag.TimeMove
            )
        else:
            self._clear_all_action_flags_()

    def _do_press_click_(self, event):
        p = event.pos()

        if self._timehandle_path.contains(p):
            return

        x = p.x()
        frame = self._coord_model.compute_unit_index_loc(x)
        if frame != self._timeframe_current:
            self._timeframe_current = int(frame)
            self.frame_accepted.emit(self._timeframe_current)
            self._refresh_widget_all_()

    def _do_press_move_(self, event):
        p = event.pos()

        x = p.x()

        frame = self._coord_model.compute_unit_index_loc(x)
        if frame != self._timeframe_current:
            self._timeframe_current = int(frame)
            self.frame_accepted.emit(self._timeframe_current)
            self._refresh_widget_all_()

    def _update_to_timehandle_(self):
        view = self.parent()
        hdl_w = 7
        self._track_timehandle.setGeometry(
            2+self._unit_current_coord-hdl_w/2, 1,
            hdl_w, view.height()-self.height()
        )
        self._track_timehandle._update_from_graph_()

    def _set_timehandle_(self, widget):
        self._track_timehandle = widget

    def __init__(self, *args, **kwargs):
        super(QtTrackTimeline, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(40)

        self._init_action_base_def_(self)

        self._text_font = _qt_core.QtFont.generate(size=10, weight=75)

        self._time_index_text_w = 64
        self._timeframe_current = 1
        
        self._timeframe_bubble_flag = False

        self._timeframe_start, self._timeframe_end = 1, 48

        self._timeline_frame_rect = QtCore.QRect()

        self._coord_model = None

        self._timeframe_current_handle_w = 20
        self._timeframe_current_handle_rect = QtCore.QRect()
        self._timehandle_path = _qt_core.QtPainterPath()
        self._timehandle_text_rect = QtCore.QRect()
        self._unit_current_coord = 0

        self._timeframe_bubble_rect = QtCore.QRect()

        self._draw_offset = -1

        self._graph = None

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
                    self._graph.eventFilter(self._graph, event)
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
                    self._graph.eventFilter(self._graph, event)
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self._clear_all_action_flags_()
            # zoom
            elif event.type() == QtCore.QEvent.Wheel:
                self._graph.eventFilter(self._graph, event)
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)

        _qt_core.PainterFnc.draw_timeline(painter, self._coord_model, self._timeline_frame_rect)

        self._draw_timehandle_(painter)

    def _get_current_timeframe_(self):
        return self._timeframe_current

    def _set_current_timeframe_(self, frame):
        self._timeframe_current = frame
        self._refresh_widget_all_()
        # sys.stdout.write('frame is change: {}.\n'.format(frame))

    def _set_coord_model_(self, model):
        self._coord_model = model

    def _set_graph_(self, widget):
        self._graph = widget

    def _draw_timehandle_(self, painter):
        painter._set_antialiasing_(False)
        painter._set_border_color_(_gui_core.GuiRgba.LightAzureBlue)
        painter._set_background_color_(_gui_core.GuiRgba.LightAzureBlue)

        # handle
        painter.drawPath(self._timehandle_path)

        # text
        painter._set_text_color_(_gui_core.GuiRgba.LightLemonYellow)
        painter._set_font_(self._text_font)
        painter.drawText(
            self._timehandle_text_rect,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            str(self._timeframe_current)
        )

        if self._timeframe_bubble_flag is True:
            # rect
            painter._set_antialiasing_(True)
            painter._set_border_color_(_gui_core.GuiRgba.LightAzureBlue)
            painter._set_background_color_(_gui_core.GuiRgba.LightAzureBlue)
            painter.drawRoundedRect(
                self._timeframe_bubble_rect, 2, 2, QtCore.Qt.AbsoluteSize
            )
            # text
            painter._set_text_color_(_gui_core.GuiRgba.LightLemonYellow)
            painter._set_font_(self._text_font)
            painter.drawText(
                self._timeframe_bubble_rect,
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                str(self._timeframe_current)
            )

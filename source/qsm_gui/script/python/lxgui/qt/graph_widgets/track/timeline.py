# coding=utf-8
# qt
from ...core.wrap import *

from ... import core as _qt_core

from ... import abstracts as _qt_abstracts


class _FramePlayThread(QtCore.QThread):
    timeout = qt_signal()

    def __init__(self, parent):
        super(_FramePlayThread, self).__init__(parent)
        self._interval = 1000.0/24

        self._running_flag = False
        self._close_flag = False

    def set_interval(self, interval):
        self._interval = interval

    def do_start(self):
        if self._close_flag is False:
            self._running_flag = True
            self.start()

    def run(self):
        while self._running_flag:
            # noinspection PyArgumentList
            QtCore.QThread.msleep(self._interval)
            self.timeout.emit()

    def do_stop(self):
        self._running_flag = False

    def do_close(self):
        self._close_flag = True
        self.do_stop()
        self.wait()
        self.deleteLater()


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

        self._unit_current_coord = self._coord_model.compute_offset_at(self._current_timeframe)

        #
        self._start_timeframe, self._end_timeframe = self._coord_model.unit_index_range

        # timehandle
        txt_w = QtGui.QFontMetrics(self._text_font).width(str(self._current_timeframe))+16

        d = self._timeframe_current_handle_w/2

        bub_h = frm_h/2
        bub_gap = (frm_h-bub_h)/2+d

        self._timehandle_text_rect.setRect(
            self._unit_current_coord-(txt_w/2), y+bub_gap, txt_w, bub_h
        )
        self._timehandle_path = _qt_core.QtPainterPath()
        self._timehandle_path._add_coords_(
            [
                (self._unit_current_coord-d, y+d),
                (self._unit_current_coord, y),
                (self._unit_current_coord+d, y+d),

                (self._unit_current_coord+d, y+frm_h),
                (self._unit_current_coord-d, y+frm_h),

                (self._unit_current_coord-d, y+d),
            ]
        )

        self._timeframe_bubble_flag = False

        # left hide
        if self._start_timeframe > self._current_timeframe:
            self._timeframe_bubble_flag = True

            self._timeframe_bubble_rect.setRect(
                x+bub_gap, y+bub_gap, txt_w, bub_h
            )

        # right hide
        elif self._end_timeframe < self._current_timeframe:
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
        self._accept_current_timeframe_(frame)

    def _do_press_move_(self, event):
        p = event.pos()

        x = p.x()

        frame = self._coord_model.compute_unit_index_loc(x)
        self._accept_current_timeframe_(frame)

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

        self._text_font = _qt_core.QtFont.generate(size=10, weight=50)

        self._time_index_text_w = 64
        self._current_timeframe = 1

        self._timeframe_bubble_flag = False

        self._start_timeframe, self._end_timeframe = 1, 48

        self._play_start_timeframe, self._play_end_timeframe = self._start_timeframe, self._end_timeframe

        self._timeline_frame_rect = qt_rect()

        self._coord_model = None

        self._autoplaying_flag = False
        self._fps = 24

        self._play_thread = _FramePlayThread(self)
        self._play_thread.timeout.connect(self._on_autoplaying_)
        self._play_thread.set_interval(int(1000.0/self._fps))

        self._timeframe_current_handle_w = 20
        self._timeframe_current_handle_rect = qt_rect()

        self._timehandle_path = _qt_core.QtPainterPath()
        self._timehandle_text_rect = qt_rect()
        self._unit_current_coord = 0

        self._timeframe_bubble_rect = qt_rect()

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
        return self._current_timeframe

    def _set_current_timeframe_(self, value):
        if value != self._current_timeframe:
            self._current_timeframe = value
            self._refresh_widget_all_()
            return True
        return False

    def _accept_current_timeframe_(self, value):
        if self._set_current_timeframe_(value) is True:
            self.frame_accepted.emit(self._current_timeframe)

    def _set_play_timeframe_range_(self, start, end):
        self._play_start_timeframe, self._play_end_timeframe = start, end

    def _set_coord_model_(self, model):
        self._coord_model = model

    def _set_graph_(self, widget):
        self._graph = widget

    def _draw_timehandle_(self, painter):
        painter._set_antialiasing_(False)
        painter.setPen(_qt_core.QtRgba.LightPurple)
        painter.setBrush(_qt_core.QtRgba.LightPurple)

        # handle
        painter.drawPath(self._timehandle_path)

        # rect
        painter._set_antialiasing_(True)
        painter.setPen(_qt_core.QtRgba.BdrBubble)
        painter.setBrush(_qt_core.QtRgba.BkgBubble)
        painter.drawRoundedRect(
            self._timehandle_text_rect, 2, 2, QtCore.Qt.AbsoluteSize
        )

        # text
        painter.setPen(_qt_core.QtRgba.TxtBubble)
        painter._set_font_(self._text_font)
        painter.drawText(
            self._timehandle_text_rect,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            str(self._current_timeframe)
        )

        if self._timeframe_bubble_flag is True:
            # rect
            painter._set_antialiasing_(True)
            painter.setPen(_qt_core.QtRgba.BdrBubble)
            painter.setBrush(_qt_core.QtRgba.BkgBubble)
            painter.drawRoundedRect(
                self._timeframe_bubble_rect, 2, 2, QtCore.Qt.AbsoluteSize
            )

            # text
            painter.setPen(_qt_core.QtRgba.TxtBubble)
            painter._set_font_(self._text_font)
            painter.drawText(
                self._timeframe_bubble_rect,
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                str(self._current_timeframe)
            )

    def _on_autoplaying_(self):
        index = self._current_timeframe

        if index > self._play_end_timeframe:
            index = self._play_start_timeframe

        if index < self._play_start_timeframe:
            index = self._play_start_timeframe

        index += 1

        self._accept_current_timeframe_(index)

    def _swap_autoplaying_(self):
        self._autoplaying_flag = not self._autoplaying_flag

        if self._autoplaying_flag is True:
            self._play_thread.do_start()
        else:
            self._play_thread.do_stop()

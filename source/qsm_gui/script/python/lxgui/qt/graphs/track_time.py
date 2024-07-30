# coding=utf-8
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts


class QtTrackTime(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtActionBaseDef,
):
    timehandle_offset_accepted = qt_signal(int)

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._update_to_timehandle_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        frm_h = self.height()

        self._unit_current_coord = self._coord_model.compute_offset_at(self._timeframe_current)
        # timehandle
        txt_w = self._time_index_text_w
        d = self._timeframe_current_handle_w/2
        self._timehandle_text_rect.setRect(
            self._unit_current_coord-(txt_w/2), y+frm_h/2, txt_w, frm_h/2
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

    def _update_from_graph_(self, rect, translate, scale):
        self._translate = translate
        self._scale = scale
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

        self._coord_model.update(translate, scale, w)

        frm_h = self.height()
        self._timeframe_basic_rect.setRect(x, y, w, frm_h)

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
            self._timeframe_current = frame
            self._refresh_widget_all_()

    def _do_press_move_(self, event):
        p = event.pos()

        x = p.x()

        frame = self._coord_model.compute_unit_index_loc(x)
        if frame != self._timeframe_current:
            self._timeframe_current = frame
            self._refresh_widget_all_()

    def _update_to_timehandle_(self):
        hdl_w = 7
        self._timehandle.setGeometry(
            2+self._unit_current_coord-hdl_w/2, 1,
            hdl_w, self.parent().height()-self.height()/2
        )
        self._timehandle._update_from_graph_()

    def _set_timehandle_(self, widget):
        self._timehandle = widget

    def __init__(self, *args, **kwargs):
        super(QtTrackTime, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(48)

        self._init_action_base_def_(self)

        self._time_index_text_w = 64
        self._timeframe_current = 1
        self._timeframe_start, self._timeframe_end = 1, 48

        self._timeframe_basic_rect = QtCore.QRect()
        self._timeframe_range_rect = QtCore.QRect()

        self._coord_model = None

        self._timeframe_current_handle_w = 20
        self._timeframe_current_handle_rect = QtCore.QRect()
        self._timehandle_path = _qt_core.QtPainterPath()
        self._timehandle_text_rect = QtCore.QRect()
        self._unit_current_coord = 0

        self._draw_offset = -1

        self._translate = 0
        self._scale = 1

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
            # zoom
            elif event.type() == QtCore.QEvent.Wheel:
                self._graph.eventFilter(self._graph, event)
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtNGPainter(self)
        self._draw_timeline_basic_(painter)
        self._draw_timehandle_(painter)

    def _set_coord_model_(self, model):
        self._coord_model = model

    def _set_graph_(self, widget):
        self._graph = widget

    def _draw_timeline_basic_(self, painter):
        x, y, w, h = (
            self._timeframe_basic_rect.x(), self._timeframe_basic_rect.y(),
            self._timeframe_basic_rect.width(), self._timeframe_basic_rect.height()
        )
        painter._set_antialiasing_(False)
        frm_line = QtCore.QLine(x, y, w, y)
        painter._set_border_color_(_gui_core.GuiRgba.Dark)
        painter._set_background_color_(_gui_core.GuiRgba.Dark)
        painter.drawRect(self._timeframe_basic_rect)
        # bottom line
        painter._set_border_color_(_gui_core.GuiRgba.Gray)
        painter.drawLine(frm_line)

        painter._set_border_color_(_gui_core.GuiRgba.LightGray)
        painter._set_font_(_qt_core.QtFont.generate(size=8))
        # draw +1
        for i in range(self._coord_model.unit_count):
            # offset -1
            i_time_index = self._coord_model.compute_draw_index_at(i)
            if i_time_index == 0:
                painter._set_border_color_(_gui_core.GuiRgba.LightYellow)
                painter._set_font_(_qt_core.QtFont.generate(size=8))
                # draw +1
            else:
                painter._set_border_color_(_gui_core.GuiRgba.LightGray)
                painter._set_font_(_qt_core.QtFont.generate(size=8))
                # draw +1
            i_x = self._coord_model.compute_draw_coord_at(i)
            # 200
            if self._coord_model.unit_size <= 0.5:
                # 200 per frame
                if not i_time_index%200:
                    i_line = QtCore.QLine(i_x, y+h*.5, i_x, y+h)
                    painter.drawLine(i_line)
                    self._draw_time_text_(painter, i_time_index, i_x, y, h)
            # 100
            elif 0.1 < self._coord_model.unit_size <= 1:
                # 100 per frame
                if not i_time_index%100:
                    i_line = QtCore.QLine(i_x, y+h*.5, i_x, y+h)
                    painter.drawLine(i_line)
                    self._draw_time_text_(painter, i_time_index, i_x, y, h)
                # 10 per frame
                elif not i_time_index%10:
                    i_line = QtCore.QLine(i_x, y+h*.75, i_x, y+h)
                    painter.drawLine(i_line)
            # 50
            elif 1 < self._coord_model.unit_size <= 2:
                # 50 per frame
                if not i_time_index%50:
                    i_line = QtCore.QLine(i_x, y+h*.5, i_x, y+h)
                    painter.drawLine(i_line)
                    self._draw_time_text_(painter, i_time_index, i_x, y, h)
                # 10 per frame
                elif not i_time_index%10:
                    i_line = QtCore.QLine(i_x, y+h*.75, i_x, y+h)
                    painter.drawLine(i_line)
            # 20
            elif 2 < self._coord_model.unit_size <= 5:
                # 20 per frame
                if not i_time_index%20:
                    i_line = QtCore.QLine(i_x, y+h*.5, i_x, y+h)
                    painter.drawLine(i_line)
                    self._draw_time_text_(painter, i_time_index, i_x, y, h)
                # 10 per frame
                elif not i_time_index%10:
                    i_line = QtCore.QLine(i_x, y+h*.75, i_x, y+h)
                    painter.drawLine(i_line)
            # 10
            elif 5 < self._coord_model.unit_size <= 10:
                # 10 per frame
                if not i_time_index%10:
                    i_line = QtCore.QLine(i_x, y+h*.5, i_x, y+h)
                    painter.drawLine(i_line)
                    self._draw_time_text_(painter, i_time_index, i_x, y, h)
                # 1 per frame
                else:
                    i_line = QtCore.QLine(i_x, y+h*.75, i_x, y+h)
                    painter.drawLine(i_line)
            # 5
            elif 10 < self._coord_model.unit_size <= 20:
                if not i_time_index%5:
                    i_line = QtCore.QLine(i_x, y+h*.5, i_x, y+h)
                    painter.drawLine(i_line)
                    self._draw_time_text_(painter, i_time_index, i_x, y, h)
                # 1 per frame
                else:
                    i_line = QtCore.QLine(i_x, y+h*.75, i_x, y+h)
                    painter.drawLine(i_line)
            # 1
            elif 20 < self._coord_model.unit_size:
                i_line = QtCore.QLine(i_x, y+h*.5, i_x, y+h)
                painter.drawLine(i_line)
                self._draw_time_text_(painter, i_time_index, i_x, y, h)

    def _draw_time_text_(self, painter, i_time_index, i_x, y, h):
        i_rect = QtCore.QRect(
            i_x-self._time_index_text_w/2, y, self._time_index_text_w, h*.5
        )
        painter.drawText(
            i_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, str(i_time_index)
        )

    def _draw_timehandle_(self, painter):
        painter._set_antialiasing_(False)
        painter._set_border_color_(_gui_core.GuiRgba.LightAzureBlue)
        painter._set_background_color_(_gui_core.GuiRgba.LightAzureBlue)
        painter.drawPath(self._timehandle_path)
        painter._set_text_color_(_gui_core.GuiRgba.LightYellow)
        painter._set_font_(_qt_core.QtFont.generate(size=10, weight=75))
        painter.drawText(
            self._timehandle_text_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
            str(self._timeframe_current)
        )

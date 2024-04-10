# coding=utf-8
import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts
# qt widgets
from . import utility as gui_qt_wgt_utility


class QtChartAsRgbaChoose(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtWidgetBaseDef,
    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtChartBaseDef,
):
    def _refresh_widget_draw_(self):
        pass

    color_choose_changed = qt_signal()

    def _execute_popup_filter_(self):
        self.update()

    def _refresh_chart_data_(self):
        def set_branch_draw_fnc_(x, y, radius_, color_h_offset_, color_h_multiply_):
            _i_pos = x, y
            if _i_pos not in poses:
                poses.append(_i_pos)
                _i_color_point = QtCore.QPoint(x, y)
                if color_path_main.contains(_i_color_point):
                    _i_sub_points = gui_core.GuiChat.get_regular_polygon_points(
                        x, y, side_count, radius_sub-1, side=0
                    )
                    _i_color_path = gui_qt_core.QtPainterPath()
                    _i_color_path._set_points_add_(_i_sub_points)
                    #
                    angle = gui_core.GuiChat.get_angle_by_coord(x, y, pos_x, pos_y)
                    length = gui_core.GuiChat.get_length_by_coord(x, y, pos_x, pos_y)
                    #
                    _color_h = -angle-color_h_offset_
                    #
                    r1 = radius_
                    a1 = angle
                    d1 = 360.0/side_count
                    d2 = 360.0/side_count/2
                    of = -d2
                    a2 = a1+of-gui_core.GuiChat.FNC_FLOOR(a1/d1)*d1
                    _l = [
                        gui_core.GuiChat.FNC_SIN(
                            gui_core.GuiChat.FNC_ANGLE(d1)
                            )/gui_core.GuiChat.FNC_COS(gui_core.GuiChat.FNC_ANGLE(a2))*r1,
                        r1
                    ][a1%180 == 0]
                    #
                    s = length/(_l-radius_sub)
                    s = float(max(min(s, 1.0), 0.0))
                    v = color_h_multiply_/100.0
                    v = float(max(min(v, 1.0), 0.0))
                    #
                    r, g, b = bsc_core.RawColorMtd.hsv2rgb(_color_h, s, v)
                    i_background_rgba = r, g, b, 255
                    i_border_rgba = 0, 0, 0, 0
                    #
                    self._chart_draw_data[i_background_rgba] = _i_color_path, _i_color_point, i_border_rgba

        #
        self._chart_draw_data = {}
        width, height = self.width(), self.height()
        #
        poses = []
        #
        pos_x, pos_y = width/2, height/2
        #
        count = self._count
        #
        side = 16
        side_count = 6
        #
        radius_main = min(width, height)/2-side
        #
        radius_sub = float(radius_main)/count
        #
        points_main = gui_core.GuiChat.get_regular_polygon_points(
            pos_x, pos_y, side_count, radius_main, radius_sub/2
        )
        color_path_main = gui_qt_core.QtPainterPath()
        color_path_main._set_points_add_(points_main)
        #
        x_count = int(count*.75)
        y_count = int(count*.75)
        #
        for i_x in range(x_count):
            for i_y in range(y_count):
                x_offset = gui_core.GuiChat.FNC_SIN(gui_core.GuiChat.FNC_ANGLE(60))*radius_sub
                #
                x_r_sub = x_offset*i_x*2-x_offset*(i_y%2)
                y_r_sub = i_y*radius_sub*1.5
                #
                x_p_sub_ = x_r_sub+pos_x
                y_p_sub_ = y_r_sub+pos_y
                #
                x_p_sub = width/2-x_r_sub
                y_p_sub = height/2-y_r_sub
                #
                set_branch_draw_fnc_(x_p_sub_, y_p_sub, radius_main, self._color_h_offset, self._color_v_multiply)
                set_branch_draw_fnc_(x_p_sub, y_p_sub, radius_main, self._color_h_offset, self._color_v_multiply)
                set_branch_draw_fnc_(x_p_sub_, y_p_sub_, radius_main, self._color_h_offset, self._color_v_multiply)
                set_branch_draw_fnc_(x_p_sub, y_p_sub_, radius_main, self._color_h_offset, self._color_v_multiply)

    def __init__(self, *args, **kwargs):
        super(QtChartAsRgbaChoose, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.installEventFilter(self)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        self._init_widget_base_def_(self)
        self._init_action_base_def_(self)
        self._init_chart_base_def_(self)
        self._gui_build_()

    def paintEvent(self, event):
        self._color_path_dict = {}
        #
        painter = gui_qt_core.QtPainter(self)
        # painter.begin(self)  # for pyside2
        painter.setRenderHint(painter.Antialiasing)
        #
        width = self.width()
        height = self.height()
        #
        if self._chart_draw_data:
            for i_background_rgba, v in self._chart_draw_data.items():
                _i_color_path, _i_color_point, i_border_rgba, = v
                painter._set_border_color_(i_border_rgba)
                painter._set_background_color_(i_background_rgba)
                #
                # painter._set_border_width_(2)
                painter.drawPath(_i_color_path)
        # draw selection
        if self._color_rgba_255 is not None:
            if self._color_rgba_255 in self._chart_draw_data:
                _i_color_path, _i_color_point, i_border_rgba = self._chart_draw_data[self._color_rgba_255]
                painter._set_background_color_(0, 0, 0, 0)
                painter._set_border_color_(255, 255, 255, 255)
                #
                painter._set_border_width_(4)
                painter.drawPath(_i_color_path)
                #
                self._color_point_temp = _i_color_point

        if self._color_rgba_255 is not None:
            painter._set_border_color_(255, 255, 255, 255)
            #
            text_rect = QtCore.QRect(
                8, 8,
                width, height
            )
            #
            painter.setFont(gui_qt_core.QtFonts.Default)
            painter._set_border_width_(1)
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                'R : {0}\r\nG : {1}\r\nB : {2}'.format(*self._color_rgba_255[:3])
            )
            #
            sh, ss, sv = self._color_hsv
            text_rect = QtCore.QRect(
                8, 64,
                width, height
            )
            #
            painter._set_font_(gui_qt_core.QtFonts.Default)
            painter._set_border_width_(1)
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                'H : {0}\r\nS : {1}\r\nV : {2}'.format(round(sh%360, 2), round(ss, 2), round(sv, 2))
            )
            #
            text_rect = QtCore.QRect(
                8, 128,
                width, height
            )
            #
            painter._set_border_color_(223, 223, 223, 255)
            painter.setFont(gui_qt_core.QtFonts.Default)
            painter._set_border_width_(1)
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                '#{}'.format(self._color_css).upper()
            )

        # painter.end()  # for pyside2

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    # Press
                    self._color_point = event.pos()
                    self._update_selected_()
                    # Move
                    self._move_flag = True
                    self._set_action_flag_(self.ActionFlag.Press)
                elif event.button() == QtCore.Qt.RightButton:
                    # Track
                    self._track_offset_start_point = event.globalPos()
                    self._track_offset_flag = True
                elif event.button() == QtCore.Qt.MidButton:
                    # Circle
                    point = event.pos()
                    self._circle_angle_start = self._get_angle_at_circle_(point)
                    self._circle_flag = True
                    self._set_action_flag_(self.ActionFlag.TrackPress)
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    # Press
                    self._set_action_flag_(self.ActionFlag.PressMove)
                    # Move
                    self._move_flag = True
                    #
                    self._color_point = event.pos()
                    self._update_selected_()
                    #
                    self.update()
                elif event.buttons() == QtCore.Qt.RightButton:
                    # Track
                    self._track_offset_flag = True
                    point = event.globalPos()-self._track_offset_start_point
                    self._do_track_offset_(point)
                elif event.buttons() == QtCore.Qt.MidButton:
                    # Circle
                    self._circle_flag = True
                    #
                    self._do_track_circle_(event)
                    self._set_action_flag_(self.ActionFlag.TrackCircle)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_is_match_(
                        self.ActionFlag.Press
                    ):
                        self._do_press_click_(event)
                    #
                    self._move_flag = True
                elif event.button() == QtCore.Qt.RightButton:
                    # Track
                    self._tmp_track_offset_x = self._track_offset_x
                    self._track_offset_y_temp = self._track_offset_y
                    self._track_offset_flag = True
                elif event.button() == QtCore.Qt.MidButton:
                    # Circle
                    self._circle_angle_temp = self._color_h_offset
                    self._circle_flag = True
                self._clear_all_action_flags_()
            elif event.type() == QtCore.QEvent.Wheel:
                self._set_action_flag_(
                    self.ActionFlag.ZoomWheel
                )
                self._do_zoom_scale_(event)
                #
                self._move_flag = False
                self._circle_flag = False
                self._track_offset_flag = False
            elif event.type() == QtCore.QEvent.Resize:
                self._move_flag = False
                self._circle_flag = False
                self._track_offset_flag = False
                self._refresh_chart_data_()
                self._refresh_widget_draw_()
        return False

    def _update_selected_(self):
        pre_color = self._color_rgba_255
        cur_color = self._color_rgba_255

        if self._chart_draw_data:
            for i_background_rgba, v in self._chart_draw_data.items():
                _i_color_path, _i_color_point, i_border_rgba = v
                if _i_color_path.contains(self._color_point):
                    cur_color = i_background_rgba

        if pre_color != cur_color:
            r, g, b, a = cur_color
            self._color_rgba_255 = r, g, b, a
            self._update_color_()

            self.color_choose_changed.emit()

            self._refresh_widget_draw_()

    def _do_press_click_(self, event):
        self._color_point = event.pos()
        self._update_selected_()

    def _do_zoom_scale_(self, event):
        delta = event.angleDelta().y()
        #
        radix = 3
        #
        pre_count = self._count
        cur_count = bsc_core.RawValueMtd.step_to(
            value=pre_count,
            delta=-delta,
            step=radix,
            value_range=(self._count_minimum, self._count_maximum),
            direction=1
        )
        if pre_count != cur_count:
            self._count = cur_count
            self._refresh_chart_data_()
            self._refresh_widget_draw_()
            self._update_selected_()

    def _do_track_circle_(self, event):
        point = event.pos()
        #
        angle_ = self._get_angle_at_circle_(point)
        #
        angle = self._circle_angle_temp+self._circle_angle_start
        angle -= angle_
        #
        if self._circle_flag is True:
            self._color_h_offset = angle
        #
        self._refresh_chart_data_()
        self._refresh_widget_draw_()
        self._update_selected_()

    def _do_track_offset_(self, point):
        _delta_x = point.x()
        delta_y = point.y()
        _radix_x = 5.0
        radix_y = 5.0
        self._color_v_multiply = bsc_core.RawValueMtd.step_to(
            value=self._color_v_multiply,
            delta=-delta_y,
            step=radix_y,
            value_range=(self._mult_v_minimum, self._mult_v_maximum),
            direction=1
        )
        #
        self._refresh_chart_data_()
        self._refresh_widget_draw_()
        self._update_selected_()

    def _get_popup_pos_from_(self, x, y, width, height):
        point = self._color_point
        pos0 = self._color_center_coord

        width0, height0 = self._size_temp

        _scale = float(min(width, height))/float(min(width0, height0))

        x_c = point.x()
        y_c = point.y()

        x_c -= (pos0[0]-x)
        y_c -= (pos0[1]-y)
        return QtCore.QPoint(x_c, y_c)

    def _get_angle_at_circle_(self, point):
        return gui_core.GuiChat.get_angle_by_coord(
            point.x(), point.y(), self.width()/2, self.height()/2
        )

    def _get_color_rgb_255_(self):
        return self._color_rgba_255

    def _get_color_rgba_(self):
        return tuple(map(lambda x: float(x/255.0), self._color_rgba_255))

    def _get_color_rgba_255_(self):
        return self._color_rgba_255

    def _set_color_rgba_(self, r, g, b, a):
        self._color_rgba_255 = tuple(map(lambda x: int(x*255), (r, g, b, a)))

    def _set_color_rgba_255_(self, rgba):
        self._color_rgba_255 = tuple(rgba)
        self._update_color_()

    def _update_color_(self):
        r, g, b, a = self._color_rgba_255
        self._color_hsv = bsc_core.RawColorMtd.rgb_to_hsv(r, g, b)
        self._color_css = hex(r)[2:].zfill(2)+hex(g)[2:].zfill(2)+hex(b)[2:].zfill(2)

    def _gui_build_(self):
        self._color_rgba_255 = 255, 255, 255, 255
        self._color_hsv = 0, 0, 1
        self._color_css = 'FFFFFF'
        #
        self.cls_colorPath = None
        #
        self._color_path_dict = {}
        #
        self._move_flag = False
        #
        self._track_offset_start_point = QtCore.QPoint(0, 0)
        #
        self._color_point = QtCore.QPoint(0, 0)
        self._color_point_temp = QtCore.QPoint(0, 0)
        self._color_center_coord = 0, 0
        self._size_temp = 240, 240
        #
        self._circle_angle_start = 0.0
        #
        self._circle_flag = False
        #
        self._circle_angle_temp = 0.0
        self._color_h_offset = 0.0
        #
        self._track_offset_flag = False
        self._tmp_track_offset_x = 0
        self._track_offset_y_temp = 0
        self._track_offset_x = 0
        self._track_offset_y = 0
        #
        self._count = 3*3+1
        self._count_maximum = 3*6+1
        self._count_minimum = 3*1+1
        #
        self._color_v_multiply = 100.0
        self._mult_v_maximum = 100.0
        self._mult_v_minimum = 0.0


class QtChartAsProgressing(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtProgressBaseDef
):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtChartAsProgressing, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        #
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        #
        self._init_progress_base_def_()

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        if self._get_progress_is_enable_() is True:
            if self._progress_raw:
                x, y = 0, 0
                w, h = self.width(), self.height()
                frm_w, frm_h = 96, 96
                frame_rect = QtCore.QRect(
                    x+(w-frm_w)/2, y+(h-frm_h)/2, frm_w, frm_h
                )
                base_rect = QtCore.QRect(
                    x, y, w, h
                )
                painter._set_border_color_(0, 0, 0, 0)
                painter._set_background_color_(15, 15, 15, 127)
                painter.drawRect(
                    base_rect
                )
                for i_index, i in enumerate(self._progress_raw):
                    i_percent, i_percent_range, i_label, i_show_percent = i
                    if i_index == 0:
                        i_data = gui_qt_core.GuiQtChartDrawDataForProcessing._get_basic_data_(
                            rect=frame_rect,
                            index=i_index,
                            percent=i_percent,
                            percent_range=i_percent_range,
                            label=i_label,
                            show_percent=i_show_percent,
                            tape_w=12, spacing=4
                        )
                    else:
                        i_data = gui_qt_core.GuiQtChartDrawDataForProcessing._get_basic_data_(
                            rect=frame_rect,
                            index=i_index,
                            percent=i_percent,
                            percent_range=i_percent_range,
                            label=i_label,
                            show_percent=i_show_percent,
                            tape_w=4, spacing=12
                        )

                    (
                        i_annulus_sector_path, i_annulus_sector_color,
                        i_show_name_rect_f, i_show_name_option, i_show_name,
                        i_show_percent_rect_f, i_show_percent_option, i_show_percent,
                        i_text_color
                    ) = i_data
                    #
                    painter._set_border_color_(gui_qt_core.QtBorderColors.Transparent)
                    if i_index == 0:
                        painter._set_background_color_(i_annulus_sector_color)
                    else:
                        painter._set_background_color_(i_text_color)
                    painter.drawPath(i_annulus_sector_path)

                    painter._set_text_color_(i_text_color)
                    painter._set_font_(gui_qt_core.QtFonts.Chart)

                    painter.drawText(
                        i_show_name_rect_f, i_show_name, i_show_name_option
                    )
                    painter.drawText(
                        i_show_percent_rect_f, i_show_percent, i_show_percent_option
                    )


class QtChartAsInfo(
    QtWidgets.QWidget,
):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtChartAsInfo, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        #
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setMaximumHeight(20)
        self.setMinimumHeight(20)

        self._info_text = ''

        self._info_draw_rect = QtCore.QRect()
        self._info_draw_size = 160, 24

    def _refresh_widget_geometry_(self, x, y, w, h):
        self.setGeometry(
            x, y, w, h
        )
        self._refresh_widget_draw_()

    def _set_info_text_(self, text):
        self._info_text = text
        if text:
            self.show()
            self._refresh_widget_draw_()
        else:
            self.hide()

    def _clear_(self):
        self._set_info_text_('')

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        if self._info_text:
            rect = self.rect()
            painter._draw_frame_by_rect_(
                rect=rect,
                border_color=gui_qt_core.QtBorderColors.Transparent,
                background_color=gui_qt_core.QtBackgroundColors.ToolTip,
            )
            painter._draw_line_by_points_(
                point_0=rect.topLeft(), point_1=rect.topRight(),
                border_color=gui_qt_core.QtBorderColors.Basic
            )
            painter._draw_text_by_rect_(
                rect=self.rect(),
                text=self._info_text,
                font=gui_qt_core.GuiQtFont.generate(size=10, italic=True),
                font_color=gui_qt_core.QtFontColors.ToolTip,
                text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
            )


class QtChartAsWaiting(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtChartBaseDef,
):
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_chart_data_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        c = self._waiting_draw_count
        c_w = c_h = self._waiting_draw_radius
        self._waiting_draw_rect.setRect(
            x, y, w, h
        )
        start_pos = x+(w-c_w)/2, y+(h-c_h)/2
        radius = min(c_w, c_h)
        self._waiting_positions = []
        for i in range(c):
            i_angle = 360.0/c*i
            i_x, i_y = gui_core.GuiEllipse2d.get_coord_at_angle(
                start=start_pos, radius=radius, angle=i_angle
            )
            self._waiting_positions.append(
                (i_x, i_y)
            )

        self._refresh_widget_draw_()

    def __init__(self, *args, **kwargs):
        super(QtChartAsWaiting, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setMouseTracking(True)
        #
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        #
        self.installEventFilter(self)

        self._init_chart_base_def_(self)

        self._waiting_draw_radius = 64
        self._waiting_draw_item_radius = 12
        self._waiting_draw_count = 10
        self._waiting_draw_rect = QtCore.QRect()
        self._waiting_positions = []
        self._waiting_timestamp = 0

        self._waiting_timer = QtCore.QTimer(self)
        self._waiting_timer.setInterval(0)
        self._waiting_timer.timeout.connect(
            self._refresh_waiting_draw_
        )

    def _start_waiting_(self):
        self._waiting_timer.start(0)
        # GuiQtApplicationOpt().set_process_run_0()

    def _stop_waiting_(self):
        self._waiting_timer.stop()
        # GuiQtApplicationOpt().set_process_run_0()

    def _refresh_waiting_draw_(self):
        self._waiting_timestamp = int(bsc_core.SysBaseMtd.get_timestamp()*5)
        self._refresh_widget_draw_()
        # GuiQtApplicationOpt().set_process_run_0()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_chart_data_()
                event.accept()
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        painter._set_border_color_(0, 0, 0, 0)
        painter._set_antialiasing_()

        painter._set_border_color_(0, 0, 0, 0)
        painter._set_background_color_(31, 31, 31, 63)
        painter.drawRect(
            self._waiting_draw_rect
        )
        c = self._waiting_draw_count
        i_r = self._waiting_draw_item_radius
        timestamp = self._waiting_timestamp
        for seq, i in enumerate(self._waiting_positions):
            i_x, i_y = i

            cur_index = c-timestamp%(c+1)
            i_c_h = abs(cur_index-seq)*(360/c)
            i_h, i_s, i_v = i_c_h, 0.5, 1.0
            i_c_r, i_c_g, i_c_b = bsc_core.RawColorMtd.hsv2rgb(i_h, i_s, i_v)
            #
            painter._set_border_color_(0, 0, 0, 0)
            painter._set_background_color_(i_c_r, i_c_g, i_c_b, 255)
            #
            if seq == cur_index:
                painter.drawEllipse(
                    i_x-i_r/2, i_y-i_r/2, i_r, i_r
                )
            else:
                i_a = 360.0/c*seq
                i_coords = [
                    gui_core.GuiEllipse2d.get_coord_at_angle_(center=(i_x, i_y), radius=i_r, angle=-90+i_a),
                    gui_core.GuiEllipse2d.get_coord_at_angle_(center=(i_x, i_y), radius=i_r, angle=-210+i_a),
                    gui_core.GuiEllipse2d.get_coord_at_angle_(center=(i_x, i_y), radius=i_r, angle=-330+i_a),
                    gui_core.GuiEllipse2d.get_coord_at_angle_(center=(i_x, i_y), radius=i_r, angle=-90+i_a)
                ]
                painter._draw_path_by_coords_(
                    i_coords
                )


class QtChartAsSector(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtChartBaseDef
):
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_chart_data_(self):
        x, y = 0, 0
        # noinspection PyUnresolvedReferences
        w, h = self.width(), self.height()
        self._chart_draw_data = gui_qt_core.GuiQtChartDrawDataForSector(
            data=self._chart_data,
            position=(x, y),
            size=(w, h),
            align=(QtCore.Qt.AlignLeft, QtCore.Qt.AlignVCenter),
            side_w=16,
            mode=self._chart_mode
        ).get()

    #
    def __init__(self, *args, **kwargs):
        super(QtChartAsSector, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.installEventFilter(self)
        #
        self._init_chart_base_def_(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_chart_data_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.MouseMove:
                self._hover_point = event.pos()
                self.update()
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        # painter.begin(self)  # for pyside2
        painter.setRenderHint(painter.Antialiasing)
        #
        if self._chart_draw_data is not None:
            painter._set_sector_chart_draw_(
                chart_draw_data=self._chart_draw_data,
                background_color=self._chart_background_color,
                border_color=self._chart_border_color,
                hover_point=self._hover_point,
            )


class QtChartAsRadar(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtChartBaseDef
):
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_chart_data_(self):
        x, y = 0, 0
        # noinspection PyUnresolvedReferences
        w, h = self.width(), self.height()
        self._chart_draw_data = gui_qt_core.GuiQtChartDrawDataForRadar(
            data=self._chart_data,
            position=(x, y),
            size=(w, h),
            align=(QtCore.Qt.AlignLeft, QtCore.Qt.AlignVCenter),
            side_w=16,
            mode=self._chart_mode
        ).get()

    #
    def __init__(self, *args, **kwargs):
        super(QtChartAsRadar, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.installEventFilter(self)
        #
        self._map_background_color = 79, 95, 151, 255
        self._map_border_color = 159, 159, 159, 255
        self._rim_background_color = 39, 39, 39, 255
        self._rim_border_color = 95, 95, 95, 255
        #
        self._init_chart_base_def_(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_chart_data_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.MouseMove:
                self._hover_point = event.pos()
                self.update()
        return False

    def paintEvent(self, event):
        painter = gui_qt_core.QtPainter(self)
        # painter.begin(self)  # for pyside2
        painter.setRenderHint(painter.Antialiasing)
        if self._chart_draw_data is not None:
            basic_data = self._chart_draw_data['basic']
            map_data = self._chart_draw_data['map']
            mark_data = self._chart_draw_data['mark']
            p_hover = self._hover_point
            #
            if basic_data is not None:
                for seq, i in enumerate(basic_data):
                    painter._set_background_color_(self._rim_background_color)
                    painter._set_border_color_(self._rim_border_color)
                    painter._set_background_style_(QtCore.Qt.FDiagPattern)
                    if seq == 0:
                        painter.drawPolygon(i)
                    else:
                        painter.drawPolyline(i)
            #
            if map_data is not None:
                i_map_brush, i_map_polygon_src, i_map_polygon_tgt = map_data
                #
                painter._set_background_color_(self._map_background_color)
                painter._set_border_color_(self._map_border_color)
                #
                painter._set_background_style_(QtCore.Qt.Dense5Pattern)
                # painter.drawPolygon(i_map_polygon_src)
                #
                painter._set_background_brush_(i_map_brush)
                painter._set_border_color_(self._map_border_color)
                painter.drawPolygon(i_map_polygon_tgt)
            #
            if mark_data:
                for i in mark_data:
                    (
                        i_background_rgba, i_border_rgba,
                        i_basic_path,
                        i_text_point_0, i_text_point_1,
                        i_text_0, i_text_1,
                        i_point_src, i_point_tgt,
                        i_text_ellipse
                    ) = i
                    #
                    r, g, b, a = i_background_rgba
                    painter._set_background_color_(
                        [(r*.75, g*.75, b*.75, 255), (r, g, b, 255)][i_text_ellipse.contains(p_hover)]
                        )
                    painter._set_border_color_(i_border_rgba)
                    #
                    painter.drawEllipse(i_text_ellipse)
                    #
                    painter.drawText(i_text_point_0, i_text_0)
                    painter.drawText(i_text_point_1, i_text_1)


class QtChartAsPie(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtChartBaseDef
):
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_chart_data_(self):
        x, y = 0, 0
        # noinspection PyUnresolvedReferences
        w, h = self.width(), self.height()
        self._chart_draw_data = gui_qt_core.GuiQtChartDrawDataForPie(
            data=self._chart_data,
            position=(x, y),
            size=(w, h),
            align=(QtCore.Qt.AlignLeft, QtCore.Qt.AlignVCenter),
            side_w=self._side_w,
            mode=self._chart_mode
        ).get()
        self._basic_data = self._chart_draw_data

    #
    def __set_press_update_(self, event):
        i_enable = False
        offset_x, offset_y = 8, 8
        if self._basic_data:
            for seq, i in enumerate(self._basic_data):
                i_color, i_name, i_value, i_percent, i_path, i_shadow_path, i_pos, i_is_selected = i
                x, y = i_pos
                if i_path.contains(event.pos()) is True:
                    if i_is_selected is False:
                        i_is_selected = True
                        self._current_name_text = i_name
                        self._current_percent = i_percent
                        i_path.translate(x, y)
                        i_shadow_path.translate(x+offset_x, y+offset_y)
                    #
                    i_enable = True
                elif i_path.contains(event.pos()) is False:
                    if i_is_selected is True:
                        i_is_selected = False
                        i_path.translate(-x, -y)
                        i_shadow_path.translate(-x-offset_x, -y-offset_y)
                #
                self._basic_data[seq] = i_color, i_name, i_value, i_percent, i_path, i_shadow_path, i_pos, i_is_selected
        #
        if not i_enable:
            self._current_name_text = None
            self._current_percent = None
        #
        self.update()

    #
    def __init__(self, *args, **kwargs):
        super(QtChartAsPie, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.installEventFilter(self)
        #
        self._side_w = 8
        self._xOffset = 0
        self._yOffset = 0
        #
        self._explainWidth = 240
        self._explainHeight = 20
        #
        self._current_name_text = None
        self._current_percent = None
        self._current_value = None
        self._pen = QtGui.QPen(QtGui.QColor(223, 223, 223, 255))
        #
        self._init_chart_base_def_(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_chart_data_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self.__set_press_update_(event)
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self.__set_press_update_(event)
                else:
                    self._hover_point = event.pos()
                    self.update()
        return False

    def paintEvent(self, event):
        width, height = self.width(), self.height()
        side = self._side_w
        #
        radius = min(width, height)
        #
        painter = gui_qt_core.QtPainter(self)
        painter.setRenderHint(painter.Antialiasing)
        if self._basic_data:
            current_shadow_path = None
            for i in self._basic_data:
                i_color, i_name, i_value, i_percent, i_path, i_sub_path, i_pos, i_is_selected = i
                i_shadow_path = i_sub_path-i_path
                painter._set_background_color_(i_color)
                if i_is_selected is True:
                    painter._set_border_color_(self._hover_chart_border_color)
                    current_shadow_path = i_shadow_path
                else:
                    painter._set_border_color_(self._chart_border_color)
                #
                painter._set_border_width_(1)
                painter.drawPath(i_path)
            #
            if current_shadow_path is not None:
                painter._set_background_color_(0, 0, 0, 64)
                painter._set_border_color_(0, 0, 0, 64)
                painter._set_border_width_(1)
                painter._set_background_style_(QtCore.Qt.FDiagPattern)
                painter.drawPath(current_shadow_path)
            # Explain
            rect = QtCore.QRect(
                side, side,
                radius-side*2, radius-side*2
            )
            if self._current_name_text and self._current_percent:
                painter.setPen(self._pen)
                painter.setFont(gui_qt_core.QtFonts.Large)
                painter.drawText(
                    rect, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
                    '{}: {}'.format(self._current_name_text, self._current_percent)
                )


class QtChartAsHistogram(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtDrawGridDef,
    #
    gui_qt_abstracts.AbsQtActionForTrackDef,
    gui_qt_abstracts.AbsQtActionForZoomDef,
    #
    gui_qt_abstracts.AbsQtChartBaseDef,
):
    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_chart_data_(self):
        x, y = 0, 0
        # noinspection PyUnresolvedReferences
        w, h = self.width(), self.height()
        self._chart_draw_data = gui_qt_core.GuiQtChartDrawDataForHistogram(
            data=self._chart_data,
            position=(x, y),
            size=(w, h),
            align=(QtCore.Qt.AlignLeft, QtCore.Qt.AlignVCenter),
            side_w=16,
            mode=self._chart_mode
        ).get()
        self._basic_data = self._chart_draw_data

        self._value_array = self._chart_data

    #
    def __set_selection_update_(self, event):
        x = event.pos().x()-self._track_offset_x-self._grid_offset_x
        self._selectedIndex = int(x/int(self._grid_width/self._zoom_scale_x))

    #
    def __init__(self, *args, **kwargs):
        super(QtChartAsHistogram, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.installEventFilter(self)
        #
        self._set_draw_grid_def_init_(self)
        self._grid_axis_lock_x, self._grid_axis_lock_y = 1, 1
        self._grid_dir_x, self._grid_dir_y = 1, -1
        # self._grid_offset_x, self._grid_offset_y = 20, 20
        #
        self._init_action_for_track_def_(self)
        self._track_offset_direction_x, self._track_offset_direction_y = self._grid_dir_x, self._grid_dir_y
        self._track_offset_minimum_x, self._track_offset_minimum_y = -10000, -10000
        self._track_offset_maximum_x, self._track_offset_maximum_y = 0, 0
        #
        self._init_action_for_zoom_def_(self)
        #
        self._init_chart_base_def_(self)
        #
        self._gui_build_()

    def _set_labels_(self, labels):
        self._xValueExplain, self._yValueExplain = labels

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_chart_data_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                pass
            elif event.type() == QtCore.QEvent.Leave:
                pass
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    x = event.pos().x()-self._track_offset_x-self._grid_offset_x
                    self._selectedIndex = int(x/int(self._grid_width/2))
                    #
                    self.update()
                    # Drag Select
                    self._move_flag = True
                #
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    self._set_tack_offset_action_start_(event)
                    # Zoom
                    self._zoom_scale_flag = False
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self._move_flag = False
                elif event.button() == QtCore.Qt.RightButton:
                    pass
                elif event.button() == QtCore.Qt.MidButton:
                    # Track
                    self._set_track_offset_action_end_(event)
                    # Zoom
                    self._zoom_scale_flag = True
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                if event.buttons() == QtCore.Qt.LeftButton:
                    if self._move_flag is True:
                        self.__set_selection_update_(event)
                        #
                        self.update()
                elif event.buttons() == QtCore.Qt.RightButton:
                    pass
                elif event.buttons() == QtCore.Qt.MidButton:
                    # Track
                    if self._track_offset_flag is True:
                        self._do_track_offset_(event)
                else:
                    event.ignore()
            #
            elif event.type() == QtCore.QEvent.Wheel:
                if self._zoom_scale_flag is True:
                    self._do_zoom_scale_(event)
        return False

    #
    def paintEvent(self, event):
        x = 0
        y = 0
        #
        width = self.width()
        height = self.height()
        #
        value_scale_x, value_scale_y = self._zoom_scale_x, self._zoom_scale_y
        #
        painter = gui_qt_core.QtPainter(self)
        rect = QtCore.QRect(
            x, y, width, height
        )
        painter._set_grid_draw_(
            rect,
            axis_dir=(self._grid_dir_x, self._grid_dir_y),
            grid_size=(self._grid_width, self._grid_height),
            grid_scale=(1.0, self._zoom_scale_y),
            translate=(self._track_offset_x, 0),
            grid_offset=(self._grid_offset_x, self._grid_offset_y),
            border_color=self._grid_border_color
        )
        #
        if self._value_array:
            value_maximum = max(self._value_array)
            value_scale_x, value_scale_y = 1.0, int(float('1'+len(str(value_maximum))*'0')/float(self._zoom_scale_y))
            #
            painter._set_histogram_draw_(
                rect,
                value_array=self._value_array,
                value_scale=(value_scale_x, value_scale_y),
                value_offset=(self._grid_value_offset_x, self._grid_value_offset_y),
                label=(self._xValueExplain, self._yValueExplain),
                grid_scale=(1.0, self._zoom_scale_y),
                grid_size=(self._grid_width, self._grid_height),
                grid_offset=(self._grid_offset_x, self._grid_offset_y),
                translate=(self._track_offset_x, 0),
                current_index=self._selectedIndex,
                mode=self._grid_value_show_mode,
            )
        #
        painter._set_grid_axis_draw_(
            rect,
            (self._grid_dir_x, self._grid_dir_y),
            (self._track_offset_x, 0),
            (self._grid_offset_x, self._grid_offset_y),
            (self._grid_axis_lock_x, self._grid_axis_lock_y),
            (self._grid_axis_border_color_x, self._grid_axis_border_color_y)
        )
        painter._set_grid_mark_draw_(
            rect,
            (self._grid_dir_x, self._grid_dir_y),
            (self._grid_width, self._grid_height),
            (self._track_offset_x, 0),
            (self._grid_offset_x, self._grid_offset_y),
            (value_scale_x, value_scale_y),
            (self._grid_value_offset_x, self._grid_value_offset_y),
            self._grid_mark_border_color,
            self._grid_value_show_mode
        )

    #
    def _set_selected_at_(self, index):
        self._selectedIndex = index

    #
    def _gui_build_(self):
        self._value_array = []
        #
        self._xValueExplain = 'X'
        self._yValueExplain = 'Y'
        #
        self._selectedIndex = -1


class QtChartAsSequence(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtNameBaseDef,
    gui_qt_abstracts.AbsQtChartBaseDef,
    gui_qt_abstracts.AbsQtStatusBaseDef,
    #
    gui_qt_abstracts.AbsQtMenuBaseDef,
):
    QT_MENU_CLS = gui_qt_wgt_utility.QtMenu

    def _refresh_chart_data_(self):
        data = self._chart_data
        if data is not None:
            index_array, index_range, name_text = data
            self._chart_index_array = index_array
            self._chart_index_range = min(index_array), max(index_array)
            #
            index_array_0 = range(index_range[0], index_range[1]+1)
            self._chart_index_array = index_array
            index_array_1 = bsc_core.RawListMtd.get_intersection(
                index_array_0, index_array
            )
            self._chart_index_merge_array = bsc_core.RawIntArrayMtd.merge_to(
                index_array_1
            )
            self._chart_index_lost_array = bsc_core.RawListMtd.get_addition(
                index_array_0, index_array_1
            )
            self._chart_index_lost_merge_array = bsc_core.RawIntArrayMtd.merge_to(
                self._chart_index_lost_array
            )
            self._chart_index_check_range = index_range
            self._name_text = '{} [{}-{}]'.format(
                name_text, *self._chart_index_range
            )
            #
            if self._chart_index_lost_array:
                self._status = gui_core.GuiStatus.Error
            else:
                self._status = gui_core.GuiStatus.Completed
            #
            self.setToolTip(
                (
                    'key="{}"\n'
                    'lost={}'
                ).format(
                    name_text,
                    str(self._chart_index_lost_merge_array)
                )
            )
            #
            self.update()

    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtChartAsSequence, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        #
        self.installEventFilter(self)
        #
        self._gui_build_()
        #
        self._init_name_base_def_(self)
        self._init_chart_base_def_(self)
        self._init_status_base_def_(self)
        #
        self._init_menu_base_def_(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                # self._refresh_chart_data_()
                self.update()
            elif event.type() == QtCore.QEvent.Enter:
                self._hover_flag = True
                self.update()
            elif event.type() == QtCore.QEvent.Leave:
                self._hover_flag = False
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    pass
                #
                elif event.button() == QtCore.Qt.RightButton:
                    self._popup_menu_()
                elif event.button() == QtCore.Qt.MidButton:
                    pass
                else:
                    event.ignore()
            elif event.type() == QtCore.QEvent.MouseMove:
                self._hover_point = event.pos()
                self.update()
        return False

    #
    def paintEvent(self, event):
        pos_x, pos_y = 0, 0
        width, height = self.width(), self.height()
        #
        side = 2
        spacing = 4
        name_w = self._name_width
        #
        painter = gui_qt_core.QtPainter(self)
        #
        painter.setFont(gui_qt_core.QtFonts.Default)
        #
        index_minimum, index_maximum = self._chart_index_check_range
        #
        count = index_maximum-index_minimum+1
        #
        if count > 0:
            name_rect = QtCore.QRect(
                pos_x+side, pos_y+side, name_w, height-side*2
            )
            painter._set_font_(gui_qt_core.GuiQtFont.generate(size=10))
            painter._set_border_color_(self._name_color)
            if self._hover_flag is True:
                if name_rect.contains(self._hover_point):
                    painter._set_border_color_(self._hover_name_color)
            #
            text_ = painter.fontMetrics().elidedText(
                self._name_text, QtCore.Qt.ElideLeft, name_rect.width(), QtCore.Qt.TextShowMnemonic
            )
            painter.drawText(
                name_rect,
                QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter,
                text_
            )
            painter._set_border_color_(self._chart_border_color)
            painter._set_background_color_(self._chart_background_color)
            painter._set_background_style_(QtCore.Qt.FDiagPattern)
            #
            x, y = pos_x+name_w+side+spacing, pos_y+side
            sequence_w = width-name_w-spacing-side*2
            sequence_rect = QtCore.QRect(
                x, y, sequence_w, height-side*2
            )
            painter.drawRect(sequence_rect)
            #
            c_h, c_s, c_v = 60, .75, .75
            if isinstance(self._chart_index_merge_array, (tuple, list)):
                d_w = float(sequence_w)/float(count)
                i_s = side+2
                for i_raw in self._chart_index_merge_array:
                    if isinstance(i_raw, (int, float)):
                        i_index = i_raw
                        i_x = x+int((i_index-index_minimum)*d_w)
                        i_y = i_s-1
                        i_w = int(d_w)
                        i_h = height-i_s*2+2
                        #
                        i_percent = float(1)/float(count)
                        #
                        i_rect = QtCore.QRect(i_x, i_y, i_w, i_h)
                        i_c_h = c_h-(1-i_percent)*c_h
                        i_c_r, i_c_g, i_c_b = bsc_core.RawColorMtd.hsv2rgb(i_c_h, c_s, c_v)
                        if self._hover_flag is True:
                            if i_rect.contains(self._hover_point):
                                i_c_r, i_c_g, i_c_b = bsc_core.RawColorMtd.hsv2rgb(i_c_h, c_s*.75, c_v)
                        #
                        painter._set_border_color_(i_c_r, i_c_g, i_c_b, 255)
                        painter._set_background_color_(i_c_r, i_c_g, i_c_b, 255)
                        painter.drawRect(i_rect)
                        #
                        painter._set_font_(gui_qt_core.QtFonts.Default)
                        painter._set_border_color_(self._chart_text_color)
                        painter._set_background_color_(0, 0, 0, 0)
                        i_point = QtCore.QPoint(i_x, i_y+i_h/2+4)
                        painter.drawText(
                            i_point,
                            str(i_raw)
                        )
                    elif isinstance(i_raw, (tuple, list)):
                        i_start_index, i_end_index = i_raw
                        i_x = x+int((i_start_index-index_minimum)*d_w)
                        i_y = i_s-1
                        i_w = int((i_end_index-i_start_index+1)*d_w)
                        i_h = height-i_s*2+2
                        #
                        i_percent = float(i_end_index-i_start_index+1)/float(count)
                        #
                        i_rect = QtCore.QRect(i_x, i_y, i_w, i_h)
                        i_c_h = c_h-(1-i_percent)*c_h
                        if i_percent == 1:
                            i_c_h = 140
                        i_c_r, i_c_g, i_c_b = bsc_core.RawColorMtd.hsv2rgb(i_c_h, c_s, c_v)
                        if self._hover_flag is True:
                            if i_rect.contains(self._hover_point):
                                i_c_r, i_c_g, i_c_b = bsc_core.RawColorMtd.hsv2rgb(i_c_h, c_s*.75, c_v)
                        #
                        painter._set_border_color_(i_c_r, i_c_g, i_c_b, 255)
                        painter._set_background_color_(i_c_r, i_c_g, i_c_b, 255)
                        painter.drawRect(i_rect)
                        #
                        painter._set_font_(gui_qt_core.QtFonts.Default)
                        painter._set_border_color_(self._chart_text_color)
                        painter._set_background_color_(0, 0, 0, 0)
                        i_point = QtCore.QPoint(i_x, i_y+i_h/2+4)
                        painter.drawText(
                            i_point,
                            '{}-{}'.format(i_start_index, i_end_index)
                        )

    #
    def _gui_build_(self):
        self._chart_index_array = []
        self._chart_index_range = 0, 0
        #
        self._chart_index_merge_array = []
        self._chart_index_check_range = 0, 0

    def _get_index_range_(self):
        return self._chart_index_range

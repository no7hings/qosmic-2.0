# coding:utf-8
import math

import lxbasic.core as bsc_core
# gui
from ... import core as gui_core
# qt
from .wrap import *


class GuiQtChartDrawDataForSector(object):
    def __init__(self, data, position, size, align, side_w, mode):
        """
        :param data: [
            (<label>, <total-count>, <occupy-count>),
            ...
        ]
        :param position: (int(x), int(y))
        :param size: (int(w), int(h))
        :param align:
        :param side_w: int(w)
        :param mode: GuiSectorChartMode
        """
        self._draw_data = self._get_data_(
            data, position, size, align, side_w, mode
        )

    @classmethod
    def _get_basic_data_at_(cls, index, datum, offset, radius, tape_w, spacing, mode):
        e_r = 4
        start_angle = 90
        offset_x, offset_y = offset
        explain, value_maximum, value = datum
        percent = float(value)/float(max(value_maximum, 1))
        #
        text = '{} : {}%'.format(explain, bsc_core.RawValueMtd.get_percent_prettify(value=value, maximum=value_maximum))
        #
        color_percent = max(min(percent, 1), .005)
        if value_maximum == 0:
            border_rgba = 95, 95, 95, 255
            background_rgba = 95, 95, 95, 255
        else:
            if percent == 1:
                r, g, b = 63, 255, 127
                if mode is gui_core.GuiSectorChartMode.Error:
                    r, g, b = 255, 0, 63
            elif percent == 0:
                r, g, b = 255, 0, 63
                if mode is gui_core.GuiSectorChartMode.Error:
                    r, g, b = 63, 255, 127
            #
            elif percent > 1:
                r, g, b = bsc_core.RawColorMtd.hsv2rgb(240-min(percent*15, 45), 1, 1)
            else:
                r, g, b = bsc_core.RawColorMtd.hsv2rgb(45*color_percent, 1, 1)
                if mode is gui_core.GuiSectorChartMode.Error:
                    r, g, b = bsc_core.RawColorMtd.hsv2rgb(45-45*color_percent, 1, 1)
            #
            background_rgba = r, g, b, 255
            border_rgba = r, g, b, 255
        #
        draw_percent = color_percent*.75
        #
        out_x, out_y = offset_x+index*tape_w/2, offset_y+index*tape_w/2
        in_x, in_y = out_x+(tape_w-spacing)/2, out_y+(tape_w-spacing)/2
        out_r = radius-index*tape_w
        in_r = out_r-tape_w+spacing
        #
        rim_path = QtGui.QPainterPath()
        rim_path.addEllipse(
            out_x, out_y, out_r, out_r
        )
        rim_path.addEllipse(
            in_x, in_y, in_r, in_r
        )
        #
        cx, cy = out_x+out_r/2, out_y+out_r/2
        #
        rim_sub_path = QtGui.QPainterPath()
        rim_sub_path.moveTo(cx, cy)
        sub_angle = -360*.25
        rim_sub_path.arcTo(out_x-1, out_y-1, out_r+2, out_r+2, start_angle, sub_angle)
        #
        percent_sub_path = QtGui.QPainterPath()
        percent_sub_path.moveTo(cx, cy)
        percent_sub_angle = -360*(1-draw_percent)
        percent_sub_path.arcTo(out_x-1, out_y-1, out_r+2, out_r+2, start_angle, percent_sub_angle)
        #
        total_path = rim_path-rim_sub_path
        occupy_path = rim_path-percent_sub_path
        #
        x1, y1 = cx, out_y+(tape_w-spacing)/4
        x2, y2 = x1+tape_w/4, y1
        x3, y3 = x2+tape_w/4, y2+tape_w/4
        x4, y4 = x3+tape_w/4, y3
        text_line = QtGui.QPolygon(
            [QtCore.QPoint(x1, y1), QtCore.QPoint(x2, y2), QtCore.QPoint(x3, y3), QtCore.QPoint(x4-e_r, y4)]
        )
        text_point = QtCore.QPoint(x4+e_r+4, y4+4)
        text_ellipse = QtCore.QRect(x4-e_r, y4-e_r, e_r*2, e_r*2)
        text_size = tape_w/3
        return (
            background_rgba, border_rgba, total_path, occupy_path, text_point, text_line, text_ellipse, text_size, text
        )

    @classmethod
    def _get_basic_data_(cls, data, offset, radius, tape_w, spacing, mode):
        lis = []
        if data:
            for i_index, i_datum in enumerate(data):
                lis.append(
                    cls._get_basic_data_at_(
                        i_index, i_datum, offset, radius, tape_w, spacing, mode
                    )
                )
        return lis

    @classmethod
    def _get_data_(cls, data, position, size, align, side_w, mode):
        if data:
            count = len(data)
            #
            pos_x, pos_y = position
            size_w, size_h = size
            align_h, align_v = align
            #
            radius = int(min(size_w, size_h))-side_w*2
            tape_w = int(radius/count*.75)
            #
            spacing = 8
            #
            if align_h is QtCore.Qt.AlignLeft:
                offset_x = pos_x+side_w
            elif align_h is QtCore.Qt.AlignHCenter:
                offset_x = pos_x+(size_w-radius)/2
            else:
                offset_x = size_w-radius-side_w
            if align_v is QtCore.Qt.AlignTop:
                offset_y = pos_y+side_w
            elif align_v is QtCore.Qt.AlignVCenter:
                offset_y = pos_y+(size_h-radius)/2
            else:
                offset_y = size_h-radius-side_w
            #
            basic_data = cls._get_basic_data_(
                data, (offset_x, offset_y), radius, tape_w, spacing, mode
            )
            return dict(
                basic=basic_data
            )

    def get(self):
        return self._draw_data


class GuiQtChartDrawDataForProcessing(object):
    @classmethod
    def _get_basic_data_(cls, rect, index, percent, percent_range, label, show_percent, tape_w=8, spacing=8):
        percent_start, percent_end = percent_range
        start_angle = 360*(1-percent_end)
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        radius = int(min(w, h))
        rim_out_x, rim_out_y = x-index*(tape_w+spacing)/2, y-index*(tape_w+spacing)/2
        rim_in_x, rim_in_y = rim_out_x+tape_w/2, rim_out_y+tape_w/2
        #
        rim_out_r = radius+index*(tape_w+spacing)
        rim_in_r = rim_out_r-tape_w
        #
        rim_path = QtGui.QPainterPath()
        rim_path.addEllipse(
            rim_out_x, rim_out_y, rim_out_r, rim_out_r
        )
        rim_path.addEllipse(
            rim_in_x, rim_in_y, rim_in_r, rim_in_r
        )
        #
        cx, cy = rim_out_x+rim_out_r/2, rim_out_y+rim_out_r/2
        rim_sub_path = QtGui.QPainterPath()
        rim_sub_path.moveTo(cx, cy)
        percent_sub_angle = 360*(1-percent)
        rim_sub_path.arcTo(rim_out_x-1, rim_out_y-1, rim_out_r+2, rim_out_r+2, start_angle, percent_sub_angle)

        annulus_sector_path = rim_path-rim_sub_path

        annulus_sector_color = QtGui.QConicalGradient(cx, cy, start_angle)
        c = 10
        colors = []
        for i in range(c):
            i_p = float(i)/float(c)
            i_color = QtGui.QColor(*bsc_core.RawColorMtd.hsv2rgb(140*(1-i_p), .5, 1))
            colors.append(i_color)
            annulus_sector_color.setColorAt(i_p, i_color)

        annulus_sector_color.setColorAt(1, colors[0])
        #
        text_w, text_h = 240, 16
        text_spacing = 2
        #
        t_x, t_y = x+w/2, y+h+index*(text_h+text_spacing)+48
        show_name_rect_f = QtCore.QRectF(
            t_x-text_w-4, t_y, text_w, text_h
        )
        show_name_option = QtGui.QTextOption(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        )
        show_percent_rect_f = QtCore.QRectF(
            t_x+4, t_y, text_w, text_h
        )
        show_percent_option = QtGui.QTextOption(
            QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter
        )
        if label:
            show_name = label
        else:
            show_name = 'process-{}'.format(index)
        #
        text_color = QtGui.QColor(*bsc_core.RawColorMtd.hsv2rgb(140*percent, .5, 1))
        return (
            annulus_sector_path, annulus_sector_color,
            show_name_rect_f, show_name_option, show_name,
            show_percent_rect_f, show_percent_option, show_percent,
            text_color
        )


class GuiQtChartDrawDataForRadar(object):
    fnc_angle = math.radians
    fnc_sin = math.sin
    fnc_cos = math.cos
    fnc_tan = math.tan

    def __init__(self, data, position, size, align, side_w, mode):
        self._draw_data = self._get_data_(
            data, position, size, align, side_w, mode
        )

    # noinspection PyUnusedLocal
    def _get_data_(self, data, position, size, align, side_w, mode):
        if data:
            pos_x, pos_y = position
            size_w, size_h = size
            align_h, align_v = align
            #
            radius = int(min(size_w, size_h))-side_w*2
            #
            spacing = 8
            #
            if align_h is QtCore.Qt.AlignLeft:
                offset_x = pos_x+side_w
            elif align_h is QtCore.Qt.AlignHCenter:
                offset_x = pos_x+(size_w-radius)/2
            else:
                offset_x = size_w-radius-side_w
            if align_v is QtCore.Qt.AlignTop:
                offset_y = pos_y+side_w
            elif align_v is QtCore.Qt.AlignVCenter:
                offset_y = pos_y+(size_h-radius)/2
            else:
                offset_y = size_h-radius-side_w
            #
            mark_data = self._get_mark_data_(
                data,
                (offset_x, offset_y),
                radius,
                spacing
            )
            #
            basic_data = self._get_basic_data_(
                data, (offset_x, offset_y), radius, spacing
            )
            image_data = self._get_image_data_(
                data, (offset_x, offset_y), radius, spacing
            )
            map_data = self._get_map_data_(
                mark_data, (offset_x, offset_y), radius
            )
            return dict(
                image=image_data,
                basic=basic_data,
                map=map_data,
                mark=mark_data
            )

    @classmethod
    def _get_basic_data_points_(cls, cx, cy, radius, count):
        lis = []
        for seq in range(count):
            angle = 360*float(seq)/float(count)+180
            x, y = cx+cls.fnc_sin(cls.fnc_angle(angle))*radius/2, cy+cls.fnc_cos(
                cls.fnc_angle(angle)
            )*radius/2
            lis.append(QtCore.QPoint(x, y))
        #
        return lis+lis[0:1]

    # noinspection PyUnusedLocal
    @classmethod
    def _get_basic_data_(cls, data, offset, radius, spacing):
        offset_x, offset_y = offset
        count = len(data)
        cx, cy = offset_x+radius/2, offset_y+radius/2
        #
        basic_polygons = []
        for i in range(6):
            r = radius*float(i+1)/float(6)
            i_polygon = QtGui.QPolygon(
                cls._get_basic_data_points_(cx, cy, r, count)
            )
            basic_polygons.append(i_polygon)
        #
        basic_polygons.reverse()
        return basic_polygons

    # noinspection PyUnusedLocal
    @classmethod
    def _get_image_data_(cls, data, offset, radius, spacing):
        offset_x, offset_y = offset
        count = len(data)
        cx, cy = offset_x+radius/2, offset_y+radius/2
        #
        image_path = QtGui.QPainterPath()
        image_path.addPolygon(
            QtGui.QPolygonF(cls._get_basic_data_points_(cx, cy, radius, count))
        )
        #
        return image_path

    @classmethod
    def _get_map_data_(cls, mark_data, offset, radius):
        offset_x, offset_y = offset
        start_angle = 90
        cx, cy = offset_x+radius/2, offset_y+radius/2
        #
        points_src = []
        points_tgt = []
        colors = []
        if mark_data:
            for i in mark_data:
                background_rgba, border_rgba, basic_path, text_point, text_point_1, text_0, text_1, \
                    server_map_point, local_map_point, map_ellipse = i
                points_src.append(server_map_point)
                points_tgt.append(local_map_point)
                colors.append(background_rgba)
        #
        g_c = QtGui.QConicalGradient(cx, cy, start_angle)
        for seq, i_rgba in enumerate(colors):
            i_r, i_g, i_b, i_a = i_rgba
            g_c.setColorAt(float(seq)/float(len(colors)), QtGui.QColor(i_r, i_g, i_b, 127))
        #
        r, g, b, a = colors[0]
        g_c.setColorAt(1, QtGui.QColor(r, g, b, 127))
        #
        map_brush = QtGui.QBrush(g_c)
        #
        map_polygon_src = QtGui.QPolygon(points_src)
        map_polygon_tgt = QtGui.QPolygon(points_tgt)
        return map_brush, map_polygon_src, map_polygon_tgt

    # noinspection PyUnusedLocal
    @classmethod
    def _get_mark_data_at_(cls, index, index_maximum, value_maximum, data, offset_x, offset_y, radius, spacing):
        e_r = 4
        start_angle = -90
        explain, value_src, value_tgt = data
        #
        percent_src = float(value_src)/float(max(value_maximum, 1))
        percent_tgt = float(value_tgt)/float(max(value_maximum, 1))
        #
        value_sub = value_tgt-value_src
        percent_sub = float(value_sub)/float(max(value_src, 1))
        text_0 = explain
        if value_sub == 0:
            text_1 = '{}'.format(bsc_core.RawIntegerMtd.get_prettify(value_tgt))
        else:
            text_1 = '{} ( {}% )'.format(
                bsc_core.RawIntegerMtd.get_prettify(value_tgt),
                bsc_core.RawValueMtd.get_percent_prettify(value=value_sub, maximum=value_src)
            )
        #
        if value_maximum == 0:
            border_rgba = 95, 95, 95, 255
            background_rgba = 95, 95, 95, 255
        else:
            if percent_sub == 0:
                r, g, b = 64, 255, 127
            elif percent_sub > 0:
                r, g, b = bsc_core.RawColorMtd.hsv2rgb(45*(1-min(percent_sub, 1)), 1, 1)
            else:
                r, g, b = bsc_core.RawColorMtd.hsv2rgb(120+45*(1-min(percent_sub, 1)), 1, 1)
            #
            background_rgba = r, g, b, 255
            border_rgba = r, g, b, 255
        #
        draw_percent_src = percent_src*.75
        draw_percent_tgt = percent_tgt*.75
        #
        x, y = offset_x, offset_y
        r = radius
        cx, cy = x+r/2, y+r/2
        basic_path = QtGui.QPainterPath()
        basic_path.moveTo(cx, cy)
        angle_start = 360*(float(index)/float(index_maximum))+180
        angle_end = 360*(float(index+1)/float(index_maximum))+180
        basic_path.arcTo(x, y, r, r, angle_start+start_angle, angle_end+start_angle)
        #
        text_x_0, text_y_0 = cx+cls.fnc_sin(cls.fnc_angle(angle_start))*radius/2, cy+cls.fnc_cos(
            cls.fnc_angle(angle_start)
        )*radius/2
        #
        map_x_0, map_y_0 = cx+cls.fnc_sin(
            cls.fnc_angle(angle_start)
        )*radius/2*draw_percent_tgt, cy+cls.fnc_cos(
            cls.fnc_angle(angle_start)
        )*radius/2*draw_percent_tgt
        map_x_1, map_y_1 = cx+cls.fnc_sin(
            cls.fnc_angle(angle_start)
        )*radius/2*draw_percent_src, cy+cls.fnc_cos(
            cls.fnc_angle(angle_start)
        )*radius/2*draw_percent_src
        #
        f = QtGui.QFont()
        f.setPointSize(8)
        m = QtGui.QFontMetrics(f)
        text_w_0 = m.width(explain)
        text_w_1 = m.width(text_1)
        text_h = m.height()
        #
        text_point_0 = QtCore.QPoint(text_x_0-text_w_0/2, text_y_0-text_h/2)
        text_point_1 = QtCore.QPoint(text_x_0-text_w_1/2, text_y_0+text_h/2)
        mark_ellipse = QtCore.QRect(map_x_0-e_r, map_y_0-e_r, e_r*2, e_r*2)
        #
        point_tgt = QtCore.QPoint(map_x_0, map_y_0)
        point_src = QtCore.QPoint(map_x_1, map_y_1)
        return background_rgba, border_rgba, basic_path, text_point_0, \
            text_point_1, text_0, text_1, point_src, point_tgt, mark_ellipse

    @classmethod
    def _get_mark_data_(cls, data, offset, radius, spacing):
        offset_x, offset_y = offset
        lis = []
        if data:
            index_maximum = len(data)
            value_maximum = max([i[2] for i in data])
            for i_index, i_data in enumerate(data):
                lis.append(
                    cls._get_mark_data_at_(
                        i_index,
                        index_maximum,
                        value_maximum,
                        i_data,
                        offset_x, offset_y,
                        radius,
                        spacing
                    )
                )
        return lis

    def get(self):
        return self._draw_data


# noinspection PyUnusedLocal
class GuiQtChartDrawDataForPie(object):
    fnc_angle = math.radians
    fnc_sin = math.sin
    fnc_cos = math.cos
    fnc_tan = math.tan

    def __init__(self, data, position, size, align, side_w, mode):
        self._draw_data = self._get_data_(
            data, position, size, align, side_w, mode
        )

    def _get_data_(self, data, position, size, align, side_w, mode):
        if data:
            basic_data = self._get_basic_data_(data, position, size, side_w)
            return basic_data
        return

    @classmethod
    def _get_basic_data_(cls, data, position, size, side):
        def rcs_fnc_(i_data_, i_seq_=0, qa=90, ma=0):
            _i_name, _i_value, color = i_data_[i_seq_]
            _i_color = bsc_core.RawTextOpt(_i_name).to_rgb()
            #
            p = float(_i_value)/float(maximum)
            _a = 360*p
            a = 360-_a
            s = ma+_a/2
            _xo = cls.fnc_sin(cls.fnc_angle(s))*(side/4)
            _yo = cls.fnc_cos(cls.fnc_angle(s))*(side/4)
            #
            pie_path = QtGui.QPainterPath()
            _s = 4
            cx = w1/2+_s/2+x1
            cy = w1/2+_s/2+y1
            pie_path.moveTo(cx, cy)
            pie_path.arcTo(x1-_s/2, y1-_s/2, w1+_s, w1+_s, qa, a)
            #
            _i_path = rim_path-pie_path
            _i_shadow_path = rim_path-pie_path
            #
            _i_percent = '{}%'.format(
                bsc_core.RawValueMtd.get_percent_prettify(value=_i_value, maximum=maximum)
            )
            #
            lis.append(
                (_i_color, _i_name, _i_value, _i_percent, _i_path, _i_shadow_path, (_xo, -_yo), False)
            )
            #
            i_seq_ += 1
            qa += a
            ma += _a
            if i_seq_ <= data_count-1:
                rcs_fnc_(i_data_, i_seq_, qa, ma)

        #
        pos_x, pos_y = position
        width, height = size
        lis = []
        if data:
            data_count = len(data)
            maximum = sum([i[1] for i in data])
            if maximum > 0:
                radius = min(width, height)
                w = radius-side*2
                x = side
                y = side
                #
                x1 = x
                y1 = y
                w1 = w
                rim_path = QtGui.QPainterPath()
                rim_path.addEllipse(x1, y1, w1, w1)
                #
                w2 = w1/2
                x2 = (w1-w2)/2+x1
                y2 = (w1-w2)/2+y1
                rim_path.addEllipse(x2, y2, w2, w2)
                #
                rcs_fnc_(data)
        return lis

    def get(self):
        return self._draw_data


# noinspection PyNoneFunctionAssignment,PyUnusedLocal
class GuiQtChartDrawDataForHistogram(object):
    def __init__(self, data, position, size, align, side_w, mode):
        self._draw_data = self._get_data_(
            data, position, size, align, side_w, mode
        )

    def _get_data_(self, data, position, size, align, side_w, mode):
        if data:
            basic_data = self._get_basic_data_(data, position, size, side_w)
            return basic_data
        return

    @classmethod
    def _get_basic_data_(cls, data, position, size, side):
        pass

    def get(self):
        return self._draw_data

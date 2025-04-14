# coding:utf-8
import time

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

from .wrap import *

from ... import core as _gui_core

from . import base as _base


class QtItemDrawBase:
    Status = _gui_core.GuiProcessStatus

    Rgba = _gui_core.GuiRgba

    @classmethod
    def _gen_rgba_args(cls, r, g, b, a):
        h, s, v = bsc_core.BscColor.rgb_to_hsv(r, g, b)
        r_, g_, b_ = bsc_core.BscColor.hsv2rgb(h, s*1.25, v*1.25)
        return QtGui.QColor(r, g, b, a), QtGui.QColor(r_, g_, b_, a)

    @classmethod
    def _gen_rgba_args_by_status(cls, status):
        if status in {cls.Status.Started}:
            return cls._gen_rgba_args(*cls.Rgba.DarkAzureBlue)
        elif status in {cls.Status.Running}:
            return cls._gen_rgba_args(*cls.Rgba.LightAzureBlue)
        elif status in {cls.Status.Waiting}:
            return cls._gen_rgba_args(*cls.Rgba.Orange)
        elif status in {cls.Status.Suspended}:
            return cls._gen_rgba_args(*cls.Rgba.LemonYellow)
        elif status in {cls.Status.Failed, cls.Status.Error}:
            return cls._gen_rgba_args(*cls.Rgba.LightRed)
        elif status in {cls.Status.Killed}:
            return cls._gen_rgba_args(*cls.Rgba.Pink)
        elif status in {cls.Status.Completed}:
            return cls._gen_rgba_args(*cls.Rgba.LightNeonGreen)
        elif status in {cls.Status.All}:
            return cls._gen_rgba_args(*cls.Rgba.DarkWhite)
        return cls._gen_rgba_args(*cls.Rgba.Transparent)

    @classmethod
    def _draw_svg(cls, painter, rect, svg_path):
        svg_render = QtSvg.QSvgRenderer(svg_path)
        svg_render.render(painter, QtCore.QRectF(rect))

    @classmethod
    def _draw_image_file(cls, painter, rect, file_path):
        pixmap = QtGui.QPixmap()
        pixmap.load(file_path)
        if pixmap.isNull() is False:
            pxm_scaled = pixmap.scaled(
                rect.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            )
            painter.drawPixmap(rect, pxm_scaled)

    @classmethod
    def _draw_pixmap(cls, painter, rect, pixmap):
        pxm_scaled = pixmap.scaled(
            rect.size(),
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        painter.drawPixmap(rect, pxm_scaled)

    @classmethod
    def _draw_icon_by_file(cls, painter, rect, file_path):
        if file_path is None:
            return
        if file_path.endswith('.svg'):
            cls._draw_svg(painter, rect, file_path)
        else:
            cls._draw_image_file(painter, rect, file_path)
    
    @classmethod
    def _draw_image(cls, painter, rect, image):
        pixmap = QtGui.QPixmap.fromImage(image, QtCore.Qt.AutoColor)
        pxm_scaled = pixmap.scaled(
            rect.size(),
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        painter.drawPixmap(rect, pxm_scaled)

    @classmethod
    def _draw_icon_by_text(cls, painter, rect, text):
        w, h = rect.width(), rect.height()
        if text:
            text = bsc_core.ensure_unicode(text)
            txt_draw = text[0].capitalize()
            txt_r = min(w, h)*.75
            r, g, b = bsc_core.BscTextOpt(text or '').to_hash_rgb(s_p=(35, 50), v_p=(65, 85))
        else:
            txt_draw = 'N/a'
            txt_r = min(w, h)*.5
            r, g, b = 71, 71, 71

        background_rgba, text_rgba = _base.QtColor.generate_color_args_by_rgb(r, g, b)

        cls._draw_frame(
            painter, rect,
            border_color=QtGui.QColor(95, 95, 95),
            background_color=QtGui.QColor(*background_rgba)
        )
        painter.setPen(QtGui.QColor(*text_rgba))
        painter.setFont(_base.QtFont.generate_2(txt_r))
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, txt_draw)

    @classmethod
    def _draw_name_text(cls, painter, rect, text, text_color, text_option=None, text_font=None):
        painter.setPen(text_color)

        if text_font:
            painter.setFont(text_font)

        text = painter.fontMetrics().elidedText(
            text,
            QtCore.Qt.ElideMiddle,
            rect.width(),
            QtCore.Qt.TextShowMnemonic
        )

        text_option = text_option or QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        painter.drawText(rect, text_option, text)

    @classmethod
    def _draw_description_text(cls, painter, rect, text, text_color, text_font=None):
        text_option = QtGui.QTextOption()
        painter.setPen(text_color)
        if text_font:
            painter.setFont(text_font)

        text_option.setWrapMode(
            text_option.WrapAnywhere
        )
        rect = QtCore.QRectF(
            rect
        )
        painter.drawText(rect, text, text_option)

    @classmethod
    def _draw_frame(cls, painter, rect, border_color, background_color, border_width=1, border_radius=0):
        if border_radius > 0:
            painter.setPen(QtGui.QPen(border_color, border_width))
            painter.setBrush(background_color)
            painter.setRenderHint(painter.Antialiasing, True)
            painter.drawRoundedRect(
                rect, border_radius, border_radius, QtCore.Qt.AbsoluteSize
            )
            painter.setRenderHint(painter.Antialiasing, False)
        else:
            pen = QtGui.QPen(border_color, border_width)
            pen.setCapStyle(QtCore.Qt.SquareCap)
            pen.setJoinStyle(QtCore.Qt.MiterJoin)
            painter.setPen(pen)
            painter.setBrush(background_color)
            painter.drawRect(rect)

    @classmethod
    def _draw_line(cls, painter, point_0, point_1, border_color, border_width=1):
        painter.setPen(QtGui.QPen(border_color, border_width))
        painter.drawLine(point_0, point_1)

    @classmethod
    def _gen_alternating_color(cls, rect, colors, width, time_offset=0, running=False, x_offset=0, y_offset=0):
        if running is True:
            x_o = (time_offset % (width*2))
        else:
            x_o = x_offset

        x, y = rect.x(), rect.y()
        gradient_color = QtGui.QLinearGradient(
            QtCore.QPoint(x+x_o, y+y_offset), QtCore.QPoint(x+width+x_o, y+width+y_offset)
        )
        gradient_color.setSpread(gradient_color.RepeatSpread)
        c = len(colors)
        p = 1/float(c)
        for seq, i_color in enumerate(colors):
            _ = float(seq)/float(c)
            i_index = max(min(_, 1), 0)
            gradient_color.setColorAt(i_index, i_color)
            gradient_color.setColorAt(i_index+p*.9, i_color)
        return gradient_color

    @classmethod
    def _draw_alternating_frame(
        cls,
        painter, rect, colors, border_radius=0, running=False, x_offset=0, y_offset=0
    ):
        assert isinstance(painter, QtGui.QPainter)

        painter.setRenderHint(painter.Antialiasing, True)
        # self._set_border_color_(colors[0])
        painter.setPen(QtGui.QColor(0, 0, 0, 0))
        background_color = cls._gen_alternating_color(
            rect, colors, 20, int(time.time()*10),
            running=running, x_offset=x_offset, y_offset=y_offset
        )
        #
        painter.setBrush(background_color)
        if border_radius > 0:
            painter.setRenderHint(painter.Antialiasing, True)
            painter.drawRoundedRect(
                rect,
                border_radius, border_radius,
                QtCore.Qt.AbsoluteSize
            )
            painter.setRenderHint(painter.Antialiasing, False)
        elif border_radius == -1:
            border_radius = rect.height()/2
            painter.setRenderHint(painter.Antialiasing, True)
            painter.drawRoundedRect(
                rect,
                border_radius, border_radius,
                QtCore.Qt.AbsoluteSize
            )
            painter.setRenderHint(painter.Antialiasing, False)
        else:
            painter.drawRect(rect)

        painter.setRenderHint(painter.Antialiasing, True)

    @classmethod
    def _draw_color_frame(cls, painter, rect, border_color, background_color):
        painter.setPen(
            QtGui.QColor(*_gui_core.GuiRgba.Gray)
        )
        painter.setBrush(background_color)
        painter.drawRect(
            rect
        )

    @classmethod
    def _draw_icon_by_pixmap(cls, painter, rect, pixmap):
        pxm_scaled = pixmap.scaled(
            rect.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
        painter.drawPixmap(rect, pxm_scaled)

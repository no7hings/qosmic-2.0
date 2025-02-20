# coding:utf-8
import contextlib

import six

import sys

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.pinyin as bsc_pinyin
# gui
from ... import core as gui_core
# qt
from .wrap import *

from . import style as _style


class QtUtil(object):
    WINDOW_KEY = 'QSM_WINDOW_FLAG'

    @classmethod
    def add_qt_fonts(cls, fonts):
        for i_font in fonts:
            # noinspection PyArgumentList
            QtGui.QFontDatabase.addApplicationFont(
                i_font
            )

    @classmethod
    def generate_qt_palette(cls, tool_tip=False):
        palette = QtGui.QPalette()
        palette.setColor(palette.All, palette.Shadow, _style.QtRgba.LightBlack)
        palette.setColor(palette.All, palette.Dark, _style.QtRgba.Dim)
        palette.setColor(palette.All, palette.Background, _style.QtRgba.Basic)
        palette.setColor(palette.All, palette.NoRole, _style.QtRgba.Dark)
        palette.setColor(palette.All, palette.Base, _style.QtRgba.Dark)
        palette.setColor(palette.All, palette.Light, _style.QtRgba.FadeBasic)
        palette.setColor(palette.All, palette.Highlight, QtGui.QColor(255, 255, 255, 0))
        palette.setColor(palette.All, palette.Button, _style.QtRgba.BkgButton)
        #
        palette.setColor(palette.All, palette.Window, _style.QtRgba.Basic)
        #
        palette.setColor(palette.All, palette.Text, _style.QtRgba.Text)
        palette.setColor(palette.All, palette.BrightText, _style.QtRgba.TextHover)
        palette.setColor(palette.All, palette.WindowText, _style.QtRgba.Text)
        palette.setColor(palette.All, palette.ButtonText, _style.QtRgba.Text)
        palette.setColor(palette.All, palette.HighlightedText, _style.QtRgba.TextHover)
        #
        palette.setColor(palette.All, palette.AlternateBase, _style.QtRgba.Dark)
        # tool-tip
        if tool_tip is True:
            # noinspection PyArgumentList
            p = QtWidgets.QToolTip.palette()
            p.setColor(palette.All, p.ToolTipBase, _style.QtRgba.BkgToolTip)
            p.setColor(palette.All, palette.ToolTipText, _style.QtRgba.TxtToolTip)
            # noinspection PyArgumentList
            QtWidgets.QToolTip.setPalette(p)
            # noinspection PyArgumentList
            QtWidgets.QToolTip.setFont(QtFont.generate(size=8))
        #
        return palette

    @classmethod
    def set_text_to_clipboard(cls, text):
        # noinspection PyArgumentList
        QtWidgets.QApplication.clipboard().setText(text)

    @staticmethod
    def find_all_qt_widgets_by_class(widget_class):
        list_ = []
        # noinspection PyArgumentList
        qt_widgets = QtWidgets.QApplication.topLevelWidgets()
        if qt_widgets:
            for i_qt_widget in qt_widgets:
                if widget_class.__name__ == i_qt_widget.__class__.__name__:
                    list_.append(i_qt_widget)
        return list_

    @classmethod
    def find_all_valid_qt_windows(cls):
        list_ = []
        # noinspection PyArgumentList
        qt_widgets = QtWidgets.QApplication.topLevelWidgets()
        for i in qt_widgets:
            if hasattr(i, cls.WINDOW_KEY):
                list_.append(i)
        return list_

    @classmethod
    def find_all_valid_and_visible_qt_windows(cls):
        list_ = []
        # noinspection PyArgumentList
        qt_widgets = QtWidgets.QApplication.topLevelWidgets()
        for i in qt_widgets:
            if hasattr(i, cls.WINDOW_KEY):
                if i.isHidden() is False:
                    list_.append(i)
        return list_

    @classmethod
    def find_valid_and_active_qt_window(cls):
        for i in cls.find_all_valid_qt_windows():
            if i.isActiveWindow() is True:
                return i

    @staticmethod
    def get_qt_widget_is_deleted(qt_widget):
        # noinspection PyUnresolvedReferences
        import shiboken2
        return shiboken2.isValid(qt_widget)

    @staticmethod
    def get_qt_active_window():
        # noinspection PyArgumentList
        return QtWidgets.QApplication.activeWindow()

    @staticmethod
    def get_qt_desktop(*args):
        # noinspection PyArgumentList
        return QtWidgets.QApplication.desktop(*args)

    @staticmethod
    def get_qt_desktop_rect(*args):
        # noinspection PyArgumentList
        desktop = QtWidgets.QApplication.desktop(*args)
        return desktop.rect()

    @staticmethod
    def get_qt_desktop_primary_rect(*args):
        # noinspection PyArgumentList
        desktop = QtWidgets.QApplication.desktop(*args)
        return desktop.availableGeometry(desktop.primaryScreen())

    @staticmethod
    def get_qt_desktop_current_rect(*args):
        desktop = QtWidgets.QApplication.desktop(*args)
        # noinspection PyArgumentList
        return desktop.availableGeometry(QtGui.QCursor.pos())

    @staticmethod
    def get_qt_cursor_point():
        # noinspection PyArgumentList
        return QtGui.QCursor.pos()

    @staticmethod
    def assign_qt_shadow(qt_widget, radius):
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(radius)
        shadow.setColor(_style.QtRgba.LightBlack)
        shadow.setOffset(2, 2)
        qt_widget.setGraphicsEffect(shadow)

    @staticmethod
    def write_clipboard(text):
        # noinspection PyArgumentList
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(text)

    @staticmethod
    def read_clipboard():
        # noinspection PyArgumentList
        return QtWidgets.QApplication.clipboard().text()
    
    @staticmethod
    def clear_clipboard():
        # noinspection PyArgumentList
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.clear()

    @staticmethod
    def show_qt_window(widget, pos=None, size=None, use_exec=False):
        if size is not None:
            w_0, h_0 = size
        else:
            q_size = widget.baseSize()
            w_0, h_0 = q_size.width(), q_size.height()

        q_margin = widget.contentsMargins()
        wl, wt, wr, wb = q_margin.left(), q_margin.top(), q_margin.right(), q_margin.bottom()
        vl, vt, vr, vb = 0, 0, 0, 0
        w_1, h_1 = w_0 + sum([wl, vl, wr, vr]), h_0 + sum([wt, vt, wb, vb])

        prt = widget.parent()
        if prt:
            w_p, w_h = prt.width(), prt.height()
            x_p, y_p = prt.pos().x(), prt.pos().y()
        else:
            desktop_rect = QtUtil.get_qt_desktop_current_rect()
            w_p, w_h = desktop_rect.width(), desktop_rect.height()
            x_p, y_p = desktop_rect.x(), desktop_rect.y()

        if hasattr(widget, '_main_window_geometry'):
            if widget._main_window_geometry is not None:
                x_p, y_p, w_p, w_h = widget._main_window_geometry

        if pos is not None:
            x, y = pos[0] + x_p, pos[1] + y_p
        else:
            x, y = (w_p - w_1)/2 + x_p, (w_h - h_1)/2 + y_p
        #
        widget.setGeometry(
            int(max(x, 0)), int(max(y, 0)), int(w_1), int(h_1)
        )
        if use_exec is True:
            widget.exec_()
        else:
            widget.show()
            widget.raise_()

    @staticmethod
    def get_exists_app():
        # noinspection PyArgumentList
        return QtWidgets.QApplication.instance()

    @classmethod
    def create_app(cls):
        # surface_format = QtGui.QSurfaceFormat()
        # surface_format.setRenderableType(surface_format.OpenGL)
        # surface_format.setProfile(surface_format.CoreProfile)
        # surface_format.setVersion(3, 3)
        # surface_format.setSwapBehavior(surface_format.DoubleBuffer)

        app = QtWidgets.QApplication(sys.argv)
        # app.setAttribute(QtCore.Qt.AA_UseOpenGLES)
        # app.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
        app.setPalette(cls.generate_qt_palette(tool_tip=True))
        cls.add_qt_fonts(gui_core.GuiFont.get_all())
        app.setFont(QtFont.generate())
        return app

    @classmethod
    def generate_tool_tip_action_css(cls, text):
        text = text.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')
        for i_keys, i_icon_name in [
            (['"LMB-click"', '"LMB-dbl-click"'], 'mouse/LMB-click'),
            (['"LMB-move"'], 'mouse/LMB-click'),
            (['"RMB-click"'], 'mouse/RMB-click'),
            (['"MMB-wheel"'], 'mouse/MMB-wheel')
        ]:
            for j_key in i_keys:
                text = text.replace(
                    j_key,
                    '<img src="{}">\n{}'.format(
                        gui_core.GuiIcon.get(i_icon_name),
                        j_key
                    )
                )
        return text

    @classmethod
    def generate_tool_tip_css(cls, title, content=None, **kwargs):
        css = (
            '<html>\n'
            '<body>\n'
            '<style>.no_wrap{white-space:nowrap;}</style>\n'
            '<style>.no_warp_and_center{white-space:nowrap;text-align: center;}</style>\n'
        )
        title = bsc_core.ensure_string(title)
        title = title.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')
        css += '<h3><p class="no_warp_and_center">{}</p></h3>\n'.format(title)

        if content:
            # add split line
            css += '<p><hr></p>\n'
            text = bsc_core.ensure_string(content)
            if isinstance(text, six.string_types):
                texts = text.split('\n')
            elif isinstance(text, (tuple, list)):
                texts = text
            else:
                raise RuntimeError()
            #
            for i_text in texts:
                i_text = bsc_core.ensure_string(i_text)
                i_text = i_text.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')
                i_text = cls.generate_tool_tip_action_css(i_text)
                css += '<p class="no_wrap">{}</p>\n'.format(i_text)

        if 'action_tip' in kwargs:
            action_tip = kwargs['action_tip']
            if isinstance(action_tip, six.string_types):
                texts = action_tip.split('\n')
            elif isinstance(action_tip, (tuple, list)):
                texts = action_tip
            else:
                raise RuntimeError()
            css += '<p><hr></p>\n'
            for i_text in texts:
                i_text = bsc_core.ensure_string(i_text)
                i_text = i_text.replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;')
                i_text = cls.generate_tool_tip_action_css(i_text)
                css += '<p class="no_wrap">{}</p>\n'.format(i_text)

        css += '</body>\n</html>'
        return css

    # noinspection PyArgumentList
    @classmethod
    @contextlib.contextmanager
    def gui_bustling(cls):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)
        yield
        # noinspection PyArgumentList
        QtWidgets.QApplication.restoreOverrideCursor()

    @classmethod
    def is_ctrl_modifier(cls):
        # noinspection PyArgumentList
        return QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier
    
    @classmethod
    def save_qt_image(cls, qt_image, file_path):
        import numpy as np

        import cv2

        ptr = qt_image.bits()
        # PyQt
        if QT_LOAD_INDEX == 0:
            ptr.setsize(qt_image.byteCount())

        width = qt_image.width()
        height = qt_image.height()
        # noinspection PyArgumentList
        img_arr = np.array(ptr).reshape(height, width, 4)
        img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGRA2BGR)

        file_path = bsc_core.ensure_unicode(file_path)
        file_path = file_path.encode('mbcs')
        cv2.imwrite(file_path, img_arr)


class QtPixmapCache(object):
    @classmethod
    def get_cached_svg_pixmap(cls, svg_path, size):
        cache_key = "{}_{}x{}".format(svg_path, size.width(), size.height())
        cached_pixmap = QtGui.QPixmapCache.find(cache_key)

        if cached_pixmap is not None:
            return cached_pixmap

        svg_renderer = QtSvg.QSvgRenderer(svg_path)
        pixmap = QtGui.QPixmap(size)
        pixmap.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()

        QtGui.QPixmapCache.insert(cache_key, pixmap)

        return pixmap


class QtIcon(object):
    @classmethod
    def generate_by_icon_name(cls, icon_name):
        icon = QtGui.QIcon()
        file_path = gui_core.GuiIcon.get(icon_name)
        if file_path:
            icon.addPixmap(
                QtGui.QPixmap(file_path),
                QtGui.QIcon.Normal,
                QtGui.QIcon.On
            )
        return icon

    @classmethod
    def generate_by_name(cls, icon_name):
        # noinspection PyArgumentList
        if QtWidgets.QApplication.instance() is not None:
            return cls.generate_by_icon_name(icon_name)

    @classmethod
    def generate_by_rgb(cls, rgb):
        icon = QtGui.QIcon()
        f_w, f_h = 13, 13
        c_w, c_h = 12, 12
        pixmap = QtGui.QPixmap(f_w, f_h)
        painter = QtGui.QPainter(pixmap)
        rect = pixmap.rect()
        pixmap.fill(
            QtCore.Qt.white
        )
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        icon_rect = qt_rect(
            x + (w - c_w) / 2, y + (h - c_h) / 2,
            c_w, c_h
        )
        r, g, b = rgb
        painter.setPen(QtGui.QColor(_style.QtRgba.BdrIcon))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(r, g, b, 255)))
        #
        painter.drawRect(icon_rect)
        painter.end()
        # painter.device()
        icon.addPixmap(
            pixmap,
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        return icon

    @classmethod
    def generate_by_text(cls, text, background_color=None):
        icon = QtGui.QIcon()
        f_w, f_h = 16, 16
        c_w, c_h = 14, 14
        pixmap = QtGui.QPixmap(f_w, f_h)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(painter.Antialiasing)
        rect = pixmap.rect()
        pixmap.fill(
            _style.QtRgba.BdrIcon
        )
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        rd = min(w, h)
        icon_rect = qt_rect(
            x + (w - c_w) / 2, y + (h - c_h) / 2,
            c_w, c_h
        )
        if text is not None:
            words = bsc_pinyin.Text.split_any_to_words(text)
            if words:
                name = words[0]
            else:
                name = '?'

            painter.setPen(_style.QtRgba.BdrIcon)
            if background_color is not None:
                r, g, b = background_color
            else:
                r, g, b = bsc_core.BscTextOpt(name).to_rgb()

            background_color_, text_color_ = QtColor.generate_color_args_by_rgb(r, g, b)
            #
            painter.setPen(_style.QtRgba.BdrIcon)
            painter.setBrush(QtGui.QBrush(QtGui.QColor(*background_color_)))
            painter.drawRoundedRect(icon_rect, 2, 2, QtCore.Qt.AbsoluteSize)
            painter.setPen(QtGui.QColor(*text_color_))
            painter.setFont(QtFont.generate(size=int(rd * .675), italic=True))
            painter.drawText(
                rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                str(bsc_core.BscText.get_first_word(name)).capitalize()
            )
        #
        painter.end()
        # painter.device()
        icon.addPixmap(
            pixmap,
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        return icon


class QtColor(object):
    COLOR_CACHE = dict()

    @classmethod
    def to_qt_color(cls, *args):
        if len(args) == 1:
            _ = args[0]
            if isinstance(_, (QtGui.QColor, QtGui.QLinearGradient, QtGui.QConicalGradient)):
                return _
            elif isinstance(_, (tuple, list)):
                return cls.to_qt_color_fnc(*_)
            raise TypeError()
        return cls.to_qt_color_fnc(*args)

    @classmethod
    def to_qt_color_fnc(cls, *args):
        def fnc_():
            if len(args) == 3:
                r, g, b = args
                a = 255
                return (r, g, b, a), QtGui.QColor(r, g, b, a)
            elif len(args) == 4:
                return args, QtGui.QColor(*args)
            raise TypeError()

        if args in cls.COLOR_CACHE:
            return cls.COLOR_CACHE[args]

        key, clr = fnc_()
        cls.COLOR_CACHE[key] = clr
        return clr

    @classmethod
    def to_rgb(cls, *args):
        if len(args) == 1:
            _ = args[0]
            if isinstance(_, QtGui.QColor):
                return _.red(), _.green(), _.blue()
            elif isinstance(_, (tuple, list)):
                return cls.to_rgb_fnc(*_)
            return 0, 0, 0
        return cls.to_rgb_fnc(*args)

    @classmethod
    def to_rgb_fnc(cls, *args):
        if len(args) == 3:
            r, g, b = args
        elif len(args) == 4:
            r, g, b, a = args
        else:
            raise TypeError()
        return r, g, b

    @classmethod
    def to_rgba(cls, *args):
        if len(args) == 1:
            _ = args[0]
            if isinstance(_, QtGui.QColor):
                return _.red(), _.green(), _.blue(), _.alpha()
            elif isinstance(_, (tuple, list)):
                return cls.to_rgba_fnc(*_)
            return 0, 0, 0, 0
        return cls.to_rgba_fnc(*args)

    @classmethod
    def to_rgba_fnc(cls, *args):
        if len(args) == 3:
            r, g, b = args
            a = 255
        elif len(args) == 4:
            r, g, b, a = args
        else:
            raise TypeError()
        return r, g, b, a

    @classmethod
    def generate_color_args_by_text(cls, text):
        return cls.generate_color_args_by_rgb(
            *bsc_core.BscTextOpt(text).to_hash_rgb(s_p=(35, 50), v_p=(65, 85))
        )

    @classmethod
    def generate_color_args_by_rgb(cls, *args):
        if len(args) == 3:
            b_r, b_g, b_b = args
            b_a = 255
        elif len(args) == 4:
            b_r, b_g, b_b, b_a = args
        else:
            raise TypeError()

        t_r, t_g, t_b = bsc_core.BscColor.get_complementary_rgb(b_r, b_g, b_b)
        b_l = QtGui.qGray(t_r, t_g, t_b)
        if b_l >= 127:
            t_l = 239
        else:
            t_l = 15
        return (b_r, b_g, b_b, b_a), (t_l, t_l, t_l, 255)


class QtFont(object):
    @classmethod
    def generate(cls, size=None, weight=None, italic=False, underline=False, strike_out=False, family='Arial'):
        f = QtGui.QFont()
        f.setPointSize(size or gui_core.GuiSize.FontSizeDefault)
        f.setFamily(family)
        f.setWeight(weight or gui_core.GuiSize.FontWeightDefault)
        f.setItalic(italic)
        f.setUnderline(underline)
        f.setWordSpacing(1)
        f.setStrikeOut(strike_out)
        return f

    @classmethod
    def generate_2(cls, size=None, weight=None, italic=False, underline=False, strike_out=False, family='Arial'):
        f = QtGui.QFont()
        f.setPixelSize(int(size) or gui_core.GuiSize.FontSizeDefault)
        f.setFamily(family)
        f.setWeight(weight or gui_core.GuiSize.FontWeightDefault)
        f.setItalic(italic)
        f.setUnderline(underline)
        f.setWordSpacing(1)
        f.setStrikeOut(strike_out)
        return f

    @classmethod
    def compute_size(cls, size, text, w_adjust=True):
        f = QtFont.generate()
        f.setPointSize(size)
        m = QtGui.QFontMetrics(f)
        w = m.width(text) + size if w_adjust is True else 0
        h = m.height()
        return w, h

    @classmethod
    def compute_size_2(cls, size, text, w_adjust=True):
        f = QtFont.generate()
        f.setPixelSize(int(size))
        m = QtGui.QFontMetrics(f)
        w = m.width(text) + size if w_adjust is True else 0
        h = m.height()
        return w, h


class QtPixmap(object):
    @classmethod
    def _to_gray_(cls, pixmap):
        w, h = pixmap.width(), pixmap.height()
        image_gray = QtGui.QImage(w, h, QtGui.QImage.Format_RGB32)
        image = pixmap.toImage()
        image_alpha = image.alphaChannel()
        for i_x in range(w):
            for i_y in range(h):
                i_p = image.pixel(i_x, i_y)
                # noinspection PyArgumentList
                i_a = QtGui.qGray(i_p)
                i_g_c = QtGui.QColor(i_a, i_a, i_a)
                image_gray.setPixel(i_x, i_y, i_g_c.rgb())
        #
        image_gray.setAlphaChannel(image_alpha)
        return pixmap.fromImage(image_gray)

    @classmethod
    def to_gray(cls, pixmap):
        w, h = pixmap.width(), pixmap.height()

        pxm_new = QtGui.QPixmap(w, h)
        painter = QtGui.QPainter(pxm_new)
        pxm_new.fill(QtCore.Qt.black)
        painter.drawPixmap(
            qt_rect(0, 0, w, h), pixmap
        )
        painter.end()

        img_gray = QtGui.QImage(w, h, QtGui.QImage.Format_RGB32)
        img_new = pxm_new.toImage()
        for i_x in range(w):
            for i_y in range(h):
                i_p = img_new.pixel(i_x, i_y)
                # noinspection PyArgumentList
                i_a = QtGui.qGray(i_p)
                i_g_c = QtGui.QColor(i_a, i_a, i_a)
                img_gray.setPixel(i_x, i_y, i_g_c.rgb())

        pxm_gray = pxm_new.fromImage(img_gray)
        pxm_mask = QtGui.QPixmap(pxm_new).createMaskFromColor(QtCore.Qt.black)
        pxm_gray.setMask(pxm_mask)
        return pxm_gray

    @classmethod
    def _to_hovered_(cls, pixmap):
        pass

    # noinspection PyUnusedLocal
    @classmethod
    def get_by_name(cls, text, size=(20, 20), icon_percent=.75, rounded=False, background_color=None):
        x, y = 0, 0
        w, h = size
        pixmap = QtGui.QPixmap(w, h)
        painter = QtGui.QPainter(pixmap)
        rect = pixmap.rect()
        pixmap.fill(
            _style.QtRgba.BdrIcon
        )
        rd = min(w, h)
        icon_rect = qt_rect(
            x, y, w - 1, h - 1
        )
        if text is not None:
            name = text.split('/')[-1] or ' '

            painter.setPen(_style.QtRgba.BdrIcon)
            r, g, b = bsc_core.BscTextOpt(name).to_rgb_0(s_p=50, v_p=50)
            if background_color is not None:
                r, g, b = background_color
            painter.setBrush(QtGui.QBrush(QtGui.QColor(r, g, b, 255)))
            if rounded is True:
                painter.drawRoundedRect(icon_rect, w / 2, h / 2, QtCore.Qt.AbsoluteSize)
            else:
                painter.drawRect(icon_rect)
            #
            painter.setPen(_style.QtRgba.Text)
            painter.setFont(QtFont.generate(size=int(rd * .6), italic=True))
            painter.drawText(
                rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                str(name[0]).capitalize()
            )
        #
        painter.end()
        return pixmap

    # noinspection PyUnusedLocal
    @classmethod
    def get_by_file(cls, file_path, size=(20, 20), icon_percent=.75):
        pixmap = QtGui.QPixmap(file_path)
        new_pixmap = pixmap.scaled(
            QtCore.QSize(*size),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        return new_pixmap

    @classmethod
    def get_by_file_ext(cls, ext, size=(20, 20), icon_percent=.75, gray=False):
        _ = gui_core.GuiIcon.get('file/{}'.format(ext[1:]))
        if _ is not None:
            pixmap = cls.get_by_file(
                file_path=_,
                size=size,
                icon_percent=icon_percent
            )
            if gray is True:
                return cls.to_gray(pixmap)
            return pixmap
        return cls.get_by_name(
            text=ext[1:],
            size=size
        )

    @classmethod
    def get_by_file_ext_with_tag(cls, ext, tag, frame_size=(20, 20), icon_percent=.75, gray=False):
        x, y = 0, 0
        frm_w, frm_h = frame_size
        icn_w, icn_h = frm_w * icon_percent, frm_h * icon_percent
        base_pixmap = cls.get_by_file_ext(
            ext=ext,
            size=(icn_w, icn_h),
            icon_percent=icon_percent,
            gray=gray
        )
        base_rect = qt_rect(
            x, y, icn_w, icn_h
        )

        pixmap = QtGui.QPixmap(frm_w, frm_h)
        rect = pixmap.rect()
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(painter.Antialiasing)
        painter.fillRect(
            rect, _style.QtRgba.FadeBasic
        )
        painter.drawPixmap(
            base_rect, base_pixmap
        )
        w, h = rect.width(), rect.height()
        rd = min(w, h)
        txt_w, txt_h = rd / 2, rd / 2
        tag_rect = qt_rect(
            x + w - txt_w - 2, y + h - txt_h - 2, txt_w, txt_h
        )
        background_color_, text_color_ = QtColor.generate_color_args_by_text(tag)
        painter.setPen(_style.QtRgba.BdrIcon)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(*background_color_)))
        painter.drawRoundedRect(tag_rect, txt_w / 2, txt_h / 2, QtCore.Qt.AbsoluteSize)
        painter.setPen(QtGui.QColor(*text_color_))
        painter.setFont(QtFont.generate(size=int(txt_w * .625)))
        painter.drawText(
            tag_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, str(tag[0]).capitalize()
        )
        painter.end()
        return pixmap


class QtSvgRender:
    @classmethod
    def to_pixmap_gray(cls, svg_render, rect):
        w, h = rect.width(), rect.height()
        pxm_new = QtGui.QPixmap(w, h)
        painter = QtGui.QPainter(pxm_new)
        pxm_new.fill(QtCore.Qt.black)
        svg_render.render(painter, QtCore.QRectF(0, 0, w, h))
        painter.end()

        img_gray = QtGui.QImage(w, h, QtGui.QImage.Format_RGB32)
        img_new = pxm_new.toImage()
        for i_x in range(w):
            for i_y in range(h):
                i_p = img_new.pixel(i_x, i_y)
                # noinspection PyArgumentList
                i_a = QtGui.qGray(i_p)
                i_g_c = QtGui.QColor(i_a, i_a, i_a)
                img_gray.setPixel(i_x, i_y, i_g_c.rgb())

        pxm_gray = pxm_new.fromImage(img_gray)
        pxm_mask = QtGui.QPixmap(pxm_new).createMaskFromColor(QtCore.Qt.black)
        pxm_gray.setMask(pxm_mask)
        return pxm_gray


class GuiQtText(object):
    @classmethod
    def get_draw_width(cls, widget, text=None):
        return widget.fontMetrics().width(text)

    @classmethod
    def get_draw_width_maximum(cls, widget, texts):
        list_ = []
        for i_text in texts:
            list_.append(widget.fontMetrics().width(i_text))
        return max(list_)

    @classmethod
    def generate_draw_args(cls, widget, text, w_maximum_text=None):
        w, h = widget.width(), widget.height()
        w_t, h_t = widget.fontMetrics().width(text), widget.fontMetrics().height() / 2
        s_t = (h - h_t) / 2
        if w_maximum_text is not None:
            w_t = min(w_t, w_maximum_text)
        # fit to max size
        w_c = w_t + s_t * 2
        return s_t, w_t, w_c, h


class GuiQtTreeWidget(object):
    @classmethod
    def _get_item_has_visible_children_(cls, qt_tree_widget, qt_tree_widget_item):
        qt_model_index = qt_tree_widget.indexFromItem(qt_tree_widget_item)
        raw_count = qt_tree_widget.model().rowCount(qt_model_index)
        for row in range(raw_count):
            child_index = qt_model_index.child(row, qt_model_index.column())
            if child_index.isValid():
                if qt_tree_widget.itemFromIndex(child_index).isHidden() is False:
                    return True
        return False

    @classmethod
    def get_item_is_ancestor_hidden(cls, qt_tree_widget, qt_tree_widget_item):
        qt_model_index = qt_tree_widget.indexFromItem(qt_tree_widget_item)
        ancestor_indices = cls._get_index_ancestor_indices_(qt_model_index)
        for ancestor_index in ancestor_indices:
            if qt_tree_widget.itemFromIndex(ancestor_index).isHidden() is True:
                return True
        return False

    @classmethod
    def _get_index_ancestor_indices_(cls, qt_model_index):
        def _rcs_fnc(index_):
            _parent = index_.parent()
            if _parent.isValid():
                list_.append(_parent)
                _rcs_fnc(_parent)

        list_ = []
        _rcs_fnc(qt_model_index)
        return list_

    @classmethod
    def _set_item_row_draw_(cls, qt_painter, qt_option, qt_model_index):
        user_data = qt_model_index.data(QtCore.Qt.UserRole)
        if user_data:
            rect = qt_option.rect
            x, y = rect.x(), rect.y()
            w, h = rect.width(), rect.height()
            b_w, b_h = 2, 2
            foregrounds = user_data.get('foregrounds')
            if foregrounds is not None:
                array_grid = bsc_core.BscList.grid_to(foregrounds, 8)
                for column, a in enumerate(array_grid):
                    for row, b in enumerate(a):
                        b_x, b_y = x + (w - b_w * column) - 2, y + (h - b_h * row) - 4
                        box_rect = qt_rect(
                            b_x, b_y,
                            b_w, b_h
                        )
                        qt_painter.fillRect(box_rect, b)


class GuiQtLayout(object):
    @staticmethod
    def clear_all_widgets(layout):
        def rcs_fnc_(layout_):
            c = layout_.count()
            for i in range(c):
                i_item = layout_.takeAt(0)
                if i_item is not None:
                    i_widget = i_item.widget()
                    if i_widget:
                        i_widget.deleteLater()
                    else:
                        _i_layout = i_item.layout()
                        if _i_layout:
                            rcs_fnc_(_i_layout)
                        else:
                            spacer = i_item.spacerItem()
                            if spacer:
                                spacer.deleteLater()

        #
        rcs_fnc_(layout)


class _ClassProperty(property):
    def __get__(self, cls, objtype=None):
        return super(_ClassProperty, self).__get__(objtype)

    def __set__(self, cls, value):
        super(_ClassProperty, self).__set__(type(cls), value)

    def __delete__(self, cls):
        super(_ClassProperty, self).__delete__(type(cls))


class QtFonts(object):
    # @_ClassProperty
    # def Default(cls):
    #     return QtFont.generate(size=8)

    Default = QtFont.generate(size=8)
    DefaultItalic = QtFont.generate(size=8, italic=True)
    Medium = QtFont.generate(size=10)
    Large = QtFont.generate(size=12)

    Index = QtFont.generate(size=8)

    NameNormal = QtFont.generate(size=8)
    NameDisable = QtFont.generate(size=8, italic=True, strike_out=True)
    NameKey = QtFont.generate(size=8, italic=True)
    NameValue = QtFont.generate(size=8)

    Description = QtFont.generate(size=10)
    Content = QtFont.generate(size=8, family='Monospace')

    Loading = QtFont.generate(size=10, weight=75, italic=True)

    Label = QtFont.generate(size=9)
    Button = QtFont.generate(size=9)
    Chart = QtFont.generate(size=10, italic=True)

    ToolGroup = QtFont.generate(size=9, weight=75, italic=True)

    Title = QtFont.generate(size=12)
    SubTitle = QtFont.generate(size=11, italic=True)

    MenuSeparator = QtFont.generate(size=8, italic=True)


class GuiQtCache(object):
    QT_IMAGE_CACHE = dict()

    @classmethod
    def generate_qt_image(cls, rect, file_path, cache_resize=False):
        rect_size = rect.size()
        w, h = rect_size.width(), rect_size.height()
        key = '{}[{}x{}]'.format(file_path, w, h)
        if key in cls.QT_IMAGE_CACHE:
            return cls.QT_IMAGE_CACHE[key]

        image = QtGui.QImage(file_path)
        img_scaled = image.scaled(
            rect_size,
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        if cache_resize is True:
            if file_path.endswith('.png'):
                path_tmp = bsc_storage.StgTmpThumbnailMtd.generate_for_qt_resize(file_path, width=max(w, h), ext='.png')
                if bsc_storage.StgPath.get_is_exists(path_tmp) is False:
                    bsc_storage.StgFileOpt(path_tmp).create_directory()
                    img_scaled.save(path_tmp)
                img_scaled = QtGui.QImage(path_tmp)

        cls.QT_IMAGE_CACHE[key] = img_scaled
        return img_scaled

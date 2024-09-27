# coding=utf-8
import six

import functools

import types

import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core

from .. import abstracts as _qt_abstracts
# qt widgets
from . import base as _base


class QtItemDelegate(QtWidgets.QItemDelegate):
    def sizeHint(self, option, index):
        size = super(QtItemDelegate, self).sizeHint(option, index)
        size.setHeight(_gui_core.GuiSize.ItemDefaultHeight)
        return size


class QtWidget(
    QtWidgets.QWidget,
    #
    _qt_abstracts.AbsQtStatusBaseDef
):
    def __init__(self, *args, **kwargs):
        super(QtWidget, self).__init__(*args, **kwargs)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #
        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        #
        self.setAutoFillBackground(True)
        #
        self._init_status_base_def_(self)

    def _refresh_widget_draw_(self):
        self.update()

    def paintEvent(self, event):
        if self._get_status_is_enable_() is True:
            painter = _qt_core.QtPainter(self)

            color, hover_color = self._get_rgba_args_by_validator_status_(self._status)
            border_color = color
            pox_x, pos_y = 0, 0
            width, height = self.width(), self.height()
            frame_rect = QtCore.QRect(
                pox_x+1, pos_y+1, width-2, height-2
            )

            painter._draw_focus_frame_by_rect_(
                frame_rect,
                color=border_color,
            )


class QtTestPaint(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtTestPaint, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)

        w, h = self.width(), self.height()

        btn_w, btn_h = 60, 20
        # left to right
        # for seq, rect in enumerate(
        #     [
        #         QtCore.QRect(0, 0, btn_h, btn_w),
        #         QtCore.QRect(0, btn_w, btn_h, btn_w)
        #     ]
        # ):
        #     r_x, r_y, r_w, r_h = rect.x(), rect.y(), rect.width(), rect.height()
        #
        #     painter.rotate(-90)
        #     painter.translate(QtCore.QPoint(-r_y-(r_y+r_h), 0))
        #
        #     rect_new = QtCore.QRect(r_y, r_x, r_h, r_w)
        #
        #     painter.fillRect(
        #         rect_new, QtGui.QColor(255, 0, 0, 255)
        #     )
        #
        #     painter.drawText(
        #         rect_new, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
        #         'TEST-' + str(seq)
        #     )
        #     painter.resetTransform()

        # right to left
        for seq, rect in enumerate(
            [
                QtCore.QRect(w-btn_h, 0, btn_h, btn_w),
                QtCore.QRect(w-btn_h, btn_w, btn_h, btn_w)
            ]
        ):
            r_x, r_y, r_w, r_h = rect.x(), rect.y(), rect.width(), rect.height()

            painter.rotate(90)
            painter.translate(QtCore.QPoint(0, -r_w-r_x))

            rect_new = QtCore.QRect(r_y, 0, r_h, r_w)
            print rect_new

            painter.fillRect(
                rect_new, QtGui.QColor(255, 0, 0, 255)
            )

            painter.drawText(
                rect_new, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                'TEST-' + str(seq)
            )
            painter.resetTransform()

        # rect = QtCore.QRect(0, 0, 60, 20)
        # painter.fillRect(
        #     rect, QtGui.QColor(0, 255, 0, 255)
        # )
        # painter.rotate(90)
        # painter.translate(QtCore.QPoint(0, -20))
        # painter.fillRect(
        #     rect, QtGui.QColor(255, 0, 0, 255)
        # )


class QtButtonFrame(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtFrameBaseDef
):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        self._frame_draw_rect.setRect(
            x, y, w, h
        )

    def __init__(self, *args, **kwargs):
        super(QtButtonFrame, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._init_frame_base_def_(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)

        painter._draw_frame_by_rect_(
            rect=self._frame_draw_rect,
            border_color=_qt_core.QtBorderColors.Transparent,
            background_color=_qt_core.QtBackgroundColors.Basic,
        )


class QtVLine(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtFrameBaseDef,
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForPressDef,
):
    def __init__(self, *args, **kwargs):
        super(QtVLine, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._init_frame_base_def_(self)

        r, g, b = 119, 119, 119
        h, s, v = bsc_core.BscColor.rgb_to_hsv(r, g, b)
        color = bsc_core.BscColor.hsv2rgb(h, s*.75, v*.75)
        hover_color = r, g, b
        self._frame_border_color = color
        self._hovered_frame_border_color = hover_color
        #
        self._frame_background_color = 0, 0, 0, 0

        self._line_draw_is_enable = False
        self._line_draw_offset_x, self._line_draw_offset_y = 1, 2

        self._init_action_for_press_def_(self)

    def _refresh_widget_draw_(self):
        self.update()

    def _set_line_draw_enable_(self, boolean):
        self._line_draw_is_enable = boolean

    def _set_line_draw_offset_x_(self, x):
        self._line_draw_offset_x = x

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)

        bdr_color = _qt_core.QtColors.HeadBorder

        offset = [0, 1][self._is_pressed]
        o_x, o_y = self._line_draw_offset_x, self._line_draw_offset_y
        x, y = o_x+offset, o_y+offset
        w, h = self.width()-o_x*2-offset, self.height()-o_y*2-offset
        rect = QtCore.QRect(x, y, w, h)
        if self._line_draw_is_enable is True:
            painter._draw_line_by_points_(
                point_0=rect.topLeft(),
                point_1=rect.bottomLeft(),
                border_color=bdr_color,
            )


class QtLineWidget(QtWidgets.QWidget):
    class Style(object):
        Null = 0x00
        Solid = 0x01

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtLineWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        # top, bottom, left, right
        self._line_styles = [self.Style.Null]*4
        self._lines = [QtCore.QLine(), QtCore.QLine(), QtCore.QLine(), QtCore.QLine()]
        self._line_border_color = _qt_core.QtBorderColors.Basic
        self._line_border_width = 1

        self._background_color = _gui_core.GuiRgba.Transparent

    def _set_line_styles_(self, line_styles):
        # top, bottom, left, right
        self._line_styles = line_styles

    def _set_background_color_(self, color):
        self._background_color = color

    def _set_top_line_mode_(self):
        self._line_styles = [self.Style.Solid, self.Style.Null, self.Style.Null, self.Style.Null]
        self._refresh_widget_all_()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        t_l, b_l, l_l, r_l = self._lines
        # top
        t_l.setP1(QtCore.QPoint(x, y+1))
        t_l.setP2(QtCore.QPoint(x+w, y+1))
        # bottom
        b_l.setP1(QtCore.QPoint(x, y+h-1))
        b_l.setP2(QtCore.QPoint(x+w, y+h-1))
        # left
        l_l.setP1(QtCore.QPoint(x+1, y))
        l_l.setP2(QtCore.QPoint(x+1, y+h))
        # right
        r_l.setP1(QtCore.QPoint(x+w-1, y))
        r_l.setP2(QtCore.QPoint(x+w-1, y+h))

    def resizeEvent(self, event):
        self._refresh_widget_draw_geometry_()

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter._set_border_color_(_gui_core.GuiRgba.Transparent)
        painter._set_background_color_(self._background_color)
        painter.drawRect(
            QtCore.QRect(0, 0, self.width(), self.height())
        )
        for seq, i in enumerate(self._line_styles):
            i_line = self._lines[seq]
            if i == self.Style.Solid:
                painter._set_border_color_(self._line_border_color)
                painter._set_border_width_(self._line_border_width)
                painter._set_antialiasing_(False)
                painter.drawLine(i_line)


class QtHLine(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtHLine, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedHeight(1)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter._set_border_color_(
            79, 79, 79, 255
        )
        painter.drawLine(
            QtCore.QLine(
                0, 0, self.width(), 1
            )
        )


class QtHFrame(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtHFrame, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedHeight(24)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter._set_border_color_(
            55, 55, 55, 255
        )
        painter._set_background_color_(
            55, 55, 55, 255
        )
        painter.drawRect(
            QtCore.QRect(
                0, 0, self.width(), self.height()
            )
        )


class QtTranslucentWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QtTranslucentWidget, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def _set_visible_(self, boolean):
        self.setVisible(boolean)


class QtMenuBar(QtWidgets.QMenuBar):
    def __init__(self, *args, **kwargs):
        super(QtMenuBar, self).__init__(*args, **kwargs)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setPalette(_qt_core.GuiQtDcc.generate_qt_palette())
        self.setAutoFillBackground(True)
        #
        self.setFont(_qt_core.QtFonts.NameNormal)
        #
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        #
        self.setStyleSheet(
            _qt_core.GuiQtStyle.get('QMenuBar')
        )


# noinspection PyArgumentList,PyUnresolvedReferences
class QtMenu(QtWidgets.QMenu):
    def __init__(self, *args, **kwargs):
        super(QtMenu, self).__init__(*args, **kwargs)
        self.setPalette(_qt_core.GuiQtDcc.generate_qt_palette())
        self.setAutoFillBackground(True)
        #
        self.setFont(_qt_core.QtFonts.NameNormal)
        #
        self.setStyleSheet(
            _qt_core.GuiQtStyle.get('QMenu')
        )

        self._menu_content_opt = _qt_core.GuiQtMenuOpt(self)

    @classmethod
    def _set_cmd_run_(cls, cmd_str):
        exec cmd_str

    @classmethod
    def _create_action_(cls, qt_menu, action_args):
        def set_disable_fnc_(qt_widget_action_):
            qt_widget_action_.setFont(_qt_core.QtFonts.NameDisable)
            qt_widget_action_.setDisabled(True)

        if action_args:
            if len(action_args) == 1:
                s = qt_menu.addSeparator()
                s.setFont(_qt_core.QtFonts.MenuSeparator)
                s.setText(action_args[0])
            elif len(action_args) >= 3:
                name, icon_name, args_extend = action_args[:3]
                item = _qt_core.QtWidgetAction(qt_menu)
                item.setFont(_qt_core.QtFonts.NameNormal)
                qt_menu.addAction(item)
                #
                item.setText(name)
                #
                is_checked = False
                #
                if args_extend is None:
                    set_disable_fnc_(item)
                else:
                    if isinstance(
                        args_extend,
                        (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)
                    ):
                        fnc = args_extend
                        item.triggered.connect(fnc)
                    elif isinstance(args_extend, six.string_types):
                        cmd_str = args_extend
                        item.triggered.connect(lambda *args, **kwargs: cls._set_cmd_run_(cmd_str))
                    elif isinstance(args_extend, (tuple, list)):
                        # check
                        if len(args_extend) == 2:
                            check_fnc, fnc = args_extend
                            if isinstance(
                                check_fnc,
                                (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)
                            ):
                                is_checked = check_fnc()
                            else:
                                is_checked = check_fnc
                            #
                            if isinstance(is_checked, bool):
                                if isinstance(
                                        fnc,
                                        (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)
                                ):
                                    item.triggered.connect(fnc)
                            else:
                                set_disable_fnc_(item)
                        elif len(args_extend) == 3:
                            check_fnc, fnc, enable_fnc = args_extend
                            if isinstance(
                                check_fnc,
                                (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)
                            ):
                                is_checked = check_fnc()
                            else:
                                is_checked = check_fnc
                            #
                            item.triggered.connect(fnc)
                            if isinstance(
                                enable_fnc,
                                (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)
                            ):
                                is_enable = enable_fnc()
                                item.setEnabled(is_enable)
                                if is_enable is False:
                                    item.setFont(_qt_core.QtFonts.NameDisable)
                                else:
                                    item.setDisabled(False)
                                    item.setFont(_qt_core.QtFonts.NameNormal)
                if icon_name is not None:
                    if isinstance(icon_name, six.string_types):
                        if icon_name:
                            if icon_name == 'box-check':
                                icon = [
                                    _qt_core.GuiQtIcon.generate_by_icon_name('basic/box-check-off'),
                                    _qt_core.GuiQtIcon.generate_by_icon_name('basic/box-check-on')
                                ][is_checked]
                                item.setIcon(icon)
                            elif icon_name == 'radio-check':
                                icon = [
                                    _qt_core.GuiQtIcon.generate_by_icon_name('basic/radio-check-off'),
                                    _qt_core.GuiQtIcon.generate_by_icon_name('basic/radio-check-on')
                                ][is_checked]
                                item.setIcon(icon)
                            else:
                                item.setIcon(_qt_core.GuiQtIcon.generate_by_name(icon_name))
                        else:
                            item.setIcon(
                                _qt_core.GuiQtIcon.generate_by_text(name, background_color=(64, 64, 64))
                            )
                else:
                    item.setIcon(
                        _qt_core.GuiQtIcon.generate_by_text(name, background_color=(64, 64, 64))
                    )
                #
                if len(action_args) >= 4:
                    shortcut = action_args[3]
                    item.setShortcut(shortcut)
                    item.setShortcutContext(QtCore.Qt.WidgetShortcut)
        else:
            qt_menu.addSeparator()

    @classmethod
    def _set_icon_color_rgb_(cls, qt_widget, color):
        icon = QtGui.QIcon()
        f_w, f_h = 13, 13
        c_w, c_h = 12, 12
        pixmap = QtGui.QPixmap(f_w, f_h)
        painter = _qt_core.QtPainter(pixmap)
        rect = pixmap.rect()
        pixmap.fill(
            QtCore.Qt.white
        )
        x, y = rect.x(), rect.y()
        w, h = rect.width(), rect.height()
        icon_rect = QtCore.QRect(
            x+(w-c_w)/2, y+(h-c_h)/2,
            c_w, c_h
        )
        painter._set_color_icon_draw_(
            icon_rect, color
        )
        painter.end()

        icon.addPixmap(
            pixmap,
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        qt_widget.setIcon(icon)

    def _set_menu_data_(self, menu_raw):
        """
        :param menu_raw: [
            ('Label', 'icon_name', fnc),
            (),
            [
                'Label', 'icon_name', [
                    ()
                ]
            ]
        ]
        :return:
        """
        if menu_raw:
            for i in menu_raw:
                if isinstance(i, tuple):
                    self._create_action_(self, i)
                # sub menu
                elif isinstance(i, list):
                    i_name, i_icon_name, sub_menu_raws = i
                    qt_action_item = self.addAction(i_name)
                    if i_icon_name is not None:
                        if isinstance(i_icon_name, six.string_types):
                            qt_action_item.setIcon(_qt_core.GuiQtIcon.generate_by_name(i_icon_name))
                    else:
                        qt_action_item.setIcon(_qt_core.GuiQtIcon.generate_by_text(i_name, background_color=(64, 64, 64)))
                    #
                    sub_menu = self.__class__(self.parent())
                    qt_action_item.setMenu(sub_menu)
                    for j in sub_menu_raws:
                        self._create_action_(sub_menu, j)

    def _set_title_text_(self, text):
        # self.setTearOffEnabled(True)
        self.setTitle(text)
        self.setIcon(
            QtGui.QIcon(
                _gui_core.GuiIcon.get('menu_h')
            )
        )

    def _set_show_(self):
        self.popup(
            QtGui.QCursor().pos()
        )

    def _set_menu_content_(self, content, append=False):
        self._menu_content_opt.create_by_content(content, append)

    @classmethod
    def _set_action_create_by_menu_content_(cls, menu):
        menu.clear()

    @classmethod
    def _add_menu_separator_(cls, menu, content):
        name = content.get('name')
        separator = menu.addSeparator()
        separator.setFont(_qt_core.QtFonts.MenuSeparator)
        separator.setText(name)

    @classmethod
    def _add_menu_action_(cls, menu, content):
        def set_disable_fnc_(widget_action_):
            widget_action_.setFont(_qt_core.QtFonts.NameDisable)
            widget_action_.setDisabled(True)

        #
        name = content.get('name')
        icon_name = content.get('icon_name')
        executable_fnc = content.get('executable_fnc')
        execute_fnc = content.get('execute_fnc')
        widget_action = _qt_core.QtWidgetAction(menu)
        widget_action.setFont(_qt_core.QtFonts.NameNormal)
        widget_action.setText(name)
        menu.addAction(widget_action)
        if icon_name:
            widget_action.setIcon(
                _qt_core.GuiQtIcon.generate_by_icon_name(icon_name)
            )
        else:
            widget_action.setIcon(
                _qt_core.GuiQtIcon.generate_by_text(name, background_color=(64, 64, 64))
            )
        #
        if isinstance(executable_fnc, (bool, int)):
            executable = executable_fnc
            if executable is False:
                set_disable_fnc_(widget_action)
        elif isinstance(executable_fnc, (types.FunctionType, types.MethodType)):
            executable = executable_fnc()
            if executable is False:
                set_disable_fnc_(widget_action)
        #
        if isinstance(execute_fnc, (types.FunctionType, types.MethodType)):
            fnc = execute_fnc
            widget_action.triggered.connect(fnc)
        elif isinstance(execute_fnc, six.string_types):
            cmd_str = execute_fnc
            widget_action.triggered.connect(lambda *args, **kwargs: cls._set_cmd_run_(cmd_str))

    def _popup_start_(self):
        self.popup(
            QtGui.QCursor().pos()
        )


class QtAction(QtWidgets.QAction):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        super(QtAction, self).__init__(*args, **kwargs)
        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)
        #
        self.setFont(_qt_core.QtFonts.NameNormal)


class _QtWidget(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtEmptyBaseDef,
):
    def __init__(self, *args, **kwargs):
        super(_QtWidget, self).__init__(*args, **kwargs)
        
        self._init_empty_base_def_(self)

        self._border_color = _qt_core.QtBackgroundColors.Transparent
        self._background_color = _qt_core.QtBackgroundColors.Basic

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        painter._set_border_color_(self._border_color)
        painter._set_background_color_(self._background_color)
        painter.drawRect(self.rect())
        if self._empty_draw_flag is True:
            painter = _qt_core.QtPainter(self)
            painter._draw_empty_image_by_rect_(
                self.rect(),
                self._empty_icon_name
            )

    def _set_border_color_(self, color):
        self._border_color = color

    def _set_background_color_(self, color):
        self._background_color = color


class QtHScrollArea(QtWidgets.QScrollArea):
    def __init__(self, *args, **kwargs):
        super(QtHScrollArea, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setWidgetResizable(True)

        self._widget = _QtWidget()
        self.setWidget(self._widget)
        self._layout = _base.QtHBoxLayout(self._widget)
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self._layout.setContentsMargins(*[0]*4)
        self._layout.setSpacing(_gui_core.GuiSize.LayoutDefaultSpacing)

        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)

        self.setStyleSheet(
            _qt_core.GuiQtStyle.get('QScrollArea')
        )

        self.verticalScrollBar().setStyleSheet(
            _qt_core.GuiQtStyle.get('QScrollBar')
        )
        self.horizontalScrollBar().setStyleSheet(
            _qt_core.GuiQtStyle.get('QScrollBar')
        )
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def keyPressEvent(self, event):
        pass

    def wheelEvent(self, event):
        if event.angleDelta().y() != 0:
            delta = event.angleDelta().y()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value()-delta)
            event.accept()
        else:
            super(QtHScrollArea, self).wheelEvent(event)

    def _add_widget_(self, widget):
        self._layout.addWidget(widget)

    def _set_border_color_(self, color):
        self._widget._border_color = color

    def _set_background_color_(self, color):
        self._widget._background_color = color

    def _set_empty_draw_flag_(self, boolean):
        self._widget._set_empty_draw_flag_(boolean)


class QtVScrollArea(QtWidgets.QScrollArea):
    def __init__(self, *args, **kwargs):
        super(QtVScrollArea, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setWidgetResizable(True)

        self._widget = _QtWidget()
        self.setWidget(self._widget)
        self._layout = _base.QtVBoxLayout(self._widget)
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self._layout.setContentsMargins(*[0]*4)
        self._layout.setSpacing(_gui_core.GuiSize.LayoutDefaultSpacing)

        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)

        self.setStyleSheet(
            _qt_core.GuiQtStyle.get('QScrollArea')
        )

        self.verticalScrollBar().setStyleSheet(
            _qt_core.GuiQtStyle.get('QScrollBar')
        )
        self.horizontalScrollBar().setStyleSheet(
            _qt_core.GuiQtStyle.get('QScrollBar')
        )

    def keyPressEvent(self, event):
        pass

    def paintEvent(self, event):
        pass

    def _add_widget_(self, widget):
        self._layout.addWidget(widget)

    def _set_border_color_(self, color):
        self._widget._border_color = color

    def _set_background_color_(self, color):
        self._widget._background_color = color
    
    def _set_empty_draw_flag_(self, boolean):
        self._widget._set_empty_draw_flag_(boolean)


class QtThreadDef(object):
    def _set_thread_def_init_(self):
        pass

    def _create_fnc_thread_(self):
        return _qt_core.QtMethodThread(self)


class QtTextItem(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtNameBaseDef,
    #
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,
    #
    _qt_abstracts.AbsQtStatusBaseDef,
):
    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtTextItem, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.installEventFilter(self)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        #
        self._init_name_base_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)

        self._init_status_base_def_(self)

        self._set_name_draw_font_(_qt_core.QtFonts.Label)
        self._name_text_option = QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        if self._name_align == self.AlignRegion.Top:
            icn_frm_w, icn_frm_h = self._name_frame_size
            t_w, t_h = self._name_draw_size
            self._name_draw_rect.setRect(
                x, y+(icn_frm_h-t_h)/2, w, t_h
            )
        else:
            self._name_draw_rect.setRect(
                x, y, w, h
            )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        self._refresh_widget_draw_geometry_()
        # name
        if self._name_text is not None:
            color, hover_color = self._get_text_rgba_args_by_validator_status_(self._status)
            text_color = [color, hover_color][self._is_hovered]

            # painter.fillRect(
            #     self._name_draw_rect, QtGui.QColor(255, 0, 0, 255)
            # )
            #
            painter._draw_text_by_rect_(
                rect=self._name_draw_rect,
                text=self._name_text,
                text_color=text_color,
                font=self._name_draw_font,
                text_option=self._name_text_option,
            )


class QtInfoLabel(
    QtWidgets.QWidget,
):

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        w_t, h_t = QtGui.QFontMetrics(self._text_font).width(self._text)+8, h
        self.setFixedWidth(w_t)
        self._text_draw_rect.setRect(
            x, y, w_t, h
        )

    def __init__(self, *args, **kwargs):
        super(QtInfoLabel, self).__init__(*args, **kwargs)
        #
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )

        self._text = ''
        self._text_draw_rect = QtCore.QRect()

        self._text_font = _qt_core.QtFont.generate(size=8)

        self.setFont(self._text_font)

        self.setFixedHeight(20)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        if self._text:
            painter._draw_text_by_rect_(
                rect=self._text_draw_rect,
                text=self._text,
                text_color=_gui_core.GuiRgba.DarkWhite,
                font=self._text_font,
                text_option=QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter,
            )

    def _set_info_(self, text):
        self._text = text
        self._refresh_widget_all_()


class QtCommonStyle(QtWidgets.QCommonStyle):
    def __init__(self):
        super(QtCommonStyle, self).__init__()

    def drawPrimitive(self, *args):
        element, option, painter, widget = args
        if element == QtWidgets.QStyle.PE_FrameFocusRect:
            return
        elif element == QtWidgets.QStyle.PE_IndicatorBranch:
            return
        else:
            QtWidgets.QCommonStyle().drawPrimitive(element, option, painter, widget)


class _QtSpacer(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(_QtSpacer, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.setFocusPolicy(QtCore.Qt.NoFocus)


class QtStyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(QtStyledItemDelegate, self).__init__(parent)
        self._icon_draw_size = QtCore.QSize(20, 20)

    @staticmethod
    def _draw_for_hover_(painter, option, index):
        if option.state&QtWidgets.QStyle.State_MouseOver:
            if index.column() == 0:
                rect = option.rect
                x, y = rect.x(), rect.y()
                w, h = rect.width(), rect.height()
                hover_rect = QtCore.QRect(
                    x, y, 4, h
                )
                painter.fillRect(
                    hover_rect, _qt_core.QtBackgroundColors.Hovered
                )
        elif option.state&QtWidgets.QStyle.State_Selected:
            if index.column() == 0:
                rect = option.rect
                x, y = rect.x(), rect.y()
                w, h = rect.width(), rect.height()
                hover_rect = QtCore.QRect(
                    x, y, 4, h
                )
                painter.fillRect(
                    hover_rect, _qt_core.QtBackgroundColors.Selected
                )

    @staticmethod
    def _draw_for_keyword_(painter, option, index):
        _ = index.data(QtCore.Qt.DisplayRole)
        if _:
            user_data = index.data(QtCore.Qt.UserRole)
            if user_data:
                filter_keyword = user_data.get('filter_keyword')
                filter_occurrence = user_data.get('filter_occurrence', False)
                if filter_keyword is not None:
                    content = index.data(QtCore.Qt.DisplayRole)
                    if content:
                        rect = option.rect
                        x, y = rect.x(), rect.y()
                        w, h = rect.width(), rect.height()
                        spans = bsc_core.RawTextMtd.find_spans(content, filter_keyword)
                        if spans:
                            line = QtCore.QLine(
                                x, y+h, x+w, y+h
                            )
                            if filter_occurrence is True:
                                painter.setPen(_qt_core.QtColors.TextKeywordFilterOccurrence)
                            else:
                                painter.setPen(_qt_core.QtColors.TextKeywordFilter)
                            painter.drawLine(line)

    def paint(self, painter, option, index):
        super(QtStyledItemDelegate, self).paint(painter, option, index)

        # self._draw_for_hover_(painter, option, index)

    def updateEditorGeometry(self, editor, option, index):
        super(QtStyledItemDelegate, self).updateEditorGeometry(editor, option, index)

    def sizeHint(self, option, index):
        size = super(QtStyledItemDelegate, self).sizeHint(option, index)
        size.setHeight(_gui_core.GuiSize.ItemDefaultHeight)
        return size


class QtListWidgetStyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, *args, **kwargs):
        super(QtListWidgetStyledItemDelegate, self).__init__(*args, **kwargs)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class QtProgressBar(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtProgressBaseDef
):
    def __init__(self, *args, **kwargs):
        super(QtProgressBar, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMaximumHeight(4)
        self.setMinimumHeight(4)
        #
        self._init_progress_base_def_()

    def _refresh_widget_draw_(self):
        self.update()

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        if self._get_progress_is_enable_() is True:
            if self._progress_raw:
                cur_rect = None
                w, h = self.width(), self.height()
                w -= 2
                layer_count = len(self._progress_raw)
                r, g, b = bsc_core.BscColor.hsv2rgb(120, .5, 1)
                for layer_index, i in enumerate(self._progress_raw):
                    i_percent, (i_range_start, i_range_end), i_label = i
                    p_w = w*(i_range_end-i_range_start)*i_percent
                    p_h = 2
                    #
                    i_x, i_y = w*i_range_start, (h-p_h)/2
                    i_x += 1
                    i_rect = QtCore.QRect(i_x, i_y, p_w+1, p_h)
                    #
                    i_p = float(layer_index)/float(layer_count)
                    r_1, g_1, b_1 = bsc_core.BscColor.hsv2rgb(120*i_p, .5, 1)
                    i_cur_color = QtGui.QColor(r_1, g_1, b_1, 255)
                    if layer_index == 0:
                        i_pre_color = QtGui.QColor(r, g, b, 255)
                        i_gradient_color = QtGui.QLinearGradient(i_rect.topLeft(), i_rect.topRight())
                        i_gradient_color.setColorAt(.5, i_pre_color)
                        i_gradient_color.setColorAt(.975, i_cur_color)
                        i_background_color = i_gradient_color
                    else:
                        i_gradient_color = QtGui.QLinearGradient(i_rect.topLeft(), i_rect.topRight())
                        i_gradient_color.setColorAt(0, _qt_core.QtBackgroundColors.Transparent)
                        i_gradient_color.setColorAt(.5, i_cur_color)
                        i_gradient_color.setColorAt(.975, i_cur_color)
                        i_gradient_color.setColorAt(1, _qt_core.QtBackgroundColors.Transparent)
                        i_background_color = i_gradient_color
                    #
                    painter._draw_frame_by_rect_(
                        i_rect,
                        border_color=_qt_core.QtBorderColors.Transparent,
                        background_color=i_background_color,
                        border_radius=1,
                    )
                    cur_rect = i_rect
                #
                if cur_rect is not None:
                    c_x, c_y = cur_rect.x(), cur_rect.y()
                    c_w, c_h = cur_rect.width(), cur_rect.height()
                    rect = QtCore.QRect(
                        c_x+c_w-2, 0, 2, h
                    )
                    painter._draw_frame_by_rect_(
                        rect,
                        border_color=_qt_core.QtBorderColors.Transparent,
                        background_color=(255, 255, 255, 255),
                        border_radius=1,
                    )


class QtFileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(QtFileDialog, self).__init__(*args, **kwargs)


class _QtHItem(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtFrameBaseDef,
    _qt_abstracts.AbsQtIndexBaseDef,
    _qt_abstracts.AbsQtTypeDef,
    _qt_abstracts.AbsQtIconBaseDef,
    _qt_abstracts.AbsQtNamesBaseDef,
    _qt_abstracts.AbsQtPathBaseDef,
    _qt_abstracts.AbsQtImageBaseDef,
    #
    _qt_abstracts.AbsQtValueBaseDef,
    #
    _qt_abstracts.AbsQtMenuBaseDef,
    # action
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,
    _qt_abstracts.AbsQtActionForSelectDef,
    _qt_abstracts.AbsQtActionForCheckDef,
    _qt_abstracts.AbsQtDeleteBaseDef,
    #
    _qt_abstracts.AbsQtItemFilterDef,
):
    delete_press_clicked = qt_signal()

    def __init__(self, *args, **kwargs):
        super(_QtHItem, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #
        self._init_frame_base_def_(self)
        self._init_index_base_def_(self)
        self._init_type_base_def_(self)
        self._init_icon_base_def_(self)
        self._init_names_base_def_(self)
        self._init_path_base_def_(self)
        self._init_image_base_def_(self)
        #
        self._init_value_base_def_(self)
        #
        self._init_menu_base_def_(self)
        #
        self._init_delete_base_def_(self)
        #
        self._init_action_for_hover_def_(self)
        self._init_action_base_def_(self)
        self._init_action_for_press_def_(self)
        self._init_action_for_check_def_(self)
        self._check_icon_file_path_0 = _gui_core.GuiIcon.get('filter_unchecked')
        self._check_icon_file_path_1 = _gui_core.GuiIcon.get('filter_checked')
        self._refresh_check_()
        self._init_action_for_select_def_(self)
        #
        self._init_item_filter_extra_def_(self)
        #
        self._frame_background_color = _qt_core.QtBackgroundColors.Light

    def _refresh_widget_all_(self, *args, **kwargs):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        #
        spacing = 2
        #
        frm_w = frm_h = h
        icn_frm_w, icn_frm_h = self._icon_frame_draw_size
        icn_frm_m_w, icn_frm_m_h = (frm_w-icn_frm_w)/2, (frm_h-icn_frm_h)/2
        icn_w, icn_h = int(icn_frm_w*self._icon_draw_percent), int(icn_frm_h*self._icon_draw_percent)
        #
        c_x, c_y = x, y
        c_w, c_h = w, h
        #
        f_x, f_y = x, y
        f_w, f_h = w, h
        # frame
        self._set_icon_frame_draw_rect_(
            c_x+icn_frm_m_w, c_y+icn_frm_m_h, icn_frm_w, icn_frm_h
        )
        # check
        if self._check_is_enable is True:
            self._set_check_action_rect_(
                c_x, c_y, icn_frm_w, c_h
            )
            self._set_check_icon_draw_rect_(
                c_x+(icn_frm_w-icn_w)/2, c_y+(icn_frm_w-icn_h)/2, icn_w, icn_h
            )
            c_x += icn_frm_w+spacing
            c_w -= icn_frm_w+spacing
            # f_x += icn_frm_w+spacing
            # f_w -= icn_frm_w+spacing
        # use icon
        if self._icon is not None or self._icon_file_path is not None:
            icn_frm_w_0, icn_frm_h_0 = c_h, c_h
            icn_w_0, icn_h_0 = int(icn_frm_w_0*self._icon_draw_percent), int(icn_frm_h_0*self._icon_draw_percent)
            self._icon_draw_rect.setRect(
                c_x+(icn_frm_w_0-icn_w_0)/2, c_y+(icn_frm_h_0-icn_h_0)/2, icn_w_0, icn_h_0
            )
            c_x += icn_frm_w_0+spacing
            c_w -= icn_frm_w_0+spacing
        # use icon name
        if self._icon_text is not None:
            icn_p = self._icon_text_draw_percent
            icn_w, icn_h = c_h*icn_p, c_h*icn_p
            self._icon_text_draw_rect.setRect(
                c_x+(c_h-icn_w)/2, c_y+(c_h-icn_h)/2, icn_w, icn_h
            )
            c_x += c_h+spacing
            c_w -= c_h+spacing
        # image
        if self._image_flag is True:
            img_p = self._image_draw_percent
            img_w, img_h = c_h*img_p, c_h*img_p
            self._set_image_rect_(
                c_x+(c_h-img_w)/2, c_y+(c_h-img_h)/2, img_w, img_h
            )
            c_x += c_h+spacing
            c_w -= c_h+spacing
        # delete
        if self._delete_is_enable is True:
            icn_w, icn_h = self._delete_icon_file_draw_size
            self._set_delete_rect_(
                x+w-icn_frm_w, c_y+(c_h-icn_frm_h)/2, icn_frm_w, icn_frm_h
            )
            self._set_delete_draw_rect_(
                x+(icn_frm_w-icn_w)/2+w-icn_frm_w, c_y+(c_h-icn_h)/2, icn_w, icn_h
            )
            c_w -= icn_frm_w+spacing
            # f_w -= icn_frm_w+spacing
        #
        self._set_frame_draw_rect_(
            f_x, f_y, f_w, f_h
        )
        #
        self._set_name_draw_rect_(
            c_x, c_y, c_w, c_h
        )
        # name text
        if self._name_indices:
            n_w, n_h = self._name_frame_size
            for i in self._name_indices:
                i_n_x, i_n_y = c_x, c_y+i*n_h
                i_n_w, i_n_h = w, n_h
                self._set_name_text_draw_rect_at_(
                    i_n_x, i_n_y, i_n_w, i_n_h, i
                )
        #
        self._index_draw_rect.setRect(
            c_x, c_y, c_w, c_h
        )

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Close:
                self.delete_text_accepted.emit(self._get_name_text_())
            #
            elif event.type() == QtCore.QEvent.Enter:
                pass
                # self._do_hover_move_(event)
            elif event.type() == QtCore.QEvent.Leave:
                self._is_check_hovered = False
                self._press_is_hovered = False
                self._delete_is_hovered = False
                self._is_hovered = False
                #
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.Show:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.RightButton:
                    self._popup_menu_()
                elif event.button() == QtCore.Qt.LeftButton:
                    self._set_action_flag_(self.ActionFlag.AnyClick)
                    if self._get_action_check_is_valid_(event) is True:
                        self.check_clicked.emit()
                        self._do_check_press_(event)
                    elif self._get_action_delete_is_valid_(event) is True:
                        self.delete_press_clicked.emit()
                    else:
                        self.clicked.emit()
                #
                self.update()
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.LeftButton:
                    self.press_dbl_clicked.emit()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._is_check_hovered is True:
                        pass
                    elif self._delete_is_hovered is True:
                        pass
                    else:
                        self.press_clicked.emit()
                    self._clear_all_action_flags_()
            elif event.type() == QtCore.QEvent.MouseMove:
                self._do_hover_move_(event)
        return False

    def paintEvent(self, event):
        painter = _qt_core.QtPainter(self)
        # todo: refresh error
        self._refresh_widget_draw_geometry_()
        #
        offset = self._get_action_offset_()
        #
        bkg_color = painter._get_frame_background_color_by_rect_(
            rect=self._frame_draw_rect,
            check_is_hovered=self._is_check_hovered,
            is_checked=self._is_checked,
            press_is_hovered=self._press_is_hovered,
            is_pressed=self._is_pressed,
            is_selected=self._is_selected,
            delete_is_hovered=self._delete_is_hovered
        )
        painter._draw_frame_by_rect_(
            self._frame_draw_rect,
            border_color=_qt_core.QtBorderColors.Transparent,
            background_color=bkg_color,
            border_radius=1
        )
        # check
        if self._check_is_enable is True:
            painter._draw_icon_file_by_rect_(
                rect=self._check_icon_draw_rect,
                file_path=self._check_icon_file_path_current,
                offset=offset,
                # frame_rect=self._check_frame_rect,
                is_hovered=self._is_check_hovered
            )

        if self._icon is not None:
            painter._draw_icon_by_rect_(
                icon=self._icon,
                rect=self._icon_draw_rect,
                offset=offset
            )
        else:
            # icon
            if self._icon_text is not None:
                painter._draw_image_use_text_by_rect_(
                    rect=self._icon_text_draw_rect,
                    text=self._icon_text,
                    background_color=bkg_color,
                    offset=offset,
                    border_radius=1, border_width=2
                )
            #
            if self._icon_file_path is not None:
                painter._draw_icon_file_by_rect_(
                    rect=self._icon_draw_rect,
                    file_path=self._icon_file_path,
                )
        # image
        if self._image_flag is True:
            painter._draw_image_data_by_rect_(
                rect=self._image_draw_rect,
                image_data=self._image_data,
                offset=offset,
                text=self._name_text
            )
        # name
        if self._name_texts:
            for i in self._name_indices:
                painter._draw_text_by_rect_(
                    rect=self._name_draw_rects[i],
                    text=self._name_texts[i],
                    text_color=self._name_draw_color,
                    font=self._name_draw_font,
                    text_option=self._name_text_option,
                    is_hovered=self._is_hovered,
                    is_selected=self._is_selected,
                    offset=offset
                )
        #
        elif self._name_text is not None:
            painter._draw_text_by_rect_(
                self._name_draw_rect,
                self._name_text,
                text_color=self._name_draw_color,
                font=self._name_draw_font,
                text_option=self._name_text_option,
                is_hovered=self._is_hovered,
                is_selected=self._is_selected,
                offset=offset
            )
        #
        if self._index_text is not None:
            painter._draw_text_by_rect_(
                self._index_draw_rect,
                self._get_index_text_(),
                text_color=self._index_color,
                font=self._index_font,
                text_option=self._index_text_option,
                offset=offset
            )
        #
        if self._delete_draw_is_enable is True:
            painter._draw_icon_file_by_rect_(
                rect=self._delete_icon_draw_rect,
                file_path=self._delete_icon_file_path,
                offset=offset,
                is_hovered=self._delete_is_hovered
            )

    def _do_hover_move_(self, event):
        p = event.pos()
        self._is_check_hovered = False
        self._press_is_hovered = False
        self._delete_is_hovered = False

        if self._check_action_is_enable is True:
            if self._check_frame_rect.contains(p):
                self._is_check_hovered = True
        if self._frame_draw_rect.contains(p):
            self._press_is_hovered = True
        if self._delete_is_enable is True:
            if self._delete_action_rect.contains(p):
                self._delete_is_hovered = True
        #
        self._is_hovered = self._is_check_hovered or self._press_is_hovered or self._delete_is_hovered
        #
        self._refresh_widget_draw_()

    def _get_is_visible_(self):
        return self.isVisible()

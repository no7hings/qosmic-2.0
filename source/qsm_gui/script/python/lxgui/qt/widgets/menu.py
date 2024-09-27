# coding=utf-8
import six

import functools

import types

# gui
from ... import core as _gui_core
# qt
from ..core.wrap import *

from .. import core as _qt_core


class QtMenuNew(QtWidgets.QMenu):
    def __init__(self, *args, **kwargs):
        super(QtMenuNew, self).__init__(*args, **kwargs)
        self.setPalette(_qt_core.GuiQtDcc.generate_qt_palette())
        self.setAutoFillBackground(True)

        self.setFont(_qt_core.QtFonts.NameNormal)

        self.item_height = 22

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
        _qt_core.GuiQtMenuOpt(self).create_by_content(content, append)

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

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        for i_action in self.actions():
            if i_action.isVisible():
                opt = QtWidgets.QStyleOptionMenuItem()
                opt.initFrom(self)
                self.initStyleOption(opt, i_action)
                opt.rect = self.actionGeometry(i_action)
                opt.icon = i_action.icon()
                # style = self.style()
                self._draw_item_(painter, opt)
                # style.drawControl(QtWidgets.QStyle.CE_MenuItem, opt, painter)

    @classmethod
    def _draw_item_(cls, painter, option):
        painter.save()
        # print option.rect
        x, y, w, h = option.rect.x(), option.rect.y(), option.rect.width(), option.rect.height()
        frame_rect = QtCore.QRect(x+1, y+1, w-2, h-2)
        select_flag = not not option.state & QtWidgets.QStyle.State_Selected
        if select_flag:
            painter.fillRect(frame_rect, QtGui.QColor(*_gui_core.GuiRgba.LightAzureBlue))

        if select_flag:
            painter.setPen(QtGui.QColor(*_gui_core.GuiRgba.LightBlack))
        else:
            painter.setPen(QtGui.QColor(*_gui_core.GuiRgba.DarkWhite))

        if option.icon.isNull():
            icon_rect = QtCore.QRect(
                x, y,
                20, 20
            )
            option.icon.paint(painter, icon_rect)

        painter.drawText(frame_rect, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, option.text)
        painter.restore()

    def sizeHint(self):
        width = super(QtMenuNew, self).sizeHint().width()
        height = len(self.actions())*self.item_height

        style = self.style()
        panel_margin = style.pixelMetric(QtWidgets.QStyle.PM_MenuPanelWidth)
        v_margin = style.pixelMetric(QtWidgets.QStyle.PM_MenuVMargin)
        h_margin = style.pixelMetric(QtWidgets.QStyle.PM_MenuHMargin)

        total_height = height+2*(v_margin+panel_margin)
        total_width = width+2*(h_margin+panel_margin)

        return QtCore.QSize(total_width, total_height)

    def actionGeometry(self, action):
        index = self.actions().index(action)
        style = self.style()

        panel_margin = style.pixelMetric(QtWidgets.QStyle.PM_MenuPanelWidth)
        v_margin = style.pixelMetric(QtWidgets.QStyle.PM_MenuVMargin)
        h_margin = style.pixelMetric(QtWidgets.QStyle.PM_MenuHMargin)

        width = self.sizeHint().width()-2*(h_margin+panel_margin)

        return QtCore.QRect(
            h_margin+panel_margin, v_margin+panel_margin+index*self.item_height, width, self.item_height
        )

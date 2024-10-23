# coding:utf-8
import functools

import types

import six

import lxbasic.content as bsc_content

import lxbasic.core as bsc_core
# gui
from ... import core as _gui_core
# qt
from .wrap import *

from . import base as _base

from . import style as _style


class QtHBoxLayout(QtWidgets.QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QtHBoxLayout, self).__init__(*args, **kwargs)
        self.setContentsMargins(*_gui_core.GuiSize.LayoutDefaultContentsMargins)
        self.setSpacing(_gui_core.GuiSize.LayoutDefaultSpacing)

    def _set_align_as_top_(self):
        self.setAlignment(
            QtCore.Qt.AlignTop
        )

    def _set_align_as_left_(self):
        self.setAlignment(
            QtCore.Qt.AlignLeft
        )

    def _get_all_widgets_(self):
        list_ = []
        layout = self
        c = layout.count()
        if c:
            for i in range(c):
                item = layout.itemAt(i)
                if item:
                    widget = item.widget()
                    list_.append(widget)
        return list_

    def _delete_latest_(self):
        layout = self
        c = layout.count()
        if c:
            item = layout.itemAt(c - 1)
            if item:
                widget = item.widget()
                widget.close()
                widget.deleteLater()

    def _clear_all_widgets_(self):
        layout = self
        c = layout.count()
        if c:
            for i in range(c):
                i_item = layout.itemAt(i)
                if i_item:
                    i_widget = i_item.widget()
                    i_widget.close()
                    i_widget.deleteLater()


class QtVBoxLayout(QtWidgets.QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QtVBoxLayout, self).__init__(*args, **kwargs)
        self.setContentsMargins(*_gui_core.GuiSize.LayoutDefaultContentsMargins)
        self.setSpacing(_gui_core.GuiSize.LayoutDefaultSpacing)

    def _set_align_as_top_(self):
        self.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop
        )

    def _set_align_as_bottom_(self):
        self.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom
        )

    def _clear_all_widgets_(self):
        layout = self
        c = layout.count()
        if c:
            for i in range(c):
                i_item = layout.itemAt(i)
                if i_item:
                    i_widget = i_item.widget()
                    i_widget.close()
                    i_widget.deleteLater()


class QtGridLayout(QtWidgets.QGridLayout):
    def __init__(self, *args, **kwargs):
        super(QtGridLayout, self).__init__(*args, **kwargs)
        self.setContentsMargins(*_gui_core.GuiSize.LayoutDefaultContentsMargins)
        self.setSpacing(_gui_core.GuiSize.LayoutDefaultSpacing)

    def _get_widget_count_(self):
        return self.count()

    def _clear_all_widgets_(self):
        layout = self
        c = layout.count()
        if c:
            for i in range(c):
                i_item = layout.itemAt(i)
                if i_item:
                    i_widget = i_item.widget()
                    i_widget.deleteLater()

    def _add_widget_(self, widget, d=2):
        c = self.count()

        index = c
        #
        column = index % d
        row = int(index / d)
        self.addWidget(widget, row, column, 1, 1)


class QtFileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        super(QtFileDialog, self).__init__(*args, **kwargs)
        self.setPalette(_base.QtUtil.generate_qt_palette())


class QtSystemTrayIcon(QtWidgets.QSystemTrayIcon):
    press_clicked = qt_signal()
    press_dbl_clicked = qt_signal()
    press_toggled = qt_signal(bool)

    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        super(QtSystemTrayIcon, self).__init__(*args, **kwargs)
        
        menu = QtWidgets.QMenu()
        # self.setPalette(_base.GuiQtDcc.generate_qt_palette())
        menu.setAutoFillBackground(True)
        menu.setFont(_base.QtFonts.NameNormal)
        if QT_LOAD_INDEX == 0:
            menu.setStyleSheet(
                _style.QtStyle.get('QMenuNew')
            )
        else:
            menu.setStyleSheet(
                _style.QtStyle.get('QMenu')
            )
        self.setContextMenu(
            menu
        )
        #
        self._window = self.parent()
        self._set_quit_action_add_(menu)

        # noinspection PyUnresolvedReferences
        self.activated.connect(self._set_window_show_normal_)

    def _set_window_show_normal_(self, *args):
        r = args[0]
        if r == self.Trigger:
            # print 'AAA'
            # if self._window.isVisible():
            #     self._window.hide()
            # else:
            #     self._window.show()
            if self._window.isMinimized():
                self._window.showNormal()
                self._window.raise_()
                self._window.activateWindow()
            else:
                self._window.showMinimized()
        # if r == self.DoubleClick:
        #     if self._window.isVisible():
        #         self._window.hide()
        #     else:
        #         self._window.show()

    def _set_quit_action_add_(self, menu):
        widget_action = QtWidgetAction(menu)
        widget_action.setFont(_base.QtFonts.NameNormal)
        widget_action.setText('quit')
        widget_action.setIcon(_base.QtIcon.generate_by_icon_name('window/close'))
        menu.addAction(widget_action)
        # noinspection PyUnresolvedReferences
        widget_action.triggered.connect(
            self._window.close
        )


class QtWidgetAction(QtWidgets.QWidgetAction):
    def __init__(self, *args, **kwargs):
        super(QtWidgetAction, self).__init__(*args, **kwargs)
        self.setFont(_base.QtFonts.NameNormal)


class _QtSeparator(QtWidgets.QWidget):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        if self._text is not None:
            txt_w = self._font_metrics.width(self._text)
            self.setMinimumWidth(txt_w)
            self._text_rect.setRect(
                0, 0, txt_w, self.height()
            )

        self._rect.setRect(
            0, 0, self.width(), self.height()
        )

    def __init__(self, *args):
        super(_QtSeparator, self).__init__(*args)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        self._text = None
        self._text_rect = QtCore.QRect()
        self._font = _base.QtFonts.MenuSeparator
        self._font_metrics = QtGui.QFontMetrics(self._font)

        self._rect = QtCore.QRect()

        self.installEventFilter(self)

    def _set_text_(self, text):
        self._text = text

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setFont(self._font)
        painter.setPen(
            _style.QtRgba.Gray
        )
        painter.drawText(
            self._text_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, self._text
        )

        painter.setPen(
            _style.QtRgba.DarkGray
        )
        painter.drawLine(
            self._rect.bottomLeft(), self._rect.bottomRight()
        )

    def sizeHint(self):
        # must add size hint
        return QtCore.QSize(5, 20)


class QtWidgetActionForSeparator(QtWidgets.QWidgetAction):

    def __init__(self, *args, **kwargs):
        QtWidgets.QWidgetAction.__init__(self, *args, **kwargs)

        self._widget = QtWidgets.QWidget(*args, **kwargs)
        self._label = _QtSeparator(self._widget)

    def setText(self, text):
        self._label._set_text_(text)

    def createWidget(self, menu):

        wgt = self._widget

        lot = QtWidgets.QHBoxLayout(wgt)
        lot.setContentsMargins(0, 0, 0, 0)
        lot.addWidget(self._label)
        wgt.setLayout(lot)

        return wgt


class GuiQtMenuOpt(object):
    def __init__(self, menu):
        if isinstance(menu, QtWidgets.QMenu):
            self._root_menu = menu
            self._item_dic = {
                '/': self._root_menu
            }
        else:
            raise RuntimeError()

    @_gui_core.GuiModifier.run_with_exception_catch
    def _set_cmd_debug_run_(self, cmd_str):
        exec cmd_str

    @_gui_core.GuiModifier.run_with_exception_catch
    def _set_fnc_debug_run_(self, fnc):
        fnc()

    def create_by_content(self, content, append=False):
        if append is False:
            self._root_menu.clear()

            self._item_dic = {
                '/': self._root_menu
            }
        # when append is True, but item_dict not root key, we create new
        else:
            if '/' not in self._item_dic:
                self._item_dic = {
                    '/': self._root_menu
                }

        if isinstance(content, bsc_content.AbsContent):
            keys = content.get_keys(regex='*.properties')
            for i_key in keys:
                i_atr_path_opt = bsc_core.BscAttributePathOpt(i_key)
                i_path = i_atr_path_opt.obj_path
                i_path_opt = bsc_core.BscNodePathOpt(i_path)
                i_content = content.get_as_content(i_key)
                i_type = i_content.get('type')
                if i_path_opt.get_is_root():
                    pass
                else:
                    menu = self._create_menu_dag(i_path_opt.get_parent())
                    if i_type == 'separator':
                        self.add_separator_fnc(menu, i_content)
                    elif i_type == 'action':
                        self.add_action_fnc(menu, i_content)
                    elif i_type == 'group':
                        self._create_menu(menu, i_path_opt, i_content)

    def _create_menu_dag(self, path_opt):
        cur_menu = self._root_menu
        components = path_opt.get_components()
        # create from root
        components.reverse()
        for i_seq, i_component in enumerate(components):
            cur_menu = self._create_menu(cur_menu, i_component)
        return cur_menu

    def _create_menu(self, menu, path_opt, content=None):
        path = path_opt.path
        if path in self._item_dic:
            return self._item_dic[path]

        name = path_opt.name
        icon_name = 'file/folder'
        widget_action = QtWidgetAction(menu)
        menu.addAction(widget_action)
        widget_action.setFont(_base.QtFonts.NameNormal)
        if content is not None:
            name = content.get('name', name)
            icon_name = content.get('icon_name', icon_name)
            
        widget_action.setText(name)
        widget_action.setIcon(
            _base.QtIcon.generate_by_icon_name(icon_name)
        )
        sub_menu = menu.__class__(menu)
        # sub_menu.setTearOffEnabled(True)
        widget_action.setMenu(sub_menu)
        self._item_dic[path] = sub_menu
        return sub_menu

    @classmethod
    def add_separator_fnc(cls, menu, content):
        name = content.get('name')
        if name is not None:
            s = QtWidgetActionForSeparator(menu)
            s.setText(name)
            menu.addAction(s)
        else:
            s = menu.addSeparator()
            s.setFont(_base.QtFonts.MenuSeparator)
            s.setText(name)
        return s

    def add_action_fnc(self, menu, content):
        def set_disable_fnc_(widget_action_):
            widget_action_.setFont(_base.QtFonts.NameDisable)
            widget_action_.setDisabled(True)

        #
        name = content.get('name')
        icon_name = content.get('icon_name')
        executable_fnc = content.get('executable_fnc')
        execute_fnc = content.get('execute_fnc')
        widget_action = QtWidgetAction(menu)
        widget_action.setFont(_base.QtFonts.NameNormal)
        widget_action.setText(name)
        menu.addAction(widget_action)
        if icon_name:
            widget_action.setIcon(
                _base.QtIcon.generate_by_icon_name(icon_name)
            )
        else:
            widget_action.setIcon(
                _base.QtIcon.generate_by_text(name, background_color=(64, 64, 64))
            )
        #
        if isinstance(executable_fnc, (bool, int)):
            executable = executable_fnc
            if executable is False:
                set_disable_fnc_(widget_action)
        elif isinstance(executable_fnc, (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)):
            executable = executable_fnc()
            if executable is False:
                set_disable_fnc_(widget_action)
        #
        if isinstance(execute_fnc, (types.FunctionType, types.MethodType, functools.partial, types.LambdaType)):
            fnc = execute_fnc
            # noinspection PyUnresolvedReferences
            widget_action.triggered.connect(
                fnc
            )
        elif isinstance(execute_fnc, six.string_types):
            cmd = execute_fnc
            # noinspection PyUnresolvedReferences
            widget_action.triggered.connect(
                lambda *args, **kwargs: self._set_cmd_debug_run_(cmd)
            )
        return widget_action


class QtApplication(object):
    def __init__(self, app=None):
        if app is None:
            # noinspection PyArgumentList
            self._instance = QtWidgets.QApplication.instance()
        else:
            self._instance = None

    def set_process_run_0(self):
        if self._instance:
            self._instance.processEvents(
                QtCore.QEventLoop.ExcludeUserInputEvents
            )

    def set_process_run_1(self):
        if self._instance:
            self._instance.processEvents()

    @classmethod
    def show_tool_dialog(cls, *args, **kwargs):
        import lxgui.qt.widgets as gui_qt_widget

        w = gui_qt_widget.QtToolDialog()
        w._set_title_(kwargs.get('title', 'Dialog'))

        if 'widget' in kwargs:
            w._add_widget_(kwargs['widget'])

        w._do_window_show_(
            size=kwargs.get('size')
        )

    @classmethod
    def exec_message_dialog(cls, *args, **kwargs):
        import lxgui.qt.widgets as gui_qt_widget

        message = args[0]

        # noinspection PyArgumentList
        w = gui_qt_widget.QtMessageDialog(QtWidgets.QApplication.activeWindow())
        w._set_title_(kwargs.get('title', 'Dialog'))

        w._set_ok_visible_(True)
        if kwargs.get('show_no', False):
            w._set_no_visible_(True)
        if kwargs.get('show_cancel', False):
            w._set_cancel_visible_(True)
        w._set_message_(message)
        if 'status' in kwargs:
            status = kwargs['status']
            if status == 'warning':
                w._set_status_(
                    _gui_core.GuiValidationStatus.Warning
                )
            elif status == 'error':
                w._set_status_(
                    _gui_core.GuiValidationStatus.Error
                )
            elif status == 'correct':
                w._set_status_(
                    _gui_core.GuiValidationStatus.Correct
                )

        w._do_window_exec_(
            size=kwargs.get('size')
        )
        return w._get_result_()
    
    @classmethod
    def exec_input_dialog(cls, *args, **kwargs):
        import lxgui.qt.widgets as gui_qt_widget
        
        w = gui_qt_widget.QtInputDialog()
        w._set_title_(kwargs.get('title', 'Dialog'))

        if 'info' in kwargs:
            w._set_info_(kwargs['info'])

        if 'type' in kwargs:
            w._set_value_type_(kwargs['type'])

        if 'value' in kwargs:
            w._set_value_(kwargs['value'])

        w._do_window_exec_(
            size=kwargs.get('size')
        )
        return w._get_result_()

    @classmethod
    def is_ctrl_modifier(cls):
        # noinspection PyArgumentList
        return QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier

    @classmethod
    def is_shift_modifier(cls):
        # noinspection PyArgumentList
        return QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier

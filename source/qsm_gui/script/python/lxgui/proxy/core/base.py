# coding:utf-8
import sys

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from lxbasic.log import bridge as log_bridge
# gui
from ... import core as gui_core
# qt
from ...qt import core as gui_qt_core


class GuiProxyUtil(object):

    @classmethod
    def show_window_proxy_auto(
        cls, prx_window_cls, show_kwargs=None, window_process_fnc=None,
        window_unique_name=None, window_ask_for_close=False,
        **window_kwargs
    ):
        exists_app = gui_qt_core.QtUtil.get_exists_app()
        is_window_running = None
        # no application, etc. clarisse, ue
        if exists_app is None:
            # check show window as unique
            if window_unique_name is not None:
                if gui_qt_core.QT_LOAD_FLAG == 'pyqt':
                    shared_memory_key = window_unique_name
                    shared_memory = gui_qt_core.QtCore.QSharedMemory(shared_memory_key)

                    if shared_memory.attach():
                        is_window_running = True
                    else:
                        shared_memory.create(1)
                        is_window_running = False

            if is_window_running is True:
                import win32gui

                import win32con

                from ...qt.widgets import window_for_dialog as _qt_wgt_window_for_dialog

                app = gui_qt_core.QtUtil.create_app()

                w = _qt_wgt_window_for_dialog.QtMessageDialog()

                w._set_message_(
                    'Window "{}" is exists, press "Ok" show it, or close it and retry.'.format(window_unique_name)
                )
                w._set_buttons_(True)
                w._do_window_exec_()

                hwnd = win32gui.FindWindow(None, window_unique_name)
                if hwnd:
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(hwnd)

                sys.exit(0)

            app = gui_qt_core.QtUtil.create_app()

            prx_window = prx_window_cls(**window_kwargs)
            prx_window.set_main_window_geometry(gui_qt_core.GuiQtDcc.get_qt_main_window_geometry_args())
            if window_ask_for_close is True:
                prx_window.set_window_ask_for_close_enable(window_ask_for_close)

            # create system tray icon
            if window_unique_name is not None:
                qt_window = prx_window.widget
                qt_system_tray_icon = gui_qt_core.QtSystemTrayIcon(qt_window)
                qt_system_tray_icon.setIcon(qt_window.windowIcon())
                qt_system_tray_icon.show()
                qt_window._set_window_system_tray_icon_(qt_system_tray_icon)

            if isinstance(show_kwargs, dict):
                prx_window.show_window_auto(**show_kwargs)
            else:
                prx_window.show_window_auto()

            if window_process_fnc is not None:
                window_process_fnc(prx_window)

            gui_qt_core.GuiQtDcc.exit_app(app)
        # has application
        else:
            prx_window = prx_window_cls(**window_kwargs)
            prx_window.set_main_window_geometry(gui_qt_core.GuiQtDcc.get_qt_main_window_geometry_args())
            if window_ask_for_close is True:
                prx_window.set_window_ask_for_close_enable(window_ask_for_close)

            if isinstance(show_kwargs, dict):
                prx_window.show_window_auto(**show_kwargs)
            else:
                prx_window.show_window_auto()

            if window_process_fnc is not None:
                window_process_fnc(prx_window)

            if gui_qt_core.GuiQtDcc.get_is_clarisse():
                gui_qt_core.GuiQtDcc.exit_app(exists_app)
            elif gui_qt_core.GuiQtDcc.get_is_ue():
                gui_qt_core.GuiQtDcc.exit_app(exists_app)

    @staticmethod
    def find_widget_proxy_by_class(widget_proxy_cls):
        list_ = []
        # noinspection PyArgumentList
        qt_widgets = gui_qt_core.QtWidgets.QApplication.topLevelWidgets()
        if qt_widgets:
            for i_qt_widget in qt_widgets:
                if hasattr(i_qt_widget, 'gui_proxy'):
                    i_widget_proxy = i_qt_widget.gui_proxy
                    if i_widget_proxy.__class__.__name__ == widget_proxy_cls.__name__:
                        list_.append(i_widget_proxy)
        return list_

    @staticmethod
    def find_widget_proxy_by_category(category_includes):
        list_ = []
        # noinspection PyArgumentList
        qt_widgets = gui_qt_core.QtWidgets.QApplication.topLevelWidgets()
        if qt_widgets:
            for i_qt_widget in qt_widgets:
                if hasattr(i_qt_widget, 'gui_proxy'):
                    i_widget_proxy = i_qt_widget.gui_proxy
                    if i_widget_proxy.PRX_CATEGORY in category_includes:
                        list_.append(i_widget_proxy)
        return list_

    @staticmethod
    def find_all_tool_window_proxies():
        qt_widgets = gui_qt_core.QtUtil.find_all_valid_qt_windows()
        list_ = []
        for i_qt_widget in qt_widgets:
            if hasattr(i_qt_widget, 'gui_proxy'):
                i_widget_proxy = i_qt_widget.gui_proxy
                if hasattr(i_widget_proxy, 'PRX_CATEGORY'):
                    if i_widget_proxy.PRX_CATEGORY == 'tool_window':
                        list_.append(i_widget_proxy)
        return list_

    @staticmethod
    def window_proxy_trace_log(window_proxy, text):
        if hasattr(window_proxy, 'append_log_use_signal'):
            window_proxy.append_log_use_signal(text)

    @staticmethod
    def window_proxy_write_log(window_proxy, text):
        if hasattr(window_proxy, 'qt_log_write_fnc'):
            window_proxy.qt_log_write_fnc(text)

    @staticmethod
    def find_window_proxy_by_unique_id(unique_id):
        qt_windows = gui_qt_core.QtUtil.find_all_valid_qt_windows()
        for i_window in qt_windows:
            if hasattr(i_window, 'gui_proxy'):
                window_proxy = i_window.gui_proxy
                if hasattr(window_proxy, 'PRX_CATEGORY'):
                    if window_proxy.get_window_unique_id() == unique_id:
                        return window_proxy

    @staticmethod
    def find_window_proxy_by_session_name(name):
        qt_windows = gui_qt_core.QtUtil.find_all_valid_qt_windows()
        for i_window in qt_windows:
            if hasattr(i_window, 'gui_proxy'):
                window_proxy = i_window.gui_proxy
                if hasattr(window_proxy, 'PRX_TYPE'):
                    if window_proxy.PRX_TYPE == 'session_window':
                        if window_proxy.session.get_name() == name:
                            return window_proxy


class GuiLog(object):
    @staticmethod
    def trace_result(text):
        window_proxies = GuiProxyUtil.find_all_tool_window_proxies()
        if window_proxies:
            window_proxy = window_proxies[0]
            return GuiProxyUtil.window_proxy_trace_log(window_proxy, text)

    @staticmethod
    def trace_warning(text):
        window_proxies = GuiProxyUtil.find_all_tool_window_proxies()
        if window_proxies:
            window_proxy = window_proxies[0]
            return GuiProxyUtil.window_proxy_trace_log(window_proxy, text)

    @staticmethod
    def trace_error(text):
        window_proxies = GuiProxyUtil.find_all_tool_window_proxies()
        if window_proxies:
            window_proxy = window_proxies[0]
            return GuiProxyUtil.window_proxy_trace_log(window_proxy, text)

    @staticmethod
    def write(text):
        window_proxies = GuiProxyUtil.find_all_tool_window_proxies()
        if window_proxies:
            window_proxy = window_proxies[0]
            return GuiProxyUtil.window_proxy_write_log(window_proxy, text)


class GuiWindowModifier(object):
    @staticmethod
    def window_proxy_waiting(method):
        def sub_fnc_(*args, **kwargs):
            _window_proxy = args[0]
            _window_proxy.start_waiting()
            _fnc = method(*args, **kwargs)
            _window_proxy.stop_waiting()
            return _fnc
        return sub_fnc_


class GuiProgress(object):
    @staticmethod
    def create(maximum, label=None):
        list_ = []
        qt_windows = gui_qt_core.QtUtil.find_all_valid_qt_windows()
        for i_window in qt_windows:
            if hasattr(i_window, 'gui_proxy'):
                window_proxy = i_window.gui_proxy
                if hasattr(window_proxy, 'PRX_CATEGORY'):
                    if window_proxy.PRX_CATEGORY in {'tool_window', 'dialog_window'}:
                        p = window_proxy.create_progress_model(maximum, label=label)
                        list_.append(p)
        return list_


class GuiExceptionCatch(object):
    ValidationStatus = gui_core.GuiValidationStatus

    @classmethod
    def _generate_window(cls):
        from .. import widgets as gui_prx_widgets

        _0 = GuiProxyUtil.find_widget_proxy_by_category(['exception_window'])
        if _0:
            return _0[0]

        _1 = gui_prx_widgets.PrxWindowForException()

        _1.set_window_title('发生异常' if gui_core.GuiUtil.get_language() == 'chs' else 'Exception occurred')
        _1.set_definition_window_size((640, 320))
        _1.show_window_auto()
        return _1

    @classmethod
    def trace(cls):
        import sys

        text = bsc_core.Debug.get_error_stack()
        if text:
            w = cls._generate_window()
            w.set_status(cls.ValidationStatus.Error)
            w.add_content(text)
            w.set_status(cls.ValidationStatus.Error)

            # show in window
            w.add_content(text)

            # save file
            file_path = bsc_log.LogBase.get_user_debug_file(
                'script', create=True
            )
            bsc_storage.StgFileOpt(
                file_path
            ).set_write(text)

            # print
            sys.stderr.write(text+'\n')
            return w


class GuiProxyLogBridge(object):
    LOG_KEY = 'gui bridge'

    @classmethod
    def generate_for_log(cls):
        if log_bridge.__dict__['BRG_FNC_LOG_GUI_TRACE_ENABLE'] is False:
            log_bridge.__dict__['BRG_FNC_LOG_GUI_TRACE_ENABLE'] = True

            log_bridge.__dict__['BRG_FNC_LOG_GUI_TRACE_RESULT'] = GuiLog.trace_result
            log_bridge.__dict__['BRG_FNC_LOG_GUI_TRACE_WARNING'] = GuiLog.trace_warning
            log_bridge.__dict__['BRG_FNC_LOG_GUI_TRACE_ERROR'] = GuiLog.trace_error

            bsc_log.Log.trace_method_result(
                cls.LOG_KEY, 'generate log trace'
            )

    @classmethod
    def generate_for_process(cls):
        if log_bridge.__dict__['BRG_FNC_LOG_GUI_PROCESS_ENABLE'] is False:
            log_bridge.__dict__['BRG_FNC_LOG_GUI_PROCESS_ENABLE'] = True

            log_bridge.__dict__['BRG_FNC_LOG_GUI_PROCESS_CREATE'] = GuiProgress.create

            bsc_log.Log.trace_method_result(
                cls.LOG_KEY, 'generate log progress'
            )

    @classmethod
    def generate_for_exception(cls):
        if log_bridge.__dict__['BRG_FNC_LOG_GUI_EXCEPTION_ENABLE'] is False:
            log_bridge.__dict__['BRG_FNC_LOG_GUI_EXCEPTION_ENABLE'] = True

            log_bridge.__dict__['BRG_FNC_LOG_GUI_EXCEPTION_TRACE'] = GuiExceptionCatch.trace

            bsc_log.Log.trace_method_result(
                cls.LOG_KEY, 'generate log exception'
            )

    @classmethod
    def generate_all(cls):
        cls.generate_for_log()
        cls.generate_for_process()
        cls.generate_for_exception()

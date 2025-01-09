# coding:utf-8
import lxbasic.log as bsc_log

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import qsm_lazy_bks.worker as lzy_bks_worker

from . import qt as _gui_qt

from .pages import task as _page_task

from .pages import notice as _page_notice


class PrxLazyBackstageTool(gui_prx_widgets.PrxSessionWindow):
    SERVER_FLAG = True

    def __init__(self, session, *args, **kwargs):
        super(PrxLazyBackstageTool, self).__init__(session, *args, **kwargs)

    def gui_setup_fnc(self):
        self.set_main_style_mode(1)
        if self.SERVER_FLAG is True:
            self.start_web_socket_server()
            self.start_task_server()

        self._prx_tab_view = gui_prx_widgets.PrxTabView()
        self.add_widget(self._prx_tab_view)

        monitor_sca = gui_prx_widgets.PrxVScrollArea()
        self.add_widget(monitor_sca)

        self._prx_tab_view.add_widget(
            monitor_sca,
            key='task',
            name=gui_core.GuiUtil.choice_gui_name(
                self._language, self._session.configure.get('build.tabs.task')
            ),
            tool_tip='...'
        )

        self._monitor_prx_page = _page_task.PrxPageForTaskMonitor(
            self, self._session
        )
        monitor_sca.add_widget(self._monitor_prx_page)

        notice_sca = gui_prx_widgets.PrxVScrollArea()
        self.add_widget(notice_sca)

        self._prx_tab_view.add_widget(
            notice_sca,
            key='notice',
            name=gui_core.GuiUtil.choice_gui_name(
                self._language, self._session.configure.get('build.tabs.notice')
            ),
            tool_tip='...'
        )

        self._notice_prx_page = _page_notice.PrxPageForNoticeMonitor(
            self, self._session
        )
        notice_sca.add_widget(self._notice_prx_page)

        self.connect_refresh_action_for(
            lambda: self.gui_refresh_all(True)
        )

        if self.SERVER_FLAG is True:
            self._task_web_server.text_message_accepted.connect(
                self._monitor_prx_page._message_process_
            )

        self.gui_refresh_all()

        self._prx_tab_view.connect_current_changed_to(self.gui_refresh_all)

    def gui_refresh_all(self, force=False):
        key = self._prx_tab_view.get_current_key()
        if key == 'task':
            self._monitor_prx_page.do_gui_refresh_all(force)
        elif key == 'notice':
            self._notice_prx_page.do_gui_refresh_all(force)

    def start_web_socket_server(self):
        self._notice_web_server = gui_qt_core.QtWebServerForWindowNotice(self._qt_widget)
        self._notice_web_server._start_(
            lzy_bks_worker.NoticeWebServerBase.NAME,
            lzy_bks_worker.NoticeWebServerBase.HOST,
            lzy_bks_worker.NoticeWebServerBase.PORT
        )
        self._task_web_server = _gui_qt.QtWebServerForTask(self._qt_widget)
        self._task_web_server._start_(
            lzy_bks_worker.TaskWebServerBase.HOST, lzy_bks_worker.TaskWebServerBase.PORT
        )

    def start_task_server(self):
        def quit_server_fnc_():
            bsc_log.Log.trace_result(
                'quit server'
            )
            server_process.terminate()
            server_process.join()
            for i in qsm_prc_server.TaskWorker.PROCESS_STACK:
                i.terminate()
                # i.join()
            bsc_log.Log.trace_result(
                'quit server completed'
            )

        import qsm_lazy_bks.worker.server as qsm_prc_server

        server_process = qsm_prc_server.start_use_process(
            lzy_bks_worker.BackstageServerBase.HOST, lzy_bks_worker.BackstageServerBase.PORT
        )

        app = gui_qt_core.QtUtil.get_exists_app()

        app.aboutToQuit.connect(quit_server_fnc_)

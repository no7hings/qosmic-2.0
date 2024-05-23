# coding:utf-8
import lxgui.proxy.widgets as prx_widgets

from . import page_for_monitor as _page_for_monitor


class PnlTaskMonitor(prx_widgets.PrxSessionWindow):
    def __init__(self, session, *args, **kwargs):
        super(PnlTaskMonitor, self).__init__(session, *args, **kwargs)

    def gui_setup_window(self):
        self.set_main_style_mode(1)
        self._prx_tab_view = prx_widgets.PrxTabView()
        self.add_widget(self._prx_tab_view)

        monitor_sca = prx_widgets.PrxVScrollArea()
        self.add_widget(monitor_sca)

        self._prx_tab_view.add_widget(
            monitor_sca,
            key='monitor',
            name='Monitor',
            tool_tip='...'
        )
        
        self._monitor_prx_page = _page_for_monitor.PrxPageForMonitor(
            self, self._session
        )
        monitor_sca.add_widget(self._monitor_prx_page)

        notice_sca = prx_widgets.PrxVScrollArea()
        self.add_widget(notice_sca)

        self._prx_tab_view.add_widget(
            notice_sca,
            key='notice',
            name='Notice',
            tool_tip='...'
        )

        self.connect_refresh_action_for(self._monitor_prx_page._gui_task_opt.gui_refresh_tasks_all)

        self.gui_refresh_all()

    def gui_refresh_all(self, force=False):
        key = self._prx_tab_view.get_current_key()
        if key == 'monitor':
            self._monitor_prx_page.do_gui_refresh_all(force)

    def start_server(self):
        pass

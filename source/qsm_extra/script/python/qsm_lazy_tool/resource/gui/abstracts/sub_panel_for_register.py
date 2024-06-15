# coding:utf-8
import lxbasic.resource as bsc_resource

import lxgui.proxy.widgets as gui_prx_widgets

from . import page_for_register as _page_for_register


class AbsPrxSubPanelForRegister(gui_prx_widgets.PrxBaseWindow):
    PAGE_FOR_REGISTER_CLS = _page_for_register.AbsPrxPageForRegister

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxSubPanelForRegister, self).__init__(*args, **kwargs)
        if window is None:
            self._window = self
        else:
            self._window = window

        self._session = session

        self._configure = bsc_resource.RscExtendConfigure.get_as_content(
            'lazy/resource/register'
        )

        self.set_window_title(
            self._configure.get('option.gui.name')
        )
        self.set_definition_window_size(
            self._configure.get('option.gui.size')
        )

        self.gui_setup_window()

    def _do_dcc_register_all_script_jobs(self):
        raise NotImplementedError()

    def apply_and_close_fnc(self):
        self._register_prx_page.do_register()
        self.do_close_window_later(500)

    def apply_fnc(self):
        self._register_prx_page.do_register()

    def close_fnc(self):
        self.do_close_window_later(500)

    def gui_setup_window(self):
        prx_sca = gui_prx_widgets.PrxVScrollArea()
        self.add_widget(prx_sca)

        self._register_prx_page = self.PAGE_FOR_REGISTER_CLS(
            self._window, self._session
        )
        prx_sca.add_widget(self._register_prx_page)

        self._bottom_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self.add_widget(self._bottom_prx_tool_bar)
        self._bottom_prx_tool_bar.set_expanded(True)

        self._apply_and_close_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._apply_and_close_prx_button)
        self._apply_and_close_prx_button.set_name('Apply and Close')
        self._apply_and_close_prx_button.connect_press_clicked_to(
            self.apply_and_close_fnc
        )

        self._apply_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._apply_prx_button)
        self._apply_prx_button.set_name('Apply')
        self._apply_prx_button.connect_press_clicked_to(
            self.apply_fnc
        )

        self._close_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._close_prx_button)
        self._close_prx_button.set_name('Close')
        self._close_prx_button.connect_press_clicked_to(
            self.close_fnc
        )
        self._log_tool_bar.set_visible(False)


# coding:utf-8
import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxPanelForMontage(gui_prx_widgets.PrxBaseWindow):
    PAGE_FOR_RIG = None
    PAGE_CLASSES = []

    def __init__(self, session, window, *args, **kwargs):
        super(AbsPrxPanelForMontage, self).__init__(*args, **kwargs)
        if window is None:
            self._window = self
        else:
            self._window = window

        self._session = session

        self._language = gui_core.GuiUtil.get_language()

        self._configure = bsc_resource.RscExtendConfigure.get_as_content(
            'lazy-validation/gui/main'
        )

        self.set_window_title(
            gui_core.GuiUtil.choice_name(self._language, self._configure.get('option.gui'))
        )
        self.set_window_icon_by_name(
            self._configure.get('option.gui.icon_name')
        )
        self.set_definition_window_size(
            self._configure.get('option.gui.size')
        )

        self.gui_setup_fnc()

    def gui_setup_fnc(self):
        self._page_dict = {}

        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._page_prx_tab_tool_box)
        
        for i_cls in self.PAGE_CLASSES:
            i_page_key = i_cls.PAGE_KEY

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            self._page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_page_key,
                name=gui_core.GuiUtil.choice_name(
                    self._language, self._window._configure.get('build.{}.tab'.format(i_page_key))
                ),
                icon_name_text='composition',
                tool_tip=gui_core.GuiUtil.choice_tool_tip(
                    self._language, self._window._configure.get('build.{}.tab'.format(i_page_key))
                )
            )
            i_prx_page = i_cls(
                self._window, self._session
            )
            self._page_dict[i_page_key] = i_prx_page
            i_prx_sca.add_widget(i_prx_page)

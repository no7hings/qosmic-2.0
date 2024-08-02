# coding:utf-8
import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxSubPanelForMontage(gui_prx_widgets.PrxBaseWindow):
    PAGE_FOR_COMPOSITION = None

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxSubPanelForMontage, self).__init__(*args, **kwargs)
        if window is None:
            self._window = self
        else:
            self._window = window

        self._session = session

        self._language = gui_core.GuiUtil.get_language()

        self._configure = bsc_resource.RscExtendConfigure.get_as_content(
            'lazy-montage/gui/main'
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

        self.gui_setup_window()

    def gui_setup_window(self):
        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._page_prx_tab_tool_box)

        composition_prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._page_prx_tab_tool_box.add_widget(
            composition_prx_sca,
            key='composition',
            name=gui_core.GuiUtil.choice_name(
                self._language, self._window._configure.get('build.composition.tab')
            ),
            icon_name_text='composition',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._language, self._window._configure.get('build.composition.tab')
            )
        )
        self._composition_prx_page = self.PAGE_FOR_COMPOSITION(
            self._window, self._session
        )
        composition_prx_sca.add_widget(self._composition_prx_page)


# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

from ..toolsets import reference_fix as _toolset_reference_fix


class PrxPageForMotionFix(gui_prx_widgets.PrxBasePage):
    GUI_KEY = 'fix'

    UNIT_CLASSES = [
        _toolset_reference_fix.PrxToolsetReferenceFix
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForMotionFix, self).__init__(window, session, *args, **kwargs)

        self._configure = self.generate_local_configure()

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        self._tab_widget_dict = {}

        self._page_prx_tab_tool_box = self.gui_create_tab_tool_box()
        self._qt_layout.addWidget(self._page_prx_tab_tool_box.widget)

        self.gui_build_all_units()

        self._page_prx_tab_tool_box.load_history()

    def gui_build_all_units(self):
        self._tab_widget_dict = {}

        for i_cls in self.UNIT_CLASSES:
            i_unit_key = i_cls.GUI_KEY

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            self._page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_unit_key,
                name=gui_core.GuiUtil.choice_gui_name(
                    self._window._language,
                    self._configure.get('build.units.{}'.format(i_unit_key))
                ),
                icon_name_text=i_unit_key,
                tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                    self._window._language,
                    self._configure.get('build.units.{}'.format(i_unit_key))
                )
            )
            i_prx_unit = self._to_unit_instance(i_cls)
            self._tab_widget_dict[i_unit_key] = i_prx_unit
            i_prx_sca.add_widget(i_prx_unit)

    def do_gui_refresh_all(self):
        pass

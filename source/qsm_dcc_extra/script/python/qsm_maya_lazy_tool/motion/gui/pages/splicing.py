# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

from ..toolsets import splicing as _toolset_splicing


class PrxPageForMotionSplicing(gui_prx_widgets.PrxBasePage):
    GUI_KEY = 'splicing'

    UNIT_CLASS_DICT = dict(
        import_motion=_toolset_splicing.PrxToolsetForImportMotion
    )

    UNIT_CLASSES = [
        _toolset_splicing.PrxToolsetForImportMotion
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForMotionSplicing, self).__init__(window, session, *args, **kwargs)

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        self._tab_widget_dict = {}

        self._page_prx_tab_tool_box = self.gui_create_tab_tool_box()
        self._qt_layout.addWidget(self._page_prx_tab_tool_box.widget)

        self.gui_build_all_units()

        self._page_prx_tab_tool_box.load_history()

    def gui_build_all_units(self):
        for i_cls in self.UNIT_CLASSES:
            i_unit_key = i_cls.GUI_KEY

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            self._page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_unit_key,
                name=self.choice_gui_name(
                    self._configure.get('build.{}.units.{}'.format(self.GUI_KEY, i_unit_key))
                ),
                icon_name_text=i_unit_key,
                tool_tip=self.choice_gui_tool_tip(
                    self._configure.get('build.{}.units.{}'.format(self.GUI_KEY, i_unit_key))
                )
            )
            i_prx_unit = self._to_unit_instance(i_cls)
            self._tab_widget_dict[i_unit_key] = i_prx_unit
            i_prx_sca.add_widget(i_prx_unit)

    def do_gui_refresh_all(self):
        self._page_prx_tab_tool_box.save_history()

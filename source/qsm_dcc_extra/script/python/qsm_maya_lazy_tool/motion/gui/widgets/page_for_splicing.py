# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

from . import toolset_for_splicing as _toolset_for_splicing


class PrxPageForMotionSplicing(gui_prx_widgets.PrxBasePage):
    PAGE_KEY = 'splicing'
    
    UNIT_CLASS_DICT = dict(
        import_motion=_toolset_for_splicing.PrxToolsetForImportMotion
    )

    UNIT_CLASSES = [
        _toolset_for_splicing.PrxToolsetForImportMotion
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForMotionSplicing, self).__init__(window, session, *args, **kwargs)

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        self._unit_dict = {}

        self._page_prx_tab_tool_box = gui_prx_widgets.PrxVTabToolBox()
        self._qt_layout.addWidget(self._page_prx_tab_tool_box.widget)
        self._page_prx_tab_tool_box.set_tab_direction(self._page_prx_tab_tool_box.TabDirections.RightToLeft)

        self._gui_build_units()

    def _gui_build_units(self):
        for i_cls in self.UNIT_CLASSES:
            i_unit_key = i_cls.UNIT_KEY

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            self._page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_unit_key,
                name=gui_core.GuiUtil.choice_name(
                    self._window._language,
                    self._window._configure.get('build.{}.units.{}'.format(self.PAGE_KEY, i_unit_key))
                ),
                icon_name_text=i_unit_key,
                tool_tip=gui_core.GuiUtil.choice_tool_tip(
                    self._window._language,
                    self._window._configure.get('build.{}.units.{}'.format(self.PAGE_KEY, i_unit_key))
                )
            )
            i_prx_unit = self._to_unit_instance(i_cls)
            self._unit_dict[i_unit_key] = i_prx_unit
            i_prx_sca.add_widget(i_prx_unit)

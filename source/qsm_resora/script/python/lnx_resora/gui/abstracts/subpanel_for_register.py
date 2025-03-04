# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_screw.core as lnx_scr_core

import lnx_screw.scripts as lnx_scr_scripts


class AbsPrxSubPanelForRegister(gui_prx_widgets.PrxBaseSubpanel):
    # CONFIGURE_KEY = 'resora/gui/register'

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxSubPanelForRegister, self).__init__(window, session, *args, **kwargs)

        self.update_valid_subpage_cls()

    def gui_setup_fnc(self):
        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._page_prx_tab_tool_box)

    def update_valid_subpage_cls(self):
        type_names = lnx_scr_scripts.ManifestStageOpt.get_valid_type_names()
        for i_resource_type in type_names:
            i_cls = self.find_register_subpage_cls(i_resource_type)
            if i_cls:
                self._sub_page_class_dict[i_resource_type] = i_cls

    @staticmethod
    def find_register_subpage_cls(resource_type):
        # noinspection PyBroadException
        try:
            module_path = 'lnx_resora_extra.{}.gui_widgets.register'.format(resource_type.replace('/', '.'))
            module = bsc_core.PyModule(module_path)
            if module.get_is_exists():
                cls = module.get_method('PrxSubpageForRegister')
                if cls:
                    return cls
        except Exception:
            pass
    
    def gui_setup_pages_for(self, resource_types):
        for i_resource_type in resource_types:

            if i_resource_type not in self._sub_page_class_dict:
                continue

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            i_prx_page = self._subwindow.gui_generate_sub_page_for(i_resource_type)
            i_prx_sca.add_widget(i_prx_page)

            self._page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_resource_type,
                name=i_prx_page.get_gui_name(),
                icon_name_text=i_resource_type,
                tool_tip=i_prx_page.get_gui_tool_tip()
            )
            self._tab_widget_dict[i_resource_type] = i_prx_page

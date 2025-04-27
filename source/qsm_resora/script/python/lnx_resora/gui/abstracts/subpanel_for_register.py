# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_screw.scripts as lnx_scr_scripts


class AbsPrxSubPanelForRegister(gui_prx_widgets.PrxBaseSubpanel):
    # CONFIGURE_KEY = 'resora/gui/register'

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxSubPanelForRegister, self).__init__(window, session, *args, **kwargs)

    def gui_setup_fnc(self):
        self._page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._page_prx_tab_tool_box)

    @staticmethod
    def _gui_find_register_subpage_cls(resource_type):
        # noinspection PyBroadException
        try:
            module_path = 'lnx_resora_extra.{}.gui_widgets.register'.format(resource_type.replace('/', '.'))
            module = bsc_core.PyMod(module_path)
            if module.is_exists():
                cls = module.get('GuiResourceRegisterMain')
                if cls:
                    bsc_log.Log.trace(
                        'find register gui for {} successful.'.format(resource_type)
                    )
                    return cls
        except Exception:
            pass
    
    def gui_setup_pages_for(self, resource_types):
        for i_resource_type in resource_types:

            if i_resource_type in self._subpage_class_dict:
                i_prx_page_cls = self._subpage_class_dict[i_resource_type]
            else:
                i_prx_page_cls = self._gui_find_register_subpage_cls(i_resource_type)

            if i_prx_page_cls:
                i_prx_page = self.gui_instance_subpage(i_prx_page_cls)
            else:
                raise RuntimeError()

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            i_prx_sca.add_widget(i_prx_page)

            self._page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_resource_type,
                name=i_prx_page.get_gui_name(),
                icon_name_text=i_resource_type,
                tool_tip=i_prx_page.get_gui_tool_tip()
            )
            self._tab_widget_dict[i_resource_type] = i_prx_page

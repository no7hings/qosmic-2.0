# coding:utf-8
import sys

import lxbasic.core as bsc_core

import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxSubpanelForTaskCreate(gui_prx_widgets.PrxBaseSubpanel):
    CONFIGURE_KEY = 'wotrix/gui/task_create'

    GUI_KEY = 'task_create'

    PROJECT_TASKS =[
    ]
    ASSET_TASKS = [
    ]
    SEQUENCE_TASKS = [
    ]
    SHOT_TASKS = [
    ]

    TASK_MODULE_ROOT = None

    @classmethod
    def _find_gui_cls(cls, resource_type, task):
        # noinspection PyBroadException
        try:
            module_path = '{}.{}.{}.gui_widgets.task_create'.format(
                cls.TASK_MODULE_ROOT, resource_type, task
            )
            module = bsc_core.PyModule(module_path)
            if module.get_is_exists():
                gui_cls = module.get_method('GuiTaskCreateMain')
                if gui_cls:
                    sys.stdout.write('find task create gui for {}/{} successful.\n'.format(resource_type, task))
                    return gui_cls
        except Exception:
            pass

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxSubpanelForTaskCreate, self).__init__(window, session, *args, **kwargs)

    def gui_setup_fnc(self):
        self._sub_page_prx_tab_tool_box = gui_prx_widgets.PrxHTabToolBox()
        self.add_widget(self._sub_page_prx_tab_tool_box)

        self._sub_page_prx_tab_tool_box.connect_current_changed_to(
            self.do_gui_refresh_all
        )

    def gui_setup(self, prx_widget, resource_properties):
        self._prx_widget = prx_widget

        resource_type = resource_properties['resource_type']
        self._resource_properties = resource_properties
        if resource_type == 'project':
            self.gui_setup_subpages_for(resource_type, self.PROJECT_TASKS)
        elif resource_type == 'asset':
            self.gui_setup_subpages_for(resource_type, self.ASSET_TASKS)
        elif resource_type == 'sequence':
            self.gui_setup_subpages_for(resource_type, self.SEQUENCE_TASKS)
        elif resource_type == 'shot':
            self.gui_setup_subpages_for(resource_type, self.SHOT_TASKS)

        self._sub_page_prx_tab_tool_box.set_history_key(
            [self._window.GUI_KEY, '{}_{}.page'.format(self._gui_path, resource_type)]
        )
        self._sub_page_prx_tab_tool_box.load_history()

    def gui_setup_subpages_for(self, resource_type, tasks):
        self._tab_widget_dict = {}

        for i_task in tasks:
            i_gui_key = '{}/{}'.format(resource_type, i_task)

            i_prx_page = None

            # when is register, use register cls, either use auto find
            if i_gui_key in self._sub_page_class_dict:
                i_prx_page = self._subwindow.gui_generate_subpage_for(i_gui_key)
            else:
                i_gui_cls = self._find_gui_cls(resource_type, i_task)
                if i_gui_cls:
                    i_prx_page = self._subwindow.gui_instance_subpage(i_gui_cls)

            if i_prx_page is None:
                continue

            i_prx_sca = gui_prx_widgets.PrxVScrollArea()
            i_prx_sca.add_widget(i_prx_page)

            self._sub_page_prx_tab_tool_box.add_widget(
                i_prx_sca,
                key=i_gui_key,
                name=i_prx_page.get_gui_name(),
                icon_name_text=i_gui_key,
                tool_tip=i_prx_page.get_gui_tool_tip()
            )

            self._tab_widget_dict[i_gui_key] = i_prx_page

    def do_gui_refresh_all(self):
        key = self._sub_page_prx_tab_tool_box.get_current_key()
        page = self._tab_widget_dict.get(key)
        if page:
            page.do_gui_refresh_all()

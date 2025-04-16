# coding:utf-8
import lxbasic.core as bsc_core


import lxgui.qt.view_widgets as gui_qt_view_widgets


import lnx_parsor.parse as lnx_prs_parse


class _GuiBaseOpt(object):
    def __init__(self, window, unit, session):
        self._window = window
        self._unit = unit
        self._session = session

        self._gui_thread_flag = 0

    def gui_update_thread_flag(self):
        self._gui_thread_flag += 1


class _GuiTaskFilterOpt(_GuiBaseOpt):
    def __init__(self, *args, **kwargs):
        super(_GuiTaskFilterOpt, self).__init__(*args, **kwargs)

        self._qt_tag_widget = gui_qt_view_widgets.QtTagWidget()
        self._unit._prx_v_splitter.add_widget(self._qt_tag_widget)
        self._qt_tag_widget._view_model.set_item_expand_record_enable(True)

        self._qt_tag_widget.refresh.connect(self.gui_load_all_task_tags)

        self._qt_tag_widget._view.check_paths_change_accepted.connect(
            self.gui_refresh_tasks
        )

    def _gui_add_entity_groups(self, path):
        path_opt = bsc_core.BscNodePathOpt(path)

        ancestor_paths = path_opt.get_ancestor_paths()
        ancestor_paths.reverse()

        for i_path in ancestor_paths:
            i_flag, i_qt_item = self._qt_tag_widget._view_model.create_group_item(i_path)
            if i_flag is True:
                i_qt_item._item_model.set_expanded(True)

    def gui_load_all_task_tags(self):
        self._qt_tag_widget._view_model.restore()

        resource_type = self._unit.RESOURCE_TYPE
        task_paths = lnx_prs_parse.Stage().generate_wsp_task_paths(resource_type)
        for i in task_paths:
            self.gui_add_task_tag(i)

    def gui_add_task_tag(self, path):
        self._gui_add_entity_groups(path)
        self._qt_tag_widget._view_model.create_item(path)

    def gui_refresh_tasks(self, task_paths):
        options = {}
        for i in task_paths:
            i_ = i.split('/')
            i_step, i_task = i_[-2:]
            options.setdefault('step', []).append(i_step)
            options.setdefault('task', []).append(i_task)

        self._unit._gui_task_opt.gui_update_task_options(options)

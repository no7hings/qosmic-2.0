# coding:utf-8
import functools

import os

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.qt.view_widgets as gui_qt_view_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_parsor.core as lnx_prs_core

import lnx_parsor.swap as lnx_prs_swap

from ... import core as _wsp_core

from . import unit_base as _unit_base


class _GuiTaskFilterOpt(_unit_base._GuiBaseOpt):
    def __init__(self, *args, **kwargs):
        super(_GuiTaskFilterOpt, self).__init__(*args, **kwargs)
        
        self._prs_root = lnx_prs_swap.Swap.generate_root()

        self._qt_tag_widget = gui_qt_view_widgets.QtTagWidget()
        self._unit._prx_h_splitter.add_widget(self._qt_tag_widget)
        self._qt_tag_widget._view_model.set_item_expand_record_enable(True)
        # self._qt_tag_widget._view_model.set_item_color_enable(True)
        self._qt_tag_widget._view_model.set_menu_name_dict(self._window._configure.get('build.menu_names'))
        
        self._qt_tag_widget.refresh.connect(
            functools.partial(self.do_gui_refresh_all, force=True)
        )
    
    def do_gui_refresh_all(self, force=False):
        self.gui_load_all_filters()

    def gui_load_all_filters(self):
        self.gui_load_all_tags()

    def _gui_add_entity_groups(self, path):
        path_opt = bsc_core.BscNodePathOpt(path)

        ancestor_paths = path_opt.get_ancestor_paths()
        ancestor_paths.reverse()

        for i_path in ancestor_paths:
            i_flag, i_qt_item = self._qt_tag_widget._view_model.create_group_item(i_path)
            if i_flag is True:
                i_qt_item._item_model.set_expanded(True)
                i_qt_item._item_model.set_icon_name('workspace/null')

                if i_path == '/':
                    i_qt_item._item_model.set_name('All')

    def gui_load_all_tags(self):
        self._gui_thread_flag += 1

        project_path_set = set()
        role_path_set = set()
        step_path_set = set()

        for i_project in self._prs_root.projects():
            i_project_path = u'/Project/{}'.format(i_project.name)
            project_path_set.add(i_project_path)

            if self._unit.RESOURCE_TYPE == lnx_prs_core.ResourceTypes.Asset:
                for j_role in i_project.roles():
                    j_role_path = u'/Role/{}'.format(j_role.name)
                    role_path_set.add(j_role_path)
            # todo: add episode filter for shot?
            # elif self._unit.RESOURCE_TYPE == lnx_prs_core.ResourceTypes.Shot:
            #     for j_episode in i_project.episodes():
            #         j_episode_path = u'/Episode/{}'.format(j_episode.name)
            #         role_path_set.add(j_episode_path)

            i_steps = i_project.steps(resource_type=self._unit.RESOURCE_TYPE)
            for j_step in i_steps:
                j_step_path = u'/Step/{}'.format(j_step)
                step_path_set.add(j_step_path)

        for i in list(project_path_set):
            self.gui_add_tag(i, self._gui_thread_flag)

        for i in list(role_path_set):
            self.gui_add_tag(i, self._gui_thread_flag)

        for i in list(step_path_set):
            self.gui_add_tag(i, self._gui_thread_flag)

    def gui_add_tag(self, path, gui_thread_flag):
        self._gui_add_entity_groups(path)

        flag, qt_item = self._qt_tag_widget._view_model.create_item(path)


class _GuiTaskOpt(_unit_base._GuiBaseOpt):
    def __init__(self, *args, **kwargs):
        super(_GuiTaskOpt, self).__init__(*args, **kwargs)

        self._qt_tree_widget = gui_qt_view_widgets.QtTreeWidget()
        self._unit._prx_h_splitter.add_widget(self._qt_tree_widget)
        self._qt_tree_widget._set_item_sort_enable(True)
        self._qt_tree_widget._view_model.set_item_expand_record_enable(True)
        self._qt_tree_widget._view_model.set_menu_name_dict(self._window._configure.get('build.menu_names'))

        self._qt_tree_widget.refresh.connect(
            functools.partial(self.do_gui_refresh_all, force=True)
        )

        self._task_options = {}
    
    def do_gui_refresh_all(self, force=False):
        self.gui_load_all_tasks(sync_flag=force)

    def gui_update_task_options(self, options):
        self._task_options = options
        self.gui_load_all_tasks()

    def _gui_add_entity_groups(self, path):
        path_opt = bsc_core.BscNodePathOpt(path)

        ancestor_paths = path_opt.get_ancestor_paths()
        ancestor_paths.reverse()

        for i_path in ancestor_paths:
            i_flag, i_qt_item = self._qt_tree_widget._view_model.create_item(i_path)
            if i_flag is True:
                i_qt_item._item_model.set_expanded(True)
                i_qt_item._item_model.set_icon_name('workspace/null')

    def gui_load_all_tasks(self, sync_flag=False):
        pass


class AbsPrxUnitForTaskOverview(gui_prx_widgets.PrxBaseUnit):
    GUI_KEY = 'task_tracker'

    TASK_PARSE_CLS = None

    RESOURCE_TYPE = None

    def __init__(self, *args, **kwargs):
        super(AbsPrxUnitForTaskOverview, self).__init__(*args, **kwargs)

        self._project = None
        self._space_key = 'release'

        self.gui_unit_setup_fnc()

    def gui_unit_setup_fnc(self):
        prx_v_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_v_sca.widget)

        self._prx_h_splitter = gui_prx_widgets.PrxHSplitter()
        prx_v_sca.add_widget(self._prx_h_splitter)

        self._gui_task_filter_opt = _GuiTaskFilterOpt(self._window, self, self._session)

        self._gui_task_opt = _GuiTaskOpt(self._window, self, self._session)

        self._prx_h_splitter.set_fixed_size_at(0, 320)

    def do_gui_refresh_all(self):
        self._gui_task_filter_opt.do_gui_refresh_all()

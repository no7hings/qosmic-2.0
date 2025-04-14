# coding:utf-8
import functools

import os

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.qt.view_widgets as gui_qt_view_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_parsor.parse as lnx_srk_parse

from ... import core as _wsp_core

from . import unit_base as _unit_base


class _GuiTaskFilterOpt(_unit_base._GuiBaseOpt):
    def __init__(self, *args, **kwargs):
        super(_GuiTaskFilterOpt, self).__init__(*args, **kwargs)

        self._qt_tree_widget = gui_qt_view_widgets.QtTreeWidget()
        self._unit._prx_h_splitter.add_widget(self._qt_tree_widget)
        self._qt_tree_widget._set_item_sort_enable_(True)
        self._qt_tree_widget._view_model.set_item_expand_record_enable(True)
        self._qt_tree_widget._view_model.set_menu_name_dict(self._window._configure.get('build.menu_names'))


class _GuiTaskOpt(_unit_base._GuiBaseOpt):
    def __init__(self, *args, **kwargs):
        super(_GuiTaskOpt, self).__init__(*args, **kwargs)

        self._qt_tree_widget = gui_qt_view_widgets.QtTreeWidget()
        self._unit._prx_h_splitter.add_widget(self._qt_tree_widget)
        self._qt_tree_widget._set_item_sort_enable_(True)
        self._qt_tree_widget._view_model.set_item_expand_record_enable(True)
        self._qt_tree_widget._view_model.set_menu_name_dict(self._window._configure.get('build.menu_names'))

        self._qt_tree_widget.refresh.connect(
            functools.partial(self.gui_load_all_tasks, sync_flag=True)
        )

        self._task_options = {}

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

    def do_gui_load_project(self, scn_entity):
        pass
        # project = scn_entity.name
        # if project != self._project:
        #     self._project = project
        #     self._gui_task_opt.gui_load_all_tasks()
        #     self._gui_task_filter_opt.gui_load_all_task_tags()

    def do_gui_refresh_all(self):
        scn_entity = self._page.get_scn_entity()
        if scn_entity is not None:
            self.do_gui_load_project(scn_entity)
            project = scn_entity.name
            space_key = self._page._space_key
            if project != self._project or space_key != self._space_key:
                self._project = project
                self._space_key = space_key
                self._gui_task_opt.gui_load_all_tasks()

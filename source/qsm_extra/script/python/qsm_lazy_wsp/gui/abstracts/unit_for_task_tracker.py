# coding:utf-8
import functools

import os

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.qt.view_widgets as gui_qt_view_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_shark.parse as qsm_srk_parse

from ... import core as _wsp_core

from . import unit_base as _unit_base


class _GuiTaskOpt(_unit_base._GuiBaseOpt):
    def __init__(self, *args, **kwargs):
        super(_GuiTaskOpt, self).__init__(*args, **kwargs)

        self._task_unit_path = None
        self._task_unit_path_tmp = None

        self._qt_tree_widget = gui_qt_view_widgets.QtTreeWidget()
        self._unit._prx_v_splitter.add_widget(self._qt_tree_widget)
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
        project = self._unit._project
        space_key = self._unit._space_key

        self._qt_tree_widget._view_model.restore()

        self.gui_update_thread_flag()

        ett_project = qsm_srk_parse.Stage().project(
            project,
            space_key=space_key
        )
        if ett_project:
            self.gui_add_project(ett_project, self._gui_thread_flag, space_key, sync_flag)

    def gui_add_project(self, ett_project, gui_thread_flag, space_key, sync_flag):
        def cache_fnc_():
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]

            if resource_type == _wsp_core.TaskParse.ResourceTypes.Project:
                return [
                    ett_project.tasks(space_key=space_key, sync_flag=sync_flag), gui_thread_flag
                ]
            elif resource_type == _wsp_core.TaskParse.ResourceTypes.Asset:
                return [
                    ett_project.assets(space_key=space_key, sync_flag=sync_flag), gui_thread_flag
                ]
            elif resource_type == _wsp_core.TaskParse.ResourceTypes.Sequence:
                return [
                    ett_project.sequences(space_key=space_key, sync_flag=sync_flag), gui_thread_flag
                ]
            elif resource_type == _wsp_core.TaskParse.ResourceTypes.Shot:
                return [
                    ett_project.shots(space_key=space_key, sync_flag=sync_flag), gui_thread_flag
                ]

            return [
                [], 0
            ]

        def build_fnc_(data_):
            _ett_resources, _gui_thread_flag = data_
            if _gui_thread_flag != self._gui_thread_flag:
                return

            _, _entity_qt_item = self._qt_tree_widget._view_model.create_item(path)
            _entity_qt_item._item_model.set_icon_name('workspace/null')
            _entity_qt_item._item_model.set_expanded(True)

            if resource_type == _wsp_core.TaskParse.ResourceTypes.Project:
                _entity_qt_item._item_model.set_menu_data(
                    [
                        (
                            'jump_to_task_manager', 'workspace/task',
                            functools.partial(self.gui_jump_to_task_manager, ett_project)
                        )
                    ]
                )
                [self.gui_add_task(_x, _gui_thread_flag, space_key) for _x in _ett_resources]
            else:
                [self.gui_add_resource(_x, _gui_thread_flag, space_key, sync_flag) for _x in _ett_resources]

        if gui_thread_flag != self._gui_thread_flag:
            return

        resource_type = self._unit.RESOURCE_TYPE
        path = ett_project.path

        self._gui_add_entity_groups(path)

        trd = self._qt_tree_widget._view._generate_thread_(
            cache_fnc_, build_fnc_
        )

        trd.do_start()

    def gui_add_resource(self, ett_resource, gui_thread_flag, space_key, sync_flag):
        def cache_fnc_():
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]

            _source_directory_ptn = qsm_srk_parse.Stage().generate_pattern_opt_for(
                '{}-source-dir'.format(resource_type), **ett_resource.variants
            )
            _source_directory_path = _source_directory_ptn.get_value()

            _release_directory_ptn = qsm_srk_parse.Stage().generate_pattern_opt_for(
                '{}-release-dir'.format(resource_type), **ett_resource.variants
            )
            _release_directory_path = _release_directory_ptn.get_value()

            return [
                [
                    _source_directory_path, _release_directory_path,
                    ett_resource.tasks(
                        space_key=space_key, sync_flag=sync_flag,
                        **self._task_options
                    )
                ],
                gui_thread_flag
            ]

        def build_fnc_(data_):
            _d, _gui_thread_flag = data_
            if _gui_thread_flag != self._gui_thread_flag:
                return

            if _d:
                _source_directory_path, _release_directory_path, _ett_tasks = _d
                _, _entity_qt_item = self._qt_tree_widget._view_model.create_item(path)
                _entity_qt_item._item_model.set_icon_name('workspace/null')
                _entity_qt_item._item_model.set_expanded(True)

                _entity_qt_item._item_model.set_menu_data(
                    [
                        (
                            'jump_to_task_manager', 'workspace/task',
                            functools.partial(self.gui_jump_to_task_manager, ett_resource)
                        ),
                        [
                            'open', 'file/folder',
                            [
                                (
                                    'work_server_directory', 'file/folder',
                                    functools.partial(
                                        bsc_storage.StgExplorer.open_directory, _source_directory_path
                                    )
                                ),
                                (
                                    'release_directory', 'file/folder',
                                    functools.partial(
                                        bsc_storage.StgExplorer.open_directory, _release_directory_path
                                    )
                                )
                            ]
                        ]
                    ]
                )

                [self.gui_add_task(_x, _gui_thread_flag, sync_flag) for _x in _ett_tasks]

        if gui_thread_flag != self._gui_thread_flag:
            return

        path = ett_resource.path
        resource_type = ett_resource.variants.resource_type
        self._gui_add_entity_groups(path)

        trd = self._qt_tree_widget._view._generate_thread_(
            cache_fnc_, build_fnc_
        )

        trd.do_start()

    def gui_jump_to_task_manager(self, ett_resource):
        resource_type = ett_resource.variants.resource_type
        page = self._window.gui_set_current_page('task_manager')
        unit = page.gui_set_current_page(resource_type)
        unit.gui_jump_to_resource(ett_resource)

    def gui_add_task(self, ett_task, gui_thread_flag, sync_flag):
        def cache_fnc_():
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]

            return [
                ett_task.versions(space_key='release', sync_flag=sync_flag), gui_thread_flag
            ]

        def build_fnc_(data_):
            _ett_versions, _gui_thread_flag = data_
            if _gui_thread_flag != self._gui_thread_flag:
                return

            _, _entity_qt_item = self._qt_tree_widget._view_model.create_item(path)
            _entity_qt_item._item_model.set_icon_name('workspace/task')
            _entity_qt_item._item_model.set_expanded(True)

            c = len(_ett_versions)
            _entity_qt_item._item_model.set_number(c)
            _entity_qt_item._item_model.set_assign_data('task', ett_task)
            _entity_qt_item._item_model.set_assign_data('versions', _ett_versions)

        if gui_thread_flag != self._gui_thread_flag:
            return

        path = ett_task.path

        self._gui_add_entity_groups(path)

        trd = self._qt_tree_widget._view._generate_thread_(
            cache_fnc_, build_fnc_
        )

        trd.do_start()

    def gui_get_ett_versions(self):
        list_ = []
        _ = self._qt_tree_widget._view_model.get_selected_items()
        if _:
            qt_item = _[-1]
            _ = qt_item._item_model.get_descendants()
            # is not task
            if _:
                flag = False
                paths = [x._item_model.get_path() for x in _]
                leaf_paths = bsc_core.BscNodePath.to_leaf_paths(paths)
            # is task
            else:
                flag = True
                leaf_paths = [qt_item._item_model.get_path()]

            if leaf_paths:
                for i_path in leaf_paths:
                    i_item = self._qt_tree_widget._view_model.find_item(i_path)
                    if i_item:
                        i_ett_versions = i_item._item_model.get_assign_data('versions')
                        if i_ett_versions:
                            if flag is True:
                                list_.extend(i_ett_versions)
                            else:
                                list_.append(i_ett_versions[-1])
        return list_


class _GuiVersionOpt(_unit_base._GuiBaseOpt):

    def __init__(self, *args, **kwargs):
        super(_GuiVersionOpt, self).__init__(*args, **kwargs)

        self._qt_list_widget = gui_qt_view_widgets.QtListWidget()
        self._unit._prx_h_splitter.add_widget(self._qt_list_widget)

        self._qt_list_widget._set_item_sort_enable_(True)
        self._qt_list_widget._view_model.apply_item_sort_order(
            self._qt_list_widget._view_model.ItemSortOrder.Descending
        )
        # self._qt_list_widget._set_item_group_enable_(True)
        self._qt_list_widget._view_model.set_item_category_enable(True)
        self._qt_list_widget._view_model.set_item_mtime_enable(True)
        self._qt_list_widget._view_model.set_item_user_enable(True)

        self._qt_list_widget._view_model.set_item_frame_size(190, 100)
        self._qt_list_widget._view_model.set_menu_name_dict(self._window._configure.get('build.menu_names'))

        self._qt_list_widget.refresh.connect(self.gui_load_all_versions)

    def gui_load_all_versions(self):
        self._qt_list_widget._view_model.restore()

        self.gui_update_thread_flag()

        ett_versions = self._unit._gui_task_opt.gui_get_ett_versions()
        for i in ett_versions:
            self.gui_add_version(i, self._gui_thread_flag)

    def gui_add_version(self, ett_version, gui_thread_flag):
        def cache_fnc_():
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]

            _release_directory_ptn = qsm_srk_parse.Stage().generate_pattern_opt_for(
                '{}-release-version-dir'.format(resource_type), **ett_version.variants
            )
            _release_directory_path = _release_directory_ptn.get_value()

            _release_preview_ptn = qsm_srk_parse.Stage().generate_pattern_opt_for(
                '{}-release-preview-mov-file'.format(resource_type), **ett_version.variants
            )
            _release_preview_path = _release_preview_ptn.get_value()
            if os.path.isfile(_release_preview_path):
                _video = _release_preview_path
            else:
                _video = None
            # mtime
            _mtime = bsc_storage.StgFileOpt(_release_directory_path).get_mtime()
            _user = bsc_storage.StgFileOpt(_release_directory_path).get_user()
            return [
                [_mtime, _user, _video, _release_directory_path], gui_thread_flag
            ]

        def build_fnc_(data_):
            _d, _gui_thread_flag = data_
            if _gui_thread_flag != self._gui_thread_flag:
                return

            if _d:
                _mtime, _user, _video, _folder = _d
                qt_item._item_model.set_mtime(_mtime)
                if _user:
                    qt_item._item_model.set_user(_user)

                if _video:
                    qt_item._item_model.set_video(_video)
                    qt_item._item_model.register_press_dbl_click_fnc(
                        functools.partial(
                            bsc_storage.StgPath.start_in_system, _video
                        )
                    )

                qt_item._item_model.set_menu_data(
                    [
                        (
                            'open_folder', 'file/folder',
                            functools.partial(bsc_storage.StgExplorer.open_directory, _folder)
                        )
                    ]
                )

        if gui_thread_flag != self._gui_thread_flag:
            return

        path = ett_version.path
        resource_type = ett_version.variants.resource_type
        flag, qt_item = self._qt_list_widget._view_model.create_item(path)

        name_var = dict(ett_version.variants)
        name_var['resource_name'] = None

        name = '{resource}.{step}.{task}.v{version}'.format(
            **ett_version.variants
        )
        qt_item._item_model.set_name(name)
        qt_item._item_model.set_icon_name('workspace/version')

        qt_item._item_model.set_show_fnc(
            cache_fnc_, build_fnc_
        )


class AbsPrxUnitForTaskTracker(gui_prx_widgets.PrxBaseUnit):
    GUI_KEY = 'task_tracker'

    TASK_PARSE_CLS = None

    RESOURCE_TYPE = None

    def __init__(self, *args, **kwargs):
        super(AbsPrxUnitForTaskTracker, self).__init__(*args, **kwargs)

        self._project = None
        self._space_key = 'release'

        self.gui_unit_setup_fnc()

    def gui_unit_setup_fnc(self):
        prx_v_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_v_sca.widget)

        self._prx_h_splitter = gui_prx_widgets.PrxHSplitter()
        prx_v_sca.add_widget(self._prx_h_splitter)

        self._prx_v_splitter = gui_prx_widgets.PrxVSplitter()
        self._prx_h_splitter.add_widget(self._prx_v_splitter)

        self._gui_task_opt = _GuiTaskOpt(self._window, self, self._session)

        self._gui_task_filter_opt = _unit_base._GuiTaskFilterOpt(self._window, self, self._session)

        self._gui_version_opt = _GuiVersionOpt(self._window, self, self._session)
        self._gui_task_opt._qt_tree_widget._view.item_select_changed.connect(
            self._gui_version_opt.gui_load_all_versions
        )

        self._prx_h_splitter.set_fixed_size_at(0, 320)
        self._prx_v_splitter.set_fixed_size_at(1, 320)

    def do_gui_load_project(self, scn_entity):
        project = scn_entity.name
        if project != self._project:
            self._project = project
            self._gui_task_opt.gui_load_all_tasks()
            self._gui_task_filter_opt.gui_load_all_task_tags()

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

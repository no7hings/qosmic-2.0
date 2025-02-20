# coding:utf-8
import functools

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.qt.view_widgets as gui_qt_view_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_general.core as qsm_gnl_core


class _GuiBaseOpt(object):
    def __init__(self, window, unit, session):
        self._window = window
        self._unit = unit
        self._session = session

        self._gui_thread_flag = 0

    def gui_update_thread_flag(self):
        self._gui_thread_flag += 1


class _GuiSourceTaskOpt(_GuiBaseOpt):
    def __init__(self, *args, **kwargs):
        super(_GuiSourceTaskOpt, self).__init__(*args, **kwargs)

        self._task_unit_history_group = [self._window.GUI_KEY, 'task_manager']
        self._task_unit_path_tmp = None

        self._qt_tree_widget = gui_qt_view_widgets.QtTreeWidget()
        self._unit._prx_h_splitter.add_widget(self._qt_tree_widget)
        self._qt_tree_widget._set_item_sort_enable_(True)
        self._qt_tree_widget._view_model.set_item_expand_record_enable(True)
        self._qt_tree_widget._view_model.set_menu_name_dict(self._window._configure.get('build.menu_names'))

        self._qt_tree_widget.refresh.connect(self.gui_load_all_tasks)

        # application
        self._application = 'maya'
        self._application_switch_qt_tool_box = self._qt_tree_widget._add_left_tool_box_('application')
        self._gui_add_application_switch_tools()
        
        # extra
        self._extra_qt_tool_box = self._qt_tree_widget._add_left_tool_box_('extra')
        self._gui_add_extra_tools()

    def _gui_add_application_switch_tools(self):

        if bsc_core.BscApplication.get_is_maya():
            self._application = 'maya'
            cfg = [
                ('maya', 'application/maya')
            ]
        elif bsc_core.BscApplication.get_is_houdini():
            self._application = 'houdini'
            cfg = [
                ('houdini', 'application/houdini')
            ]
        elif bsc_core.BscApplication.get_is_katana():
            self._application = 'katana'
            cfg = [
                ('katana', 'application/katana')
            ]
        else:
            self._application = 'maya'
            cfg = [
                ('maya', 'application/maya'), ('houdini', 'application/houdini'), ('katana', 'application/katana')
            ]

        tools = []
        for i_application, i_icon_name in cfg:
            i_tool = gui_prx_widgets.PrxToggleButton()
            self._application_switch_qt_tool_box._add_widget_(i_tool)
            i_tool._qt_widget._set_exclusive_widgets_(tools)
            i_tool.set_name(i_application)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip('"LMB-click" for switch to scale to "{}"'.format(i_application))

            if i_application == self._application:
                i_tool.set_checked(True)

            tools.append(i_tool._qt_widget)
            i_tool.connect_check_changed_as_exclusive_to(
                functools.partial(self._gui_switch_application, i_application)
            )

    def _gui_switch_application(self, application):
        if application != self._application:
            self._application = application

            self.gui_load_all_tasks()
            self._window.popup_message(
                self._window.choice_gui_message(
                    self._window._configure.get('build.messages.switch_application')
                ).format(application=self._application)
            )

    def _gui_add_extra_tools(self):
        self._setting_qt_button = gui_qt_widgets.QtIconPressButton()
        self._extra_qt_tool_box._add_widget_(self._setting_qt_button)
        self._setting_qt_button._set_name_text_('setting')
        self._setting_qt_button._set_icon_name_('option')
        self._setting_qt_button._set_tool_tip_('Press Show Setting')

    def gui_add_root_auto(self, path):
        path_opt = bsc_core.BscNodePathOpt(path)

        parent_path = path_opt.get_parent_path()

        flag, item = self._qt_tree_widget._view_model.create_root_item(path=parent_path, name='All')
        if flag is True:
            item._item_model.set_expanded(True)
            item._item_model.set_icon_name('workspace/null')

    def gui_load_all_tasks(self):
        def cache_fnc_():
            _task_dir_ptn_opt = self._unit._task_parse.generate_pattern_opt_for(
                '{}-source-task-dir'.format(self._unit.RESOURCE_TYPE), **resource_properties
            )
            _matches = _task_dir_ptn_opt.find_matches()
            return [_matches, self._gui_thread_flag]

        def build_fnc_(data_):
            _matches, _gui_thread_flag = data_
            if _gui_thread_flag != self._gui_thread_flag:
                return

            if _matches:
                for _i_match in _matches:
                    _i_task_variants = dict(resource_properties)
                    _i_task_variants.update(_i_match)
                    self.gui_add_task(_i_task_variants, _gui_thread_flag)

        self._qt_tree_widget._view_model.restore()

        self.gui_update_thread_flag()

        self._unit.gui_update_task_session()

        resource_properties = self._unit._resource_properties
        resource_type = resource_properties['resource_type']

        # if force is True:
        #     # restore this variant?
        self.gui_load_task_unit_history(resource_type)

        if resource_properties is None:
            return

        trd = self._qt_tree_widget._view._generate_thread_(
            cache_fnc_, build_fnc_
        )

        trd.do_start()

    def gui_add_task(self, task_variants, gui_thread_flag):
        def cache_fnc_():
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]

            _task_unit_ptn_opt = self._unit._task_parse.generate_pattern_opt_for(
                '{}-source-task_unit-dir'.format(self._unit.RESOURCE_TYPE), **task_variants
            )
            _matches = _task_unit_ptn_opt.find_matches()
            return [_matches, self._gui_thread_flag]

        def build_fnc_(data_):
            _matches, _gui_thread_flag = data_
            if _gui_thread_flag != self._gui_thread_flag:
                return

            if _matches:
                for _i_match in _matches:
                    _i_task_unit_variants = dict(task_variants)
                    _i_task_unit_variants.update(_i_match)
                    self.gui_add_task_unit(_i_task_unit_variants, _gui_thread_flag)

            qt_item._item_model.set_menu_data(
                [
                    ('open_folder', 'file/folder', open_folder_fnc_)
                ]
            )

            qt_item._item_model.set_tool_tip(directory_path)

        def open_folder_fnc_():
            bsc_storage.StgExplorer.open_directory(directory_path)

        directory_path = task_variants['result']

        path = self._unit._task_parse.to_wsp_task_path(**task_variants)

        self.gui_add_root_auto(path)

        flag, qt_item = self._qt_tree_widget._view_model.create_item(path)
        if flag is True:
            task_variants['entity_type'] = 'task'
            task_variants['path'] = path
            qt_item._item_model.set_assign_properties(task_variants)

            qt_item._item_model.set_icon_name('workspace/task')
            qt_item._item_model.set_expanded(True)
            qt_item._item_model.set_show_fnc(cache_fnc_, build_fnc_)

    def gui_add_task_unit(self, task_unit_variants, gui_thread_flag):
        def cache_fnc_():
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]

            _task_scene_ptn_opt = self._unit._task_parse.generate_source_task_scene_src_pattern_opt_for(
                application=self._application,
                **task_unit_variants
            )
            _matches = _task_scene_ptn_opt.find_matches(sort=True)
            return [
                _matches, gui_thread_flag
            ]

        def build_fnc_(data_):
            def press_dbl_click_fnc_():
                if _matches:
                    _task_unit_scene_variants = dict(task_unit_variants)
                    _task_unit_scene_variants.update(_matches[-1])

                    self._unit.on_open_task_scene(_task_unit_scene_variants)
                    self._unit.gui_update_current_task_unit(_task_unit_scene_variants)

            _matches, _gui_thread_flag = data_
            if _gui_thread_flag != self._gui_thread_flag:
                return

            _c = len(_matches)
            qt_item._item_model.set_number(_c)
            qt_item._item_model.set_menu_data(
                [
                    ('open_folder', 'file/folder', open_folder_fnc_)
                ]
            )

            qt_item._item_model.register_press_dbl_click_fnc(press_dbl_click_fnc_)

            qt_item._item_model.set_tool_tip(directory_path)

        def open_folder_fnc_():
            bsc_storage.StgExplorer.open_directory(directory_path)

        directory_path = task_unit_variants['result']
        task_unit = task_unit_variants['task_unit']
        path = self._unit._task_parse.to_wsp_task_unit_path(**task_unit_variants)
        resource_type = task_unit_variants['resource_type']

        flag, qt_item = self._qt_tree_widget._view_model.create_item(path)
        if flag is True:
            task_unit_variants['entity_type'] = 'task_unit'
            task_unit_variants['path'] = path
            qt_item._item_model.set_assign_properties(task_unit_variants)

            if task_unit == 'main':
                qt_item._item_model.set_icon_name('workspace/task-unit-main')
            else:
                qt_item._item_model.set_icon_name('workspace/task-unit')

            if self._unit._task_session is not None:
                resource_path = self._unit._resource_path
                task_unit_path = self._unit._task_session.task_unit_path
                # check is task unit is current resource
                if task_unit_path.startswith(resource_path):
                    if path == task_unit_path:
                        qt_item._item_model.focus_select()
                        qt_item._item_model.set_status(
                            qt_item._item_model.Status.Correct
                        )
                else:
                    if path.endswith('main'):
                        self.gui_save_task_unit_history(path, resource_type)
                        qt_item._item_model.focus_select()
            else:
                if self._task_unit_path_tmp is None:
                    # select main as default
                    if path.endswith('main'):
                        self.gui_save_task_unit_history(path, resource_type)
                        qt_item._item_model.focus_select()
                else:
                    if path == self._task_unit_path_tmp:
                        qt_item._item_model.focus_select()

            qt_item._item_model.set_show_fnc(cache_fnc_, build_fnc_)
        return path

    def gui_get_current_entity_variants(self):
        items = self._qt_tree_widget._view_model.get_selected_items()
        if items:
            item = items[-1]
            return item._item_model.get_assign_properties()

    def gui_set_current_task_unit_path(self, path):
        pass

    def gui_get_task_unit_variants_list_by_task_path(self, task_path):
        list_ = []
        task_item = self._qt_tree_widget._view_model.find_item(task_path)
        if task_item:
            task_unit_items = task_item._item_model.get_children()
            for i_task_unit_item in task_unit_items:
                i_task_unit_variants = i_task_unit_item._item_model.get_assign_properties()
                if i_task_unit_variants:
                    list_.append(i_task_unit_variants)
        return list_

    def gui_get_all_task_unit_paths(self):
        return self._qt_tree_widget._view_model.get_all_item_paths()

    def do_gui_refresh_task_unit(self, task_unit_path):
        qt_item = self._qt_tree_widget._view_model.find_item(task_unit_path)
        if qt_item is not None:
            qt_item._item_model.focus_select()

            self._qt_tree_widget._view_model.clear_all_items_status()
            qt_item._item_model.set_status(
                qt_item._item_model.Status.Correct
            )

    def do_gui_refresh_all(self):
        self._qt_tree_widget._view_model.clear_all_items_status()

        task_session = self._unit._task_session
        if task_session is not None:
            task_unit_path = task_session.task_unit_path
            qt_item = self._qt_tree_widget._view_model.find_item(task_unit_path)
            if qt_item is not None:
                qt_item._item_model.set_status(qt_item._item_model.Status.Correct)
                qt_item._item_model.focus_select()

    def gui_load_task_unit_history(self, resource_type=None):
        self._task_unit_path_tmp = gui_core.GuiHistoryStage().get_one(
            self._task_unit_history_group+[resource_type]
        )
        return self._task_unit_path_tmp

    def gui_save_task_unit_history(self, task_unit_path, resource_type=None):
        self._task_unit_path_tmp = task_unit_path
        gui_core.GuiHistoryStage().set_one(
            self._task_unit_history_group+[resource_type],
            self._task_unit_path_tmp
        )

    def gui_restore(self):
        self._qt_tree_widget._view_model.restore()


class _GuiSourceTaskUnitSceneOpt(_GuiBaseOpt):

    def find_thumbnail(self, application, **kwargs):
        thumbnail_ptn_opt = self._unit._task_parse.generate_source_task_thumbnail_pattern_opt_for(
            application, **kwargs
        )
        return thumbnail_ptn_opt.get_value()

    def __init__(self, *args, **kwargs):
        super(_GuiSourceTaskUnitSceneOpt, self).__init__(*args, **kwargs)

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

        self._qt_list_widget.refresh.connect(self.gui_load_task_unit_scenes)

    def gui_load_task_unit_scenes(self):
        self._qt_list_widget._view_model.restore()

        self.gui_update_thread_flag()
        application = self._unit._gui_task_opt._application

        entity_variants = self._unit._gui_task_opt.gui_get_current_entity_variants()
        if not entity_variants:
            return

        entity_type = entity_variants['entity_type']
        if entity_type == 'task':
            self.gui_load_task_unit_scene_for_task(application, entity_variants, self._gui_thread_flag)
        elif entity_type == 'task_unit':
            self.gui_load_task_unit_scene_for_task_unit(application, entity_variants, self._gui_thread_flag)

    def gui_load_task_unit_scene_for_task(self, application, task_variants, gui_thread_flag):
        def cache_fnc_():
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]

            _task_unit_scene_variants_list = []

            _task_path = task_variants['path']
            _task_unit_variants_list = self._unit._gui_task_opt.gui_get_task_unit_variants_list_by_task_path(_task_path)
            for _i_task_unit_variants in _task_unit_variants_list:
                _i_task_scene_ptn_opt = self._unit._task_parse.generate_source_task_scene_src_pattern_opt_for(
                    application=application,
                    **_i_task_unit_variants
                )
                _i_matches = _i_task_scene_ptn_opt.find_matches()
                _i_task_unit_scene_variants = dict(_i_task_unit_variants)
                _i_task_unit_scene_variants.update(_i_matches[-1])
                _task_unit_scene_variants_list.append(_i_task_unit_scene_variants)
            return [
                _task_unit_scene_variants_list, gui_thread_flag
            ]

        def build_fnc_(data_):
            _task_unit_variants_list, _gui_thread_flag = data_

            for _i_task_scene_variants in _task_unit_variants_list:
                self.gui_add_task_unit_scene(application, _i_task_scene_variants, _gui_thread_flag)

        trd = self._qt_list_widget._view._generate_thread_(
            cache_fnc_, build_fnc_
        )

        trd.do_start()

    def gui_load_task_unit_scene_for_task_unit(self, application, task_unit_variants, gui_thread_flag):
        def cache_fnc_():
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]

            _task_scene_ptn_opt = self._unit._task_parse.generate_source_task_scene_src_pattern_opt_for(
                application=application,
                **task_unit_variants
            )
            _matches = _task_scene_ptn_opt.find_matches()
            _task_unit_scene_variants_list = []
            for _i_match in _matches[-10:]:
                _i_task_scene_variants = dict(task_unit_variants)
                _i_task_scene_variants.update(_i_match)
                _task_unit_scene_variants_list.append(_i_task_scene_variants)
            return [
                _task_unit_scene_variants_list, gui_thread_flag
            ]

        def build_fnc_(data_):
            _task_unit_scene_variants_list, _gui_thread_flag = data_

            for _i_task_scene_variants in _task_unit_scene_variants_list:
                self.gui_add_task_unit_scene(application, _i_task_scene_variants, _gui_thread_flag)

        trd = self._qt_list_widget._view._generate_thread_(
            cache_fnc_, build_fnc_
        )

        trd.do_start()

    def _gui_task_menu_generate_fnc(self, application, scene_path, thumbnail_path):
        def show_in_explorer_fnc_():
            bsc_storage.StgFileOpt(scene_path).show_in_system()

        def copy_path_fnc_():
            gui_qt_core.QtUtil.write_clipboard(scene_path.replace('/', '\\'))

        def copy_unit_path_fnc_():
            gui_qt_core.QtUtil.write_clipboard(scene_path)

        menu_data = [
            ('show_in_explorer', 'file/folder', show_in_explorer_fnc_),
            [
                'copy', 'tool/copy',
                [
                    ('path', 'file/file', copy_path_fnc_),
                    ('unix_path', 'file/file', copy_unit_path_fnc_),
                ],
            ],
        ]

        sub_menu_data_for_send = []
        if self._unit._artist != self._unit._artist_self:
            sub_menu_data_for_send.append(
                (
                    'my_space', 'file/file',
                    functools.partial(self._send_to_self_space_fnc, scene_path, thumbnail_path)
                )
            )
        if self._unit._artist != self._unit._artist_shared:
            sub_menu_data_for_send.append(
                (
                    'shared_space', 'file/file',
                    functools.partial(self._send_to_share_space_fnc, scene_path, thumbnail_path)
                )
            )
        if sub_menu_data_for_send:
            menu_data.append(
                [
                    'send_to', 'tool/copy',
                    sub_menu_data_for_send,
                ]
            )

        if bsc_core.BscApplication.get_is_dcc() is False:
            if application == 'maya':
                sub_menu_data = []
                maya_exe_dict = qsm_gnl_core.MayaBin.generate_dict()

                for k, v in maya_exe_dict.items():
                    sub_menu_data.append(
                        (k, 'file/file', functools.partial(qsm_gnl_core.MayaBin.open_file, v, scene_path))
                    )

                menu_data.append(
                    [
                        'launch_local', 'application/{}'.format(application),
                        sub_menu_data
                    ]
                )
        return menu_data

    def _send_to_self_space_fnc(self, scene_path, thumbnail_path):
        self._send_to_space_fnc(self._unit._artist_self, scene_path, thumbnail_path)

    def _send_to_share_space_fnc(self, scene_path, thumbnail_path):
        self._send_to_space_fnc(self._unit._artist_shared, scene_path, thumbnail_path)

    def _send_to_space_fnc(self, artist, scene_path, thumbnail_path):

        application = self._unit._gui_task_opt._application

        # to user
        new_task_session_0 = self._unit._task_parse.generate_task_session_by_resource_source_scene_src(
            scene_path, artist=artist
        )

        task_units = new_task_session_0.get_all_task_units()
        if not task_units:
            task_units.append('main')

        result = gui_core.GuiApplication.exec_input_dialog(
            type='choose',
            info='Choose or entry a name...',
            options=task_units,
            value=task_units[0],
            title='Save As'
        )
        if not result:
            return

        if result:
            # to task unit
            new_task_session_1 = self._unit._task_parse.generate_task_session_by_resource_source_scene_src(
                scene_path, artist=artist, task_unit=result
            )
            new_task_session_1.send_source_task_scene_src(
                application, scene_path, thumbnail_path
            )

    def gui_add_task_unit_scene(self, application, task_unit_scene_variants, gui_thread_flag):
        def cache_fnc_():
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]
            # mtime
            _mtime = bsc_storage.StgFileOpt(scene_src_path).get_mtime()
            # user
            _artist = bsc_storage.StgFileOpt(scene_src_path).get_user()
            return [
                [_mtime, _artist], gui_thread_flag
            ]

        def build_fnc_(data_):
            _d, _gui_thread_flag = data_
            if _gui_thread_flag != self._gui_thread_flag:
                return

            if _d:
                _mtime, _artist = _d
                qt_item._item_model.set_mtime(_mtime)
                if _artist:
                    qt_item._item_model.set_user(_artist)

            qt_item._item_model.set_tool_tip(scene_src_path)

        def press_dbl_click_fnc_():
            self._unit.on_open_task_scene(task_unit_scene_variants)
            self._unit.gui_update_current_task_unit(task_unit_scene_variants)

        scene_src_path = task_unit_scene_variants['result']

        path = self._unit._task_parse.to_wsp_task_unit_scene_path(**task_unit_scene_variants)

        flag, qt_item = self._qt_list_widget._view_model.create_item(path)
        if flag is True:
            # image
            thumbnail_path = self.find_thumbnail(application, **task_unit_scene_variants)
            if thumbnail_path:
                qt_item._item_model.set_image(thumbnail_path)

            name = '{task_unit}.v{version}'.format(**task_unit_scene_variants)

            qt_item._item_model.set_name(name)
            qt_item._item_model.set_icon_name('application/{}'.format(application))
            qt_item._item_model.set_category(task_unit_scene_variants['task_unit'])
            qt_item._item_model.set_show_fnc(
                cache_fnc_, build_fnc_
            )

            qt_item._item_model.set_menu_data_generate_fnc(
                functools.partial(self._gui_task_menu_generate_fnc, application, scene_src_path, thumbnail_path)
            )

            if self._unit._task_session is not None:
                if path == self._unit._task_session.scene_src_path:
                    qt_item._item_model.set_status(
                        qt_item._item_model.Status.Correct
                    )
                    qt_item._item_model.focus_select()

            qt_item._item_model.register_press_dbl_click_fnc(press_dbl_click_fnc_)

    def do_gui_refresh_task_scene_for(self, properties):
        path = self._unit._task_parse.to_wsp_task_unit_scene_path(**properties)
        qt_item = self._qt_list_widget._view_model.find_item(path)
        if qt_item is not None:
            self._qt_list_widget._view_model.clear_all_items_status()
            qt_item._item_model.set_status(
                qt_item._item_model.Status.Correct
            )
            qt_item._item_model.focus_select()
        else:
            self.gui_load_task_unit_scenes()

    def do_gui_refresh_all(self):
        self._qt_list_widget._view_model.clear_all_items_status()
        task_session = self._unit._task_session
        if task_session is not None:
            scene_src_path = task_session.scene_src_path
            qt_item = self._qt_list_widget._view_model.find_item(scene_src_path)
            if qt_item is not None:
                qt_item._item_model.set_status(
                    qt_item._item_model.Status.Correct
                )
                qt_item._item_model.focus_select()

    def gui_restore(self):
        self._qt_list_widget._view_model.restore()


class AbsPrxUnitForTaskManager(gui_prx_widgets.PrxBaseUnit):
    GUI_KEY = 'task_manager'

    TASK_PARSE_CLS = None

    RESOURCE_TYPE = None

    def on_open_task_scene(self, task_unit_scene_variants):
        scene_path = task_unit_scene_variants.get('result')
        bsc_storage.StgExplorer.open_file(scene_path)
        return False

    def gui_update_current_task_unit(self, task_unit_scene_variants):
        path = self._task_parse.to_wsp_task_unit_path(**task_unit_scene_variants)
        resource_type = task_unit_scene_variants['resource_type']
        self._gui_task_opt.gui_save_task_unit_history(path, resource_type)

    def on_increment_and_save_task_scene(self):
        # regenerate a session to save
        task_session = self._task_parse.generate_task_session_by_resource_source_scene_src_auto()
        if task_session:
            with self._window.gui_minimized():
                task_unit_scene_variants = task_session.increment_and_save_source_task_scene_src()
                if task_unit_scene_variants:
                    scene_path = task_unit_scene_variants.get('result')
                    if scene_path:
                        self.gui_load_task_unit_scene(task_unit_scene_variants)

    def on_save_task_scene_as(self):
        task_session = self._task_parse.generate_task_session_by_resource_source_scene_src_auto()
        if task_session:
            task_units = task_session.get_all_task_units()
            result = gui_core.GuiApplication.exec_input_dialog(
                type='choose',
                info='Choose or entry a name...',
                options=task_units,
                value=task_units[0],
                title='Save As'
            )
            if not result:
                return

            with self._window.gui_minimized():
                properties = task_session.save_source_task_scene_scr_to(result)
                if properties:
                    scene_path = properties.get('result')
                    if scene_path:
                        self.gui_load_task_unit_scene(properties)

    def __init__(self, *args, **kwargs):
        super(AbsPrxUnitForTaskManager, self).__init__(*args, **kwargs)
        self._resource_properties = None

        self._task_parse = self.TASK_PARSE_CLS()
        self._task_session = None

        self._artist_self = bsc_core.BscSystem.get_user_name()

        self._artist_shared = 'shared'
        self._artist = self._artist_shared

        self._scan_resource_path = None
        self._resource_path = None

        self.gui_unit_setup_fnc()

    def dcc_set_scene_project(self, task_session):
        pass

    def gui_load_task_unit_scene(self, task_unit_scene_variants):
        scene_path = task_unit_scene_variants.get('result')
        if scene_path:
            task_session = self._task_parse.generate_task_session_by_resource_source_scene_src(scene_path)
            if task_session:
                self._task_session = task_session
                # set project for maya
                self.dcc_set_scene_project(task_session)

                task_unit_path = task_session.task_unit_path
                if task_unit_path in self._gui_task_opt.gui_get_all_task_unit_paths():
                    self.do_gui_refresh_task_unit(task_unit_path)
                    self.do_gui_refresh_task_scene_for(task_unit_scene_variants)
                else:
                    self.do_gui_refresh_all_tasks()

    def do_gui_refresh_task_unit(self, task_unit_path):
        self._gui_task_opt.do_gui_refresh_task_unit(task_unit_path)

    def do_gui_refresh_task_scene_for(self, task_unit_scene_variants):
        self._gui_task_scene_opt.do_gui_refresh_task_scene_for(task_unit_scene_variants)

    def do_gui_refresh_all_tasks(self):
        self._gui_task_opt.gui_load_all_tasks()

    def _on_gui_left_visible_swap(self, boolean):
        self._prx_h_splitter.swap_contract_left_or_top_at(0)

    def _do_gui_refresh_resource_for(self, scan_resource_path):
        self._resource_properties = None
        self._resource_path = None

        scan_resource_prx_input = self._page.gui_get_scan_resource_prx_input(self.RESOURCE_TYPE)
        scan_entity = scan_resource_prx_input.get_entity(scan_resource_path)

        if scan_entity is not None:
            scan_resource_properties = scan_entity.properties
            scan_resource_type = scan_entity.type.lower()
            if scan_resource_type == self.RESOURCE_TYPE:
                if scan_entity.type == self._task_parse.EntityTypes.Project:
                    resource_properties = dict(
                        project=scan_resource_properties.project,
                        resource_type='project',
                        file_format='ma',
                        artist=self._artist,
                    )
                    self._resource_path = self._task_parse.to_wsp_resource_path(**resource_properties)

                    self.gui_setup(resource_properties)
                if scan_entity.type == self._task_parse.EntityTypes.Asset:
                    resource_properties = dict(
                        project=scan_resource_properties.project,
                        resource_type='asset',
                        role=scan_resource_properties.role,
                        asset=scan_resource_properties.asset,
                        file_format='ma',
                        artist=self._artist,
                    )
                    self._resource_path = self._task_parse.to_wsp_resource_path(**resource_properties)

                    self.gui_setup(resource_properties)
                elif scan_entity.type == self._task_parse.EntityTypes.Sequence:
                    resource_properties = dict(
                        project=scan_resource_properties.project,
                        resource_type='sequence',
                        episode=scan_resource_properties.episode,
                        sequence=scan_resource_properties.sequence,
                        file_format='ma',
                        artist=self._artist,
                    )
                    self._resource_path = self._task_parse.to_wsp_resource_path(**resource_properties)

                    self.gui_setup(resource_properties)
                elif scan_entity.type == self._task_parse.EntityTypes.Shot:
                    resource_properties = dict(
                        project=scan_resource_properties.project,
                        resource_type='shot',
                        episode=scan_resource_properties.episode,
                        sequence=scan_resource_properties.sequence,
                        shot=scan_resource_properties.shot,
                        file_format='ma',
                        artist=self._artist,
                    )
                    self._resource_path = self._task_parse.to_wsp_resource_path(**resource_properties)
                    self.gui_setup(resource_properties)
                else:
                    self._gui_task_scene_opt.gui_restore()
                    self._gui_task_opt.gui_restore()
            else:
                self._gui_task_scene_opt.gui_restore()
                self._gui_task_opt.gui_restore()
        else:
            self._gui_task_scene_opt.gui_restore()
            self._gui_task_opt.gui_restore()

    def gui_unit_setup_fnc(self):
        prx_v_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_v_sca.widget)

        self._prx_h_splitter = gui_prx_widgets.PrxHSplitter()
        prx_v_sca.add_widget(self._prx_h_splitter)

        self._gui_task_opt = _GuiSourceTaskOpt(self._window, self, self._session)

        self._gui_task_scene_opt = _GuiSourceTaskUnitSceneOpt(self._window, self, self._session)

        self._gui_task_opt._qt_tree_widget._view.item_select_changed.connect(
            self._gui_task_scene_opt.gui_load_task_unit_scenes
        )

        self._prx_h_splitter.set_fixed_size_at(0, 320)

        self._bottom_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._bottom_prx_tool_bar._qt_widget)
        self._bottom_prx_tool_bar.set_expanded(True)
        self._bottom_prx_tool_bar.set_align_right()

        # increment save
        self._increment_and_save_qt_button = gui_qt_widgets.QtPressButton()
        self._bottom_prx_tool_bar.add_widget(self._increment_and_save_qt_button)
        self._increment_and_save_qt_button._set_name_text_(
            self._window.choice_gui_name(
                self._window._configure.get('build.{}.buttons.increment_and_save'.format(self._page.GUI_KEY))
            )
        )
        self._increment_and_save_qt_button._set_icon_name_('tool/save')
        self._increment_and_save_qt_button._set_auto_width_(True)
        self._increment_and_save_qt_button.press_clicked.connect(self.on_increment_and_save_task_scene)
        # save as
        self._save_as_qt_button = gui_qt_widgets.QtPressButton()
        self._bottom_prx_tool_bar.add_widget(self._save_as_qt_button)
        # self._save_as_qt_button.set_action_enable(False)
        self._save_as_qt_button._set_name_text_(
            self._window.choice_gui_name(
                self._window._configure.get('build.{}.buttons.save_as'.format(self._page.GUI_KEY))
            )
        )
        self._save_as_qt_button._set_icon_name_('tool/save-as')
        self._save_as_qt_button._set_sub_icon_name_('action/add')
        self._save_as_qt_button._set_auto_width_(True)
        self._save_as_qt_button.press_clicked.connect(self.on_save_task_scene_as)

    def gui_setup_post_fnc(self):
        pass

    def gui_setup(self, resource_properties):
        if resource_properties != self._resource_properties:
            self._resource_properties = resource_properties

            self._gui_task_opt.gui_load_all_tasks()

    def gui_get_resource_properties(self):
        return self._resource_properties

    def gui_jump_to_resource(self, ett_task):
        scan_resource_prx_input = self._page.gui_get_scan_resource_prx_input(self.RESOURCE_TYPE)
        scan_resource_path = self._task_parse.to_scan_resource_path(
            **ett_task.variants
        )
        scan_resource_prx_input.set_path(scan_resource_path)

    def do_gui_refresh_all(self, force=False):
        scan_resource_prx_input = self._page.gui_get_scan_resource_prx_input(self.RESOURCE_TYPE)

        self.gui_update_task_session()

        # update resource path
        if self._task_session:
            # check resource branch is match
            if self._task_session.properties.resource_type == self.RESOURCE_TYPE:
                scan_resource_prx_input.set_path(self._task_session.scan_resource_path)

        artist = self._page._artist

        scan_resource_path = scan_resource_prx_input.get_path()
        if (
            scan_resource_path != self._scan_resource_path
            or artist != self._artist
            or force is True
        ):
            self._artist = artist
            self._scan_resource_path = scan_resource_path
            self._do_gui_refresh_resource_for(scan_resource_path)

        self._gui_task_opt.do_gui_refresh_all()
        self._gui_task_scene_opt.do_gui_refresh_all()

    def gui_update_task_session(self):
        self._task_session = self._task_parse.generate_task_session_by_resource_source_scene_src_auto()
        return self._task_session

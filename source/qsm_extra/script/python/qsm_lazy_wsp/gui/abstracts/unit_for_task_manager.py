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

import qsm_lazy.gui.proxy.widgets as lzy_gui_prx_widgets


class _GuiBaseOpt(object):
    def __init__(self, window, page, session):
        self._window = window
        self._page = page
        self._session = session

        self._gui_thread_flag = 0

    def gui_update_thread_flag(self):
        self._gui_thread_flag += 1


class _GuiSourceTaskOpt(_GuiBaseOpt):
    def __init__(self, window, page, session):
        super(_GuiSourceTaskOpt, self).__init__(window, page, session)

        self._task_unit_path = None
        self._task_unit_path_tmp = None

        self._qt_tree_widget = gui_qt_view_widgets.QtTreeWidget()
        self._page._prx_v_splitter.add_widget(self._qt_tree_widget)
        self._qt_tree_widget._view_model.set_item_expand_record_enable(True)

        self._qt_tree_widget.refresh.connect(self.gui_load_tasks)

    def gui_load_tasks(self):
        def cache_fnc_():
            _task_dir_ptn_opt = self._page._task_parse.generate_pattern_opt_for(
                '{}-source-task-dir'.format(self._page.RESOURCE_BRANCH), **entity_properties
            )
            _matches = _task_dir_ptn_opt.find_matches()
            return [_matches, self._gui_thread_flag]

        def build_fnc_(data_):
            _matches, _gui_thread_flag = data_
            if _gui_thread_flag != self._gui_thread_flag:
                return

            if _matches:
                _flag, _root_qt_item = self._qt_tree_widget._view_model.create_root_item()
                _root_qt_item._item_model.set_icon_name('database/group')
                _root_qt_item.setExpanded(True)

                _project_path = self._page._task_parse.to_project_path(**entity_properties)
                _flag, _root_qt_item = self._qt_tree_widget._view_model.create_item(_project_path)
                _root_qt_item._item_model.set_icon_name('workspace/project')
                _root_qt_item.setExpanded(True)

                _resource_path = self._page._task_parse.to_resource_path(**entity_properties)
                _flag, _root_qt_item = self._qt_tree_widget._view_model.create_item(_resource_path)
                _root_qt_item._item_model.set_icon_name('workspace/resource')
                _root_qt_item.setExpanded(True)

                for _i_match in _matches:
                    self.gui_add_task(_i_match, _gui_thread_flag)

        self._qt_tree_widget._view_model.restore()

        self.gui_update_thread_flag()

        self._task_unit_path_tmp = None

        entity_properties = self._page._resource_properties

        if entity_properties is None:
            return

        trd = self._qt_tree_widget._view._generate_thread_(
            cache_fnc_, build_fnc_
        )

        trd.do_start()

    def gui_add_task(self, properties, gui_thread_flag):
        def cache_fnc_():
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]

            _task_unit_ptn_opt = self._page._task_parse.generate_pattern_opt_for(
                '{}-source-task_unit-dir'.format(self._page.RESOURCE_BRANCH), **properties
            )
            _matches = _task_unit_ptn_opt.find_matches()
            return [_matches, self._gui_thread_flag]

        def build_fnc_(data_):
            _matches, _gui_thread_flag = data_
            if _gui_thread_flag != self._gui_thread_flag:
                return

            if _matches:
                for _i_match in _matches:
                    self.gui_add_task_unit(_i_match, _gui_thread_flag)

            if gui_core.GuiUtil.language_is_chs():
                qt_item._item_model.set_menu_data(
                    [
                        ('打开文件夹', 'file/folder', open_folder_fnc_)
                    ]
                )
            else:
                qt_item._item_model.set_menu_data(
                    [
                        ('Open Folder', 'file/folder', open_folder_fnc_)
                    ]
                )

            qt_item._item_model.set_tool_tip(directory_path)

        def open_folder_fnc_():
            bsc_storage.StgExplorer.open_directory(directory_path)

        directory_path = properties['result']

        path = self._page._task_parse.to_task_path(**properties)

        flag, qt_item = self._qt_tree_widget._view_model.create_item(path)
        # fixme: show scene when task is select?
        # qt_item._item_model.set_assign_properties(properties)
        qt_item._item_model.set_icon_name('workspace/task')

        qt_item._item_model.set_show_fnc(cache_fnc_, build_fnc_)

    def gui_add_task_unit(self, properties, gui_thread_flag):
        def cache_fnc_():
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]

            _task_scene_ptn_opt = self._page._task_parse.generate_source_task_scene_src_pattern_opt_for(
                **properties)
            _matches = _task_scene_ptn_opt.find_matches(sort=True)
            return [
                _matches, gui_thread_flag
            ]

        def build_fnc_(data_):
            def press_dbl_click_fnc_():
                if _matches:
                    self._page.on_open_task_scene(_matches[-1])

            _matches, _gui_thread_flag = data_
            if _gui_thread_flag != self._gui_thread_flag:
                return

            _c = len(_matches)
            qt_item._item_model.set_number(_c)

            if gui_core.GuiUtil.language_is_chs():
                qt_item._item_model.set_menu_data(
                    [
                        ('打开文件夹', 'file/folder', open_folder_fnc_)
                    ]
                )
            else:
                qt_item._item_model.set_menu_data(
                    [
                        ('Open Folder', 'file/folder', open_folder_fnc_)
                    ]
                )

            qt_item._item_model.register_press_dbl_click_fnc(press_dbl_click_fnc_)

            qt_item._item_model.set_tool_tip(directory_path)

        def open_folder_fnc_():
            bsc_storage.StgExplorer.open_directory(directory_path)

        directory_path = properties['result']
        task_unit = properties['task_unit']
        path = self._page._task_parse.to_task_unit_path(**properties)

        flag, qt_item = self._qt_tree_widget._view_model.create_item(path)
        qt_item._item_model.set_assign_properties(properties)

        if task_unit == 'main':
            qt_item._item_model.set_icon_name('workspace/task-unit-main')
        else:
            qt_item._item_model.set_icon_name('workspace/task-unit')

        if self._page._task_session is not None:
            resource_path = self._page._resource_path
            task_unit_path = self._page._task_session.task_unit_path
            # check is task is current resource
            if task_unit_path.startswith(resource_path):
                if path == task_unit_path:
                    qt_item._item_model.focus_select()

                    qt_item._item_model.set_status(
                        qt_item._item_model.Status.Correct
                    )
            else:
                if path.endswith('main'):
                    self._task_unit_path_tmp = path
                    qt_item._item_model.focus_select()
        else:
            if self._task_unit_path_tmp is None:
                if path.endswith('main'):
                    self._task_unit_path_tmp = path
                    qt_item._item_model.focus_select()

        qt_item._item_model.set_show_fnc(cache_fnc_, build_fnc_)

    def gui_get_current_entity_properties(self):
        items = self._qt_tree_widget._view_model.get_selected_items()
        if items:
            item = items[-1]
            return item._item_model.get_assign_properties()

    def gui_set_current_task_unit_path(self, path):
        pass

    def gui_get_current_task_unit_path(self):
        qt_item = self._qt_tree_widget._view_model.get_current_item()
        if qt_item:
            return qt_item._item_model.get_path()

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

        task_session = self._page._task_session
        if task_session is not None:
            task_unit_path = task_session.task_unit_path
            qt_item = self._qt_tree_widget._view_model.find_item(task_unit_path)
            if qt_item is not None:
                qt_item._item_model.set_status(qt_item._item_model.Status.Correct)
                qt_item._item_model.focus_select()

    def gui_restore(self):
        self._qt_tree_widget._view_model.restore()


class _GuiSourceTaskSceneOpt(_GuiBaseOpt):

    def find_thumbnail(self, **kwargs):
        thumbnail_ptn_opt = self._page._task_parse.generate_resource_source_task_scene_src_thumbnail_pattern_opt_for(
            **kwargs)
        return thumbnail_ptn_opt.get_value()

    def __init__(self, window, page, session):
        super(_GuiSourceTaskSceneOpt, self).__init__(window, page, session)

        self._qt_list_widget = gui_qt_view_widgets.QtListWidget()
        self._page._prx_h_splitter.add_widget(self._qt_list_widget)

        self._qt_list_widget._set_item_sort_enable_(True)
        self._qt_list_widget._view_model.apply_item_sort_order(
            self._qt_list_widget._view_model.ItemSortOrder.Descending
        )
        self._qt_list_widget._set_item_group_enable_(True)
        self._qt_list_widget._view_model.set_item_category_enable(True)
        self._qt_list_widget._view_model.set_item_mtime_enable(True)
        self._qt_list_widget._view_model.set_item_user_enable(True)

        self._qt_list_widget._view_model.set_item_frame_size(190, 100)

        self._qt_list_widget.refresh.connect(self.gui_load_task_scenes)

        self._application_switch_tool_box = self._qt_list_widget._insert_left_tool_box_(0, 'application')
        self._gui_add_application_tools()

    def _gui_add_application_tools(self):
        tools = []
        if bsc_core.BscApplication.get_is_maya():
            cfg = [
                ('maya', True)
            ]
        elif bsc_core.BscApplication.get_is_houdini():
            cfg = [
                ('houdini', True)
            ]
        elif bsc_core.BscApplication.get_is_katana():
            cfg = [
                ('katana', True)
            ]
        else:
            cfg = [
                ('maya', True), ('houdini', False), ('katana', False)
            ]
        for i_key, i_enable in cfg:
            i_tool = gui_prx_widgets.PrxToggleButton()
            self._application_switch_tool_box._add_widget_(i_tool)
            i_tool._qt_widget._set_exclusive_widgets_(tools)
            i_tool.set_name(i_key)
            i_tool.set_icon_name('application/{}'.format(i_key))
            i_tool.set_tool_tip('"LMB-click" for switch to scale to "{}"'.format(i_key))
            if i_enable is True:
                i_tool.set_checked(True)

            tools.append(i_tool._qt_widget)
            i_tool.connect_check_changed_as_exclusive_to(
                functools.partial(self._gui_switch_application, i_key)
            )

    def _gui_switch_application(self, application):
        pass

    def gui_load_task_scenes(self):
        def cache_fnc_():
            _task_scene_ptn_opt = self._page._task_parse.generate_source_task_scene_src_pattern_opt_for(
                **entity_properties)
            _matches = _task_scene_ptn_opt.find_matches()
            return [
                _matches, self._gui_thread_flag
            ]

        def build_fnc_(data_):
            _matches, _gui_thread_flag = data_

            for i_match in _matches:
                self.gui_add_scene(i_match, _gui_thread_flag)

        self._qt_list_widget._view_model.restore()

        self.gui_update_thread_flag()

        entity_properties = self._page._gui_task_opt.gui_get_current_entity_properties()
        if not entity_properties:
            return

        trd = self._qt_list_widget._view._generate_thread_(
            cache_fnc_, build_fnc_
        )

        trd.do_start()

    def gui_add_scene(self, properties, gui_thread_flag):
        def cache_fnc_():
            if gui_thread_flag != self._gui_thread_flag:
                return [[], 0]
            # mtime
            _mtime = bsc_storage.StgFileOpt(scene_src_path).get_mtime()
            # user
            _user = bsc_storage.StgFileOpt(scene_src_path).get_user()
            return [
                [_mtime, _user], gui_thread_flag
            ]

        def build_fnc_(data_):
            _d, _gui_thread_flag = data_
            if _gui_thread_flag != self._gui_thread_flag:
                return

            if _d:
                _mtime, _user = _d
                qt_item._item_model.set_mtime(_mtime)
                if _user:
                    qt_item._item_model.set_user(_user)

            if gui_core.GuiUtil.language_is_chs():
                qt_item._item_model.set_menu_data(
                    [
                        ('在资源管理器中显示', 'file/folder', show_in_explorer_fnc_),
                        ('复制', ),
                        ('复制路径', 'tool/copy', copy_path_fnc_),
                        ('复制UNIX路径', 'tool/copy', copy_unit_path_fnc_)
                    ]
                )
            else:
                qt_item._item_model.set_menu_data(
                    [
                        ('Show in Explorer', 'file/folder', show_in_explorer_fnc_),
                        ('Copy',),
                        ('Copy Path', 'tool/copy', copy_path_fnc_),
                        ('Copy Unit Path', 'tool/copy', copy_unit_path_fnc_)
                    ]
                )

            qt_item._item_model.set_tool_tip(scene_src_path)

        def show_in_explorer_fnc_():
            bsc_storage.StgFileOpt(scene_src_path).show_in_system()

        def copy_path_fnc_():
            gui_qt_core.QtUtil.copy_text_to_clipboard(scene_src_path.replace('/', '\\'))

        def copy_unit_path_fnc_():
            gui_qt_core.QtUtil.copy_text_to_clipboard(scene_src_path)

        def press_dbl_click_fnc_():
            self._page.on_open_task_scene(properties)

        scene_src_path = properties['result']

        path = self._page._task_parse.to_source_scene_src_path(**properties)

        flag, qt_item = self._qt_list_widget._view_model.create_item(path)

        # image
        image_path = self.find_thumbnail(**properties)
        if image_path:
            qt_item._item_model.set_image(image_path)

        qt_item._item_model.set_icon_name('application/maya')
        qt_item._item_model.set_category(properties['task_unit'])
        qt_item._item_model.set_show_fnc(
            cache_fnc_, build_fnc_
        )

        if self._page._task_session is not None:
            if path == self._page._task_session.scene_src_path:
                qt_item._item_model.set_status(
                    qt_item._item_model.Status.Correct
                )
                qt_item._item_model.focus_select()

        qt_item._item_model.register_press_dbl_click_fnc(press_dbl_click_fnc_)

    def do_gui_refresh_task_scene_for(self, properties):
        path = self._page._task_parse.to_source_scene_src_path(**properties)
        qt_item = self._qt_list_widget._view_model.find_item(path)
        if qt_item is not None:
            self._qt_list_widget._view_model.clear_all_items_status()
            qt_item._item_model.set_status(
                qt_item._item_model.Status.Correct
            )
            qt_item._item_model.focus_select()
        else:
            self.gui_load_task_scenes()

    def do_gui_refresh_all(self):
        self._qt_list_widget._view_model.clear_all_items_status()
        task_session = self._page._task_session
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

    RESOURCE_BRANCH = None

    def on_open_task_scene(self, properties):
        scene_path = properties.get('result')
        bsc_storage.StgExplorer.open_file(scene_path)
        return False

    def on_increment_and_save_task_scene(self):
        # regenerate a session to save
        task_session = self._task_parse.generate_task_session_by_resource_source_scene_src_auto()
        if task_session:
            with self._window.gui_minimized():
                properties = task_session.increment_and_save_source_task_scene_src()
                if properties:
                    scene_path = properties.get('result')
                    if scene_path:
                        self.gui_load_task_scene(properties)

    def on_save_task_scene_to(self):
        pass

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
                        self.gui_load_task_scene(properties)

    def __init__(self, *args, **kwargs):
        super(AbsPrxUnitForTaskManager, self).__init__(*args, **kwargs)
        self._resource_properties = None

        self._task_parse = self.TASK_PARSE_CLS()
        self._task_session = None

        self._user = 'shared'
        self._studio = qsm_gnl_core.Sync().studio.get_current()

        self._scan_resource_path = None
        self._resource_path = None

        self.gui_unit_setup_fnc()

    def gui_load_task_scene(self, properties):
        scene_path = properties.get('result')
        if scene_path:
            task_session = self._task_parse.generate_task_session_by_resource_source_scene_src(scene_path)
            if task_session:
                self._task_session = task_session

                task_unit_path = task_session.task_unit_path
                if task_unit_path in self._gui_task_opt.gui_get_all_task_unit_paths():
                    self.do_gui_refresh_task_unit(task_unit_path)
                    self.do_gui_refresh_task_scene_for(properties)
                else:
                    self.do_gui_refresh_all_tasks()

    def do_gui_refresh_task_unit(self, task_unit_path):
        self._gui_task_opt.do_gui_refresh_task_unit(task_unit_path)

    def do_gui_refresh_task_scene_for(self, properties):
        self._gui_task_scene_opt.do_gui_refresh_task_scene_for(properties)

    def do_gui_refresh_all_tasks(self):
        self._gui_task_opt.gui_load_tasks()

    def _on_gui_left_visible_swap(self, boolean):
        self._prx_h_splitter.swap_contract_left_or_top_at(0)

    def _on_gui_switch_user(self):
        options = ['shared', bsc_core.BscSystem.get_user_name()]
        result = gui_core.GuiApplication.exec_input_dialog(
            type='choose',
            options=options,
            info='Choose Name for User...',
            value=self._user,
            title='Switch User'
        )
        if result:
            if result in options:
                self._user = result
                self._user_qt_info_bubble._set_text_(
                    '{}:{}'.format(self._studio, self._user)
                )

    def _gui_add_main_tools(self):
        self._left_visible_swap_tool = gui_prx_widgets.PrxToggleButton()
        self._main_prx_tool_box.add_widget(self._left_visible_swap_tool)
        self._left_visible_swap_tool.set_name('task')
        self._left_visible_swap_tool.set_icon_name('tree')
        self._left_visible_swap_tool.set_checked(True)
        self._left_visible_swap_tool.connect_check_toggled_to(self._on_gui_left_visible_swap)

        self._user_switch_qt_button = gui_qt_widgets.QtIconPressButton()
        self._main_prx_tool_box.add_widget(self._user_switch_qt_button)
        self._user_switch_qt_button._set_name_text_('user switch')
        self._user_switch_qt_button._set_icon_name_('users')
        self._user_switch_qt_button.press_clicked.connect(self._on_gui_switch_user)

        self._user_qt_info_bubble = gui_qt_widgets.QtInfoBubble()
        self._main_prx_tool_box.add_widget(self._user_qt_info_bubble)
        self._user_qt_info_bubble._set_style_(
            self._user_qt_info_bubble.Style.Frame
        )
        self._user_qt_info_bubble._set_text_('{}:{}'.format(self._studio, self._user))

    def _do_gui_refresh_resource_for(self, scan_resource_path):
        self._resource_properties = None
        self._scan_resource_path = None
        self._resource_path = None

        resource = self._scan_resource_prx_input.get_entity(scan_resource_path)

        if resource is not None:
            if resource.type == 'Asset':
                scan_resource_properties = resource.properties
                entity_properties = dict(
                    project=scan_resource_properties.project,
                    resource_branch='asset',
                    role=scan_resource_properties.role,
                    asset=scan_resource_properties.asset,
                    file_format='ma',
                    artist='shared',
                )
                self._scan_resource_path = self._task_parse.to_scan_resource_path(**entity_properties)
                self._resource_path = self._task_parse.to_resource_path(**entity_properties)

                self.gui_setup(entity_properties)
            elif resource.type == 'Shot':
                scan_resource_properties = resource.properties
                entity_properties = dict(
                    project=scan_resource_properties.project,
                    resource_branch='shot',
                    episode=scan_resource_properties.episode,
                    sequence=scan_resource_properties.sequence,
                    shot=scan_resource_properties.shot,
                    file_format='ma',
                    artist='shared',
                )
                self._scan_resource_path = self._task_parse.to_scan_resource_path(**entity_properties)
                self._resource_path = self._task_parse.to_resource_path(**entity_properties)

                self.gui_setup(entity_properties)
            else:
                self._gui_task_scene_opt.gui_restore()
                self._gui_task_opt.gui_restore()
        else:
            self._gui_task_scene_opt.gui_restore()
            self._gui_task_opt.gui_restore()

    def _gui_show_task_create_window(self):
        if self._resource_properties:
            w = self._window.gui_generate_sub_panel_for('task_create')
            w.gui_setup(self, self._resource_properties)
            w.do_gui_refresh_all()
            w.show_window_auto()

    def gui_unit_setup_fnc(self):
        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)

        # main tool box
        self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'main'
        )
        self._gui_add_main_tools()

        self._resource_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'reference', size_mode=1
        )
        if self.RESOURCE_BRANCH == 'asset':
            self._scan_resource_prx_input = lzy_gui_prx_widgets.PrxInputForAssetCharacterAndProp(
                history_key='lazy-workspace.{}-path'.format(self.RESOURCE_BRANCH)
            )
        elif self.RESOURCE_BRANCH == 'sequence':
            self._scan_resource_prx_input = lzy_gui_prx_widgets.PrxInputForSequence(
                history_key='lazy-workspace.{}-path'.format(self.RESOURCE_BRANCH)
            )
        elif self.RESOURCE_BRANCH == 'shot':
            self._scan_resource_prx_input = lzy_gui_prx_widgets.PrxInputForShot(
                history_key='lazy-workspace.{}-path'.format(self.RESOURCE_BRANCH)
            )
        else:
            raise RuntimeError()

        self._resource_prx_tool_box.add_widget(self._scan_resource_prx_input)

        self._scan_resource_prx_input.connect_input_change_accepted_to(self._do_gui_refresh_resource_for)

        self._create_task_qt_button = gui_qt_widgets.QtPressButton()
        self._scan_resource_prx_input.add_widget(self._create_task_qt_button)
        self._create_task_qt_button._set_name_text_(
            self._window.choice_gui_name(
                self._window._configure.get('build.{}.buttons.create_task'.format(self._page.GUI_KEY))
            )
        )
        self._create_task_qt_button._set_icon_name_('workspace/task-create')
        self._create_task_qt_button.setFixedWidth(96)
        self._create_task_qt_button.press_clicked.connect(self._gui_show_task_create_window)

        prx_v_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_v_sca.widget)

        self._prx_h_splitter = gui_prx_widgets.PrxHSplitter()
        prx_v_sca.add_widget(self._prx_h_splitter)

        self._prx_v_splitter = gui_prx_widgets.PrxVSplitter()
        self._prx_h_splitter.add_widget(self._prx_v_splitter)

        self._gui_task_opt = _GuiSourceTaskOpt(self._window, self, self._session)

        self._gui_task_scene_opt = _GuiSourceTaskSceneOpt(self._window, self, self._session)

        self._gui_task_opt._qt_tree_widget._view.item_select_changed.connect(
            self._gui_task_scene_opt.gui_load_task_scenes
        )
        self._prx_h_splitter.set_contract_enable(False)
        self._prx_h_splitter.set_fixed_size_at(0, 320)

        self._bottom_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._bottom_prx_tool_bar._qt_widget)
        self._bottom_prx_tool_bar.set_expanded(True)
        self._bottom_prx_tool_bar.set_align_right()

        # increment save
        self._increment_and_save_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._increment_and_save_prx_button)
        self._increment_and_save_prx_button.set_name(
            self._window.choice_gui_name(
                self._window._configure.get('build.{}.buttons.increment_and_save'.format(self._page.GUI_KEY))
            )
        )
        self._increment_and_save_prx_button.set_icon_name('tool/save')
        self._increment_and_save_prx_button.set_width(96)
        self._increment_and_save_prx_button.connect_press_clicked_to(self.on_increment_and_save_task_scene)
        # save as
        self._save_as_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._save_as_prx_button)
        # self._save_as_prx_button.set_action_enable(False)
        self._save_as_prx_button.set_name(
            self._window.choice_gui_name(
                self._window._configure.get('build.{}.buttons.save_as'.format(self._page.GUI_KEY))
            )
        )
        self._save_as_prx_button.set_icon_name('tool/save-as')
        self._save_as_prx_button.set_width(96)
        self._save_as_prx_button.connect_press_clicked_to(self.on_save_task_scene_as)

    def gui_setup_post_fnc(self):
        self._top_prx_tool_bar.do_gui_refresh()

    def do_gui_refresh_all(self, force=False):
        self._task_session = self._task_parse.generate_task_session_by_resource_source_scene_src_auto()
        # update resource path
        if self._task_session:
            # check resource branch is match
            if self._task_session.properties.resource_branch == self.RESOURCE_BRANCH:
                self._scan_resource_prx_input.set_path(self._task_session.scan_resource_path)

        scan_resource_path = self._scan_resource_prx_input.get_path()
        if scan_resource_path != self._scan_resource_path or force is True:
            self._do_gui_refresh_resource_for(self._scan_resource_prx_input.get_path())

        self._gui_task_opt.do_gui_refresh_all()
        self._gui_task_scene_opt.do_gui_refresh_all()

        self._top_prx_tool_bar.do_gui_refresh()

    def gui_setup(self, entity_properties):
        self._resource_properties = entity_properties
        self._gui_task_opt.gui_load_tasks()

    def gui_get_resource_properties(self):
        return self._resource_properties
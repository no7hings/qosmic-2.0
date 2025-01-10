# coding:utf-8
import functools

import lxbasic.core as bsc_core

import lxbasic.scan as bsc_scan

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.qt.view_widgets as gui_qt_vew_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_general.core as qsm_gnl_core

import qsm_scan as qsm_scan

import qsm_lazy.validation.scripts as lzy_vld_scripts


class AbsPrxPageForScnModelBatch(gui_prx_widgets.PrxBasePage):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    GUI_KEY = 'scenery_batch'

    def _start_delay(self, window, file_paths, process_options):
        process_args = []
        for i_file_path in file_paths:
            i_args = self._validation_opt.generate_process_args(i_file_path)
            if i_args is not None:
                i_task_name, i_cmd_script, i_validation_cache_path, i_mesh_count_cache_path = i_args
                if i_cmd_script is not None:
                    process_args.append(
                        (i_file_path, i_task_name, i_cmd_script, i_validation_cache_path, i_mesh_count_cache_path)
                    )
                else:
                    self._trace_result(
                        i_file_path, i_validation_cache_path, i_mesh_count_cache_path, process_options
                    )

        if process_args:
            window.show_window_auto(exclusive=False)

            for i_args in process_args:
                i_qt_item, i_task_name, i_cmd_script, i_validation_cache_path, i_mesh_count_cache_path = i_args
                window.submit(
                    'scenery_validation_process',
                    i_task_name,
                    i_cmd_script,
                    completed_fnc=functools.partial(
                        self._trace_result,
                        i_qt_item, i_validation_cache_path, i_mesh_count_cache_path, process_options
                    )
                )
        else:
            window.close_window()

    def _trace_result(self, file_path, validation_cache_path, mesh_count_cache_path, process_options):
        result, result_description, html = self._validation_opt.to_validation_result_args(
            validation_cache_path, mesh_count_cache_path, process_options
        )
        if file_path in self._file_to_item_dict:
            qt_item = self._file_to_item_dict[file_path]
            qt_item._item_model.set_assign_data('validation', html)

            if result == 'pass':
                qt_item._item_model.set_status(qt_item._item_model.Status.Correct)
            elif result == 'warning':
                qt_item._item_model.set_status(qt_item._item_model.Status.Warning)
            elif result == 'error':
                qt_item._item_model.set_status(qt_item._item_model.Status.Error)

            qt_item.setText(1, result_description)
            self._result_prx_text_browser.append_html(html)

    def _show_results(self):
        self._result_prx_text_browser.set_content('')
        qt_items = self._asset_qt_tree_widget._view_model.get_selected_leaf_items()

        for i_qt_item in qt_items:
            i_result = i_qt_item._item_model.get_assign_data('validation')
            if i_result:
                self._result_prx_text_browser.append_html(i_result)

    def _do_start(self):
        checked_qt_items = self._asset_qt_tree_widget._view_model.get_checked_leaf_items()
        selected_qt_items = self._asset_qt_tree_widget._view_model.get_selected_leaf_items()

        qt_items = list(set(checked_qt_items+selected_qt_items))

        if not qt_items:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.{}.messages.no_assets'.format(self.GUI_KEY))
                ),
                status='warning'
            )
            return

        process_options = self._validation_opt.generate_process_options(self._prx_options_node.to_dict())
        if not process_options:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.{}.messages.no_process_options'.format(self.GUI_KEY))
                ),
                status='warning'
            )
            return

        self._result_prx_text_browser.set_content('')

        window = gui_prx_widgets.PrxSprcTaskWindow()
        if window._language == 'chs':
            window.set_window_title('场景批量检查')
            window.set_tip(
                '正在运行检查程序，请耐心等待；\n'
                '如需要终止任务，请点击“关闭”。'
            )
        else:
            window.set_window_title('Scenery Batch Validation')

        file_paths = [x._item_model.get_assign_file() for x in qt_items]
        window.run_fnc_delay(
            functools.partial(
                self._start_delay,
                window, file_paths, process_options),
            500
        )

    def _do_list_assets(self):
        self._file_to_item_dict = {}
        self._asset_qt_tree_widget._view_model.restore()

        directory_path = self._prx_options_node.get('directory')
        if not directory_path:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.{}.messages.no_directory'.format(self.GUI_KEY))
                ),
                status='warning'
            )
            return

        pattern = self._prx_options_node.get('file_pattern')
        if not pattern:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.{}.messages.no_file_pattern'.format(self.GUI_KEY))
                ),
                status='warning'
            )
            return

        process_options = self._validation_opt.generate_process_options(self._prx_options_node.to_dict())
        if not process_options:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.{}.messages.no_process_options'.format(self.GUI_KEY))
                ),
                status='warning'
            )
            return

        self._gui_thread_flag += 1

        self._result_prx_text_browser.set_content(
            gui_core.GuiUtil.choice_gui_description(
                self._window._language,
                self._window._configure.get('build.{}.contents.start_scan'.format(self.GUI_KEY))
            )
        )

        roles = qsm_gnl_core.QsmAsset.get_scenery_role_mask()

        role = roles[0]
        # add root
        self._create_root()
        self._create_role(role)
        self._add_for_role(role, pattern, directory_path, process_options, self._gui_thread_flag)

    def _create_root(self):
        flag, qt_item = self._asset_qt_tree_widget._view_model.create_item('/')
        qt_item._item_model.set_expanded(True)
        qt_item._item_model.set_icon_name('file/folder')

    def _create_role(self, role):
        role_path = '/{}'.format(role)
        flag, qt_item = self._asset_qt_tree_widget._view_model.create_item(role_path)
        qt_item._item_model.set_expanded(True)
        qt_item._item_model.set_icon_name('file/folder')

    def _add_for_role(self, role, pattern, directory_path, process_options, gui_thread_flag):
        def finish_fnc_():
            if self._window._language == 'chs':
                self._result_prx_text_browser.set_content_with_thread(
                    '扫描完成。'
                )

        pattern_opt = bsc_core.BscStgParseOpt(
            pattern,
            variants=dict(
                directory=directory_path, role=role,
            )
        )

        path_regex = pattern_opt.get_pattern_for_fnmatch()

        bsc_scan.ScanGlob.concurrent_glob_file(
            path_regex,
            result_fnc=functools.partial(self._signals.accepted.emit, (role, process_options, gui_thread_flag)),
            finish_fnc=finish_fnc_
        )

    def _add_asset_fnc(self, args, file_path):
        role, process_options, gui_thread_flag = args
        if gui_thread_flag != self._gui_thread_flag:
            return

        self._add_asset(role, process_options, gui_thread_flag, file_path)

    # last arg must be file path
    def _add_asset(self, role, process_options, gui_thread_flag, file_path):
        def cache_fnc_():
            if gui_thread_flag != self._gui_thread_flag:
                return []

            _args = self._validation_opt.generate_process_args(file_path)
            if _args is not None:
                _task_name, _cmd_script, _validation_cache_path, _mesh_count_cache_path = _args
                if _cmd_script is None:
                    _result, _result_description, _html = self._validation_opt.to_validation_result_args(
                        _validation_cache_path, _mesh_count_cache_path, process_options
                    )
                    return [_result, _result_description, _html]
            return []

        def build_fnc_(data_):
            if gui_thread_flag != self._gui_thread_flag:
                return

            if data_:
                _result, _result_description, _html = data_
                qt_item._item_model.set_assign_data('validation', _html)
                if _result == 'pass':
                    qt_item._item_model.set_status(qt_item._item_model.Status.Correct)
                elif _result == 'warning':
                    qt_item._item_model.set_status(qt_item._item_model.Status.Warning)
                elif _result == 'error':
                    qt_item._item_model.set_status(qt_item._item_model.Status.Error)

                qt_item.setText(1, _result_description)

        def generate_menu_data_fnc_():
            def open_folder_fnc_():
                bsc_storage.StgFileOpt(file_path).show_in_system()

            def copy_path_fnc():
                gui_qt_core.QtUtil.write_clipboard(file_path)

            return [
                ('Open Folder', 'file/folder', open_folder_fnc_),
                ('Copy Path', 'copy', copy_path_fnc)
            ]

        file_opt = bsc_storage.StgFileOpt(file_path)

        path = '/{}/{}'.format(role, file_opt.name)
        flag, qt_item = self._asset_qt_tree_widget._view_model.create_item(path)

        qt_item._item_model.set_assign_file(file_path)
        qt_item._item_model.set_icon_name('file/file')

        qt_item._item_model.set_show_fnc(cache_fnc_, build_fnc_)

        qt_item._item_model.set_menu_data_generate_fnc(generate_menu_data_fnc_)

        self._file_to_item_dict[file_path] = qt_item

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForScnModelBatch, self).__init__(window, session, *args, **kwargs)

        self._scan_root = qsm_scan.Stage().get_root()

        self._signals = gui_qt_core.QtConcurrentGlobSignals(self._qt_widget)
        self._signals.accepted.connect(self._add_asset_fnc)

        self._gui_thread_flag = 0

        self._validation_opt = lzy_vld_scripts.SceneryValidationOpt()

        self._file_to_item_dict = {}

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        prx_v_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_v_sca.widget)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self._window.choice_gui_name(
                self._window._configure.get('build.{}.options'.format(self.GUI_KEY))
            )
        )
        prx_v_sca.add_widget(self._prx_options_node)
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.{}.options.parameters'.format(self.GUI_KEY)),
        )

        process_options = self._validation_opt.options.generate_process_options()
        for k, v in process_options.items():
            self._prx_options_node.set(k, v)

        self._file_prx_tool_group = gui_prx_widgets.PrxHToolGroup()
        prx_v_sca.add_widget(self._file_prx_tool_group)
        self._file_prx_tool_group.set_expanded(True)
        self._file_prx_tool_group.set_name(
            gui_core.GuiUtil.choice_gui_name(
                self._window._language,
                self._window._configure.get('build.{}.groups.files'.format(self.GUI_KEY))
            )
        )

        # asset
        self._asset_qt_tree_widget = gui_qt_vew_widgets.QtTreeWidget()
        self._file_prx_tool_group.add_widget(self._asset_qt_tree_widget)
        self._asset_qt_tree_widget._set_item_check_enable_(True)
        self._asset_qt_tree_widget._view_model.set_item_sort_enable(True)
        self._asset_qt_tree_widget._view_model.set_head_data(
            [('asset', 4), ('description', 4)], max_width=560
        )

        self._asset_qt_tree_widget._view.item_select_changed.connect(self._show_results)

        # results
        self._result_prx_tool_group = gui_prx_widgets.PrxHToolGroup()
        prx_v_sca.add_widget(self._result_prx_tool_group)
        self._result_prx_tool_group.set_expanded(True)
        self._result_prx_tool_group.set_name(
            gui_core.GuiUtil.choice_gui_name(
                self._window._language,
                self._window._configure.get('build.{}.groups.results'.format(self.GUI_KEY))
            )
        )
        self._result_prx_text_browser = gui_prx_widgets.PrxTextBrowser()
        self._result_prx_tool_group.add_widget(self._result_prx_text_browser)
        self._result_prx_text_browser.set_content(
            gui_core.GuiUtil.choice_gui_description(
                self._window._language,
                self._window._configure.get('build.{}.contents.results'.format(self.GUI_KEY))
            )
        )

        # buttons
        self._bottom_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._bottom_prx_tool_bar.widget)
        self._bottom_prx_tool_bar.set_expanded(True)

        self._list_asset_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._list_asset_prx_button)
        self._list_asset_prx_button.set_name(
            gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._window._configure.get('build.{}.buttons.list_assets'.format(self.GUI_KEY))
            )
        )
        self._list_asset_prx_button.connect_press_clicked_to(
            self._do_list_assets
        )

        self._start_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._start_prx_button)
        self._start_prx_button.set_name(
            gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._window._configure.get('build.{}.buttons.start'.format(self.GUI_KEY))
            )
        )
        self._start_prx_button.connect_press_clicked_to(
            self._do_start
        )

        # self._save_result_button = gui_prx_widgets.PrxPressButton()
        # self._bottom_prx_tool_bar.add_widget(self._save_result_button)
        # self._save_result_button.set_name(
        #     gui_core.GuiUtil.choice_gui_name(
        #         self._window._language, self._window._configure.get('build.{}.buttons.save'.format(self.GUI_KEY))
        #     )
        # )

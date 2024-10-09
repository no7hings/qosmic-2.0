# coding:utf-8
import copy

import functools

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.qt.widgets as qt_widgets

import qsm_general.core as qsm_gnl_core

import qsm_general.scan as qsm_gnl_scan

import qsm_lazy.validation.scripts as qsm_lzy_vld_scripts

import qsm_gui.proxy.widgets as qsm_gui_prx_widgets


class AbsPrxPageForScenery(gui_prx_widgets.PrxBasePage):
    PAGE_KEY = 'scenery'

    def _trace_result(self, file_path, validation_cache_path, mesh_count_cache_path, process_options):
        result, html = self._validation_opt.to_validation_result_args(
            validation_cache_path, mesh_count_cache_path, process_options
        )
        self._result_prx_text_browser.append_html(html)
        # self._prx_options_node.get_port('files').remove(file_path)

    def _on_dcc_load_asset(self):
        if self._asset_path is not None:
            self._prx_options_node.get_port('files').append(self._asset_path)

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
                i_file_path, i_task_name, i_cmd_script, i_validation_cache_path, i_mesh_count_cache_path = i_args
                window.submit(
                    'scenery_validation_process',
                    i_task_name,
                    i_cmd_script,
                    completed_fnc=functools.partial(
                        self._trace_result,
                        i_file_path, i_validation_cache_path, i_mesh_count_cache_path, process_options
                    )
                )
        else:
            window.close_window()

    def _do_start(self):
        file_paths = self._prx_options_node.get('files')
        if not file_paths:
            self._window.exec_message_dialog(
                self._window.choice_message(
                    self._window._configure.get('build.{}.messages.no_files'.format(self.PAGE_KEY))
                ),
                status='warning'
            )
            return

        process_options = self._validation_opt.generate_process_options(self._prx_options_node.to_dict())
        if not process_options:
            self._window.exec_message_dialog(
                self._window.choice_message(
                    self._window._configure.get('build.{}.messages.no_process_options'.format(self.PAGE_KEY))
                ),
                status='warning'
            )
            return

        self._result_prx_text_browser.set_content('')

        window = gui_prx_widgets.PrxSprcTaskWindow()
        if window._language == 'chs':
            window.set_window_title('场景检查')
            window.set_tip(
                '正在运行检查程序，请耐心等待；\n'
                '如需要终止任务，请点击“关闭”。'
            )
        else:
            window.set_window_title('Scenery Validation')

        window.run_fnc_delay(
            functools.partial(
                self._start_delay,
                window, file_paths, process_options),
            500
        )

    def _do_gui_refresh_asset_for(self, path):
        self._asset_path = None
        self._asset_load_qt_button._set_action_enable_(False)
        entity = self._asset_prx_input.get_entity(path)
        if entity is not None:
            if entity.type == 'Asset':
                task = entity.task(self._scan_root.EntityTasks.Model)
                if task is not None:
                    result = task.find_result(
                        self._scan_root.StoragePatterns.MayaModelFIle
                    )
                    if result is not None:
                        self._asset_path = result
                        self._asset_load_qt_button._set_action_enable_(True)

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForScenery, self).__init__(window, session, *args, **kwargs)
        self._asset_path = None
        self._scan_root = qsm_gnl_scan.Root.generate()

        self._validation_opt = qsm_lzy_vld_scripts.SceneryValidationOpt()

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)
        # load tool
        self._asset_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'load', size_mode=1
        )
        self._asset_prx_input = qsm_gui_prx_widgets.PrxAssetInputForScenery()
        self._asset_prx_tool_box.add_widget(self._asset_prx_input)
        # self._asset_prx_input.widget.setMaximumWidth(516)

        self._asset_load_qt_button = qt_widgets.QtPressButton()
        self._asset_prx_input.add_widget(self._asset_load_qt_button)
        self._asset_load_qt_button.setMaximumWidth(64)
        self._asset_load_qt_button.setMinimumWidth(64)
        self._asset_load_qt_button._set_name_text_(
            self._window.choice_name(
                self._window._configure.get('build.{}.buttons.add'.format(self.PAGE_KEY))
            )
        )
        self._asset_load_qt_button.press_clicked.connect(self._on_dcc_load_asset)
        self._asset_load_qt_button._set_action_enable_(False)

        v_prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(v_prx_sca.widget)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self._window.choice_name(
                self._window._configure.get('build.{}.options'.format(self.PAGE_KEY))
            )
        )
        v_prx_sca.add_widget(self._prx_options_node)
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.{}.options.parameters'.format(self.PAGE_KEY)),
        )
        # validation results
        self._result_prx_tool_group = gui_prx_widgets.PrxHToolGroup()
        v_prx_sca.add_widget(self._result_prx_tool_group)
        self._result_prx_tool_group.set_expanded(True)
        self._result_prx_tool_group.set_name(
            gui_core.GuiUtil.choice_name(
                self._window._language, 
                self._window._configure.get('build.{}.groups.results'.format(self.PAGE_KEY))
            )
        )
        self._result_prx_text_browser = gui_prx_widgets.PrxTextBrowser()
        self._result_prx_tool_group.add_widget(self._result_prx_text_browser)
        self._result_prx_text_browser.set_content(
            gui_core.GuiUtil.choice_description(
                self._window._language, 
                self._window._configure.get('build.{}.contents.results'.format(self.PAGE_KEY))
            )
        )
        # buttons
        self._bottom_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(self._bottom_prx_tool_bar.widget)
        self._bottom_prx_tool_bar.set_expanded(True)

        self._start_prx_button = gui_prx_widgets.PrxPressButton()
        self._bottom_prx_tool_bar.add_widget(self._start_prx_button)
        self._start_prx_button.set_name(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.{}.buttons.start'.format(self.PAGE_KEY))
            )
        )
        self._start_prx_button.connect_press_clicked_to(
            self._do_start
        )

        self._asset_prx_input.connect_input_change_accepted_to(self._do_gui_refresh_asset_for)
        self._do_gui_refresh_asset_for(self._asset_prx_input.get_path())

        process_options = self._validation_opt.options.generate_process_options()
        for k, v in process_options.items():
            self._prx_options_node.set(k, v)

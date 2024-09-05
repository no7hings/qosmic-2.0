# coding:utf-8
import copy

import functools
import json

import six

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.resource as bsc_resource

import lxbasic.pinyin as bsc_pinyin

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.qt.widgets as qt_widgets

import qsm_general.core as qsm_gnl_core

import qsm_general.scan as qsm_gnl_scan

import qsm_gui.proxy.widgets as qsm_gui_prx_widgets


class AbsPrxPageForRigValidation(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget
    PAGE_KEY = 'rig_validation'

    def _do_dcc_load_asset(self):
        if self._asset_path is not None:
            self._prx_options_node.get_port('files').append(self._asset_path)

    def _do_gui_refresh_asset_for(self, path):
        self._asset_path = None
        self._asset_load_qt_button._set_action_enable_(False)
        entity = self._asset_prx_input.get_entity(path)
        if entity is not None:
            if entity.type == 'Asset':
                task = entity.task(self._scan_root.EntityTasks.Rig)
                if task is not None:
                    result = task.find_result(
                        self._scan_root.ResultPatterns.MayaRigFile
                    )
                    if result is not None:
                        self._asset_path = result
                        self._asset_load_qt_button._set_action_enable_(True)

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForRigValidation, self).__init__(*args, **kwargs)

        self._window = window
        self._session = session

        self._asset_path = None
        self._scan_root = qsm_gnl_scan.Root.generate()
        
        self._validation_options = qsm_gnl_core.DccValidationOptions('rig/adv_validation_options')

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        qt_v_lot = gui_qt_widgets.QtVBoxLayout(self._qt_widget)
        qt_v_lot.setContentsMargins(*[0]*4)
        qt_v_lot.setSpacing(2)

        self._top_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        qt_v_lot.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_align_left()
        self._top_prx_tool_bar.set_expanded(True)
        # load tool
        self._asset_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
            'load', size_mode=1
        )
        self._asset_prx_input = qsm_gui_prx_widgets.PrxInputForAsset()
        self._asset_prx_tool_box.add_widget(self._asset_prx_input)
        self._asset_prx_input.widget.setMaximumWidth(516)

        self._asset_load_qt_button = qt_widgets.QtPressButton()
        self._asset_prx_input.add_widget(self._asset_load_qt_button)
        self._asset_load_qt_button.setMaximumWidth(64)
        self._asset_load_qt_button.setMinimumWidth(64)
        self._asset_load_qt_button._set_name_text_(
            self._window.choice_name(
                self._window._configure.get('build.{}.buttons.add'.format(self.PAGE_KEY))
            )
        )
        self._asset_load_qt_button.press_clicked.connect(self._do_dcc_load_asset)
        self._asset_load_qt_button._set_action_enable_(False)

        v_prx_sca = gui_prx_widgets.PrxVScrollArea()
        qt_v_lot.addWidget(v_prx_sca.widget)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self._window.choice_name(
                self._window._configure.get('build.{}.units.main.options'.format(self.PAGE_KEY))
            )
        )
        v_prx_sca.add_widget(self._prx_options_node)
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.{}.units.main.options.parameters'.format(self.PAGE_KEY)),
        )

        # validation result
        self._result_prx_tool_group = gui_prx_widgets.PrxHToolGroup()
        v_prx_sca.add_widget(self._result_prx_tool_group)
        self._result_prx_tool_group.set_expanded(True)
        self._result_prx_tool_group.set_name(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.{}.validation_result'.format(self.PAGE_KEY))
            )
        )
        self._result_prx_text_browser = gui_prx_widgets.PrxTextBrowser()
        self._result_prx_tool_group.add_widget(self._result_prx_text_browser)
        self._result_prx_text_browser.set_content(
            gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.{}.validation_result'.format(self.PAGE_KEY))
            )
        )
        # buttons
        self._bottom_prx_tool_bar = gui_prx_widgets.PrxHToolBar()
        qt_v_lot.addWidget(self._bottom_prx_tool_bar.widget)
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

        process_options = self._validation_options.generate_process_options()
        for k, v in process_options.items():
            self._prx_options_node.set(k, v)
        
    def _trace_result(self, cache_path, process_options):
        result = self._to_result(cache_path, process_options)
        self._result_prx_text_browser.append(result)

    def _to_result(self, cache_path, process_options):
        data = bsc_storage.StgFileOpt(cache_path).set_read()
        validation_opt = qsm_gnl_core.DccValidationOptions('rig/adv_validation_options')
        validation_opt.update_process_options(process_options)
        return validation_opt.to_text(data)

    def _start_delay(self, window, file_paths, process_options):
        process_args = []
        for i_file_path in file_paths:
            i_args = self._generate_process_args(i_file_path, process_options)
            if i_args is not None:
                i_task_name, i_cmd_script, i_cache_file_path = i_args
                if i_cmd_script is not None:
                    process_args.append(
                        (i_task_name, i_cmd_script, i_cache_file_path)
                    )
                else:
                    self._trace_result(i_cache_file_path, process_options)
        
        if process_args:
            window.show_window_auto(exclusive=False)

            for i_args in process_args:
                i_task_name, i_cmd_script, i_cache_file_path = i_args
                window.submit(
                    'rig_validation_process',
                    i_task_name,
                    i_cmd_script,
                    completed_fnc=functools.partial(self._trace_result, i_cache_file_path, process_options)
                )
        else:
            window.close_window()

    def _do_start(self):
        file_paths = self._prx_options_node.get('files')
        if not file_paths:
            self._window.exec_message_dialog(
                self._window.choice_message(
                    self._window._configure.get('build.rig_validation.messages.no_files')
                ),
                status='warning'
            )
            return

        process_options = self._generate_process_options()
        if not process_options:
            self._window.exec_message_dialog(
                self._window.choice_message(
                    self._window._configure.get('build.rig_validation.messages.no_process_options')
                ),
                status='warning'
            )
            return

        self._result_prx_text_browser.set_content('')

        window = gui_prx_widgets.PrxSprcTaskWindow()
        if window._language == 'chs':
            window.set_window_title('绑定检查')
            window.set_tip(
                '正在运行检查程序，请耐心等待；\n'
                '如需要终止任务，请点击“关闭”。'
            )
        else:
            window.set_window_title('Rig Validation')

        window.run_fnc_delay(
            functools.partial(
                self._start_delay,
                window, file_paths, process_options),
            500
        )

    def _generate_process_options(self):
        options = dict()
        data = self._prx_options_node.to_dict()
        branches = [
            'joint',
            'control'
        ]
        for i_branch in branches:
            i_leafs = data[i_branch]
            if i_leafs:
                options[i_branch] = i_leafs
        return options

    def _generate_process_args(self, file_path, process_options):
        process_options = copy.copy(process_options)
        process_options['version'] = 2.0
        option_hash = bsc_core.BscHash.to_hash_key(process_options)

        task_name = '[rig-validation][{}]'.format(
            bsc_storage.StgFileOpt(file_path).name
        )
        cache_path = qsm_gnl_core.MayaCache.generate_rig_validation_result_file(file_path, version=option_hash)
        if bsc_storage.StgFileOpt(cache_path).get_is_file() is False:
            cmd_script = qsm_gnl_core.MayaCacheProcess.generate_cmd_script_by_option_dict(
                'rig-validation',
                dict(
                    file_path=file_path,
                    cache_path=cache_path,
                    process_options=process_options
                )
            )
            return task_name, cmd_script, cache_path
        return task_name, None, cache_path

    def do_gui_refresh_all(self):
        pass

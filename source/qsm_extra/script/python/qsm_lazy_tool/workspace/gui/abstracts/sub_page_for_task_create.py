# coding:utf-8
import copy

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_lazy.workspace.core as qsm_lzy_wsp_core


class AbsPrxSubPageForAssetTaskCreate(gui_prx_widgets.PrxBaseSubPage):
    PAGE_KEY = 'asset'

    def _on_apply(self):
        page = self._sub_window._window.gui_find_page('task_manager')
        if page is not None:
            if bsc_core.BscApplication.get_is_maya():
                import qsm_maya.core as qsm_mya_core

                import qsm_maya_lazy.workspace.core as qsm_mya_lzy_wsp_core

                if qsm_mya_core.SceneFile.new_with_dialog() is True:
                    task_parse = qsm_lzy_wsp_core.TaskParse()
                    step_task = self._prx_options_node.get('step_task')
                    task_unit = self._prx_options_node.get('task_unit')
                    if not task_unit:
                        return

                    step, task = step_task.split('.')
                    kwargs = copy.copy(page.gui_get_entity_properties())
                    kwargs['step'] = step
                    kwargs['task'] = task
                    kwargs['task_unit'] = task_unit
                    if 'version' in kwargs:
                        kwargs.pop('version')

                    task_scene_ptn_opt = task_parse.generate_task_scene_pattern_opt_for(**kwargs)

                    matches = task_scene_ptn_opt.find_matches(sort=True)
                    if matches:
                        last_version = int(matches[-1]['version'])
                        version = last_version+1
                    else:
                        version = 1

                    kwargs_new = copy.copy(kwargs)

                    kwargs_new['version'] = str(version).zfill(3)

                    task_scene_ptn_opt_new = task_parse.generate_task_scene_pattern_opt_for(**kwargs_new)

                    task_scene_path = task_scene_ptn_opt_new.get_value()

                    if bsc_storage.StgPath.get_is_file(task_scene_path) is False:
                        qsm_mya_lzy_wsp_core.TaskBuild(task_parse, kwargs_new).execute()

                        qsm_mya_core.SceneFile.save_to(task_scene_path)

                        kwargs_new['result'] = task_scene_path

                        thumbnail_ptn_opt = task_parse.generate_task_scene_thumbnail_pattern_opt_for(**kwargs_new)
                        thumbnail_path = thumbnail_ptn_opt.get_value()

                        qsm_mya_core.SceneFile.refresh()

                        with self._sub_window._window.gui_minimized():
                            gui_qt_core.QtMaya.make_snapshot(thumbnail_path)

                        page.gui_load_task_scene(kwargs_new)

    def _on_close(self):
        self._sub_window.close_window()

    def _on_apply_and_close(self):
        self._on_apply()
        self._on_close()

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(AbsPrxSubPageForAssetTaskCreate, self).__init__(window, session, sub_window, *args, **kwargs)
        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_sca.widget)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self._sub_window.choice_name(
                self._sub_window._configure.get('build.{}.options'.format(self.PAGE_KEY))
            )
        )
        prx_sca.add_widget(self._prx_options_node)

        self._prx_options_node.build_by_data(
            self._sub_window._configure.get('build.{}.options.parameters'.format(self.PAGE_KEY)),
        )

        bottom_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(bottom_tool_bar.widget)
        bottom_tool_bar.set_expanded(True)

        self._apply_button = gui_qt_widgets.QtPressButton()
        bottom_tool_bar.add_widget(self._apply_button)
        self._apply_button._set_name_text_(
            self._sub_window.choice_name(
                self._sub_window._configure.get('build.main.buttons.apply')
            )
        )
        self._apply_button.press_clicked.connect(self._on_apply)

        self._apply_and_close_button = gui_qt_widgets.QtPressButton()
        bottom_tool_bar.add_widget(self._apply_and_close_button)
        self._apply_and_close_button._set_name_text_(
            self._sub_window.choice_name(
                self._sub_window._configure.get('build.main.buttons.apply_and_close')
            )
        )
        self._apply_and_close_button.press_clicked.connect(self._on_apply_and_close)

        self._close_button = gui_qt_widgets.QtPressButton()
        bottom_tool_bar.add_widget(self._close_button)
        self._close_button._set_name_text_(
            self._sub_window.choice_name(
                self._sub_window._configure.get('build.main.buttons.close')
            )
        )
        self._close_button.press_clicked.connect(self._on_close)

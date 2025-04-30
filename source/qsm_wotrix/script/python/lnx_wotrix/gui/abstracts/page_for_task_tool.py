# coding:utf-8
import sys

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxPageForTaskTool(gui_prx_widgets.PrxBasePage):
    GUI_KEY = 'task_tool'

    TASK_PARSE_CLS = None

    TASK_MODULE_ROOT = None

    @classmethod
    def _find_gui_cls(cls, resource_type, task):
        # noinspection PyBroadException
        try:
            module_path = '{}.{}.{}.gui_widgets.task_tool'.format(
                cls.TASK_MODULE_ROOT, resource_type, task
            )
            module = bsc_core.PyModule(module_path)
            if module.get_is_exists():
                gui_cls = module.get_method('GuiTaskToolMain')
                if gui_cls:
                    bsc_log.Log.trace(
                        'find task tool gui for {}/{} successful.'.format(resource_type, task)
                    )
                    return gui_cls
        except Exception:
            bsc_log.LogDebug.trace()

    def __init__(self, window, session, *args, **kwargs):
        super(AbsPrxPageForTaskTool, self).__init__(window, session, *args, **kwargs)

        self._task_parse = self.TASK_PARSE_CLS()
        self._task_session = None

        self._task = None

        self._gui_task_unit = None

    def do_gui_refresh_all(self, force=False):
        # catch task session
        self._task_session = self._task_parse.generate_task_session_by_resource_source_scene_src_auto()
        if self._task_session:
            resource_type = self._task_session.properties['resource_type']
            task = self._task_session.properties['task']
        else:
            resource_type = None
            task = None

        if task is not None and task != self._task:
            self._task = task

            self._qt_layout._clear_all_widgets_()

            self._gui_task_unit = None

            gui_cls = self._find_gui_cls(resource_type, task)
            if gui_cls:
                self._gui_task_unit = self.gui_instance_unit(gui_cls)
                self._qt_layout.addWidget(self._gui_task_unit.widget)
            else:
                placeholder = gui_qt_widgets.QtVScrollArea()
                self._qt_layout.addWidget(placeholder)
                placeholder._set_empty_draw_flag_(True)

        if self._gui_task_unit is not None:
            self._gui_task_unit.do_gui_refresh_all()

        if task is None:
            self._qt_layout._clear_all_widgets_()

    def gui_setup_post_fnc(self):
        if self._gui_task_unit is not None:
            self._gui_task_unit.gui_setup_post_fnc()

# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxPageForTaskTool(gui_prx_widgets.PrxBasePage):
    GUI_KEY = 'task_tool'

    TASK_PARSE_CLS = None

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
            task = self._task_session.properties['task']
        else:
            task = 'gnl'

        if task != self._task:
            self._task = task

            self._qt_layout._clear_all_widgets_()

            self._gui_task_unit = None

            if self._task in self._unit_class_dict:
                self._gui_task_unit = self._unit_class_dict[self._task](self._window, self, self._session)
                self._qt_layout.addWidget(self._gui_task_unit.widget)

        if self._gui_task_unit is not None:
            self._gui_task_unit.do_gui_refresh_all()

    def gui_setup_post_fnc(self):
        if self._gui_task_unit is not None:
            self._gui_task_unit.gui_setup_post_fnc()

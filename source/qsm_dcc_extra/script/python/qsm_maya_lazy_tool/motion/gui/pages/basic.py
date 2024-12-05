# coding:utf-8
import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import qsm_lazy.gui.qt.widgets as lzy_gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core

from ..toolsets import basic as _toolset_basic


class PrxPageForMotionMain(gui_prx_widgets.PrxBasePage):
    GUI_KEY = 'main'

    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    SCRIPT_JOB_NAME = 'lazy_tool_for_motion_main'

    def _do_dcc_register_all_script_jobs(self):
        self._script_job_opt = qsm_mya_core.ScriptJobOpt(
            self.SCRIPT_JOB_NAME
        )
        self._script_job_opt.register(
            [
                self._gui_rig_picker_unit.do_gui_refresh_by_dcc_selection,
                self._gui_motion_copy_and_paste_prx_toolset.do_gui_refresh_by_dcc_selection,
            ],
            self._script_job_opt.EventTypes.SelectionChanged
        )
        self._script_job_opt.register(
            self.do_gui_refresh_all,
            self._script_job_opt.EventTypes.SceneNew,
        )
        self._script_job_opt.register(
            self.do_gui_refresh_all,
            self._script_job_opt.EventTypes.SceneOpened,
        )
        self._script_job_opt.register(
            self.do_gui_refresh_all,
            self._script_job_opt.EventTypes.Undo,
        )
        self._script_job_opt.register(
            self.do_gui_refresh_all,
            self._script_job_opt.EventTypes.Redo,
        )

    def _do_dcc_destroy_all_script_jobs(self):
        self._script_job_opt.destroy()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPageForMotionMain, self).__init__(window, session, *args, **kwargs)

        self.gui_page_setup_fnc()

    def gui_get_tool_tab_box(self):
        return self._page_prx_tab_tool_box

    def gui_close_fnc(self):
        self._script_job_opt.destroy()

    def gui_page_setup_fnc(self):
        self._qt_widget.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        # central
        central_qt_wgt = gui_qt_widgets.QtTranslucentWidget()
        self._qt_layout.addWidget(central_qt_wgt)
        central_qt_lot = gui_qt_widgets.QtHBoxLayout(central_qt_wgt)
        central_qt_lot.setContentsMargins(*[0]*4)
        central_qt_lot.setSpacing(2)
        # chart
        self._qt_picker = lzy_gui_qt_widgets.QtAdvCharacterPicker()
        central_qt_lot.addWidget(self._qt_picker)
        self._gui_rig_picker_unit = _toolset_basic.UnitForRigPicker(
            self._window, self, self._session, self._qt_picker,
        )
        # page
        self._page_prx_tab_tool_box = self.gui_create_tab_tool_box()
        central_qt_lot.addWidget(self._page_prx_tab_tool_box.widget)
        self._page_prx_tab_tool_box.set_tab_direction(self._page_prx_tab_tool_box.TabDirections.RightToLeft)
        # tool set
        # copy and paste
        self._gui_motion_copy_and_paste_prx_toolset = _toolset_basic.ToolsetForMotionCopyAndPaste(
            self._window, self, self._session
        )
        # keyframe
        self._gui_motion_keyframe_prx_toolset = _toolset_basic.ToolsetForMotionKeyframe(
            self._window, self, self._session
        )
        # move
        self._gui_move_prx_toolset = _toolset_basic.ToolsetForMove(
            self._window, self, self._session
        )
        # constrain and deform
        self._gui_constraint_and_deform_prx_toolset = _toolset_basic.ToolsetForConstraintAndDeform(
            self._window, self, self._session
        )
        #
        self._page_prx_tab_tool_box.load_history()

        self._do_dcc_register_all_script_jobs()
        self._window.register_window_close_method(self.gui_close_fnc)

    def do_gui_refresh_all(self, force=False):
        self._page_prx_tab_tool_box.save_history()

        self._gui_rig_picker_unit.do_gui_refresh_all()
        if self._page_prx_tab_tool_box.get_current_key() == 'keyframe':
            self._gui_motion_keyframe_prx_toolset.do_gui_refresh_all()

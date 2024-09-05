# coding:utf-8
import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_gui.qt.widgets as qsm_qt_widgets

import qsm_maya.core as qsm_mya_core

from . import unit_for_motion_main_tool as _unit_for_motion_main_tool


class PrxPageForMotionMainTool(gui_prx_abstracts.AbsPrxWidget):
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
        super(PrxPageForMotionMainTool, self).__init__(*args, **kwargs)

        self._window = window
        self._session = session

        self.gui_page_setup_fnc()

    def gui_get_tool_tab_box(self):
        return self._page_prx_tab_tool_box

    def gui_close_fnc(self):
        self._page_prx_tab_tool_box.save_history()
        self._script_job_opt.destroy()

    def gui_page_setup_fnc(self):
        self._qt_widget.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        main_qt_lot = gui_qt_widgets.QtVBoxLayout(self._qt_widget)
        main_qt_lot.setContentsMargins(*[0]*4)
        main_qt_lot.setSpacing(2)
        # central
        qt_widget = gui_qt_widgets.QtTranslucentWidget()
        main_qt_lot.addWidget(qt_widget)
        qt_lot = gui_qt_widgets.QtHBoxLayout(qt_widget)
        qt_lot.setContentsMargins(*[0]*4)
        qt_lot.setSpacing(2)
        # chart
        self._qt_picker = qsm_qt_widgets.QtAdvCharacterPicker()
        qt_lot.addWidget(self._qt_picker)
        self._gui_rig_picker_unit = _unit_for_motion_main_tool.UnitForRigPicker(
            self._window, self, self._session, self._qt_picker,
        )
        # page
        self._page_prx_tab_tool_box = gui_prx_widgets.PrxVTabToolBox()
        qt_lot.addWidget(self._page_prx_tab_tool_box.widget)
        self._page_prx_tab_tool_box.set_tab_direction(self._page_prx_tab_tool_box.TabDirections.RightToLeft)
        # tool set
        # copy and paste
        self._gui_motion_copy_and_paste_prx_toolset = _unit_for_motion_main_tool.ToolsetForMotionCopyAndPaste(
            self._window, self, self._session
        )
        # keyframe
        self._gui_motion_keyframe_prx_toolset = _unit_for_motion_main_tool.ToolsetForMotionKeyframe(
            self._window, self, self._session
        )
        # move
        self._gui_move_toolset_unit = _unit_for_motion_main_tool.ToolsetForMove(
            self._window, self, self._session
        )
        #
        self._page_prx_tab_tool_box.set_history_key('lazy-motion-tool.main.page_key_current')
        self._page_prx_tab_tool_box.load_history()
        self._page_prx_tab_tool_box.connect_current_changed_to(self.do_gui_refresh_all)

        self._do_dcc_register_all_script_jobs()
        self._window.register_window_close_method(self.gui_close_fnc)

    def do_gui_refresh_all(self, force=False):
        self._gui_rig_picker_unit.do_gui_refresh_all()
        if self._page_prx_tab_tool_box.get_current_key() == 'keyframe':
            self._gui_motion_keyframe_prx_toolset.do_gui_refresh_all()

# coding:utf-8
import qsm_lazy_tool.resource.gui.abstracts as _abstracts

from . import page_for_register_tool as _page_for_register_tool

from . import page_for_load_tool as _page_for_load_tool

import qsm_maya.core as qsm_mya_core


class PrxSubPanelForTool(_abstracts.AbsPrxSubPanelForRegister):
    PAGE_FOR_REGISTER_CLS = _page_for_register_tool.PrxPageForRegisterTool
    PAGE_FOR_LOAD_CLS = _page_for_load_tool.PrxPageForLoadTool

    SCRIPT_JOB_NAME = 'lazy_resource_tool'

    def _do_dcc_register_all_script_jobs(self):
        self._script_job = qsm_mya_core.ScriptJob(
            self.SCRIPT_JOB_NAME
        )
        self._script_job.register(
            [
                self.do_gui_update_by_dcc_selection,
            ],
            self._script_job.EventTypes.SelectionChanged
        )

    def _do_dcc_destroy_all_script_jobs(self):
        self._script_job.destroy()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxSubPanelForTool, self).__init__(window, session, *args, **kwargs)

        self._do_dcc_register_all_script_jobs()
        self._window.connect_window_close_to(self._do_dcc_destroy_all_script_jobs)
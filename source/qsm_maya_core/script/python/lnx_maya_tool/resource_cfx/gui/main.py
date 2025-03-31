# coding:utf-8
import qsm_lazy_tool.resource_cfx.gui.abstracts as _abstracts

from .pages import register as _page_register

from .pages import load as _page_load

import qsm_maya.core as qsm_mya_core


class PrxLazyResourceCfxTool(_abstracts.AbsPrxSubPanelForTool):
    PAGE_FOR_REGISTER_TOOL_CLS = _page_register.PrxPageForRegisterTool
    PAGE_FOR_LOAD_TOOL_CLS = _page_load.PrxPageForLoadTool

    SCRIPT_JOB_NAME = 'lazy_resource_tool'

    def _do_dcc_register_all_script_jobs(self):
        self._script_job_opt = qsm_mya_core.ScriptJobOpt(
            self.SCRIPT_JOB_NAME
        )
        self._script_job_opt.register(
            [
                self.do_gui_update_by_dcc_selection,
            ],
            self._script_job_opt.EventTypes.SelectionChanged
        )

    def _do_dcc_destroy_all_script_jobs(self):
        self._script_job_opt.destroy()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxLazyResourceCfxTool, self).__init__(window, session, *args, **kwargs)

        self._do_dcc_register_all_script_jobs()
        self._window.register_window_close_method(self._do_dcc_destroy_all_script_jobs)

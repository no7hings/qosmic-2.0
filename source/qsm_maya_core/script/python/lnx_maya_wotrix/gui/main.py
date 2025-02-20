# coding:utf-8
from lnx_wotrix.gui.abstracts import panel_for_main as _abs_panel_for_workspace

from .pages import task_manager as _page_task_manager

from .pages import task_tool as _page_task_tool

from .pages import task_release as _page_task_release

from .subpanels import task_create as _subpanel_task_create


class PrxWotrixTool(_abs_panel_for_workspace.AbsPrxWotrixTool):
    PAGE_CLASSES = [
        # task manager
        _page_task_manager.PrxPageForTaskManager,
        # task tool
        _page_task_tool.PrxPageFortTaskTool,
        # task publish
        _page_task_release.PrxPageForTaskRelease
    ]

    SUB_PANEL_CLASSES = [
        # create
        _subpanel_task_create.PrxSubPanelForTaskCreate
    ]

    def __init__(self, window, session, *args, **kwargs):
        super(PrxWotrixTool, self).__init__(window, session, *args, **kwargs)

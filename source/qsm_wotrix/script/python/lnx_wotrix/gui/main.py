# coding:utf-8
from .abstracts import panel_for_main as _abs_panel_for_workspace

from .pages import task_overview as _page_task_overview

from .pages import task_manager as _page_task_manager

from .pages import task_tracker as _page_task_tracker

from .subpanels import task_create as _subpanel_task_create


class PrxWotrixTool(_abs_panel_for_workspace.AbsPrxWotrixTool):
    PAGE_CLASSES = [
        # task overview
        _page_task_overview.PrxPageForTaskOverview,
        # task manager
        _page_task_manager.PrxPageForTaskManager,
        # task tool
        # _page_task_tool.PrxPageForTaskTool,
        # task publish
        # _page_task_release.PrxPageForTaskRelease,
        _page_task_tracker.PrxPageForTaskTracker,
    ]

    SUBPANEL_CLASSES = [
        _subpanel_task_create.PrxSubpanelForTaskCreate
    ]

    RESOURCE_TYPE = 'shot'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxWotrixTool, self).__init__(window, session, *args, **kwargs)

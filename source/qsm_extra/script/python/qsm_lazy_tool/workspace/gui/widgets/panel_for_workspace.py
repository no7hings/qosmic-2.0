# coding:utf-8
from ..abstracts import panel_for_workspace as _abs_panel_for_workspace

from . import page_for_task_manager as _page_for_task_manager

from . import page_for_task_tool as _page_for_task_tool

from . import page_for_task_release as _page_for_task_publish

from . import sub_panel_for_task_create as _sub_panel_for_task_create


class PrxPanelForWorkspace(_abs_panel_for_workspace.AbsPrxPanelForWorkspace):
    PAGE_CLASSES = [
        # task manager
        _page_for_task_manager.PrxPageForTaskManager,
        # task tool
        # _page_for_task_tool.PrxPageForTaskTool,
        # task publish
        # _page_for_task_publish.PrxPageForTaskRelease
    ]

    SUB_PANEL_CLASSES = [
        _sub_panel_for_task_create.PrxSubPanelForTaskCreate
    ]

    RESOURCE_BRANCH = 'shot'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPanelForWorkspace, self).__init__(window, session, *args, **kwargs)

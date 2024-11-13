# coding:utf-8
from ..abstracts import panel_for_workspace as _abs_panel_for_workspace

from . import page_for_task_manager as _page_for_task_manager

from . import page_for_task_tool as _page_for_task_tool

from . import page_for_task_release as _page_for_task_publish

from . import sub_panel_for_task_create as _sub_panel_for_task_create


class PrxPanelForAssetWorkspace(_abs_panel_for_workspace.AbsPrxPanelForWorkspace):
    PAGE_CLASS_DICT = {
        # task manager
        _page_for_task_manager.PrxPageForAssetTaskManager.GUI_KEY:
        _page_for_task_manager.PrxPageForAssetTaskManager,
        # task tool
        _page_for_task_tool.PrxPageForAssetTaskTool.GUI_KEY:
        _page_for_task_tool.PrxPageForAssetTaskTool,
        # task publish
        _page_for_task_publish.PrxPageForAssetTaskRelease.GUI_KEY:
        _page_for_task_publish.PrxPageForAssetTaskRelease

    }

    SUB_PANEL_CLASS_DICT = {
        _sub_panel_for_task_create.PrxSubPanelForAssetTaskCreate.GUI_KEY:
        _sub_panel_for_task_create.PrxSubPanelForAssetTaskCreate
    }

    RESOURCE_BRANCH = 'asset'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPanelForAssetWorkspace, self).__init__(window, session, *args, **kwargs)


class PrxPanelForShotWorkspace(_abs_panel_for_workspace.AbsPrxPanelForWorkspace):
    PAGE_CLASS_DICT = {
        # task manager
        _page_for_task_manager.PrxPageForShotTaskManager.GUI_KEY:
        _page_for_task_manager.PrxPageForShotTaskManager,
        # task tool
        _page_for_task_tool.PrxPageForShotTaskTool.GUI_KEY:
        _page_for_task_tool.PrxPageForShotTaskTool,
        # task publish
        _page_for_task_publish.PrxPageForShotTaskRelease.GUI_KEY:
        _page_for_task_publish.PrxPageForShotTaskRelease
    }

    SUB_PANEL_CLASS_DICT = {
        _sub_panel_for_task_create.PrxSubPanelForShotTaskCreate.GUI_KEY:
        _sub_panel_for_task_create.PrxSubPanelForShotTaskCreate
    }

    RESOURCE_BRANCH = 'shot'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxPanelForShotWorkspace, self).__init__(window, session, *args, **kwargs)

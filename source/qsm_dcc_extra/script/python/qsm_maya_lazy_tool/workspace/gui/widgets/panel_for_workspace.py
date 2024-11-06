# coding:utf-8
from qsm_lazy_tool.workspace.gui.abstracts import panel_for_workspace as _abs_panel_for_workspace

from . import page_for_task_manager as _page_for_task_manager

from . import page_for_task_tool as _page_for_task_tool

from . import page_for_task_release as _page_for_task_publish

from . import sub_panel_for_task_create as _sub_panel_for_task_create


class PrxPanelForWorkspace(_abs_panel_for_workspace.AbsPrxPanelForWorkspace):
    PAGE_CLASS_DICT = {
        # task manager
        _page_for_task_manager.PrxPageForTaskManager.PAGE_KEY:
        _page_for_task_manager.PrxPageForTaskManager,
        # task tool
        _page_for_task_tool.PrxPageForTaskTool.PAGE_KEY:
        _page_for_task_tool.PrxPageForTaskTool,
        # task publish
        _page_for_task_publish.PrxPageForTaskPublish.PAGE_KEY:
        _page_for_task_publish.PrxPageForTaskPublish

    }

    SUB_PANEL_CLASS_DICT = {
        _sub_panel_for_task_create.PrxSubPanelForTaskCreate.SUB_PANEL_KEY:
        _sub_panel_for_task_create.PrxSubPanelForTaskCreate

    }

    def __init__(self, *args, **kwargs):
        super(PrxPanelForWorkspace, self).__init__(*args, **kwargs)

# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ...base.gui_operates import task_release as _asset_gnl_task_release


class GuiTaskReleaseOpt(_asset_gnl_task_release.GuiTaskReleaseOpt):
    def __init__(self, *args, **kwargs):
        super(GuiTaskReleaseOpt, self).__init__(*args, **kwargs)

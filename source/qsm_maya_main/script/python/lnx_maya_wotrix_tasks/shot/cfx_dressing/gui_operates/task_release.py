# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ...base.gui_operates import task_release as _shot_gnl_release


class GuiTaskReleaseOpt(_shot_gnl_release.MayaShotTaskReleaseOpt):
    def __init__(self, *args, **kwargs):
        super(GuiTaskReleaseOpt, self).__init__(*args, **kwargs)

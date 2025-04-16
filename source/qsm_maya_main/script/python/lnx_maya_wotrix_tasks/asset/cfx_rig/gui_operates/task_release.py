# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ...base.gui_operates import task_release as _asset_gnl_task_release


class MayaAssetCfxRigReleaseOpt(_asset_gnl_task_release.MayaAssetTaskReleaseOpt):
    def __init__(self, *args, **kwargs):
        super(MayaAssetCfxRigReleaseOpt, self).__init__(*args, **kwargs)

# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import asset_gnl_release as _asset_gnl_release


class MayaAssetCfxRigReleaseOpt(_asset_gnl_release.MayaAssetGnlReleaseOpt):
    def __init__(self, *args, **kwargs):
        super(MayaAssetCfxRigReleaseOpt, self).__init__(*args, **kwargs)

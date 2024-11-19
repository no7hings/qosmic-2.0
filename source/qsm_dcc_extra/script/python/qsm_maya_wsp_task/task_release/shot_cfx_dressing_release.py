# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import shot_gnl_release as _shot_gnl_release


class MayaShotCfxDressingReleaseOpt(_shot_gnl_release.MayaShotGnlReleaseOpt):
    def __init__(self, *args, **kwargs):
        super(MayaShotCfxDressingReleaseOpt, self).__init__(*args, **kwargs)

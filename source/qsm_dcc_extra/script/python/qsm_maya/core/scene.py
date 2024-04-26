# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from . import time_ as _time

from . import scene_file as _scene_file

from . import playblast as _playblast


class Scene(
    _time.Time,
    _scene_file.SceneFile,
    _playblast.Playblast
):
    @classmethod
    def show_message(cls, message, keyword, position='topCenter', fade=1, drag_kill=0, alpha=.5):
        # topLeft topCenter topRight
        # midLeft midCenter midCenterTop midCenterBot midRight
        # botLeft botCenter botRight
        cmds.inViewMessage(
            assistMessage='%s <hl>%s</hl>'%(message, keyword),
            fontSize=12,
            position=position,
            fade=fade,
            dragKill=drag_kill,
            alpha=alpha
        )

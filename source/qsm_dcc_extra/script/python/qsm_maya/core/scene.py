# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.storage as bsc_storage

from . import time_ as _time

from . import scene_file as _scene_file

from . import playblast as _playblast


class Scene(object):
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

    @classmethod
    def make_snapshot_auto(cls):
        file_path = _scene_file.SceneFile.get_current_file_path()
        file_opt = bsc_storage.StgFileOpt(file_path)
        directory_path = file_opt.get_directory_path()
        name_base = file_opt.get_name_base()
        image_file_path = '{}/.snapshot/{}.jpg'.format(directory_path, name_base)
        _playblast.Playblast.make_snapshot(image_file_path, _time.Frame.get_current_frame(), (480, 240))

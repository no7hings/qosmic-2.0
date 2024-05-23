# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.storage as bsc_storage

from . import time_ as _time

from . import scene_file as _scene_file

from . import playblast as _playblast


class Scene(object):

    @staticmethod
    def get_is_ui_mode():
        return not cmds.about(batch=1)

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

    # include instanced
    @classmethod
    def find_all_dag_nodes(cls, type_includes):
        list_ = []
        _ = cmds.ls(type=type_includes, noIntermediate=1, long=1) or []
        for i_path in _:
            i_parent_paths = cmds.listRelatives(i_path, fullPath=1, allParents=1) or []
            if len(i_parent_paths) > 1:
                i_name = i_path.split('|')[-1]
                for j_path in i_parent_paths:
                    j_path_shape = '{}|{}'.format(j_path, i_name)
                    list_.append(j_path_shape)
            else:
                list_.append(i_path)

        return list_

    @classmethod
    def remove_instanced(cls, transform_path):
        transform_name = transform_path.split('|')[-1]
        transform_name_copy = '{}_copy'.format(transform_name)
        transform_copy = cmds.duplicate(
            transform_path, name=transform_name_copy
        )
        cmds.delete(transform_path)
        cmds.rename(transform_copy[0], transform_name)

    @classmethod
    def remove_all_instanced(cls, type_includes):
        _ = cmds.ls(type=type_includes, long=1) or []
        for i_path in _:
            i_parent_paths = cmds.listRelatives(i_path, fullPath=1, allParents=1) or []
            if len(i_parent_paths) > 1:
                i_name = i_path.split('|')[-1]
                for j_transform_path in i_parent_paths:
                    j_path_shape = '{}|{}'.format(j_transform_path, i_name)
                    if j_path_shape != i_path:
                        cls.remove_instanced(j_transform_path)

    @classmethod
    def remove_all_empty_groups(cls):
        mel.eval('source cleanUpScene;deleteEmptyGroups;')

    @classmethod
    def set_background_color(cls, rgb):
        cmds.displayRGBColor('background', *rgb)
        cmds.displayRGBColor('backgroundTop', *rgb)
        cmds.displayRGBColor('backgroundBottom', *rgb)

    @classmethod
    def clear_all_hud(cls):
        for i in cmds.headsUpDisplay(listHeadsUpDisplays=1) or []:
            cmds.headsUpDisplay(i, remove=1)

    @classmethod
    def hide_all_hud(cls):
        for i in cmds.headsUpDisplay(listHeadsUpDisplays=1) or []:
            cmds.headsUpDisplay(i, edit=1, visible=0)

    @classmethod
    def clear_unknown_nodes(cls):
        _ = cmds.ls(type='unknown', long=1) or []
        if _:
            for i in _:
                if cmds.objExists(i) is True:
                    if cmds.referenceQuery(i, isNodeReferenced=1) is False:
                        cmds.lockNode(i, lock=0)
                        cmds.delete(i)

# coding:utf-8
from .wrap import *


class Selection(object):
    @classmethod
    def set(cls, paths):
        cmds.select([x for x in paths if cmds.objExists(x)])

    @classmethod
    def set_current(cls, path):
        if cmds.objExists(path):
            cmds.select(path)

    @classmethod
    def clear(cls):
        cmds.select(clear=1)

    @classmethod
    def get(cls):
        return cmds.ls(selection=1, long=1) or []

    @classmethod
    def get_as_nodes(cls):
        return [x.split('.')[0] for x in cmds.ls(selection=1, long=1) or []]

    @classmethod
    def get_all_meshes(cls, dag=True):
        return cmds.ls(selection=1, dag=dag, type='mesh', noIntermediate=1, long=1) or []

    @classmethod
    def get_all_transforms(cls, dag=False):
        return cmds.ls(selection=1, dag=dag, type='transform', noIntermediate=1, long=1) or []

    @classmethod
    def get_all_anm_curves(cls):
        return cmds.ls(selection=1, type='animCurve', long=1) or []

    @classmethod
    def get_main_controls(cls):
        list_ = []
        _ = [x.split('.')[0] for x in cmds.ls(selection=1, long=1) or []]
        for i in _:
            if cmds.objExists(i+'.translate') is True and cmds.objExists(i+'.rotate') is True:
                list_.append(i)
        return list_

    @classmethod
    def get_one_node(cls):
        _ = cls.get_as_nodes()
        if _:
            return _[0]
    
    @classmethod
    def get_path_map(cls):
        dict_ = {}
        _ = cmds.ls(selection=1, long=1) or []
        for i_path in _:
            if '.' in i_path:
                i_key = i_path.split('.')[0]
                dict_.setdefault(i_key, []).append(i_path)
            else:
                i_shapes = cmds.listRelatives(i_path, children=1, shapes=1, noIntermediate=1, fullPath=1)
                if i_shapes:
                    dict_.setdefault(i_path, []).extend(i_shapes)
                else:
                    dict_.setdefault(i_path, []).append(i_path)

        return dict_

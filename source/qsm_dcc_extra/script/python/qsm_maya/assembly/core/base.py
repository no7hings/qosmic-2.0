# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

from ... import core as _mya_core


class UnitAssemblyQuery(object):
    class Keys(object):
        GPU = 'GPU'
        GPU_LOD = 'GPU-LOD{}'
        GPU_LOD_1 = 'GPU-LOD1'
        GPU_LOD_2 = 'GPU-LOD2'
        Mesh = 'Mesh'
        Mesh_LOD = 'Mesh-LOD{}'
        Mesh_LOD_1 = 'Mesh-LOD1'
        Mesh_LOD_2 = 'Mesh-LOD2'

        All = [
            GPU,
            GPU_LOD_1,
            GPU_LOD_2,
            Mesh,
            Mesh_LOD_1,
            Mesh_LOD_2
        ]

    UNIT_PATTERN = '*/unit-assembly/*/unit/*/unit.AD.ma'

    @classmethod
    def to_unit_path(cls, path):
        pass

    @classmethod
    def get_all_units(cls):
        list_ = []
        _ = cmds.ls(
            type='assemblyReference', long=1
        )
        for i_path in _:
            i_file_path = _mya_core.AssemblyReference.get_file(i_path)
            if bsc_core.PtnFnmatchMtd.filter(
                [i_file_path], cls.UNIT_PATTERN
            ):
                list_.append(i_path)
        return list_

    @classmethod
    def find_unit(cls, path):
        if _mya_core.Node.is_transform(path):
            return None
        path_opt = bsc_core.PthNodeOpt(path)
        paths = path_opt.get_ancestor_paths()
        for i_path in paths:
            if i_path != _mya_core.DagNode.PATHSEP:
                if _mya_core.Node.is_assembly_reference(i_path) is True:
                    return i_path


class AsbGroupOpt(object):

    def __init__(self, path):
        self._path = path

    def get_all_units(self):
        _ = cmds.ls(
            self._path, type='assemblyReference', long=1, dag=1
        )
        _.remove(self._path)
        return _

    def is_include(self, path):
        return not not bsc_core.PtnFnmatchMtd.filter(
            [path], '{}|*'.format(self._path)
        )

    def find_unit(self, path):
        if _mya_core.Node.is_transform(path):
            return None
        path_opt = bsc_core.PthNodeOpt(path)
        paths = path_opt.get_ancestor_paths()
        for i_path in paths:
            if i_path != _mya_core.DagNode.PATHSEP:
                if _mya_core.Node.is_assembly_reference(i_path) is True:
                    if i_path != self._path:
                        return i_path

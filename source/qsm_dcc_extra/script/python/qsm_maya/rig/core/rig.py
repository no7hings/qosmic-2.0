# coding:utf-8
import collections
import copy
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.asset.core as qsm_mya_ast_core


class Rig(object):
    def __init__(self, namespace):
        self.namespace = namespace

    def __str__(self):
        return 'Rig(path="{}")'.format(
            self.__dict__['path']
        )

    def get_root(self):
        _ = cmds.ls('|{}:*'.format(self.namespace), long=1)
        if _:
            return _[0]

    def get_geometry_location(self):
        _ = cmds.ls('{}:Geometry'.format(self.namespace), long=1)
        if _:
            return _[0]

    def get_motion_location(self):
        _ = cmds.ls('{}:MotionSystem'.format(self.namespace), long=1)
        if _:
            return _[0]

    def get_deformation_location(self):
        _ = cmds.ls('{}:DeformationSystem'.format(self.namespace), long=1)
        if _:
            return _[0]

    def get_skin_proxy_location(self):
        _ = cmds.ls('{}:skin_proxy_dgc'.format(self.namespace), long=1)
        if _:
            return _[0]

    def get_skin_proxy_exists(self):
        _ = self.get_skin_proxy_location()
        if _:
            if cmds.objExists(_) is True:
                return True
        return False

    def get_dynamic_gpu_location(self):
        _ = cmds.ls('{}:dynamic_gpu_dgc'.format(self.namespace), long=1)
        if _:
            return _[0]

    def get_dynamic_gpu_exists(self):
        _ = self.get_dynamic_gpu_location()
        if _:
            if cmds.objExists(_) is True:
                return True
        return False

    def get_location_for_selection(self, scheme):
        if self.get_dynamic_gpu_exists() is True:
            return self.get_dynamic_gpu_location()
        if scheme == 'root':
            return self.get_root()
        elif scheme == 'geometry':
            return self.get_geometry_location()
        elif scheme == 'motion':
            return self.get_motion_location()
        elif scheme == 'deformation':
            return self.get_deformation_location()


class RigsQuery(object):
    STG_PTN = 'X:/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'

    DAG_PTN = '/{namespace}'

    def __init__(self):
        self._pth = bsc_core.PtnStgParseOpt(
            self.STG_PTN
        )
        self._cache_dict = collections.OrderedDict()

        self._cache_all()

    def _cache_all(self):
        _ = qsm_mya_core.References.get_all()
        for i_path in _:
            i_file_path = qsm_mya_core.Reference.get_file_path(i_path)
            if self._pth.get_is_matched(i_file_path) is True:
                i_namespace = cmds.referenceQuery(i_path, namespace=1, shortName=1)
                i_reference_node = qsm_mya_core.ReferenceNode(i_path)
                i_variants = self._pth.get_variants(i_file_path)
                i_rig = Rig(i_namespace)
                i_rig.reference_node = i_reference_node
                i_kwargs = copy.copy(i_variants)
                i_kwargs['namespace'] = i_namespace
                i_path = '/{}'.format(i_namespace)
                i_rig.path = i_path
                i_rig.path_opt = bsc_core.PthNodeOpt(i_path)
                i_rig.variants = i_variants
                self._cache_dict[i_path] = i_rig

    def get_all(self):
        return self._cache_dict.values()

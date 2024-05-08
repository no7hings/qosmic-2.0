# coding:utf-8
import collections
import copy
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import qsm_maya.core as qsm_mya_core


class AdvOptions(object):
    Geometry = 'Geometry'


class AdvRigOpt(object):
    def __init__(self, namespace):
        self.namespace = namespace

    def __str__(self):
        return 'AdvRigOpt(path="{}")'.format(
            self.__class__.__name__,
            self.__dict__['path']
        )

    def is_exists(self):
        return not not self.get_root()

    def get_root(self):
        _ = cmds.ls('|{}:*'.format(self.namespace), long=1)
        if _:
            return _[0]

    def get_geometry_location(self):
        _ = cmds.ls('{}:Geometry'.format(self.namespace), long=1)
        if _:
            return _[0]

    def get_animation_location(self):
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
            return self.get_animation_location()
        elif scheme == 'deformation':
            return self.get_deformation_location()


class AdvRigQuery(object):
    STG_PTN = 'X:/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'

    DAG_PTN = '/{namespace}'

    def __init__(self):
        self._pth = bsc_core.PtnStgParseOpt(
            self.STG_PTN
        )
        self._cache_dict = collections.OrderedDict()

        self.do_update()

    def do_update(self):
        _ = qsm_mya_core.References.get_all()
        for i_path in _:
            i_file_path = qsm_mya_core.Reference.get_file(i_path)
            if self._pth.get_is_matched(i_file_path) is True:
                i_namespace = cmds.referenceQuery(i_path, namespace=1, shortName=1)
                i_reference_opt = qsm_mya_core.ReferenceOpt(i_path)
                i_variants = self._pth.get_variants(i_file_path)
                i_rig_opt = AdvRigOpt(i_namespace)
                i_rig_opt.reference_opt = i_reference_opt
                i_kwargs = copy.copy(i_variants)
                i_kwargs['namespace'] = i_namespace
                i_path = '/{}'.format(i_namespace)
                i_rig_opt.path = i_path
                i_rig_opt.path_opt = bsc_core.PthNodeOpt(i_path)
                i_rig_opt.variants = i_variants
                self._cache_dict[i_namespace] = i_rig_opt

    def get_all(self):
        return self._cache_dict.values()

    def to_valid_namespaces(self, namespaces):
        return [i for i in namespaces if i in self._cache_dict]

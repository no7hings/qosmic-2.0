# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core

from ...resource import core as _rsc_core


class AdvRig(_rsc_core.Resource):
    def __init__(self, *args, **kwargs):
        super(AdvRig, self).__init__(*args, **kwargs)

    def get_root(self):
        _ = cmds.ls('|{}:*'.format(self.namespace), long=1)
        if _:
            return _[0]

    def get_geometry_root(self):
        _ = cmds.ls('{}:Geometry'.format(self.namespace), long=1)
        if _:
            return _[0]

    def get_all_meshes(self):
        _ = self.get_geometry_root()
        if _:
            return cmds.ls(
                _, type='mesh', long=1, noIntermediate=1, dag=1
            )

    def get_motion_root(self):
        _ = cmds.ls('{}:MotionSystem'.format(self.namespace), long=1)
        if _:
            return _[0]

    def get_deformation_root(self):
        _ = cmds.ls('{}:DeformationSystem'.format(self.namespace), long=1)
        if _:
            return _[0]

    def get_main_control(self):
        _ = cmds.ls('{}:Main'.format(self.namespace), long=1)
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

    def get_skin_proxy_is_enable(self):
        _ = self.get_skin_proxy_location()
        if _:
            return _mya_core.NodeDisplay.is_visible(_)
        return False

    def set_skin_proxy_enable(self, boolean):
        location = self.get_skin_proxy_location()
        layers = _mya_core.Container.find_all_nodes(
            location, ['displayLayer']
        )
        _mya_core.NodeDisplay.set_visible(
            location, boolean
        )
        if layers:
            for i in layers:
                _mya_core.DisplayLayer.set_visible(i, not boolean)

    def get_dynamic_gpu_location(self):
        _ = cmds.ls('{}:dynamic_gpu_dgc'.format(self.namespace), long=1)
        if _:
            return _[0]

    def get_dynamic_gpu_is_enable(self):
        _ = self.get_dynamic_gpu_location()
        if _:
            return _mya_core.NodeDisplay.is_visible(_)
        return False

    def set_dynamic_gpu_enable(self, boolean):
        location = self.get_dynamic_gpu_location()
        layers = _mya_core.Container.find_all_nodes(
            location, ['displayLayer']
        )
        _mya_core.NodeDisplay.set_visible(
            location, boolean
        )
        if layers:
            for i in layers:
                _mya_core.DisplayLayer.set_visible(i, not boolean)

    def get_dynamic_gpu_exists(self):
        _ = self.get_dynamic_gpu_location()
        if _:
            if cmds.objExists(_) is True:
                return True
        return False

    def find_nodes_by_scheme(self, scheme):
        if self.get_dynamic_gpu_is_enable() is True:
            return [self.get_dynamic_gpu_location()]

        if scheme == 'root':
            return [self.get_root()]
        elif scheme == 'geometry_root':
            return [self.get_geometry_root()]
        elif scheme == 'motion_root':
            return [self.get_motion_root()]
        elif scheme == 'deformation_root':
            return [self.get_deformation_root()]
        elif scheme == 'main_control':
            return [self.get_main_control()]

    def get_joint(self, name):
        _ = cmds.ls('{}:{}'.format(self.namespace, name), long=1)
        if _:
            return _[0]


class AdvRigsQuery(_rsc_core.ResourcesQuery):
    STG_PTN = 'X:/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'

    RESOURCE_CLS = AdvRig

    def __init__(self):
        super(AdvRigsQuery, self).__init__()

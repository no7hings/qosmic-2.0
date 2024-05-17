# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ...resource import core as _rsc_core


class AdvRig(_rsc_core.Resource):
    def __init__(self, *args, **kwargs):
        super(AdvRig, self).__init__(*args, **kwargs)

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

    def find_nodes_by_scheme(self, scheme):
        if self.get_dynamic_gpu_exists() is True:
            return [self.get_dynamic_gpu_location()]
        if scheme == 'root':
            return [self.get_root()]
        elif scheme == 'geometry':
            return [self.get_geometry_location()]
        elif scheme == 'motion':
            return [self.get_motion_location()]
        elif scheme == 'deformation':
            return [self.get_deformation_location()]


class AdvRigsQuery(_rsc_core.ResourcesQuery):
    STG_PTN = 'X:/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'

    RESOURCE_CLS = AdvRig

    def __init__(self):
        super(AdvRigsQuery, self).__init__()

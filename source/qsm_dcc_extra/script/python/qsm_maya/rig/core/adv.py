# coding:utf-8
import collections

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

from ... import core as _mya_core

from ...resource import core as _rsc_core


class AdvRig(_rsc_core.Resource):
    def __init__(self, *args, **kwargs):
        super(AdvRig, self).__init__(*args, **kwargs)
        
        self._switch_result = {}

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

    def is_skin_proxy_exists(self):
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
        if location is None:
            return False

        layers = _mya_core.Container.find_all_nodes(
            location, ['displayLayer']
        )
        _mya_core.NodeDisplay.set_visible(
            location, boolean
        )
        if layers:
            for i in layers:
                _mya_core.DisplayLayer.set_visible(i, not boolean)
        return True

    def remove_skin_proxy(self):
        location = self.get_skin_proxy_location()
        if location is None:
            return False
        _mya_core.Node.delete(location)
        return True

    def get_dynamic_gpu_location(self):
        _ = cmds.ls('{}:dynamic_gpu_dgc'.format(self.namespace), long=1)
        if _:
            return _[0]

    def is_dynamic_gpu_exists(self):
        _ = self.get_dynamic_gpu_location()
        if _:
            if cmds.objExists(_) is True:
                return True
        return False

    def get_dynamic_gpu_is_enable(self):
        _ = self.get_dynamic_gpu_location()
        if _:
            return _mya_core.NodeDisplay.is_visible(_)
        return False

    def set_dynamic_gpu_enable(self, boolean):
        location = self.get_dynamic_gpu_location()
        if location is None:
            return False

        layers = _mya_core.Container.find_all_nodes(
            location, ['displayLayer']
        )
        _mya_core.NodeDisplay.set_visible(
            location, boolean
        )
        if layers:
            for i in layers:
                _mya_core.DisplayLayer.set_visible(i, not boolean)

        return True

    def remove_dynamic_gpu(self):
        location = self.get_dynamic_gpu_location()
        if location is None:
            return False
        _mya_core.Node.delete(location)
        return True

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

    def find_joint(self, name):
        _ = cmds.ls('{}:{}'.format(self.namespace, name), long=1)
        if _:
            return _[0]

    def switch_to_original(self):
        self._switch_result = {}
        if self.get_skin_proxy_is_enable() is True:
            self._switch_result['skin_proxy'] = True
            self.set_skin_proxy_enable(False)

        if self.get_dynamic_gpu_is_enable():
            self._switch_result['dynamic_gpu'] = True
            self.set_dynamic_gpu_enable(False)

        return self._switch_result

    def switch_to_cache(self):
        for k, v in self._switch_result.items():
            if k == 'skin_proxy':
                self.set_skin_proxy_enable(True)
            elif k == 'dynamic_gpu':
                self.set_dynamic_gpu_enable(True)
    
    def generate_joint_transformation_data(self):
        joint_root = self.get_deformation_root()
        if joint_root:
            return collections.OrderedDict(
                [
                    (':'.join(x.split('|')[-1].split(':')[1:]), _mya_core.Transform.get_world_transformation(x))
                    for x in cmds.ls(joint_root, dag=1, type='joint', long=1) or []
                ]
            )
        return {}

    def generate_geometry_bbox_data(self):
        dict_ = collections.OrderedDict()
        geometry_root = self.get_geometry_root()
        if geometry_root:
            _ = cmds.ls(geometry_root, dag=1, type='mesh', noIntermediate=1, long=1)
            for i in _:
                i_transform_path = _mya_core.Shape.get_transform(i)
                i_key = ':'.join(i_transform_path.split('|')[-1].split(':')[1:])
                dict_[i_key] = _mya_core.Transform.get_world_extent(i_transform_path)
        return dict_

    def find_geometry_shape(self, key):
        _ = cmds.ls('{namespace}:{transform}'.format(namespace=self.namespace, transform=key), long=1)
        if _:
            return _[0]


class AdvRigsQuery(_rsc_core.ResourcesQuery):
    STG_PTN = 'X:/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'

    RESOURCE_CLS = AdvRig

    def __init__(self):
        super(AdvRigsQuery, self).__init__()

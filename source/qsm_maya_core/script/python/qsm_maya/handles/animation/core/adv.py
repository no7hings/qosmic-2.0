# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.general.core as qsm_mya_gnl_core

import qsm_maya.resource.core as qsm_mya_rsc_core


class AdvRigAsset(qsm_mya_rsc_core.Asset):

    @classmethod
    def filter_namespaces(cls, namespaces):
        return [x for x in namespaces if cls(x).find_motion_location() is not None]

    def __init__(self, *args, **kwargs):
        super(AdvRigAsset, self).__init__(*args, **kwargs)
        
        self._switch_result = {}

    def get_root(self):
        # fixme: use * as temporary, need new method to fild root
        _ = cmds.ls('|{}:*'.format(self.namespace), long=1)
        if _:
            return _[0]
        # root may put in group
        _ = cmds.ls('*|{}:*'.format(self.namespace), long=1)
        if _:
            return _[0]

    def find_geometry_location(self):
        _ = cmds.ls('{}:Geometry'.format(self.namespace), long=1)
        if _:
            return _[0]

    def find_geo_lower_location(self):
        """
        ADV没有这个设置，这是个临时设置，后面会使用配置控制
        """
        _0 = cmds.ls('{}:Low_Grp'.format(self._namespace), long=1)
        if _0:
            return _0[0]
        _1 = cmds.ls('{}:Group'.format(self._namespace), long=1)
        if _1:
            return _1[0]

    def find_motion_location(self):
        _ = cmds.ls('{}:MotionSystem'.format(self.namespace), long=1)
        if _:
            return _[0]

    def find_deformation_location(self):
        _ = cmds.ls('{}:DeformationSystem'.format(self.namespace), long=1)
        if _:
            return _[0]

    def find_main_control(self):
        _ = cmds.ls('{}:Main'.format(self.namespace), long=1)
        if _:
            return _[0]

    def find_sub_controls(self):
        pass

    # skin proxy
    def get_skin_proxy_location(self):
        _ = cmds.ls(
            '{}:{}'.format(self.namespace, qsm_mya_gnl_core.ResourceCacheNodes.SkinProxyName),
            long=1
        )
        if _:
            return _[0]

    def is_skin_proxy_exists(self):
        _ = self.get_skin_proxy_location()
        if _:
            if cmds.objExists(_) is True:
                return True
        return False

    def is_skin_proxy_enable(self):
        _ = self.get_skin_proxy_location()
        if _:
            return qsm_mya_core.NodeDisplay.is_visible(_)
        return False

    def set_skin_proxy_enable(self, boolean):
        location = self.get_skin_proxy_location()
        if location is None:
            return False

        layers = qsm_mya_core.Container.find_all_nodes(
            location, ['displayLayer']
        )
        qsm_mya_core.NodeDisplay.set_visible(
            location, boolean
        )
        if layers:
            for i in layers:
                qsm_mya_core.DisplayLayer.set_visible(i, not boolean)
        return True

    def remove_skin_proxy(self):
        location = self.get_skin_proxy_location()
        if location is None:
            return False
        qsm_mya_core.Node.delete(location)
        return True

    # dynamic gpu
    def get_dynamic_gpu_location(self):
        _ = cmds.ls(
            '{}:{}'.format(self.namespace, qsm_mya_gnl_core.ResourceCacheNodes.DynamicGpuName),
            long=1
        )
        if _:
            return _[0]

    def is_dynamic_gpu_exists(self):
        _ = self.get_dynamic_gpu_location()
        if _:
            if cmds.objExists(_) is True:
                return True
        return False

    def is_dynamic_gpu_enable(self):
        _ = self.get_dynamic_gpu_location()
        if _:
            return qsm_mya_core.NodeDisplay.is_visible(_)
        return False

    def set_dynamic_gpu_enable(self, boolean):
        location = self.get_dynamic_gpu_location()
        if location is None:
            return False

        layers = qsm_mya_core.Container.find_all_nodes(
            location, ['displayLayer']
        )
        qsm_mya_core.NodeDisplay.set_visible(
            location, boolean
        )
        if layers:
            for i in layers:
                qsm_mya_core.DisplayLayer.set_visible(i, not boolean)

        return True

    def remove_dynamic_gpu(self):
        location = self.get_dynamic_gpu_location()
        if location is None:
            return False
        qsm_mya_core.Node.delete(location)
        return True

    # cfx cloth
    def get_cfx_cloth_location(self):
        _ = cmds.ls(
            '{}:{}'.format(self.namespace, qsm_mya_gnl_core.ResourceCacheNodes.CfxClothName),
            long=1
        )
        if _:
            return _[0]

    def is_cfx_cloth_exists(self):
        _ = self.get_cfx_cloth_location()
        if _:
            if cmds.objExists(_) is True:
                return True
        return False
    
    def find_nodes_by_scheme(self, scheme):
        if self.is_dynamic_gpu_enable() is True:
            return [self.get_dynamic_gpu_location()]

        if scheme == 'root':
            return [self.get_root()]
        elif scheme == 'geometry_root':
            return [self.find_geometry_location()]
        elif scheme == 'motion_root':
            return [self.find_motion_location()]
        elif scheme == 'deformation_root':
            return [self.find_deformation_location()]
        elif scheme == 'main_control':
            return [self.find_main_control()]

    def find_joint(self, name):
        _ = cmds.ls('{}:{}'.format(self.namespace, name), type='joint', long=1)
        if _:
            return _[0]

    def find_one_control(self, control_key):
        _ = cmds.ls('{}:{}'.format(self.namespace, control_key), long=1)
        if _:
            return _[0]

    def find_many_controls(self, regex):
        return cmds.ls('{}:{}'.format(self.namespace, regex), long=1) or []

    def switch_to_original(self):
        self._switch_result = {}
        if self.is_skin_proxy_enable() is True:
            self._switch_result['skin_proxy'] = True
            self.set_skin_proxy_enable(False)

        if self.is_dynamic_gpu_enable():
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
        joint_root = self.find_deformation_location()
        if joint_root:
            return collections.OrderedDict(
                [
                    (':'.join(x.split('|')[-1].split(':')[1:]), qsm_mya_core.Transform.get_world_transformation(x))
                    for x in cmds.ls(joint_root, dag=1, type='joint', long=1) or []
                ]
            )
        return {}

    def generate_geometry_bbox_data(self):
        dict_ = collections.OrderedDict()
        geometry_root = self.find_geometry_location()
        if geometry_root:
            _ = cmds.ls(geometry_root, dag=1, type='mesh', noIntermediate=1, long=1) or []
            for i in _:
                i_transform_path = qsm_mya_core.Shape.get_transform(i)
                i_key = ':'.join(i_transform_path.split('|')[-1].split(':')[1:])
                dict_[i_key] = qsm_mya_core.Transform.get_world_extent(i_transform_path)
        return dict_

    @classmethod
    def path_to_key(cls, namespace, root, path, pathsep):
        path_strip = path[len(root):]
        return '/'.join(
            map(
                lambda x: x[len(namespace)+1:] if x.startswith(namespace) else x,
                path_strip.split(pathsep)
            )
        )

    @classmethod
    def key_to_path(cls, namespace, root, key, pathsep):
        return '{}{}'.format(
            root, pathsep.join(map(lambda x: '{}:{}'.format(namespace, x) if x else x, key.split('/')))
        )

    def find_geometry_shape(self, key):
        _ = cmds.ls(
            '{namespace}:{transform}|*:*'.format(namespace=self.namespace, transform=key),
            noIntermediate=1, type='mesh', long=1
        )
        if _:
            return _[0]

    def find_all_meshes(self):
        geometry_root = self.find_geometry_location()
        if geometry_root:
            return cmds.ls(geometry_root, dag=1, type='mesh', noIntermediate=1, long=1) or []
        return []

    def generate_geometry_topology_data(self):
        dict_ = collections.OrderedDict()
        namespace = self._namespace
        geometry_root = self.find_geometry_location()
        if geometry_root:
            _ = cmds.ls(geometry_root, dag=1, type='mesh', noIntermediate=1, long=1) or []
            for i in _:
                i_transform_path = qsm_mya_core.Shape.get_transform(i)
                i_transform_name = i_transform_path.split('|')[-1]
                # ignore when not form this asset
                if not i_transform_name.startswith(namespace+':'):
                    continue
                i_key = self.path_to_key(namespace, geometry_root, i_transform_path, pathsep='|')
                dict_[i_key] = qsm_mya_core.MeshShapeOpt(i).get_face_vertices_as_uuid()
        return dict_

    def pull_geometry_topology_data(self):
        if self._file_path:
            data_path = qsm_gnl_core.DccCache.generate_rig_geometry_data_file(
                self._file_path, 'topology'
            )
            if bsc_storage.StgPath.get_is_file(data_path) is True:
                data = bsc_storage.StgFileOpt(data_path).set_read()
            else:
                data = self.generate_geometry_topology_data()
                bsc_storage.StgFileOpt(data_path).set_write(data)
            return data

    def get_all_for_isolate_select(self):
        roots = list(filter(None, [self.get_root()]))
        _ = self.get_skin_proxy_location()
        if _:
            roots.append(_)
        _ = self.get_dynamic_gpu_location()
        if _:
            roots.append(_)
        return roots


class AdvRigAssetsQuery(qsm_mya_rsc_core.AssetsQuery):
    SCENE_PATTERN = 'X:/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'

    RESOURCE_CLS = AdvRigAsset

    def __init__(self):
        super(AdvRigAssetsQuery, self).__init__()

    def check_is_valid(self, *args, **kwargs):
        is_loaded = kwargs['is_loaded']
        if is_loaded:
            namespace = kwargs['namespace']
            _ = cmds.ls('{}:Root_M'.format(namespace), long=1)
            if _:
                if cmds.nodeType(_[0]) == 'joint':
                    return True
            return False
        else:
            file_path = kwargs['file']
            return self._pth.check_is_matched(file_path)

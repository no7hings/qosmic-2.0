# coding:utf-8
import collections

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from .... import core as _mya_core

from ...animation import core as _animation_core


class CfxAdvRigAssetOld(_animation_core.AdvRigAsset):
    def __init__(self, *args, **kwargs):
        super(CfxAdvRigAssetOld, self).__init__(*args, **kwargs)

    def generate_cfx_cloth_export_args(self):
        mesh_transforms = []
        root = self.get_root()
        if root:
            _ = cmds.ls(
                '{}:*'.format(self._namespace), dag=1, type='nCloth', noIntermediate=1, long=1
            ) or []
            for i_path in _:
                i_mesh_transform_path = _mya_core.NCloth.find_input_mesh_transform(i_path)
                if i_mesh_transform_path:
                    mesh_transforms.append(i_mesh_transform_path)
        return mesh_transforms
    
    def generate_cfx_component_data(self):
        dict_ = collections.OrderedDict()
        root = self.get_root()
        if root:
            # nCloth
            results = cmds.ls(
                '{}:*'.format(self._namespace), dag=1, type='nCloth', noIntermediate=1, long=1
            ) or []
            for i in results:
                i_mesh_transform_path = _mya_core.NCloth.find_input_mesh_transform(i)
                if i_mesh_transform_path:
                    i_mesh_path = '{}/{}'.format(
                        self._path, _mya_core.DagNode.to_name_without_namespace(i_mesh_transform_path)
                    )
                    i_node_path = '{}/{}'.format(
                        i_mesh_path, _mya_core.DagNode.to_name_without_namespace(i)
                    )
                    dict_[i_mesh_path] = i_mesh_transform_path
                    dict_[i_node_path] = i
            # nRigid
            results = cmds.ls(
                '{}:*'.format(self._namespace), dag=1, type='nRigid', noIntermediate=1, long=1
            ) or []
            for i in results:
                i_mesh_transform_path = _mya_core.NRigid.find_input_mesh_transform(i)
                if i_mesh_transform_path:
                    i_mesh_path = '{}/{}'.format(
                        self._path, _mya_core.DagNode.to_name_without_namespace(i_mesh_transform_path)
                    )
                    i_node_path = '{}/{}'.format(
                        i_mesh_path, _mya_core.DagNode.to_name_without_namespace(i)
                    )
                    dict_[i_mesh_path] = i_mesh_transform_path
                    dict_[i_node_path] = i
            # nucleus
            results = cmds.ls(
                '{}:*'.format(self._namespace), dag=1, type='nucleus', long=1
            ) or []
            for i in results:
                i_node_path = '{}/{}'.format(
                    self._path, _mya_core.DagNode.to_name_without_namespace(i)
                )
                dict_[i_node_path] = i

        return dict_


class CfxAdvRigAssetsQueryOld(_animation_core.AdvRigAssetsQuery):
    SCENE_PATTERN = 'X:/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'

    RESOURCE_CLS = CfxAdvRigAssetOld

    def __init__(self):
        super(CfxAdvRigAssetsQueryOld, self).__init__()


class CfxAdvRigAsset(_animation_core.AdvRigAsset):
    def __init__(self, *args, **kwargs):
        super(CfxAdvRigAsset, self).__init__(*args, **kwargs)

    def load_cfx_rig(self):
        pass

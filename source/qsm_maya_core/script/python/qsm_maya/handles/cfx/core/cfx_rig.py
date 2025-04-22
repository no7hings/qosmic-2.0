# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

from ...animation import core as _tsk_anm_core


class CfxAdvRigAsset(_tsk_anm_core.AdvRigAsset):
    def __init__(self, *args, **kwargs):
        super(CfxAdvRigAsset, self).__init__(*args, **kwargs)

        self._cfx_rig_namespace = '{}:cfx_rig'.format(self._namespace)

    def generate_cloth_abc_cache_export_args(self):
        return []
    
    def generate_cfx_component_data(self):
        dict_ = collections.OrderedDict()
        root = self.get_root()
        if root:
            # nCloth
            results = cmds.ls(
                '{}:*'.format(self._cfx_rig_namespace), dag=1, type='nCloth', noIntermediate=1, long=1
            ) or []
            for i in results:
                i_mesh_transform_path = qsm_mya_core.NCloth.find_input_mesh_transform(i)
                if i_mesh_transform_path:
                    i_mesh_path = '{}/{}'.format(
                        self._path, qsm_mya_core.DagNode.to_name_without_namespace(i_mesh_transform_path)
                    )
                    i_node_path = '{}/{}'.format(
                        i_mesh_path, qsm_mya_core.DagNode.to_name_without_namespace(i)
                    )
                    dict_[i_mesh_path] = i_mesh_transform_path
                    dict_[i_node_path] = i
            # nRigid
            results = cmds.ls(
                '{}:*'.format(self._cfx_rig_namespace), dag=1, type='nRigid', noIntermediate=1, long=1
            ) or []
            for i in results:
                i_mesh_transform_path = qsm_mya_core.NRigid.find_input_mesh_transform(i)
                if i_mesh_transform_path:
                    i_mesh_path = '{}/{}'.format(
                        self._path, qsm_mya_core.DagNode.to_name_without_namespace(i_mesh_transform_path)
                    )
                    i_node_path = '{}/{}'.format(
                        i_mesh_path, qsm_mya_core.DagNode.to_name_without_namespace(i)
                    )
                    dict_[i_mesh_path] = i_mesh_transform_path
                    dict_[i_node_path] = i
            # nucleus
            results = cmds.ls(
                '{}:*'.format(self._cfx_rig_namespace), dag=1, type='nucleus', long=1
            ) or []
            for i in results:
                i_node_path = '{}/{}'.format(
                    self._path, qsm_mya_core.DagNode.to_name_without_namespace(i)
                )
                dict_[i_node_path] = i

        return dict_


class CfxAdvRigAssetsQuery(_tsk_anm_core.AdvRigAssetsQuery):
    SCENE_PATTERN = 'X:/{project}/Assets/{role}/{asset}/Rig/Final/scenes/{asset}_Skin.ma'

    RESOURCE_CLS = CfxAdvRigAsset

    def __init__(self):
        super(CfxAdvRigAssetsQuery, self).__init__()

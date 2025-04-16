# coding:utf-8
import json
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core

import qsm_maya.adv as qsm_mya_adv

from . import dcc_organize as _cfx_rig_operate


# rig
class AssetCfxRigSceneOpt(object):
    RIG_NAMESPACE = 'rig'

    @classmethod
    def load_rig(cls, scene_path):
        qsm_mya_core.SceneFile.reference_file(
            scene_path, cls.RIG_NAMESPACE
        )

    @classmethod
    def remove_rig(cls):
        qsm_mya_core.Frame.set_current(1)

        opt = qsm_mya_adv.AdvOpt(cls.RIG_NAMESPACE)
        opt.rest_controls_transformation(translate=True, rotate=True)
        qsm_mya_core.SceneFile.refresh()

        node = qsm_mya_core.ReferencesCache().get(cls.RIG_NAMESPACE)
        qsm_mya_core.Reference.remove(node)

    def __init__(self, *args, **kwargs):
        if qsm_mya_core.Namespace.is_exists(self.RIG_NAMESPACE) is False:
            raise RuntimeError()

        self._adv_rig = qsm_mya_adv.AdvOpt(self.RIG_NAMESPACE)

        self._mesh_set = set(self._adv_rig.find_all_meshes())
        self._mesh_set.update(set(self._adv_rig.find_all_lower_meshes()))
        self._control_set = set(self._adv_rig.find_all_transform_controls())

    def find_rig_node(self, name):
        _ = cmds.ls('{}:{}'.format(self.RIG_NAMESPACE, name), long=1)
        if _:
            return _[0]

    @property
    def mesh_set(self):
        return self._mesh_set

    @property
    def control_set(self):
        return self._control_set

    def generate_blend_map(self, disable=False):
        dict_ = {}
        for i_mesh_shape in self._mesh_set:
            i_mesh_transform = qsm_mya_core.Shape.get_transform(i_mesh_shape)
            i_name = qsm_mya_core.DagNode.to_name_without_namespace(i_mesh_transform)
            i_blend_nodes = qsm_mya_core.MeshBlendSource.get_deform_nodes(
                i_mesh_transform
            )
            if i_blend_nodes:
                i_names = []
                for j_blend_node in i_blend_nodes:
                    # ignore form reference
                    if qsm_mya_core.Reference.is_from_reference(j_blend_node) is True:
                        continue

                    j_name = qsm_mya_core.DagNode.to_name_without_namespace(j_blend_node)
                    i_names.append(j_name)

                    qsm_mya_core.NodeAttribute.create_as_string(
                        j_blend_node, 'qsm_blend_source', i_name
                    )

                    if disable is True:
                        qsm_mya_core.NodeAttribute.set_value(
                            j_blend_node, 'envelope', 0
                        )

                if i_names:
                    dict_[i_name] = i_names
        return dict_

    def generate_constraint_map(self, disable=False):
        dict_ = {}
        for i_control_transform in self._control_set:
            i_name = qsm_mya_core.DagNode.to_name_without_namespace(i_control_transform)

            i_constraint_nodes = qsm_mya_core.ParentConstraintSource.get_constraint_nodes(i_control_transform)
            if i_constraint_nodes:
                i_names = []
                for j_constraint_node in i_constraint_nodes:
                    # ignore form reference
                    if qsm_mya_core.Reference.is_from_reference(j_constraint_node) is True:
                        continue

                    j_name = qsm_mya_core.DagNode.to_name_without_namespace(j_constraint_node)
                    i_names.append(j_name)

                    qsm_mya_core.NodeAttribute.create_as_string(
                        j_constraint_node, 'qsm_constraint_source', i_name
                    )

                if i_names:
                    dict_[i_name] = i_names
        return dict_

    def generate_hidden_set(self):
        layer_name = _cfx_rig_operate.CfxSourceGeoLyrOrg().NAME

        set_ = set()
        if qsm_mya_core.Node.is_exists(layer_name):
            paths = [
                qsm_mya_core.DagNode.to_path(x) for x in qsm_mya_core.DisplayLayer.get_all(layer_name)
            ]
            # qsm_mya_core.DisplayLayer.set_visible(layer_name, False)
            for i_mesh_shape in self._mesh_set:
                i_mesh_transform = qsm_mya_core.Shape.get_transform(i_mesh_shape)
                if i_mesh_transform not in paths:
                    continue

                i_name = qsm_mya_core.DagNode.to_name_without_namespace(i_mesh_transform)
                # if qsm_mya_core.Transform.is_override_hidden(i_mesh_transform) is True:
                set_.add(i_name)

            qsm_mya_core.NodeAttribute.create_as_string(
                layer_name, 'qsm_hidden_set', json.dumps(list(set_))
            )
        return set_

    def generate_connect_map(self, disable=False):
        return dict(
            blend=self.generate_blend_map(disable),
            constraint=self.generate_constraint_map(disable),
            hidden=list(self.generate_hidden_set()),
        )

    def generate_mesh_hash_map(self):
        dict_ = {}
        for i_mesh_shape in self._mesh_set:
            i_mesh_opt = qsm_mya_core.MeshShapeOpt(i_mesh_shape)
            i_key = i_mesh_opt.to_hash()
            dict_[i_key] = i_mesh_shape
        return dict_

    def generate_mesh_face_vertices_map(self):
        dict_ = {}
        for i_mesh_shape in self._mesh_set:
            i_mesh_opt = qsm_mya_core.MeshShapeOpt(i_mesh_shape)
            i_key = i_mesh_opt.get_face_vertices_as_uuid()
            dict_[i_key] = i_mesh_shape
        return dict_

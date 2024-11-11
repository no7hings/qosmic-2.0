# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from .... import core as _mya_core

from ....adv import core as _adv_core


# rig
class AssetRigOpt(object):
    NAMESPACE = 'rig'

    @classmethod
    def load_rig(cls, scene_path):
        _mya_core.SceneFile.reference_file(
            scene_path, cls.NAMESPACE
        )

    @classmethod
    def remove_rig(cls):
        _mya_core.Frame.set_current(1)

        opt = _adv_core.AdvOpt(cls.NAMESPACE)
        opt.rest_controls_transformation(translate=True, rotate=True)
        _mya_core.SceneFile.refresh()

        node = _mya_core.ReferenceNamespacesCache().get(cls.NAMESPACE)
        _mya_core.Reference.remove(node)

    def __init__(self, *args, **kwargs):
        if _mya_core.Namespace.is_exists(self.NAMESPACE) is False:
            raise RuntimeError()

        self._adv_rig = _adv_core.AdvOpt(self.NAMESPACE)

        self._mesh_set = set(self._adv_rig.find_all_meshes())
        self._mesh_set.update(set(self._adv_rig.find_all_lower_meshes()))
        self._control_set = set(self._adv_rig.find_all_transform_controls())

    @property
    def mesh_set(self):
        return self._mesh_set

    @property
    def control_set(self):
        return self._control_set

    def generate_blend_map(self, disable=False):
        dict_ = {}
        for i_mesh_shape in self._mesh_set:
            i_mesh_transform = _mya_core.Shape.get_transform(i_mesh_shape)
            i_name = _mya_core.DagNode.to_name_without_namespace(i_mesh_transform)
            i_blend_nodes = _mya_core.MeshBlendSource.get_deform_nodes(
                i_mesh_transform
            )
            if i_blend_nodes:
                i_names = []
                for j_blend_node in i_blend_nodes:
                    # ignore form reference
                    if _mya_core.Reference.is_from_reference(j_blend_node) is True:
                        continue

                    i_names.append(j_blend_node)
                    _mya_core.NodeAttribute.create_as_string(
                        j_blend_node, 'qsm_blend_source', i_name
                    )
                    if disable is True:
                        _mya_core.NodeAttribute.set_value(
                            j_blend_node, 'envelope', 0
                        )

                if i_names:
                    dict_[i_name] = i_names
        return dict_

    def generate_constrain_map(self, disable=False):
        dict_ = {}
        for i_control_transform in self._control_set:
            i_name = _mya_core.DagNode.to_name_without_namespace(i_control_transform)

            i_constrain_nodes = _mya_core.ParentConstraintSource.get_constrain_nodes(i_control_transform)
            if i_constrain_nodes:
                i_names = []
                for j_constrain_path in i_constrain_nodes:
                    # ignore form reference
                    if _mya_core.Reference.is_from_reference(j_constrain_path) is True:
                        continue

                    j_name = _mya_core.DagNode.to_name_without_namespace(j_constrain_path)
                    i_names.append(j_name)

                if i_names:
                    dict_[i_name] = i_names
        return dict_

    def generate_connect_map(self, disable=False):
        return dict(
            blend=self.generate_blend_map(disable),
            constrain=self.generate_constrain_map(disable)
        )

    def generate_mesh_hash_map(self):
        dict_ = {}
        for i_mesh_shape in self._mesh_set:
            i_mesh_opt = _mya_core.MeshShapeOpt(i_mesh_shape)
            i_key = i_mesh_opt.to_hash()
            dict_[i_key] = i_mesh_shape
        return dict_

    def generate_mesh_face_vertices_map(self):
        dict_ = {}
        for i_mesh_shape in self._mesh_set:
            i_mesh_opt = _mya_core.MeshShapeOpt(i_mesh_shape)
            i_key = i_mesh_opt.get_face_vertices_as_uuid()
            dict_[i_key] = i_mesh_shape
        return dict_

# coding:utf-8
import collections

import lxbasic.core as bsc_core

from .... import core as _mya_core

from ... import _abc

from . import cfx_rig_operate as _cfx_operate


class CfxGroup(_abc.AbsGroupOpt):
    LOCATION = '|master|cfx'

    def __init__(self):
        if _mya_core.Node.is_exists(self.LOCATION):
            _mya_core.Group.create_dag(self.LOCATION)

        super(CfxGroup, self).__init__(
            self.LOCATION
        )
    
    def generate_component_data(self):
        dict_ = collections.OrderedDict()

        location_key = '/cfx'
        nucleus_location_key = '{}/nucleus'.format(location_key)
        ncloth_location_key = '{}/ncloth'.format(location_key)
        nrigid_location_key = '{}/nrigid'.format(location_key)
        wrap_location_key = '{}/wrap'.format(location_key)

        meshes = self._group_opt.find_all_shapes_by_type('mesh')
        for i_mesh_shape in meshes:
            i_mesh_transform = _mya_core.Shape.get_transform(i_mesh_shape)
            i_ncloth_args = _mya_core.MeshNCloth.get_args(
                i_mesh_transform
            )
            if i_ncloth_args:
                i_location_key = ncloth_location_key
                i_ntransform, i_nucleus = i_ncloth_args
                # transform
                i_mesh_transform_key = '{}/{}'.format(
                    i_location_key, _mya_core.DagNode.to_name_without_namespace(i_mesh_transform)
                )
                dict_[i_mesh_transform_key] = i_mesh_transform
                # shape
                i_mesh_shap_key = '{}/{}'.format(
                    i_mesh_transform_key, _mya_core.DagNode.to_name_without_namespace(i_mesh_shape)
                )
                dict_[i_mesh_shap_key] = i_mesh_shape

                i_nshape = _mya_core.Transform.get_shape(i_ntransform)
                i_nshape_key = '{}/{}'.format(
                    i_mesh_transform_key, _mya_core.DagNode.to_name_without_namespace(i_nshape)
                )
                dict_[i_nshape_key] = i_nshape
                # nucleus
                if i_nucleus:
                    i_nucleus_key = '{}/{}'.format(
                        nucleus_location_key, _mya_core.DagNode.to_name_without_namespace(i_nucleus)
                    )
                    dict_[i_nucleus_key] = i_nucleus
                continue

            i_nrigid_args = _mya_core.MeshNRigid.get_args(
                i_mesh_transform
            )
            if i_nrigid_args:
                i_location_key = nrigid_location_key
                i_ntransform, i_nucleus = i_nrigid_args
                # transform
                i_mesh_transform_key = '{}/{}'.format(
                    i_location_key, _mya_core.DagNode.to_name_without_namespace(i_mesh_transform)
                )
                dict_[i_mesh_transform_key] = i_mesh_transform
                # shape
                i_mesh_shap_key = '{}/{}'.format(
                    i_mesh_transform_key, _mya_core.DagNode.to_name_without_namespace(i_mesh_shape)
                )
                dict_[i_mesh_shap_key] = i_mesh_shape

                i_nshape = _mya_core.Transform.get_shape(i_ntransform)
                i_nshape_key = '{}/{}'.format(
                    i_mesh_transform_key, _mya_core.DagNode.to_name_without_namespace(i_nshape)
                )
                dict_[i_nshape_key] = i_nshape
                # nucleus
                if i_nucleus:
                    i_nucleus_key = '{}/{}'.format(
                        nucleus_location_key, _mya_core.DagNode.to_name_without_namespace(i_nucleus)
                    )
                    dict_[i_nucleus_key] = i_nucleus
                continue

            i_wrap_args = _mya_core.MeshWrapTarget.get_args(
                i_mesh_transform
            )
            if i_wrap_args:
                i_location_key = wrap_location_key
                i_deform_node, i_wrap_transforms, i_wrap_base_transforms = i_wrap_args
                # transform
                i_mesh_transform_key = '{}/{}'.format(
                    i_location_key, _mya_core.DagNode.to_name_without_namespace(i_mesh_transform)
                )
                dict_[i_mesh_transform_key] = i_mesh_transform
                # shape
                i_mesh_shap_key = '{}/{}'.format(
                    i_mesh_transform_key, _mya_core.DagNode.to_name_without_namespace(i_mesh_shape)
                )
                dict_[i_mesh_shap_key] = i_mesh_shape

                i_deform_node_key = '{}/{}'.format(
                    i_mesh_transform_key, _mya_core.DagNode.to_name_without_namespace(i_deform_node)
                )
                dict_[i_deform_node_key] = i_deform_node

                for j_wrap_transform in i_wrap_transforms:
                    j_driver_transform_key = '{}/{}'.format(
                        i_deform_node_key, _mya_core.DagNode.to_name_without_namespace(j_wrap_transform)
                    )
                    dict_[j_driver_transform_key] = j_wrap_transform

                for j_base_transform in i_wrap_base_transforms:
                    j_base_transform_key = '{}/{}'.format(
                        i_deform_node_key, _mya_core.DagNode.to_name_without_namespace(j_base_transform)
                    )
                    dict_[j_base_transform_key] = j_base_transform
                continue
        return dict_

    @_mya_core.Undo.execute
    def auto_collection(self):
        def valid_fnc(path_):
            # check exists first, maybe node is already collected
            if _mya_core.Node.is_exists(path_) is False:
                return False
            
            # ignore is in group
            if path_.startswith(self._location):
                return False

            # todo: ignore from adv rig but not reference
            if '|Geometry|' in path_:
                return False

            return True

        meshes = self._group_opt.find_all_shapes_by_type('mesh')
        for i_mesh_shape in meshes:
            if _mya_core.Node.is_exists(i_mesh_shape) is False:
                continue

            i_mesh_transform = _mya_core.Shape.get_transform(i_mesh_shape)

            # input cloth
            i_ncloth_args = _mya_core.MeshNCloth.get_args(
                i_mesh_transform
            )
            if i_ncloth_args:
                i_ntransform, i_nucleus = i_ncloth_args
                if valid_fnc(i_ntransform) is True:
                    _cfx_operate.CfxNClothGrpOpt().add_one(i_ntransform)

                if valid_fnc(i_nucleus) is True:
                    _cfx_operate.CfxNucleusGrpOpt().add_one(i_nucleus)

            # input rigid
            i_nrigid_args = _mya_core.MeshNRigid.get_args(
                i_mesh_transform
            )
            if i_nrigid_args:
                i_ntransform, i_nucleus = i_nrigid_args
                if valid_fnc(i_ntransform) is True:
                    _cfx_operate.CfxNRigidGrpOpt().add_one(i_ntransform)

                if valid_fnc(i_nucleus) is True:
                    _cfx_operate.CfxNucleusGrpOpt().add_one(i_nucleus)
            
            # input wrap
            i_input_wrap_args = _mya_core.MeshWrapTarget.get_args(
                i_mesh_transform
            )
            if i_input_wrap_args:
                i_deform_node, i_wrap_transforms, i_wrap_base_transforms = i_input_wrap_args
                for j_wrap_transform in i_wrap_transforms:
                    if valid_fnc(j_wrap_transform) is True:
                        j_wrap_transform_new = _cfx_operate.CfxWrapGrpOpt().add_one(j_wrap_transform)

                        _mya_core.MeshWrapSource.auto_collect_base_transforms(j_wrap_transform_new)

            # output wrap
            _mya_core.MeshWrapSource.auto_collect_base_transforms(i_mesh_transform)

    @_mya_core.Undo.execute
    def auto_name(self):
        rig_opt = _cfx_operate.RigOpt()
        mesh_hash_dict = rig_opt.generate_mesh_hash_map()
        mesh_face_vertices_dict = rig_opt.generate_mesh_face_vertices_map()

        meshes = self._group_opt.find_all_shapes_by_type('mesh')
        for i_mesh_shape in meshes:
            if _mya_core.Node.is_exists(i_mesh_shape) is False:
                continue

            i_mesh_transform = _mya_core.Shape.get_transform(i_mesh_shape)

            # check is visible
            if _mya_core.NodeDisplay.is_visible(i_mesh_transform) is False:
                continue

            i_mesh_opt = _mya_core.MeshShapeOpt(i_mesh_shape)

            i_key = i_mesh_opt.to_hash()

            if i_key in mesh_hash_dict:
                i_mesh_shape_src = mesh_hash_dict[i_key]

                i_mesh_transform_src = _mya_core.MeshShape.get_transform(i_mesh_shape_src)
                self.rename_fnc(i_mesh_transform, i_mesh_transform_src)
            else:
                if i_key in mesh_face_vertices_dict:
                    i_mesh_shape_src = mesh_face_vertices_dict[i_key]
                    i_mesh_transform_src = _mya_core.MeshShape.get_transform(i_mesh_shape_src)
                    self.rename_fnc(i_mesh_transform, i_mesh_transform_src)

    @staticmethod
    def rename_fnc(i_mesh_transform, i_mesh_transform_src):
        i_name = _mya_core.DagNode.to_name_without_namespace(i_mesh_transform_src)

        i_name_old = _mya_core.DagNode.to_name_without_namespace(i_mesh_transform)
        i_name_new = '{}__copy'.format(i_name)

        if bsc_core.BscNodeName.is_name_match(i_name_old, '{}__copy*'.format(i_name)) is False:
            _mya_core.Node.rename(
                i_mesh_transform, i_name_new
            )

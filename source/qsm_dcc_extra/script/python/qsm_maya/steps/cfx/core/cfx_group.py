# coding:utf-8
import collections

from .... import core as _mya_core

from ... import _abc

from . import cfx_operate as _cfx_operate


class CfxGroup(_abc.AbsGroupOpt):
    LOCATION = '|master|cfx'

    def __init__(self):
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

            i_wrap_args = _mya_core.MeshWrap.get_args(
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
            if _mya_core.Node.is_exists(path_) is False:
                return False

            if path_.startswith(self._path):
                return False

            # ignore from adv rig and not reference
            if '|Geometry|' in path_:
                return False

            return True

        meshes = self._group_opt.find_all_shapes_by_type('mesh')
        for i_mesh_shape in meshes:
            i_mesh_transform = _mya_core.Shape.get_transform(i_mesh_shape)
            i_ncloth_args = _mya_core.MeshNCloth.get_args(
                i_mesh_transform
            )
            if i_ncloth_args:
                i_ntransform, i_nucleus = i_ncloth_args
                if valid_fnc(i_ntransform) is True:
                    _cfx_operate.CfxNClothGrpOpt().add_one(i_ntransform)

                if valid_fnc(i_nucleus) is True:
                    _cfx_operate.CfxNucleusGrpOpt().add_one(i_nucleus)

            i_nrigid_args = _mya_core.MeshNRigid.get_args(
                i_mesh_transform
            )
            if i_nrigid_args:
                i_ntransform, i_nucleus = i_nrigid_args
                if valid_fnc(i_ntransform) is True:
                    _cfx_operate.CfxNRigidGrpOpt().add_one(i_ntransform)

                if valid_fnc(i_nucleus) is True:
                    _cfx_operate.CfxNucleusGrpOpt().add_one(i_nucleus)

            i_wrap_args = _mya_core.MeshWrap.get_args(
                i_mesh_transform
            )
            if i_wrap_args:
                i_deform_node, i_wrap_transforms, i_wrap_base_transforms = i_wrap_args
                for j_wrap_transform in i_wrap_transforms:
                    if valid_fnc(j_wrap_transform) is True:
                        _cfx_operate.CfxWrapGeoGrpOpt().add_one(j_wrap_transform)

                for j_wrap_base_transform in i_wrap_base_transforms:
                    if valid_fnc(j_wrap_base_transform) is True:
                        _cfx_operate.CfxWrapBaseGeoGrpOpt().add_one(j_wrap_base_transform)

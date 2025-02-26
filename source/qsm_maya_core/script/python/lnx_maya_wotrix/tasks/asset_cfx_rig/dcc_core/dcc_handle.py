# coding:utf-8
import collections

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

import qsm_maya.core as qsm_mya_core

from qsm_maya.handles import abc_

from . import dcc_organize as _cfx_rig_operate

from . import dcc_asset as _rig_operate


class AssetCfxRigHandle(abc_.AbsGroupOpt):
    LOCATION = '|master|cfx_rig'
    LOCATION_NAME = 'cfx_rig'

    def __init__(self, *args, **kwargs):
        # create force
        if qsm_mya_core.Node.is_exists(self.LOCATION) is False:
            qsm_mya_core.Group.create_dag(self.LOCATION)

        super(AssetCfxRigHandle, self).__init__(
            self.LOCATION, *args, **kwargs
        )

    @classmethod
    def get_rig_variant_name(cls):
        location = cls.LOCATION
        if qsm_mya_core.NodeAttribute.is_exists(location, 'qsm_variant'):
            return qsm_mya_core.NodeAttribute.get_as_string(location, 'qsm_variant')
        return 'default'

    @classmethod
    def get_rig_variant_names(cls):
        current = cls.get_rig_variant_name()
        if current:
            if current != 'default':
                return [current, 'default']
        return ['default']
    
    @classmethod
    def mark_rig_variant(cls, name):
        qsm_mya_core.NodeAttribute.create_as_string(
            cls.LOCATION, 'qsm_variant', name
        )

    # rig preset
    @classmethod
    def get_rig_preset_name(cls, namespace=None):
        if namespace is not None:
            location = '{}:{}'.format(namespace, cls.LOCATION_NAME)
        else:
            location = cls.LOCATION

        if qsm_mya_core.NodeAttribute.is_exists(location, 'qsm_preset'):
            return qsm_mya_core.NodeAttribute.get_as_string(location, 'qsm_preset')
        return 'default'

    @classmethod
    def create_or_update_rig_preset(cls, name, namespace=None):
        if namespace is not None:
            location = '{}:{}'.format(namespace, cls.LOCATION_NAME)
        else:
            location = cls.LOCATION

        qsm_mya_core.NodeAttribute.create_as_string(
            location, 'qsm_preset', name
        )

        group_opt = qsm_mya_core.GroupOpt(location)
        n_clothes = group_opt.find_all_shapes_by_type('nCloth')
        for i_n_cloth in n_clothes:
            i_n_cloth_opt = qsm_mya_core.EtrNodeOpt(i_n_cloth)
            i_dict = i_n_cloth_opt.get_dict(key_includes=qsm_mya_core.NCloth.PRESET_KEY_INCLUDES)
            i_atr_name = 'qsm_preset_{}'.format(name)
            qsm_mya_core.NodeAttribute.create_as_dict(i_n_cloth, i_atr_name, i_dict)

            qsm_mya_core.NodeAttribute.create_as_string(i_n_cloth, 'qsm_preset', name)

    @classmethod
    def load_rig_preset(cls, name, namespace=None):
        if namespace is not None:
            location = '{}:{}'.format(namespace, cls.LOCATION_NAME)
        else:
            location = cls.LOCATION

        qsm_mya_core.NodeAttribute.create_as_string(
            location, 'qsm_preset', name
        )
        group_opt = qsm_mya_core.GroupOpt(location)
        n_clothes = group_opt.find_all_shapes_by_type('nCloth')
        for i_n_cloth in n_clothes:
            i_atr_name = 'qsm_preset_{}'.format(name)
            if qsm_mya_core.NodeAttribute.is_exists(i_n_cloth, i_atr_name):
                i_n_cloth_opt = qsm_mya_core.EtrNodeOpt(i_n_cloth)
                i_dict = qsm_mya_core.NodeAttribute.get_as_dict(i_n_cloth, i_atr_name)
                i_n_cloth_opt.set_dict(i_dict)

                qsm_mya_core.NodeAttribute.create_as_string(i_n_cloth, 'qsm_preset', name)

    @classmethod
    def get_rig_preset_names(cls, namespace=None):
        if namespace is not None:
            location = '{}:{}'.format(namespace, cls.LOCATION_NAME)
        else:
            location = cls.LOCATION

        list_ = []
        group_opt = qsm_mya_core.GroupOpt(location)
        n_clothes = group_opt.find_all_shapes_by_type('nCloth')
        for i_n_cloth in n_clothes:
            i_n_cloth_opt = qsm_mya_core.EtrNodeOpt(i_n_cloth)
            i_names = i_n_cloth_opt.get_all_customize_port_paths()
            i_matches = bsc_core.BscFnmatch.filter(i_names, 'qsm_preset_*')
            for j in i_matches:
                j_name = j[len('qsm_preset_'):]
                if j_name not in list_:
                    list_.append(j_name)
        return list_ or ['default']

    # component data
    def generate_component_data(self):
        return self.generate_component_data_for(
            '/cfx_rig', self.LOCATION
        )

    @classmethod
    def generate_component_data_for(cls, gui_location, dcc_location):
        dict_ = collections.OrderedDict()

        dict_[gui_location] = dcc_location

        group_opt = qsm_mya_core.GroupOpt(dcc_location)

        nucleus_location_key = '{}/nucleus'.format(gui_location)
        ncloth_location_key = '{}/ncloth'.format(gui_location)
        nrigid_location_key = '{}/nrigid'.format(gui_location)
        wrap_location_key = '{}/wrap'.format(gui_location)

        meshes = group_opt.find_all_shapes_by_type('mesh')
        for i_mesh_shape in meshes:
            i_mesh_transform = qsm_mya_core.Shape.get_transform(i_mesh_shape)
            i_ncloth_args = qsm_mya_core.MeshNCloth.get_args(
                i_mesh_transform
            )
            if i_ncloth_args:
                i_location_key = ncloth_location_key
                i_ntransform, i_nucleus = i_ncloth_args
                # transform
                i_mesh_transform_key = '{}/{}'.format(
                    i_location_key, qsm_mya_core.DagNode.to_name_without_namespace(i_mesh_transform)
                )
                dict_[i_mesh_transform_key] = i_mesh_transform
                # shape
                i_mesh_shap_key = '{}/{}'.format(
                    i_mesh_transform_key, qsm_mya_core.DagNode.to_name_without_namespace(i_mesh_shape)
                )
                dict_[i_mesh_shap_key] = i_mesh_shape

                i_nshape = qsm_mya_core.Transform.get_shape(i_ntransform)
                i_nshape_key = '{}/{}'.format(
                    i_mesh_transform_key, qsm_mya_core.DagNode.to_name_without_namespace(i_nshape)
                )
                dict_[i_nshape_key] = i_nshape
                # nucleus
                if i_nucleus:
                    i_nucleus_key = '{}/{}'.format(
                        nucleus_location_key, qsm_mya_core.DagNode.to_name_without_namespace(i_nucleus)
                    )
                    dict_[i_nucleus_key] = i_nucleus
                continue

            i_nrigid_args = qsm_mya_core.MeshNRigid.get_args(
                i_mesh_transform
            )
            if i_nrigid_args:
                i_location_key = nrigid_location_key
                i_ntransform, i_nucleus = i_nrigid_args
                # transform
                i_mesh_transform_key = '{}/{}'.format(
                    i_location_key, qsm_mya_core.DagNode.to_name_without_namespace(i_mesh_transform)
                )
                dict_[i_mesh_transform_key] = i_mesh_transform
                # shape
                i_mesh_shap_key = '{}/{}'.format(
                    i_mesh_transform_key, qsm_mya_core.DagNode.to_name_without_namespace(i_mesh_shape)
                )
                dict_[i_mesh_shap_key] = i_mesh_shape

                i_nshape = qsm_mya_core.Transform.get_shape(i_ntransform)
                i_nshape_key = '{}/{}'.format(
                    i_mesh_transform_key, qsm_mya_core.DagNode.to_name_without_namespace(i_nshape)
                )
                dict_[i_nshape_key] = i_nshape
                # nucleus
                if i_nucleus:
                    i_nucleus_key = '{}/{}'.format(
                        nucleus_location_key, qsm_mya_core.DagNode.to_name_without_namespace(i_nucleus)
                    )
                    dict_[i_nucleus_key] = i_nucleus
                continue

            i_wrap_args = qsm_mya_core.MeshWrapTarget.get_args(
                i_mesh_transform
            )
            if i_wrap_args:
                i_location_key = wrap_location_key
                i_deform_node, i_wrap_transforms, i_wrap_base_transforms = i_wrap_args
                # transform
                i_mesh_transform_key = '{}/{}'.format(
                    i_location_key, qsm_mya_core.DagNode.to_name_without_namespace(i_mesh_transform)
                )
                dict_[i_mesh_transform_key] = i_mesh_transform
                # shape
                i_mesh_shap_key = '{}/{}'.format(
                    i_mesh_transform_key, qsm_mya_core.DagNode.to_name_without_namespace(i_mesh_shape)
                )
                dict_[i_mesh_shap_key] = i_mesh_shape

                i_deform_node_key = '{}/{}'.format(
                    i_mesh_transform_key, qsm_mya_core.DagNode.to_name_without_namespace(i_deform_node)
                )
                dict_[i_deform_node_key] = i_deform_node

                for j_wrap_transform in i_wrap_transforms:
                    j_driver_transform_key = '{}/{}'.format(
                        i_deform_node_key, qsm_mya_core.DagNode.to_name_without_namespace(j_wrap_transform)
                    )
                    dict_[j_driver_transform_key] = j_wrap_transform

                for j_base_transform in i_wrap_base_transforms:
                    j_base_transform_key = '{}/{}'.format(
                        i_deform_node_key, qsm_mya_core.DagNode.to_name_without_namespace(j_base_transform)
                    )
                    dict_[j_base_transform_key] = j_base_transform
                continue
        return dict_

    @qsm_mya_core.Undo.execute
    def auto_collection(self):
        def valid_fnc(path_):
            # check exists first, maybe node is already collected
            if qsm_mya_core.Node.is_exists(path_) is False:
                return False
            
            # ignore is in group
            if path_.startswith(self._location):
                return False

            # todo: ignore from adv rig but not reference
            if '|Geometry|' in path_:
                return False

            if '|Low_Grp|' in path_:
                return False

            if '|Low|' in path_:
                return False

            return True

        meshes = self._group_opt.find_all_shapes_by_type('mesh')
        with bsc_log.LogProcessContext.create(maximum=len(meshes), label='auto collection') as l_p:
            for i_mesh_shape in meshes:
                if qsm_mya_core.Node.is_exists(i_mesh_shape) is False:
                    continue
    
                i_mesh_transform = qsm_mya_core.Shape.get_transform(i_mesh_shape)
    
                # input cloth
                i_ncloth_args = qsm_mya_core.MeshNCloth.get_args(
                    i_mesh_transform
                )
                if i_ncloth_args:
                    i_ntransform, i_nucleus = i_ncloth_args
                    if valid_fnc(i_ntransform) is True:
                        _cfx_rig_operate.CfxNClothGrpOrg().add_one(i_ntransform)
    
                    if valid_fnc(i_nucleus) is True:
                        _cfx_rig_operate.CfxNucleusGrpOrg().add_one(i_nucleus)
    
                # input rigid
                i_nrigid_args = qsm_mya_core.MeshNRigid.get_args(
                    i_mesh_transform
                )
                if i_nrigid_args:
                    i_ntransform, i_nucleus = i_nrigid_args
                    if valid_fnc(i_ntransform) is True:
                        _cfx_rig_operate.CfxNRigidGrpOrg().add_one(i_ntransform)
    
                    if valid_fnc(i_nucleus) is True:
                        _cfx_rig_operate.CfxNucleusGrpOrg().add_one(i_nucleus)
                
                # input wrap
                i_input_wrap_args = qsm_mya_core.MeshWrapTarget.get_args(
                    i_mesh_transform
                )
                if i_input_wrap_args:
                    i_deform_node, i_wrap_transforms, i_wrap_base_transforms = i_input_wrap_args
                    for j_wrap_transform in i_wrap_transforms:
                        if valid_fnc(j_wrap_transform) is True:
                            j_wrap_transform_new = _cfx_rig_operate.CfxWrapGrpOrg().add_one(j_wrap_transform)
    
                            qsm_mya_core.MeshWrapSource.auto_collect_base_transforms(j_wrap_transform_new)
    
                # output wrap
                qsm_mya_core.MeshWrapSource.auto_collect_base_transforms(i_mesh_transform)

            l_p.do_update()
            
    @qsm_mya_core.Undo.execute
    def auto_name(self):
        rig_opt = _rig_operate.AssetCfxRigSceneOpt()
        mesh_hash_dict = rig_opt.generate_mesh_hash_map()
        mesh_face_vertices_dict = rig_opt.generate_mesh_face_vertices_map()

        meshes = self._group_opt.find_all_shapes_by_type('mesh')
        with bsc_log.LogProcessContext.create(maximum=len(meshes), label='auto name') as l_p:
            for i_mesh_shape in meshes:
                if qsm_mya_core.Node.is_exists(i_mesh_shape) is False:
                    continue
    
                i_mesh_transform = qsm_mya_core.Shape.get_transform(i_mesh_shape)
    
                # check is visible
                if qsm_mya_core.NodeDisplay.is_visible(i_mesh_transform) is False:
                    continue
    
                i_mesh_opt = qsm_mya_core.MeshShapeOpt(i_mesh_shape)
    
                i_key = i_mesh_opt.to_hash()
    
                if i_key in mesh_hash_dict:
                    i_mesh_shape_src = mesh_hash_dict[i_key]
    
                    i_mesh_transform_src = qsm_mya_core.MeshShape.get_transform(i_mesh_shape_src)
                    self.rename_fnc(i_mesh_transform, i_mesh_transform_src)
                    # add source to layer
                    _cfx_rig_operate.CfxSourceGeoLyrOrg().add_one(i_mesh_transform_src)
                else:
                    i_key = i_mesh_opt.get_face_vertices_as_uuid()
                    if i_key in mesh_face_vertices_dict:
                        i_mesh_shape_src = mesh_face_vertices_dict[i_key]
                        i_mesh_transform_src = qsm_mya_core.MeshShape.get_transform(i_mesh_shape_src)
                        self.rename_fnc(i_mesh_transform, i_mesh_transform_src)
                        # add source to layer
                        _cfx_rig_operate.CfxSourceGeoLyrOrg().add_one(i_mesh_transform_src)
                    else:
                        bsc_log.Log.trace_warning(
                            'no match found for: "{}"'.format(i_mesh_shape)
                        )

                l_p.do_update()

    @staticmethod
    def rename_fnc(mesh_transform, mesh_transform_src):
        name = qsm_mya_core.DagNode.to_name_without_namespace(mesh_transform_src)

        name_old = qsm_mya_core.DagNode.to_name_without_namespace(mesh_transform)
        name_new = '{}__copy'.format(name)

        if bsc_core.BscNodeName.is_name_match(name_old, '{}__copy*'.format(name)) is False:
            qsm_mya_core.Node.rename(
                mesh_transform, name_new
            )

    @qsm_mya_core.Undo.execute
    def auto_connection(self):
        """
        temporary function
        """
        errors = []
        rig_opt = _rig_operate.AssetCfxRigSceneOpt()
        mesh_set = rig_opt.mesh_set
        with bsc_log.LogProcessContext.create(maximum=len(mesh_set), label='auto connection') as l_p:
            for i_mesh_shape_src in mesh_set:
                i_mesh_transform_src = qsm_mya_core.Shape.get_transform(i_mesh_shape_src)
                i_mesh_shape_tgt = qsm_mya_core.DagNode.to_path_without_namespace(i_mesh_shape_src)
                if qsm_mya_core.Node.is_exists(i_mesh_shape_tgt) is True:
                    i_uuid_src = qsm_mya_core.MeshShapeOpt(i_mesh_shape_src).get_face_vertices_as_uuid()
                    i_uuid_tgt = qsm_mya_core.MeshShapeOpt(i_mesh_shape_tgt).get_face_vertices_as_uuid()

                    if i_uuid_src != i_uuid_tgt:
                        bsc_log.Log.trace_warning(
                            'topology is changed for: "{}"'.format(i_mesh_shape_tgt)
                        )
                        continue

                    i_mesh_transform_tgt = qsm_mya_core.Shape.get_transform(i_mesh_shape_tgt)
                    i_blend_nodes = qsm_mya_core.MeshBlendSource.get_deform_nodes(
                        i_mesh_transform_tgt
                    )
                    # has blend
                    if i_blend_nodes:
                        self.add_to_bridge_and_auto_blend(
                            i_mesh_transform_src, i_mesh_transform_tgt
                        )
                    else:
                        i_wrap_nodes = qsm_mya_core.MeshWrapSource.get_deform_nodes(
                            i_mesh_transform_tgt
                        )
                        # has wrap
                        if i_wrap_nodes:
                            self.add_to_bridge_and_auto_blend(
                                i_mesh_transform_src, i_mesh_transform_tgt
                            )

                l_p.do_update()

    @classmethod
    def add_to_bridge_and_auto_blend(cls, mesh_transform_src, mesh_transform_tgt):
        # break deform
        qsm_mya_core.MeshDeform.break_deform(mesh_transform_tgt)
        # rename
        name = qsm_mya_core.DagNode.to_name_without_namespace(mesh_transform_src)
        new_name = '{}__copy'.format(name)
        result = qsm_mya_core.DagNode.rename(mesh_transform_tgt, new_name)
        # collection
        mesh_transform_tgt_new = _cfx_rig_operate.CfxBridgeGeoGrpOrg().add_one(result)
        _cfx_rig_operate.CfxBridgeGeoLyrOrg().add_one(mesh_transform_tgt_new)
        _cfx_rig_operate.CfxBridgeGeoMtlOrg().assign_to(mesh_transform_tgt_new)
        # blend
        qsm_mya_core.BlendShape.create(mesh_transform_src, mesh_transform_tgt_new)
        # auto collection wrap base
        qsm_mya_core.MeshWrapSource.auto_collect_base_transforms(
            mesh_transform_tgt_new
        )

    @classmethod
    def save_properties_template(cls, name):
        pass
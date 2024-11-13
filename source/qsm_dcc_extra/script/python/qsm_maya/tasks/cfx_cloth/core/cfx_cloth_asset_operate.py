# coding:utf-8
import json
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from .... import core as _mya_core

from ...cfx_rig import core as _cfx_rig_core


class CfxClothAssetOpt(object):
    def __init__(self, rig_namespace):
        self._rig_namespace = rig_namespace

        self._cfx_rig_namespace = self.to_cfx_rig_namespace(self._rig_namespace)

        self._cfx_rig_group_opt = ShotCfxRigGroupOpt(self._cfx_rig_namespace)

    @property
    def rig_namespace(self):
        return self._rig_namespace

    @property
    def cfx_rig_namespace(self):
        return self._cfx_rig_namespace
    
    @property
    def cfx_rig_group_opt(self):
        return self._cfx_rig_group_opt

    def find_cfx_rig_location(self):
        _ = cmds.ls('{}:cfx_rig'.format(self._cfx_rig_namespace), long=1)
        if _:
            return _[0]

    def find_cfx_rig_nuclei(self):
        return _mya_core.Namespace.find_match_nodes(self._cfx_rig_namespace, node_type='nucleus')

    @staticmethod
    def to_cfx_rig_namespace(rig_namespace):
        return '{}:cfx_rig'.format(rig_namespace)

    def load_cfx_rig_from(self, scene_path):
        _mya_core.SceneFile.reference_file(
            scene_path, self._cfx_rig_namespace
        )

    def update_cfx_rig_scene(self, scene_path):
        reference_node = _mya_core.ReferencesCache().get(self._cfx_rig_namespace)
        if reference_node:
            _mya_core.Reference.replace(reference_node, scene_path)

    def get_cfx_rig_is_loaded(self):
        return bool(_mya_core.ReferencesCache().get(self._cfx_rig_namespace))

    def get_cfx_rig_scene_path(self):
        return _mya_core.ReferencesCache().get_file(self._cfx_rig_namespace)

    def get_cfx_rig_is_enable(self):
        reference_node = _mya_core.ReferencesCache().get(self._cfx_rig_namespace)
        if reference_node:
            return _mya_core.Reference.is_loaded(reference_node)
        return None

    def set_cfx_rig_enable(self, boolean):
        reference_node = _mya_core.ReferencesCache().get(self._cfx_rig_namespace)
        if reference_node is not None:
            if boolean is True:
                _mya_core.Reference.reload(reference_node)
                layer = self.cfx_rig_group_opt.find_source_geo_layer()
                # turn off the layer visibility later
                if layer:
                    _mya_core.DisplayLayer.set_visible(layer, False)
            else:
                # turn on the layer visibility first
                layer = self.cfx_rig_group_opt.find_source_geo_layer()
                if layer:
                    _mya_core.DisplayLayer.set_visible(layer, True)
                _mya_core.Reference.unload(reference_node)

    def set_cfx_rig_solver_enable(self, boolean):
        nuclei = self.find_cfx_rig_nuclei()
        for i_nucleus in nuclei:
            _mya_core.NodeAttribute.set_value(i_nucleus, 'enable', boolean)

    def check_cfx_rig_is_referenced(self):
        return

    def connect_blends(self):
        blend_shape_nodes = _mya_core.Namespace.find_match_nodes(
            self._cfx_rig_namespace, 'blendShape'
        )
        for i_blend_node in blend_shape_nodes:
            if _mya_core.NodeAttribute.is_exists(
                i_blend_node, 'qsm_blend_source'
            ):
                i_source_transform_name = _mya_core.NodeAttribute.get_as_string(
                    i_blend_node, 'qsm_blend_source'
                )
                i_source_transform_path = _mya_core.Namespace.find_one(
                    self._rig_namespace, node_name=i_source_transform_name
                )
                if i_source_transform_path:
                    _mya_core.MeshBlend.set_source_transform(i_blend_node, i_source_transform_path)

    def connect_constraints(self):
        constraint_nodes = _mya_core.Namespace.find_match_nodes(
            self._cfx_rig_namespace, 'parentConstraint'
        )
        for i_constraint_node in constraint_nodes:
            if _mya_core.NodeAttribute.is_exists(
                i_constraint_node, 'qsm_constraint_source'
            ):
                i_source_transform_name = _mya_core.NodeAttribute.get_as_string(
                    i_constraint_node, 'qsm_constraint_source'
                )
                i_source_transform_path = _mya_core.Namespace.find_one(
                    self._rig_namespace, node_name=i_source_transform_name
                )
                if i_source_transform_path:
                    _mya_core.ParentConstraint.set_source(i_constraint_node, i_source_transform_path)

    def connect_hidden(self):
        layer_name = _cfx_rig_core.CfxSourceGeoLyrOpt.NAME
        layer = '{}:{}'.format(self._cfx_rig_namespace, layer_name)
        if _mya_core.NodeAttribute.is_exists(layer, 'qsm_hidden_set'):
            value = _mya_core.NodeAttribute.get_value(layer, 'qsm_hidden_set')
            if value:
                data = json.loads(value)
                for i in data:
                    i_transform_path = _mya_core.Namespace.find_one(
                        self._rig_namespace, node_name=i
                    )
                    if i_transform_path:
                        _mya_core.DisplayLayer.add_one(layer, i_transform_path)
    
    def connect_to_rig(self):
        self.connect_blends()
        self.connect_constraints()
        self.connect_hidden()


class ShotCfxRigGroupOpt(object):
    def __init__(self, namespace):
        self._namespace = namespace
        self._rig_namespace = ':'.join(self._namespace.split(':')[:-1])
    
    def find_location(self):
        _ = cmds.ls('{}:cfx_rig'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_output_geo_location(self):
        _ = cmds.ls('{}:cfx_output_geo_grp'.format(self._namespace), long=1)
        if _:
            return _[0]

    def find_source_geo_layer(self):
        return _mya_core.Namespace.find_one(
            self._namespace, node_name=_cfx_rig_core.CfxSourceGeoLyrOpt.NAME
        )
    
    def generate_component_data(self):
        dcc_location = self.find_location()
        if dcc_location:
            gui_location = '/{}/cfx_rig'.format(self._rig_namespace)
            return _cfx_rig_core.AssetCfxRigGroupOpt.generate_component_data_for(dcc_location, gui_location)
        return {}
    
    def generate_export_args(self):
        location = self.find_output_geo_location()
        meshes = _mya_core.Group.find_siblings(
            location, 'mesh'
        )
        for i_shape in meshes:
            i_transform = _mya_core.Shape.get_transform(i_shape)
            if _mya_core.Transform.is_visible(i_transform):
                print i_transform

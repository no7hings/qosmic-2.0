# coding:utf-8
import os

import json
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

import qsm_general.core as qsm_gnl_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.adv as qsm_mya_adv

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core

from ...asset_cfx_rig import dcc_core as _asset_cfx_rig_core

from ...shot_animation import dcc_core as _shot_animation_core

from . import dcc_organize as _cfx_group


class ShotCfxClothAssetHandle:

    @staticmethod
    def to_cfx_rig_namespace(rig_namespace):
        return '{}:cfx_rig'.format(rig_namespace)

    @staticmethod
    def to_ani_geo_cache_namespace(rig_namespace):
        return '{}:ani_geo_cache'.format(rig_namespace)

    @staticmethod
    def to_ani_ctl_cache_namespace(rig_namespace):
        return '{}:ani_ctl_cache'.format(rig_namespace)

    def __init__(self, rig_namespace):
        self._rig_namespace = rig_namespace
        self._rig_opt = qsm_mya_hdl_anm_core.AdvRigAsset(rig_namespace)

        self._cfx_rig_namespace = self.to_cfx_rig_namespace(self._rig_namespace)
        self._cfx_rig_handle = ShotCfxRigHandle(self._cfx_rig_namespace)

        self._ani_geo_cache_namespace = self.to_ani_geo_cache_namespace(self._rig_namespace)
        self._ani_geo_cache_handle = ShotAniGeoCacheHandle(self._ani_geo_cache_namespace)

        self._ani_ctl_cache_namespace = self.to_ani_ctl_cache_namespace(self._rig_namespace)
        self._ani_ctl_cache_handle = ShotAniCtlCacheHandle(self._ani_ctl_cache_namespace)

    @property
    def rig_namespace(self):
        return self._rig_namespace

    @property
    def cfx_rig_namespace(self):
        return self._cfx_rig_namespace

    @property
    def rig_opt(self):
        return self._rig_opt
    
    @property
    def cfx_rig_handle(self):
        return self._cfx_rig_handle

    @property
    def ani_geo_cache_handle(self):
        return self._ani_geo_cache_handle

    @property
    def ani_ctl_cache_handle(self):
        return self._ani_ctl_cache_handle

    def unload_rig(self):
        path = qsm_mya_core.ReferencesCache().get(self._rig_namespace)
        if path:
            qsm_mya_core.Reference.unload(path)

    def sync_ani_cache_auto(self, directory_path):
        # create namespace auto
        if qsm_mya_core.Namespace.is_exists(self._rig_namespace) is False:
            qsm_mya_core.Namespace.create(self._rig_namespace)

        name = self._rig_namespace
        # fix mult layer namespace
        name = name.replace(':', '__')
        options = dict(
            directory=directory_path,
            namespace=name
        )

        geometry_abc_path = qsm_gnl_core.DccFilePatterns.AniGeoCacheAbcFile.format(**options)
        if os.path.isfile(geometry_abc_path):
            self._ani_geo_cache_handle.load_cache_auto(geometry_abc_path)

        control_abc_path = qsm_gnl_core.DccFilePatterns.AniCtlCacheAbcFile.format(**options)
        if os.path.isfile(control_abc_path):
            self._ani_ctl_cache_handle.load_cache_auto(control_abc_path)

        self.unload_rig()


class ShotCfxRigHandle:
    LOG_KEY = 'cfx rig handle'

    def __init__(self, namespace):
        self._cfx_rig_namespace = namespace

        self._rig_namespace = ':'.join(self._cfx_rig_namespace.split(':')[:-1])
        self._ani_geo_cache_namespace = ShotCfxClothAssetHandle.to_ani_geo_cache_namespace(self._rig_namespace)
        self._ani_ctl_cache_namespace = ShotCfxClothAssetHandle.to_ani_ctl_cache_namespace(self._rig_namespace)
    
    def find_location(self):
        _ = cmds.ls('{}:cfx_rig'.format(self._cfx_rig_namespace), long=1)
        if _:
            return _[0]

    def get_scene_path(self):
        return qsm_mya_core.ReferencesCache().get_file(self._cfx_rig_namespace)

    def get_is_enable(self):
        reference_node = qsm_mya_core.ReferencesCache().get(self._cfx_rig_namespace)
        if reference_node:
            return qsm_mya_core.Reference.is_loaded(reference_node)
        return None
    
    def set_enable(self, boolean):
        reference_node = qsm_mya_core.ReferencesCache().get(self._cfx_rig_namespace)
        if reference_node is not None:
            if boolean is True:
                qsm_mya_core.Reference.reload(reference_node)
                layer = self.find_source_geo_layer()
                # turn off the layer visibility later
                if layer:
                    qsm_mya_core.DisplayLayer.set_visible(layer, False)
            else:
                # turn on the layer visibility first
                layer = self.find_source_geo_layer()
                if layer:
                    qsm_mya_core.DisplayLayer.set_visible(layer, True)
                qsm_mya_core.Reference.unload(reference_node)

    def get_is_loaded(self):
        return bool(qsm_mya_core.ReferencesCache().get(self._cfx_rig_namespace))

    def get_ani_geo_cache_is_loaded(self):
        return bool(qsm_mya_core.ReferencesCache().get(self._ani_geo_cache_namespace))

    def get_ani_ctl_cache_is_loaded(self):
        return bool(qsm_mya_core.ReferencesCache().get(self._ani_ctl_cache_namespace))

    def reference_scene(self, scene_path):
        qsm_mya_core.SceneFile.reference_file(scene_path, self._cfx_rig_namespace)
        
    def replace_scene(self, scene_path, force=False):
        reference_node = qsm_mya_core.ReferencesCache().get(self._cfx_rig_namespace)
        if reference_node:
            if force is True:
                # todo: bug for replace, remove and re-reference again?
                bsc_log.Log.trace_method_result(
                    self.LOG_KEY, 'replace reference force: {}'.format(self._cfx_rig_namespace)
                )
                qsm_mya_core.Reference.remove(reference_node)
                self.reference_scene(scene_path)
            else:
                qsm_mya_core.Reference.replace(reference_node, scene_path)
                self.repair_solver()

    def load_scene_auto(self, scene_path, force=False):
        if self.get_is_loaded() is False:
            self.reference_scene(scene_path)
        else:
            self.replace_scene(scene_path, force)

        locations = qsm_mya_core.Namespace.find_roots(self._cfx_rig_namespace)
        for i_location in locations:
            _cfx_group.ShotCfxRigGroupOrg().add_one(i_location)

        if self.get_ani_geo_cache_is_loaded() or self.get_ani_ctl_cache_is_loaded():
            self.connect_to_ani_geo_cache()
            self.connect_to_ani_ctl_cache()
        else:
            self.connect_to_rig()

    def find_output_geo_location(self):
        _ = cmds.ls('{}:cfx_output_geo_grp'.format(self._cfx_rig_namespace), long=1)
        if _:
            return _[0]

    def find_source_geo_layer(self):
        return qsm_mya_core.Namespace.find_one(
            self._cfx_rig_namespace, node_name=_asset_cfx_rig_core.CfxSourceGeoLyrOrg.NAME
        )

    def find_nuclei(self):
        return qsm_mya_core.Namespace.find_match_nodes(self._cfx_rig_namespace, node_type='nucleus')
    
    def set_all_solver_enable(self, boolean):
        nuclei = self.find_nuclei()
        for i_nucleus in nuclei:
            qsm_mya_core.NodeAttribute.set_value(i_nucleus, 'enable', boolean)
    
    def apply_all_solver_start_frame(self, frame):
        nuclei = self.find_nuclei()
        for i_nucleus in nuclei:
            qsm_mya_core.NodeAttribute.set_value(i_nucleus, 'startFrame', frame)

    def generate_location_args(self):
        gui_location = '/{}/cfx_rig'.format(self._rig_namespace)
        dcc_location = self.find_location()
        if dcc_location:
            return gui_location, dcc_location
        return gui_location, None

    def get_rig_variant_name(self):
        location = self.find_location()
        if qsm_mya_core.NodeAttribute.is_exists(location, 'qsm_variant'):
            return qsm_mya_core.NodeAttribute.get_as_string(location, 'qsm_variant')
        return 'default'
    
    def generate_component_data(self):
        gui_location, dcc_location = self.generate_location_args()
        if dcc_location:
            return _asset_cfx_rig_core.AssetCfxRigHandle.generate_component_data_for(gui_location, dcc_location)
        return {}

    def generate_export_args(self):
        mesh_transforms = []
        location = self.find_output_geo_location()
        meshes = qsm_mya_core.Group.find_siblings(
            location, 'mesh'
        )
        for i_shape in meshes:
            i_transform = qsm_mya_core.Shape.get_transform(i_shape)
            if qsm_mya_core.Transform.is_visible(i_transform):
                mesh_transforms.append(i_transform)
        return mesh_transforms

    def get_extend_geometry_args(self):
        mesh_transforms = []
        adv_opt = qsm_mya_adv.AdvChrOpt(self._rig_namespace)
        meshes = adv_opt.find_all_meshes()
        for i_mesh in meshes:
            i_transform = qsm_mya_core.Shape.get_transform(i_mesh)
            if qsm_mya_core.MeshDeform.is_valid(i_transform) is True:
                mesh_transforms.append(i_transform)
            elif qsm_mya_core.MeshDynamic.is_valid(i_transform) is True:
                mesh_transforms.append(i_transform)
        return mesh_transforms

    # to rig
    def connect_to_rig_blends(self):
        blend_shape_nodes = qsm_mya_core.Namespace.find_match_nodes(
            self._cfx_rig_namespace, 'blendShape'
        )
        for i_blend_node in blend_shape_nodes:
            if qsm_mya_core.NodeAttribute.is_exists(
                i_blend_node, 'qsm_blend_source'
            ):
                i_source_transform_name = qsm_mya_core.NodeAttribute.get_as_string(
                    i_blend_node, 'qsm_blend_source'
                )
                i_source_transform_path = qsm_mya_core.Namespace.find_one(
                    self._rig_namespace, node_name=i_source_transform_name
                )
                if i_source_transform_path:
                    qsm_mya_core.MeshBlend.set_source_transform(i_blend_node, i_source_transform_path)

    def connect_to_rig_hidden(self):
        layer_name = _asset_cfx_rig_core.CfxSourceGeoLyrOrg.NAME
        layer = '{}:{}'.format(self._cfx_rig_namespace, layer_name)
        if qsm_mya_core.NodeAttribute.is_exists(layer, 'qsm_hidden_set'):
            value = qsm_mya_core.NodeAttribute.get_value(layer, 'qsm_hidden_set')
            if value:
                data = json.loads(value)
                for i in data:
                    i_transform_path = qsm_mya_core.Namespace.find_one(
                        self._rig_namespace, node_name=i
                    )
                    if i_transform_path:
                        qsm_mya_core.DisplayLayer.add_one(layer, i_transform_path)

    def connect_to_rig_constraints(self):
        constraint_nodes = qsm_mya_core.Namespace.find_match_nodes(
            self._cfx_rig_namespace, 'parentConstraint'
        )
        for i_constraint_node in constraint_nodes:
            if qsm_mya_core.NodeAttribute.is_exists(
                i_constraint_node, 'qsm_constraint_source'
            ):
                i_source_transform_name = qsm_mya_core.NodeAttribute.get_as_string(
                    i_constraint_node, 'qsm_constraint_source'
                )
                i_source_transform_path = qsm_mya_core.Namespace.find_one(
                    self._rig_namespace, node_name=i_source_transform_name
                )
                if i_source_transform_path:
                    qsm_mya_core.ParentConstraint.set_source(i_constraint_node, i_source_transform_path)

    def connect_to_rig(self):
        bsc_log.Log.trace_method_result(
            self.LOG_KEY, 'connect to rig: {}'.format(self._rig_namespace)
        )
        self.connect_to_rig_blends()
        self.connect_to_rig_hidden()
        self.connect_to_rig_constraints()

    # to animation cache
    def connect_to_ani_geo_cache_blends(self):
        blend_shape_nodes = qsm_mya_core.Namespace.find_match_nodes(
            self._cfx_rig_namespace, 'blendShape'
        )
        for i_blend_node in blend_shape_nodes:
            if qsm_mya_core.NodeAttribute.is_exists(
                i_blend_node, 'qsm_blend_source'
            ):
                i_source_transform_name = qsm_mya_core.NodeAttribute.get_as_string(
                    i_blend_node, 'qsm_blend_source'
                )
                i_source_transform_path = qsm_mya_core.Namespace.find_one(
                    self._ani_geo_cache_namespace, node_name=i_source_transform_name
                )
                if i_source_transform_path:
                    qsm_mya_core.MeshBlend.set_source_transform(i_blend_node, i_source_transform_path)

    def connect_to_ani_geo_cache_hidden(self):
        layer_name = _asset_cfx_rig_core.CfxSourceGeoLyrOrg.NAME
        layer = '{}:{}'.format(self._cfx_rig_namespace, layer_name)
        if qsm_mya_core.NodeAttribute.is_exists(layer, 'qsm_hidden_set'):
            value = qsm_mya_core.NodeAttribute.get_value(layer, 'qsm_hidden_set')
            if value:
                data = json.loads(value)
                for i in data:
                    i_transform_path = qsm_mya_core.Namespace.find_one(
                        self._ani_geo_cache_namespace, node_name=i
                    )
                    if i_transform_path:
                        qsm_mya_core.DisplayLayer.add_one(layer, i_transform_path)

    def connect_to_ani_geo_cache(self):
        bsc_log.Log.trace_method_result(
            self.LOG_KEY, 'connect to animation geometry cache: {}'.format(self._rig_namespace)
        )
        self.connect_to_ani_geo_cache_blends()
        self.connect_to_ani_geo_cache_hidden()

    def connect_to_ani_ctl_cache(self):
        bsc_log.Log.trace_method_result(
            self.LOG_KEY, 'connect to animation control cache: {}'.format(self._rig_namespace)
        )
        constraint_nodes = qsm_mya_core.Namespace.find_match_nodes(
            self._cfx_rig_namespace, 'parentConstraint'
        )
        for i_constraint_node in constraint_nodes:
            if qsm_mya_core.NodeAttribute.is_exists(
                i_constraint_node, 'qsm_constraint_source'
            ):
                i_source_transform_name = qsm_mya_core.NodeAttribute.get_as_string(
                    i_constraint_node, 'qsm_constraint_source'
                )
                i_source_transform_path = qsm_mya_core.Namespace.find_one(
                    self._ani_ctl_cache_namespace, node_name=i_source_transform_name
                )
                if i_source_transform_path:
                    qsm_mya_core.ParentConstraint.set_source(i_constraint_node, i_source_transform_path)

    def repair_solver(self):
        """
        method for when reference is replaced, nucleus is broken.
        """
        nuclei = qsm_mya_core.Namespace.find_match_nodes(self._cfx_rig_namespace, node_type='nucleus')
        n_clothes = qsm_mya_core.Namespace.find_match_nodes(self._cfx_rig_namespace, node_type='nCloth')
        for i in nuclei:
            for j in n_clothes:
                qsm_mya_core.Nucleus.assign_to(i, j, force=False)

        n_rigids = qsm_mya_core.Namespace.find_match_nodes(self._cfx_rig_namespace, node_type='nRigid')
        for i in nuclei:
            for j in n_rigids:
                qsm_mya_core.Nucleus.assign_to(i, j, force=False)


class ShotAniGeoCacheHandle:
    def __init__(self, namespace):
        self._ani_geo_cache_namespace = namespace
        self._rig_namespace = ':'.join(self._ani_geo_cache_namespace.split(':')[:-1])

    def get_cache_path(self):
        return qsm_mya_core.ReferencesCache().get_file(self._ani_geo_cache_namespace)
    
    def reference_cache(self, cache_path):
        qsm_mya_core.Material.unlock_default()
        qsm_mya_core.SceneFile.reference_file(
            cache_path, self._ani_geo_cache_namespace
        )

    def replace_cache(self, cache_path, force=False):
        qsm_mya_core.Material.unlock_default()
        reference_node = qsm_mya_core.ReferencesCache().get(self._ani_geo_cache_namespace)
        if reference_node:
            if force is True:
                qsm_mya_core.Reference.remove(reference_node)
                self.reference_cache(cache_path)
            else:
                qsm_mya_core.Reference.replace(reference_node, cache_path)

    def load_cache_auto(self, cache_path):
        if self.get_is_loaded() is False:
            self.reference_cache(cache_path)
        else:
            self.replace_cache(cache_path)

        locations = qsm_mya_core.Namespace.find_roots(self._ani_geo_cache_namespace)
        for i_location in locations:
            _shot_animation_core.ShotAnimationCacheGroupOrg().add_one(i_location)

        ShotCfxClothAssetHandle(self._rig_namespace).cfx_rig_handle.connect_to_ani_geo_cache()

    def get_is_enable(self):
        reference_node = qsm_mya_core.ReferencesCache().get(self._ani_geo_cache_namespace)
        if reference_node:
            return qsm_mya_core.Reference.is_loaded(reference_node)
        return None

    def get_is_loaded(self):
        return bool(qsm_mya_core.ReferencesCache().get(self._ani_geo_cache_namespace))

    def find_location(self):
        _ = cmds.ls('{}:Geometry'.format(self._ani_geo_cache_namespace), long=1)
        if _:
            return _[0]

    def generate_location_args(self):
        gui_location = '/{}/ani_geo_cache'.format(self._rig_namespace)
        dcc_location = self.find_location()
        if dcc_location:
            return gui_location, dcc_location
        return gui_location, None


class ShotAniCtlCacheHandle:
    def __init__(self, namespace):
        self._ani_ctl_cache_namespace = namespace
        self._rig_namespace = ':'.join(self._ani_ctl_cache_namespace.split(':')[:-1])

    def get_cache_path(self):
        return qsm_mya_core.ReferencesCache().get_file(self._ani_ctl_cache_namespace)

    def get_is_enable(self):
        reference_node = qsm_mya_core.ReferencesCache().get(self._ani_ctl_cache_namespace)
        if reference_node:
            return qsm_mya_core.Reference.is_loaded(reference_node)
        return None

    def get_is_loaded(self):
        return bool(qsm_mya_core.ReferencesCache().get(self._ani_ctl_cache_namespace))

    def reference_cache(self, cache_path):
        qsm_mya_core.Material.unlock_default()
        qsm_mya_core.SceneFile.reference_file(
            cache_path, self._ani_ctl_cache_namespace
        )
    
    def replace_cache(self, cache_path, force=False):
        qsm_mya_core.Material.unlock_default()
        reference_node = qsm_mya_core.ReferencesCache().get(self._ani_ctl_cache_namespace)
        if reference_node:
            if force is True:
                qsm_mya_core.Reference.remove(reference_node)
                self.reference_cache(cache_path)
            else:
                qsm_mya_core.Reference.replace(reference_node, cache_path)

    def load_cache_auto(self, cache_path):
        if self.get_is_loaded() is False:
            self.reference_cache(cache_path)
        else:
            self.replace_cache(cache_path)

        locations = qsm_mya_core.Namespace.find_roots(self._ani_ctl_cache_namespace)
        for i_location in locations:
            _shot_animation_core.ShotAnimationCacheGroupOrg().add_one(i_location)

        ShotCfxClothAssetHandle(self._rig_namespace).cfx_rig_handle.connect_to_ani_ctl_cache()

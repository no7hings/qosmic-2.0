# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from .... import core as _mya_core

from ....adv import core as _adv_core


# rig
class AbsRigOpt(object):
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
            i_blend_nodes = _mya_core.MeshBlendShapeSource.get_deform_nodes(
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


class RigOpt(AbsRigOpt):
    def __init__(self, *args, **kwargs):
        super(RigOpt, self).__init__(*args, **kwargs)


# group
class AbsGroupOpt(object):
    LOCATION = None

    def __init__(self):
        if _mya_core.Node.is_exists(self.LOCATION) is False:
            _mya_core.Group.create_dag(self.LOCATION)

    def add_one(self, path):
        if path.startswith('{}|'.format(self.LOCATION)):
            return path
        return _mya_core.Group.add_one(self.LOCATION, path)


#   bridge
class CfxBridgeGeoGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx|cfx_bridge_grp|cfx_bridge_geo_grp'

    def __init__(self):
        super(CfxBridgeGeoGrpOpt, self).__init__()


class CfxBridgeControlGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx|cfx_bridge_grp|cfx_bridge_control_grp'

    def __init__(self):
        super(CfxBridgeControlGrpOpt, self).__init__()


#   cloth
class CfxClothGeoGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx|cfx_output_geo_grp|cfx_cloth_geo_grp'

    def __init__(self):
        super(CfxClothGeoGrpOpt, self).__init__()


#   cloth proxy
class CfxClothProxyGeoGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx|cfx_cloth_proxy_grp|cfx_cloth_proxy_geo_grp'

    def __init__(self):
        super(CfxClothProxyGeoGrpOpt, self).__init__()


class CfxNClothGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx|cfx_ncloth_grp'

    def __init__(self):
        super(CfxNClothGrpOpt, self).__init__()


class CfxNRigidGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx|cfx_nrigid_grp'

    def __init__(self):
        super(CfxNRigidGrpOpt, self).__init__()


#   collider
class CfxColliderGeoGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx|cfx_collider_grp|cfx_collider_geo_grp'

    def __init__(self):
        super(CfxColliderGeoGrpOpt, self).__init__()


#   appendix
class CfxAppendixGeoGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx|cfx_output_geo_grp|cfx_appendix_geo_grp'

    def __init__(self):
        super(CfxAppendixGeoGrpOpt, self).__init__()


#   dynamic
class CfxNucleusGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx|cfx_nucleus_grp'

    def __init__(self):
        super(CfxNucleusGrpOpt, self).__init__()


#   wrap
class CfxWrapGrpOpt(AbsGroupOpt):
    LOCATION = '|master|cfx|cfx_wrap_grp'

    def __init__(self):
        super(CfxWrapGrpOpt, self).__init__()


# layer
class AbsLayerOpt(object):
    NAME = None
    RGB = (0, 0, 0)
    VISIBLE = 0

    def __init__(self):
        if _mya_core.Node.is_exists(self.NAME) is False:
            _mya_core.DisplayLayer.create(self.NAME)
            _mya_core.DisplayLayer.set_rgb(self.NAME, self.RGB)
            _mya_core.DisplayLayer.set_visible(self.NAME, self.VISIBLE)

    def add_one(self, path):
        _mya_core.DisplayLayer.add_one(self.NAME, path)


#   source
class CfxSourceGeoLyrOpt(AbsLayerOpt):
    NAME = 'CFX_SOURCE_GEO_LYR'
    RGB = (0, 0, 0)
    VISIBLE = 0

    def __init__(self):
        super(CfxSourceGeoLyrOpt, self).__init__()


#   bridge
class CfxBridgeGeoLyrOpt(AbsLayerOpt):
    NAME = 'CFX_BRIDGE_GEO_LYR'
    RGB = (1, 0, 0)
    VISIBLE = 1

    def __init__(self):
        super(CfxBridgeGeoLyrOpt, self).__init__()


class CfxBridgeControlLyrOpt(AbsLayerOpt):
    NAME = 'CFX_BRIDGE_CONTROL_LYR'
    RGB = (0, 1, 1)
    VISIBLE = 1

    def __init__(self):
        super(CfxBridgeControlLyrOpt, self).__init__()


#   cloth
class CfxClothGeoLyrOpt(AbsLayerOpt):
    NAME = 'CFX_CLOTH_GEO_LYR'
    RGB = (1, 0, 1)
    VISIBLE = 1

    def __init__(self):
        super(CfxClothGeoLyrOpt, self).__init__()


#   cloth proxy
class CfxClothProxyGeoLyrOpt(AbsLayerOpt):
    NAME = 'CFX_CLOTH_PROXY_GEO_LYR'
    RGB = (0, 1, 0)
    VISIBLE = 1

    def __init__(self):
        super(CfxClothProxyGeoLyrOpt, self).__init__()


#   collider
class CfxColliderGeoLyrOpt(AbsLayerOpt):
    NAME = 'CFX_COLLIDER_GEO_LYR'
    RGB = (0, 0, 1)
    VISIBLE = 1

    def __init__(self):
        super(CfxColliderGeoLyrOpt, self).__init__()


#   appendix
class CfxAppendixGeoLyrOpt(AbsLayerOpt):
    NAME = 'CFX_APPENDIX_GEO_LYR'
    RGB = (1, 1, 0)
    VISIBLE = 1

    def __init__(self):
        super(CfxAppendixGeoLyrOpt, self).__init__()


# material
class AbsMaterialOpt(object):
    NAME = None
    RGB = (0, 0, 0)

    def __init__(self):
        if _mya_core.Node.is_exists(self.NAME) is False:
            _mya_core.Material.create_as_lambert(self.NAME, self.RGB)

    def assign_to(self, path):
        _mya_core.Material.assign_to(
            self.NAME, path
        )


#   bridge
class CfxBridgeGeoMtlOpt(AbsMaterialOpt):
    NAME = 'CFX_BRIDGE_MTL'
    RGB = (1, 0, 0)

    def __init__(self):
        super(CfxBridgeGeoMtlOpt, self).__init__()


#   cloth
class CfxClothGeoMtlOpt(AbsMaterialOpt):
    NAME = 'CFX_CLOTH_MTL'
    RGB = (1, 0, 1)

    def __init__(self):
        super(CfxClothGeoMtlOpt, self).__init__()


#   cloth proxy
class CfxClothProxyGeoMtlOpt(AbsMaterialOpt):
    NAME = 'CFX_CLOTH_PROXY_MTL'
    RGB = (0, 1, 0)

    def __init__(self):
        super(CfxClothProxyGeoMtlOpt, self).__init__()


#   collider
class CfxColliderGeoMtlOpt(AbsMaterialOpt):
    NAME = 'CFX_COLLIDER_MTL'
    RGB = (0, 0, 1)

    def __init__(self):
        super(CfxColliderGeoMtlOpt, self).__init__()


#   appendix
class CfxAppendixGeoMtlOpt(AbsMaterialOpt):
    NAME = 'CFX_APPENDIX_MTL'
    RGB = (1, 1, 0)

    def __init__(self):
        super(CfxAppendixGeoMtlOpt, self).__init__()

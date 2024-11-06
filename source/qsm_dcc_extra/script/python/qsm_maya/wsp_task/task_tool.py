# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_general.wsp_task as qsm_dcc_wsp_task

import qsm_maya.core as qsm_mya_core

import qsm_maya.steps.cfx_rig.core as qsm_mya_stp_cfx_rig_core


class MayaGnlToolOpt(qsm_dcc_wsp_task.DccTaskToolOpt):
    def __init__(self, *args, **kwargs):
        super(MayaGnlToolOpt, self).__init__(*args, **kwargs)


class MayaAssetGnlToolOpt(MayaGnlToolOpt):
    @classmethod
    def test(cls):
        cls(qsm_dcc_wsp_task.TaskParse(), {}).create_groups_for('cfx_rig')

    def __init__(self, *args, **kwargs):
        super(MayaAssetGnlToolOpt, self).__init__(*args, **kwargs)

    def create_groups_for(self, task):
        content = self._task_session._task_parse.configure.get_as_content(
            'dcc-asset-group.{}'.format(task), relative=True
        )

        for i_key in content.get_all_keys():
            i_path = '|{}'.format(i_key.replace('.', '|'))
            qsm_mya_core.Group.create(i_path)


class MayaAssetCfxRigToolOpt(MayaAssetGnlToolOpt):
    def __init__(self, *args, **kwargs):
        super(MayaAssetCfxRigToolOpt, self).__init__(*args, **kwargs)
        self._rig_opt = qsm_mya_stp_cfx_rig_core.RigOpt()

    # cloth
    @qsm_mya_core.Undo.execute
    def add_to_cloth_geo_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh not in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path

                self.add_to_cloth_geo(i_transform_path)

    @qsm_mya_core.Undo.execute
    def copy_as_cloth_geo_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path
                i_transform_name = qsm_mya_core.DagNode.to_name_without_namespace(i_transform_path)
                i_transform_name_new = '{}__copy'.format(
                    qsm_mya_core.DagNode.to_name_without_namespace(i_transform_name)
                )

                i_results = cmds.duplicate(
                    i_transform_path, name=i_transform_name_new, inputConnections=0
                )
                if i_results:
                    # add source
                    qsm_mya_stp_cfx_rig_core.CfxSourceGeoLyrOpt().add_one(i_transform_path)

                    i_result = i_results[0]
                    qsm_mya_core.Transform.delete_all_intermediate_shapes(i_result)

                    i_transform_path_new = self.add_to_cloth_geo(i_result)

                    # create blend
                    if kwargs.get('auto_blend'):
                        qsm_mya_core.BlendShape.create(
                            i_transform_path, i_transform_path_new
                        )

    @staticmethod
    def add_to_cloth_geo(transform_path):
        """
        transform_path is mesh transform
        """
        transform_path_new = qsm_mya_stp_cfx_rig_core.CfxClothGeoGrpOpt().add_one(transform_path)
        qsm_mya_stp_cfx_rig_core.CfxClothGeoLyrOpt().add_one(transform_path_new)
        qsm_mya_stp_cfx_rig_core.CfxClothGeoMtlOpt().assign_to(transform_path_new)
        return transform_path_new
    
    @qsm_mya_core.Undo.execute
    def create_ncloth_by_select(self):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh not in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path

                self.create_ncloth(i_transform_path)

    @classmethod
    def create_ncloth(cls, transform_path):
        args = qsm_mya_core.MeshNCloth.create_auto(
            transform_path
        )
        if args:
            flag, (ntransform, nucleus) = args
            if flag is True:
                qsm_mya_stp_cfx_rig_core.NCloth(ntransform).apply_properties(
                    qsm_mya_stp_cfx_rig_core.NCloth.DEFAULT_PROPERTIES
                )
            qsm_mya_stp_cfx_rig_core.CfxNClothGrpOpt().add_one(ntransform)
            qsm_mya_stp_cfx_rig_core.CfxNucleusGrpOpt().add_one(nucleus)

    # cloth proxy
    @qsm_mya_core.Undo.execute
    def add_to_cloth_proxy_geo_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh not in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path

                self.add_to_cloth_proxy_geo(i_transform_path)

    @qsm_mya_core.Undo.execute
    def copy_as_cloth_proxy_geo_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path
                i_transform_name = qsm_mya_core.DagNode.to_name_without_namespace(i_transform_path)
                i_transform_name_new = '{}__copy'.format(
                    qsm_mya_core.DagNode.to_name_without_namespace(i_transform_name)
                )

                i_results = cmds.duplicate(
                    i_transform_path, name=i_transform_name_new, inputConnections=0
                )
                if i_results:
                    # add source
                    qsm_mya_stp_cfx_rig_core.CfxSourceGeoLyrOpt().add_one(i_transform_path)

                    i_result = i_results[0]
                    qsm_mya_core.Transform.delete_all_intermediate_shapes(i_result)

                    i_transform_path_new = self.add_to_cloth_proxy_geo(i_result)

                    # create blend
                    if kwargs.get('auto_blend'):
                        qsm_mya_core.BlendShape.create(
                            i_transform_path, i_transform_path_new
                        )

    @staticmethod
    def add_to_cloth_proxy_geo(transform_path):
        """
        transform_path is mesh transform
        """
        transform_path_new = qsm_mya_stp_cfx_rig_core.CfxClothProxyGeoGrpOpt().add_one(transform_path)
        qsm_mya_stp_cfx_rig_core.CfxClothProxyGeoLyrOpt().add_one(transform_path_new)
        qsm_mya_stp_cfx_rig_core.CfxClothProxyGeoMtlOpt().assign_to(transform_path_new)
        return transform_path_new

    # appendix
    @qsm_mya_core.Undo.execute
    def add_to_appendix_geo_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh not in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path

                self.add_to_appendix_geo(i_transform_path)
    
    @qsm_mya_core.Undo.execute
    def copy_as_appendix_geo_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path
                i_transform_name = qsm_mya_core.DagNode.to_name_without_namespace(i_transform_path)
                i_transform_name_new = '{}__copy'.format(
                    qsm_mya_core.DagNode.to_name_without_namespace(i_transform_name)
                )

                i_results = cmds.duplicate(
                    i_transform_path, name=i_transform_name_new, inputConnections=0
                )
                if i_results:
                    qsm_mya_stp_cfx_rig_core.CfxSourceGeoLyrOpt().add_one(i_transform_path)

                    self.add_to_appendix_geo(i_results[0])

    @staticmethod
    def add_to_appendix_geo(transform_path):
        """
        transform_path is mesh transform
        """
        transform_path_new = qsm_mya_stp_cfx_rig_core.CfxAppendixGeoGrpOpt().add_one(transform_path)
        qsm_mya_stp_cfx_rig_core.CfxAppendixGeoLyrOpt().add_one(transform_path_new)
        qsm_mya_stp_cfx_rig_core.CfxAppendixGeoMtlOpt().assign_to(transform_path_new)
        return transform_path_new

    # collider
    @qsm_mya_core.Undo.execute
    def add_to_collider_geo_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh not in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path

                self.add_to_collider_geometry(i_transform_path)

    @qsm_mya_core.Undo.execute
    def copy_as_collider_geo_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path
                i_transform_name = qsm_mya_core.DagNode.to_name_without_namespace(i_transform_path)
                i_transform_name_new = '{}__copy'.format(
                    qsm_mya_core.DagNode.to_name_without_namespace(i_transform_name)
                )

                i_results = cmds.duplicate(
                    i_transform_path, name=i_transform_name_new, inputConnections=0
                )
                if i_results:
                    # add source
                    qsm_mya_stp_cfx_rig_core.CfxSourceGeoLyrOpt().add_one(i_transform_path)

                    i_result = i_results[0]
                    qsm_mya_core.Transform.delete_all_intermediate_shapes(i_result)

                    i_transform_path_new = self.add_to_collider_geometry(i_result)

                    # create blend
                    if kwargs.get('auto_blend'):
                        qsm_mya_core.BlendShape.create(
                            i_transform_path, i_transform_path_new
                        )

    @staticmethod
    def add_to_collider_geometry(transform_path):
        """
        transform_path is mesh transform
        """
        transform_path_new = qsm_mya_stp_cfx_rig_core.CfxColliderGeoGrpOpt().add_one(transform_path)
        qsm_mya_stp_cfx_rig_core.CfxColliderGeoLyrOpt().add_one(transform_path_new)
        qsm_mya_stp_cfx_rig_core.CfxColliderGeoMtlOpt().assign_to(transform_path_new)
        return transform_path_new

    @qsm_mya_core.Undo.execute
    def create_nrigid_by_select(self):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh not in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path

                self.create_nrigid(i_transform_path)

    @classmethod
    def create_nrigid(cls, transform_path):
        args = qsm_mya_core.MeshNRigid.create_auto(
            transform_path
        )
        if args:
            flag, (ntransform, nucleus) = args
            if flag is True:
                qsm_mya_stp_cfx_rig_core.NRigid(ntransform).apply_properties(
                    qsm_mya_stp_cfx_rig_core.NRigid.DEFAULT_PROPERTIES
                )
            qsm_mya_stp_cfx_rig_core.CfxNRigidGrpOpt().add_one(ntransform)
            qsm_mya_stp_cfx_rig_core.CfxNucleusGrpOpt().add_one(nucleus)

    # bridge
    @qsm_mya_core.Undo.execute
    def add_to_bridge_geo_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh not in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path

                self.add_to_bridge_geometry(i_transform_path)

    @qsm_mya_core.Undo.execute
    def copy_as_bridge_geo_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path
                i_transform_name = qsm_mya_core.DagNode.to_name_without_namespace(i_transform_path)
                i_transform_name_new = '{}__copy'.format(
                    qsm_mya_core.DagNode.to_name_without_namespace(i_transform_name)
                )

                i_results = cmds.duplicate(
                    i_transform_path, name=i_transform_name_new, inputConnections=0
                )
                if i_results:
                    # add source
                    qsm_mya_stp_cfx_rig_core.CfxSourceGeoLyrOpt().add_one(i_transform_path)

                    i_result = i_results[0]
                    qsm_mya_core.Transform.delete_all_intermediate_shapes(i_result)

                    i_transform_path_new = self.add_to_bridge_geometry(i_result)

                    # create blend
                    if kwargs.get('auto_blend'):
                        qsm_mya_core.BlendShape.create(
                            i_transform_path, i_transform_path_new
                        )

    @staticmethod
    def add_to_bridge_geometry(transform_path):
        """
        transform_path is mesh transform
        """
        transform_path_new = qsm_mya_stp_cfx_rig_core.CfxBridgeGeoGrpOpt().add_one(transform_path)
        qsm_mya_stp_cfx_rig_core.CfxBridgeGeoLyrOpt().add_one(transform_path_new)
        qsm_mya_stp_cfx_rig_core.CfxBridgeGeoMtlOpt().assign_to(transform_path_new)
        return transform_path_new

    #   control
    @qsm_mya_core.Undo.execute
    def copy_as_bridge_control_by_select(self, *args, **kwargs):
        control_set = self._rig_opt.control_set
        _ = qsm_mya_core.Selection.get_all_transforms()
        for i_transform_path in _:
            if i_transform_path in control_set:
                i_transform_name = qsm_mya_core.DagNode.to_name_without_namespace(i_transform_path)
                i_transform_name_new = '{}__locator'.format(
                    qsm_mya_core.DagNode.to_name_without_namespace(i_transform_name)
                )

                i_flag, i_result = qsm_mya_core.VectorLocator.create(
                    i_transform_name_new
                )

                i_result = qsm_mya_stp_cfx_rig_core.CfxBridgeControlGrpOpt().add_one(i_result)
                qsm_mya_stp_cfx_rig_core.CfxBridgeControlLyrOpt().add_one(i_result)

                if kwargs.get('auto_constrain'):
                    qsm_mya_core.ParentConstraint.create(i_transform_path, i_result)

    #
    @staticmethod
    def auto_collection():
        qsm_mya_stp_cfx_rig_core.CfxGroup().auto_collection()

    @staticmethod
    def auto_name():
        qsm_mya_stp_cfx_rig_core.CfxGroup().auto_name()

    @qsm_mya_core.Undo.execute
    def rest_rig_controls_transformation(self, *args, **kwargs):
        self._rig_opt._adv_rig.rest_controls_transformation(translate=True, rotate=True)

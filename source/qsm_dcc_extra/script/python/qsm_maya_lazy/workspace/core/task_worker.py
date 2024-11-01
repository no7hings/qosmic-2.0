# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_lazy.workspace.core as qsm_lzy_wsp_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.adv.core as qsm_mya_adv_core

import qsm_maya.steps.cfx.core as qsm_mya_stp_cfx_core


class MayaAssetTaskWorker(qsm_lzy_wsp_core.DccTaskWorker):
    @classmethod
    def test(cls):
        """
        (
            root_source=Z:/projects
            file_format=ma
            root_temporary=Z:/projects
            artist=shared
            task=cfx_rig
            project=QSM_TST
            task_unit=main
            step=cfx
            version=001
            role=chr
            asset=carol
            root_release=X:
            resource_type=asset
        )
        """
        cls(qsm_lzy_wsp_core.TaskParse(), {}).create_groups_for('cfx_rig')

    def __init__(self, *args, **kwargs):
        super(MayaAssetTaskWorker, self).__init__(*args, **kwargs)

    def create_groups_for(self, task):
        content = self._task_parse.configure.get_as_content(
            'dcc-asset-group.{}'.format(task), relative=True
        )

        for i_key in content.get_all_keys():
            i_path = '|{}'.format(i_key.replace('.', '|'))
            qsm_mya_core.Group.create(i_path)


class _RigOpt(object):

    def __init__(self, namespace):
        self._namespace = namespace

        self._adv_rig = qsm_mya_adv_core.AdvOpt(self._namespace)

        self._mesh_set = set(self._adv_rig.find_all_meshes())

    @property
    def mesh_set(self):
        return self._mesh_set


class _CfxOpt(object):
    def __init__(self, location):
        self._location = location


class MayaAssetCfxRigWorker(MayaAssetTaskWorker):
    def __init__(self, *args, **kwargs):
        super(MayaAssetCfxRigWorker, self).__init__(*args, **kwargs)
        self._rig_opt = _RigOpt('rig')

    # bridge
    @qsm_mya_core.Undo.execute
    def add_to_bridge_geometry_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh not in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path

                self.add_to_bridge_geometry(i_transform_path)

    @qsm_mya_core.Undo.execute
    def copy_as_bridge_geometry_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path
                i_transform_name = i_shape_opt.transform_name
                i_transform_name_new = '{}__geo'.format(
                    qsm_mya_core.DagNode.to_name_without_namespace(i_transform_name)
                )
                i_transform_path_new = '{}|{}'.format(
                    qsm_mya_stp_cfx_core.CfxBridgeGeoGrpOpt.PATH, i_transform_name_new
                )
                if qsm_mya_core.Node.is_exists(i_transform_path_new) is True:
                    continue

                i_results = cmds.duplicate(
                    i_transform_path, name=i_transform_name_new, inputConnections=0
                )
                if i_results:
                    # add source
                    qsm_mya_stp_cfx_core.CfxSourceGeoLyrOpt().add_one(i_transform_path)

                    i_result = i_results[0]
                    qsm_mya_core.Transform.delete_all_intermediate_shapes(i_result)

                    self.add_to_bridge_geometry(i_result)

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
        transform_path = qsm_mya_stp_cfx_core.CfxBridgeGeoGrpOpt().add_one(transform_path)
        qsm_mya_stp_cfx_core.CfxBridgeGeoLyrOpt().add_one(transform_path)
        qsm_mya_stp_cfx_core.CfxBridgeGeoMtlOpt().assign_to(transform_path)

    # cloth
    @qsm_mya_core.Undo.execute
    def add_to_cloth_geometry_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh not in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path

                self.add_to_cloth_geometry(i_transform_path)

    @qsm_mya_core.Undo.execute
    def copy_as_cloth_geometry_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path
                i_transform_name = i_shape_opt.transform_name
                i_transform_name_new = '{}__geo'.format(
                    qsm_mya_core.DagNode.to_name_without_namespace(i_transform_name)
                )
                i_transform_path_new = '{}|{}'.format(
                    qsm_mya_stp_cfx_core.CfxClothGeoGrpOpt.PATH, i_transform_name_new
                )
                if qsm_mya_core.Node.is_exists(i_transform_path_new) is True:
                    continue

                i_results = cmds.duplicate(
                    i_transform_path, name=i_transform_name_new, inputConnections=0
                )
                if i_results:
                    # add source
                    qsm_mya_stp_cfx_core.CfxSourceGeoLyrOpt().add_one(i_transform_path)

                    i_result = i_results[0]
                    qsm_mya_core.Transform.delete_all_intermediate_shapes(i_result)

                    self.add_to_cloth_geometry(i_result)

                    # create blend
                    if kwargs.get('auto_blend'):
                        qsm_mya_core.BlendShape.create(
                            i_transform_path, i_transform_path_new
                        )

    @staticmethod
    def add_to_cloth_geometry(transform_path):
        """
        transform_path is mesh transform
        """
        transform_path = qsm_mya_stp_cfx_core.CfxClothGeoGrpOpt().add_one(transform_path)
        qsm_mya_stp_cfx_core.CfxClothGeoLyrOpt().add_one(transform_path)
        qsm_mya_stp_cfx_core.CfxClothGeoMtlOpt().assign_to(transform_path)
    
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
                qsm_mya_stp_cfx_core.NCloth(ntransform).apply_properties(
                    qsm_mya_stp_cfx_core.NCloth.DEFAULT_PROPERTIES
                )
            qsm_mya_stp_cfx_core.CfxNClothGrpOpt().add_one(ntransform)
            qsm_mya_stp_cfx_core.CfxNucleusGrpOpt().add_one(nucleus)
    
    # collider
    @qsm_mya_core.Undo.execute
    def add_to_collider_geometry_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh not in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path

                self.add_to_collider_geometry(i_transform_path)

    @qsm_mya_core.Undo.execute
    def copy_as_collider_geometry_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path
                i_transform_name = i_shape_opt.transform_name
                i_transform_name_new = '{}__geo'.format(
                    qsm_mya_core.DagNode.to_name_without_namespace(i_transform_name)
                )
                i_transform_path_new = '{}|{}'.format(
                    qsm_mya_stp_cfx_core.CfxColliderGeoGrpOpt.PATH, i_transform_name_new
                )
                if qsm_mya_core.Node.is_exists(i_transform_path_new) is True:
                    continue

                i_results = cmds.duplicate(
                    i_transform_path, name=i_transform_name_new, inputConnections=0
                )
                if i_results:
                    # add source
                    qsm_mya_stp_cfx_core.CfxSourceGeoLyrOpt().add_one(i_transform_path)

                    i_result = i_results[0]
                    qsm_mya_core.Transform.delete_all_intermediate_shapes(i_result)

                    self.add_to_collider_geometry(i_result)

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
        transform_path = qsm_mya_stp_cfx_core.CfxColliderGeoGrpOpt().add_one(transform_path)
        qsm_mya_stp_cfx_core.CfxColliderGeoLyrOpt().add_one(transform_path)
        qsm_mya_stp_cfx_core.CfxColliderGeoMtlOpt().assign_to(transform_path)

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
                qsm_mya_stp_cfx_core.NRigid(ntransform).apply_properties(
                    qsm_mya_stp_cfx_core.NRigid.DEFAULT_PROPERTIES
                )
            qsm_mya_stp_cfx_core.CfxNRigidGrpOpt().add_one(ntransform)
            qsm_mya_stp_cfx_core.CfxNucleusGrpOpt().add_one(nucleus)

    # appendix
    def copy_as_appendix_geometry_by_select(self, *args, **kwargs):
        mesh_set = self._rig_opt.mesh_set
        _ = qsm_mya_core.Selection.get_all_meshes()
        for i_mesh in _:
            if i_mesh in mesh_set:
                i_shape_opt = qsm_mya_core.ShapeOpt(i_mesh)

                i_transform_path = i_shape_opt.transform_path
                i_transform_name = i_shape_opt.transform_name
                i_transform_name_new = '{}__geo'.format(
                    qsm_mya_core.DagNode.to_name_without_namespace(i_transform_name)
                )
                i_transform_path_new = '{}|{}'.format(
                    qsm_mya_stp_cfx_core.CfxAppendixGeoGrpOpt.PATH, i_transform_name_new
                )
                if qsm_mya_core.Node.is_exists(i_transform_path_new) is True:
                    continue

                i_results = cmds.duplicate(
                    i_transform_path, name=i_transform_name_new, inputConnections=0
                )
                if i_results:
                    qsm_mya_stp_cfx_core.CfxSourceGeoLyrOpt().add_one(i_transform_path)

                    self.add_to_appendix_geometry(i_results[0])

    @staticmethod
    def add_to_appendix_geometry(transform_path):
        """
        transform_path is mesh transform
        """
        transform_path = qsm_mya_stp_cfx_core.CfxAppendixGeoGrpOpt().add_one(transform_path)
        qsm_mya_stp_cfx_core.CfxAppendixGeoLyrOpt().add_one(transform_path)
        qsm_mya_stp_cfx_core.CfxAppendixGeoMtlOpt().assign_to(transform_path)

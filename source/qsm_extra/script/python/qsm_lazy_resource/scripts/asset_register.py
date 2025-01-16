# coding:utf-8
import lxbasic.storage as bsc_storage

import lxbasic.log as bsc_log

import qsm_general.core as qsm_gnl_core

import qsm_scan as qsm_scan

import qsm_screw.core as qsm_scr_core


class AssetBatchRegisterOpt(object):
    def __init__(self, project_name, project_chs_name):
        self._project_name = project_name
        self._project_chs_name = project_chs_name
        self._scan_root = qsm_scan.Stage().get_root()

        self._scr_stage = qsm_scr_core.Stage('asset_test')

    def execute(self, character=False, prop=False, scenery=False):
        self.register_project(self._project_name, self._project_chs_name)
        self.register_roles(self._project_name)
        if character is True:
            self.register_character_assets(self._project_name)
        if prop is True:
            self.register_prop_assets(self._project_name)
        if scenery is True:
            self.register_scenery_assets(self._project_name)

    def register_asset(self, asset_path, scr_type_path, maya_scene_path, task_name):
        scr_node_path = '/{}'.format('_'.join(asset_path.split('/')[1:]))
        scene_opt = bsc_storage.StgFileOpt(maya_scene_path)
        if self._scr_stage.get_node(scr_node_path):
            return

        self._scr_stage.create_node(scr_node_path, ctime=scene_opt.get_ctime(), mtime=scene_opt.get_mtime())
        self._scr_stage.create_node_type_assign(
            scr_node_path, scr_type_path
        )
        self._scr_stage.create_or_update_parameters(
            scr_node_path, 'scene', maya_scene_path
        )
        scr_task_tag_path = '/task/{}'.format(task_name)
        self._scr_stage.create_node_tag_assign(
            scr_node_path, scr_task_tag_path
        )
        # todo: remove this
        # assign unspecified
        # self._scr_stage.create_node_tag_assign(
        #     scr_node_path, '/mesh_count/face/unspecified'
        # )
        # self._scr_stage.create_node_tag_assign(
        #     scr_node_path, '/system_resource_usage/memory/unspecified'
        # )

    def register_project(self, project_name, project_chs_name):
        scr_type_path = '/{}'.format(self._project_name)
        self._scr_stage.create_type_as_group(
            scr_type_path, gui_name=project_name, gui_name_chs=project_chs_name
        )

    def register_roles(self, project_name):
        for i_name, i_gui_name, i_gui_name_chs in [
            ('character', 'Character', '角色'),
            ('prop', 'Prop', '道具'),
            ('scenery', 'Scenery', '场景'),
        ]:
            i_type_path = '/{}/{}'.format(project_name, i_name)
            self._scr_stage.create_type(
                i_type_path, gui_name=i_gui_name, gui_name_chs=i_gui_name_chs
            )

    def register_character_assets(self, project_name):
        project = self._scan_root.project(project_name)
        assets = project.find_assets(dict(role=qsm_gnl_core.QsmAsset.get_character_role_mask()))
        with bsc_log.LogProcessContext.create(maximum=len(assets)) as l_p:
            for i_asset in assets:
                i_task = i_asset.task(self._scan_root.EntityTasks.Rig)
                if i_task is not None:
                    i_maya_scene_path = i_task.find_result(
                        self._scan_root.FilePatterns.MayaRigFile
                    )
                    if i_maya_scene_path is not None:
                        i_asset_path = i_asset.path
                        i_type_path = '/{}/character'.format(project_name)
                        self.register_asset(i_asset_path, i_type_path, i_maya_scene_path, 'rig')

                l_p.do_update()

    def register_prop_assets(self, project_name):
        project = self._scan_root.project(project_name)
        assets = project.find_assets(dict(role=qsm_gnl_core.QsmAsset.get_prop_role_mask()))
        with bsc_log.LogProcessContext.create(maximum=len(assets)) as l_p:
            for i_asset in assets:
                i_task = i_asset.task(self._scan_root.EntityTasks.Rig)
                if i_task is not None:
                    i_maya_scene_path = i_task.find_result(
                        self._scan_root.FilePatterns.MayaRigFile
                    )
                    if i_maya_scene_path is not None:
                        i_asset_path = i_asset.path
                        i_type_path = '/{}/prop'.format(project_name)
                        self.register_asset(i_asset_path, i_type_path, i_maya_scene_path, 'rig')

                l_p.do_update()

    def register_scenery_assets(self, project_name):
        project = self._scan_root.project(project_name)
        assets = project.find_assets(dict(role=qsm_gnl_core.QsmAsset.get_scenery_role_mask()))
        with bsc_log.LogProcessContext.create(maximum=len(assets)) as l_p:
            for i_asset in assets:
                i_task = i_asset.task(self._scan_root.EntityTasks.Model)
                if i_task is not None:
                    i_maya_scene_path = i_task.find_result(
                        self._scan_root.FilePatterns.MayaModelFIle
                    )
                    if i_maya_scene_path is not None:
                        i_asset_path = i_asset.path
                        i_type_path = '/{}/scenery'.format(project_name)
                        self.register_asset(i_asset_path, i_type_path, i_maya_scene_path, 'model')

                l_p.do_update()


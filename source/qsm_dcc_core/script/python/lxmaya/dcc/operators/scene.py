# coding:utf-8
import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.dcc.abstracts as bsc_dcc_abstracts
# maya
from ... import core as mya_core


# noinspection PyUnusedLocal
class SceneOpt(bsc_dcc_abstracts.AbsSceneOpt):
    def __init__(self, *args, **kwargs):
        """
        stage is universe
        :param args:
        :param kwargs:
        """
        self._stage = args[0]

    @property
    def stage(self):
        return self._stage

    def get_mesh_data_content(self, directory_path, file_path):
        from ..objects import node_for_geometry as mya_dcc_obj_node_for_geometry

        from . import node_for_geometry as mya_dcc_opt_node_for_geometry

        if file_path:
            yml_file_path = bsc_storage.StgTmpYamlMtd.get_file_path(file_path, 'mesh-comparer')
            yml_file = bsc_storage.StgFileOpt(yml_file_path)
            if yml_file.get_is_exists() is False:
                content_0 = ctt_core.Content(value={})
                content_0.set('file', file_path)
                dcc_objs = self._stage.get_objs()
                if dcc_objs:
                    with bsc_log.LogProcessContext.create(maximum=len(dcc_objs), label='build comparer-data') as g_p:
                        for i_dcc_obj in dcc_objs:
                            g_p.do_update()
                            obj_type_name = i_dcc_obj.type.name
                            if obj_type_name == 'mesh':
                                dcc_path = i_dcc_obj.path
                                dcc_obj_name = i_dcc_obj.name
                                #
                                dcc_path_dag_opt = bsc_core.PthNodeOpt(dcc_path)
                                mya_path_dag_opt = dcc_path_dag_opt.translate_to(mya_core.MyaUtil.OBJ_PATHSEP)
                                mya_obj_path = mya_path_dag_opt.path
                                mya_mesh = mya_dcc_obj_node_for_geometry.Mesh(mya_obj_path)
                                mya_mesh_opt = mya_dcc_opt_node_for_geometry.MeshOpt(mya_mesh)
                                #
                                content_0.set('name.{}'.format(dcc_obj_name), dcc_path)
                                content_0.set('name.{}'.format(dcc_path), dcc_obj_name)
                                #
                                face_vertices_uuid = mya_mesh_opt.get_face_vertices_as_uuid()
                                content_0.set('face_vertices_uuids.{}'.format(face_vertices_uuid), dcc_path)
                                content_0.set('face_vertices_uuids.{}'.format(dcc_path), face_vertices_uuid)
                                #
                                points_uuid = mya_mesh_opt.get_points_as_uuid()
                                content_0.set('points_uuids.{}'.format(points_uuid), dcc_path)
                                content_0.set('points_uuids.{}'.format(dcc_path), points_uuid)
                #
                return content_0
            return ctt_core.Content(value=yml_file_path)
        return ctt_core.Content(value={})

    def get_mesh_comparer_data(self, file_path):
        if file_path:
            yml_file_path = bsc_storage.StgTmpYamlMtd.get_file_path(file_path, 'mesh-comparer')
            return self._get_mesh_data_content_(self._stage, file_path, yml_file_path)
        return ctt_core.Content(value={})

    @classmethod
    def _get_mesh_data_content_(cls, stage, file_path, yml_file_path):
        from ..objects import node_for_geometry as mya_dcc_obj_node_for_geometry

        from . import node_for_geometry as mya_dcc_opt_node_for_geometry

        yml_file = bsc_storage.StgFileOpt(yml_file_path)
        if yml_file.get_is_exists() is True:
            return ctt_core.Content(value=yml_file_path)

        content_0 = ctt_core.Content(value={})
        dcc_objs = stage.get_objs()
        if dcc_objs:
            with bsc_log.LogProcessContext.create(maximum=len(dcc_objs), label='gain build comparer-data') as g_p:
                for i_dcc_obj in dcc_objs:
                    g_p.do_update()
                    obj_type_name = i_dcc_obj.type.name
                    if obj_type_name == 'mesh':
                        dcc_path = i_dcc_obj.path
                        #
                        dcc_path_dag_opt = bsc_core.PthNodeOpt(dcc_path)
                        mya_path_dag_opt = dcc_path_dag_opt.translate_to(mya_core.MyaUtil.OBJ_PATHSEP)
                        mya_obj_path = mya_path_dag_opt.path
                        mya_mesh = mya_dcc_obj_node_for_geometry.Mesh(mya_obj_path)
                        mya_mesh_opt = mya_dcc_opt_node_for_geometry.MeshOpt(mya_mesh)
                        #
                        dcc_obj_name = i_dcc_obj.name
                        face_vertices_uuid = mya_mesh_opt.get_face_vertices_as_uuid()
                        points_uuid = mya_mesh_opt.get_points_as_uuid()
                        cls._build_mesh_comparer_data(
                            content_0,
                            dcc_path,
                            dcc_obj_name, face_vertices_uuid, points_uuid
                        )

        return content_0

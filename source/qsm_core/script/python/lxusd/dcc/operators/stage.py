# coding:utf-8
import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import lxbasic.dcc.abstracts as bsc_dcc_abstracts

import lxbasic.dcc.objects as bsc_dcc_objects
# usd dcc
from . import geometry as usd_dcc_opt_geometry


class SceneOpt(bsc_dcc_abstracts.AbsSceneOpt):
    def __init__(self, stage, namespace=None):
        self._stage = stage
        if namespace is not None:
            self._namespace = namespace
        else:
            self._namespace = 'usd'

    @property
    def stage(self):
        return self._stage

    def get_mesh_comparer_data(self, file_path):
        if file_path:
            yml_file_path = bsc_storage.StgTmpYamlMtd.get_file_path(
                file_path, 'mesh-comparer-{}'.format(self._namespace)
            )
            return self._get_mesh_data_content_(self._stage, file_path, yml_file_path)
        return ctt_core.Content(value={})

    @classmethod
    def _get_mesh_data_content_(cls, stage, file_path, yml_file_path):
        yml_file = bsc_dcc_objects.StgYaml(yml_file_path)
        if yml_file.get_is_exists() is True:
            if yml_file.set_read():
                bsc_log.Log.trace_method_result(
                    'geometry-comparer data read',
                    'cache="{}", source="{}"'.format(yml_file_path, file_path)
                )
                return ctt_core.Content(value=yml_file_path)
        #
        content_0 = ctt_core.Content(value={})
        c = len([i for i in stage.TraverseAll()])
        if c:
            with bsc_log.LogProcessContext.create(maximum=c, label='gain geometry-comparer data') as g_p:
                for i_prim in stage.TraverseAll():
                    g_p.do_update()
                    i_obj_type_name = i_prim.GetTypeName()
                    if i_obj_type_name == 'Mesh':
                        i_mesh_obj_opt = usd_dcc_opt_geometry.MeshOpt(i_prim)
                        i_dcc_obj_path = i_prim.GetPath().pathString
                        #
                        i_dcc_obj_name = i_prim.GetName()
                        i_face_vertices_uuid = i_mesh_obj_opt.get_face_vertices_as_uuid()
                        i_points_uuid = i_mesh_obj_opt.get_points_as_uuid()
                        cls._build_mesh_comparer_data(
                            content_0,
                            i_dcc_obj_path,
                            i_dcc_obj_name, i_face_vertices_uuid, i_points_uuid
                        )
        #
        if content_0.value:
            bsc_log.Log.trace_method_result(
                'geometry comparer-data write',
                'cache="{}", source="{}"'.format(yml_file_path, file_path)
            )
            yml_file.set_write(content_0.value)
        else:
            bsc_log.Log.trace_method_warning(
                'geometry comparer-data resolver',
                'file="{}" geometry is not found'.format(file_path)
            )

        #
        return content_0

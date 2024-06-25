# coding:utf-8
import os.path

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from ... import core as _maya_core

from ...general import core as _gnl_core

from ...resource import core as _rsc_core


class NClothCacheOpt(_rsc_core.ResourceScriptOpt):
    CACHE_ROOT = _gnl_core.ResourceCaches.CfxClothRoot
    CACHE_NAME = _gnl_core.ResourceCaches.CfxClothName

    def __init__(self, *args, **kwargs):
        super(NClothCacheOpt, self).__init__(*args, **kwargs)

    def create_cache_root_auto(self):
        if cmds.objExists(self.CACHE_ROOT) is False:
            cmds.createNode(
                'dagContainer', name=self.CACHE_ROOT.split('|')[-1], shared=1, skipSelect=1
            )
            cmds.setAttr(self.CACHE_ROOT+'.iconName', 'folder-closed.png', type='string')

    def do_export(
        self, directory_path, frame_range, frame_step, frame_offset,
        with_alembic_cache=True, with_geometry_cache=True
    ):
        clothes, meshes = self._resource.find_all_cloth_export_args()
        if meshes:
            options = dict(
                directory=directory_path,
                namespace=self._namespace
            )

            mcx_path = _gnl_core.FilePatterns.CfxClothMcxFile.format(**options)
            abc_path = _gnl_core.FilePatterns.CfxClothAbcFile.format(**options)
            json_path = _gnl_core.FilePatterns.CfxClothJsonFile.format(**options)

            data = dict(
                scene_file=_maya_core.SceneFile.get_current(),
                scene_fps=_maya_core.Frame.get_fps(),
                user=bsc_core.BscSystem.get_user_name(),
                host=bsc_core.BscSystem.get_host(),
                time=bsc_core.BscSystem.get_time(),

                frame_range=frame_range,
                frame_step=frame_step,
                frame_offset=frame_offset,
            )

            bsc_storage.StgFileOpt(json_path).set_write(data)
            if with_geometry_cache is True:
                _maya_core.GeometryCacheOpt(
                    file_path=mcx_path,
                    location=meshes,
                    frame_range=frame_range,
                    frame_step=frame_step
                ).create_and_assign()

            if with_alembic_cache is True:
                _maya_core.AlembicCacheExport(
                    file_path=abc_path,
                    location=meshes,
                    frame_range=frame_range,
                    frame_step=frame_step
                ).execute()

    def do_import_abc(
        self, abc_path
    ):
        # abc_path = '{}/abc/{}.cloth.abc'.format(directory_path, self._namespace)
        # if os.path.exists(abc_path) is False:
        #     return
        #
        # json_path = '{}/json/{}.cloth.json'.format(directory_path, self._namespace)

        self.create_cache_root_auto()
        cache_location_new = '{}|{}:{}'.format(self.CACHE_ROOT, self._namespace, self.CACHE_NAME)
        cache_location = '|{}:{}'.format(self._namespace, self.CACHE_NAME)
        if cmds.objExists(cache_location) is False and cmds.objExists(cache_location_new) is False:
            cache_location = _maya_core.Container.create_as_default(cache_location)
            nodes = _maya_core.SceneFile.import_file(
                abc_path, self._namespace
            )
            dags = []
            non_dags = []
            for i in nodes:
                if _maya_core.DagNode.check_is_dag(i):
                    dags.append(i)
                else:
                    non_dags.append(i)

            meshes = [x for x in dags if _maya_core.Node.is_mesh(x)]
            geometry_root = self._resource.get_geometry_root()
            if geometry_root is None:
                return

            data = self._resource.pull_geometry_topology_data()
            if not data:
                return

            query_dict = {v: k for k, v in data.items()}
            for i_mesh_path in meshes:
                i_mesh_opt = _maya_core.MeshOpt(i_mesh_path)
                i_uuid = i_mesh_opt.get_face_vertices_as_uuid()
                if i_uuid in query_dict:
                    i_key = query_dict[i_uuid]
                    print i_key
                    i_path_tgt = self._resource.key_to_path(self._namespace, geometry_root, i_key, '|')
                    if i_path_tgt is None:
                        continue

                    i_path_src = _maya_core.Shape.get_transform(i_mesh_path)
                    i_results = _maya_core.BlendShape.create(i_path_src, i_path_tgt)
                    non_dags.extend(i_results)

            dag_roots = _maya_core.DagNode.find_roots(dags)
            _maya_core.Container.add_dag_nodes(cache_location, dag_roots)
            _maya_core.Container.add_nodes(cache_location, non_dags)

            _maya_core.NodeDisplay.set_visible(cache_location, False)
            _maya_core.DagNode.parent_to(cache_location, self.CACHE_ROOT)

        # print nodes





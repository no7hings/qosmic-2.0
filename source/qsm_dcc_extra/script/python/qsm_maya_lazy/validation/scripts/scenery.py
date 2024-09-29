# coding:utf-8
import os

import sys
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.content as bsc_content

import lxbasic.log as bsc_log

import qsm_maya.core as qsm_mya_core

import qsm_general.core as qsm_gnl_core

import qsm_maya_lazy.resource.scripts as qsm_mya_lzy_scr_scripts

from .. import prc as _prc


class SceneryValidationOpt(object):
    def __init__(self, namespace):
        self._namespace = namespace
        self._file_path = qsm_mya_core.ReferenceNamespacesCache().get_file(namespace)

        self._validation_options = qsm_gnl_core.DccValidationOptions('lazy-validation/option/scenery')

        self._result_content = bsc_content.Dict()

        self._kwargs = dict(
            namespace=self._namespace,
            result_content=self._result_content,
            validation_options=self._validation_options
        )

    def execute(self, cache_file_path=None):
        process_options = self._validation_options.generate_process_options()
        with bsc_log.LogProcessContext.create(maximum=len(process_options)) as l_p:
            for i_branch, i_leafs in process_options.items():
                if i_branch == 'mesh':
                    self.meshes_prc(i_branch, i_leafs)

                l_p.do_update()

        results = self._result_content.value
        data = dict(
            file=self._file_path,
            results=results
        )
        if cache_file_path is not None:
            bsc_storage.StgFileOpt(cache_file_path).set_write(data)

        # sys.stdout.write(
        #     bsc_core.auto_unicode(
        #         self._validation_options.to_html(data)
        #     )
        # )

    def meshes_prc(self, branch, leafs):
        if 'triangle' in leafs:
            i_prc = _prc.MeshTriangle(
                **self._kwargs
            )
            if i_prc.BRANCH != branch:
                raise RuntimeError()

            i_prc.execute()


class SceneryValidationProcess(object):
    def __init__(self, file_path, validation_cache_path, mesh_count_cache_path, process_options):
        self._file_path = file_path
        self._validation_cache_path = validation_cache_path
        self._mesh_count_cache_path = mesh_count_cache_path
        self._process_options = process_options
        self._namespace = 'scenery_validation'

    def execute(self):
        with bsc_log.LogProcessContext.create(maximum=5) as l_p:
            # step 1
            qsm_mya_core.SceneFile.new()
            l_p.do_update()
            # step 2
            if os.path.isfile(self._file_path) is False:
                raise RuntimeError()
            qsm_mya_core.SceneFile.reference_file(
                self._file_path, namespace=self._namespace
            )
            l_p.do_update()
            # step 3
            qsm_mya_lzy_scr_scripts.ProcessUtils.find_all_gpu_caches_and_textures_from(self._file_path)
            l_p.do_update()
            # step 4
            if bsc_storage.StgPath.get_is_file(self._mesh_count_cache_path) is False:
                bsc_storage.StgFileOpt(self._mesh_count_cache_path).set_write(
                    qsm_mya_lzy_scr_scripts.AssetMeshCountGenerate(self._namespace).generate()
                )
            l_p.do_update()
            # step 5
            if bsc_storage.StgPath.get_is_file(self._validation_cache_path) is False:
                SceneryValidationOpt(self._namespace).execute(self._validation_cache_path)
            l_p.do_update()

# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log

import qsm_maya.core as qsm_mya_core

from . import asset_general as _asset_general


class AssetSnapshotProcess(object):
    def __init__(self, file_path, image_path):
        self._file_path = file_path
        self._image_path = image_path
        self._namespace = 'SNAPSHOT'

    def execute(self):
        with bsc_log.LogProcessContext.create(maximum=4) as l_p:
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
            _asset_general.ProcessUtils.find_all_gpu_caches_and_textures_from(self._file_path)
            l_p.do_update()
            # step 4
            locations = qsm_mya_core.Namespace.find_roots(self._namespace)
            qsm_mya_core.Snapshot.create(
                locations, self._image_path
            )
            l_p.do_update()

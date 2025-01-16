# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.general.scripts as qsm_mya_hdl_gnl_scripts

from ..core.base import util as _cor_bsc_util

from ..core.transfer import resource as _cor_tsf_resource

from ..core.transfer import handle as _cor_trf_handle

from . import build as _build


class MoCapFbxMotionGenerateProcess(object):
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def execute(self):
        fbx_path = self._kwargs.get('fbx_path')
        motion_json_path = self._kwargs.get('motion_json_path')
        preview_mov_path = self._kwargs.get('preview_mov_path')
        image_sequence_dir_path = self._kwargs.get('image_sequence_dir_path')
        if not fbx_path:
            raise RuntimeError()

        if bsc_storage.StgPath.get_is_file(fbx_path) is False:
            raise RuntimeError()

        with bsc_log.LogProcessContext.create(maximum=4) as l_p:

            # 1. import fbx
            qsm_mya_core.SceneFile.new()
            qsm_mya_core.SceneFile.import_fbx(fbx_path, namespace='mocap')
            # mark fps
            fps_tag = qsm_mya_core.Frame.get_fps_tag()
            # mark fbx flag, check is mixamo
            namespaces = _cor_tsf_resource.TransferResource.find_mocap_namespaces()
            if namespaces:
                mocap_namespace = namespaces[0]
            else:
                raise RuntimeError(
                    'no valid namespace is found.'
                )
            l_p.do_update()

            # 2. create sketch and export motion json
            transfer_handle = _cor_trf_handle.MocapTransferHandle(mocap_namespace)
            transfer_handle.setup()
            transfer_handle.connect_to_mocap()
            transfer_handle.export_mocap_to(motion_json_path)
            l_p.do_update()

            # 3. import motion for create preview
            qsm_mya_core.SceneFile.new()
            # load fps
            qsm_mya_core.Frame.set_fps_tag(fps_tag)
            preview_rig_namespace = 'preview'
            scp = _build.MtgBuildScp(preview_rig_namespace)
            scp.setup_for_mocap()
            _build.MtgBuildScp.import_motion_json(preview_rig_namespace, motion_json_path)
            l_p.do_update()

            # 4. create preview
            camera_shape_name = _cor_bsc_util.MtgRigNamespace.to_persp_camera_shape_name(preview_rig_namespace)
            qsm_mya_hdl_gnl_scripts.PlayblastOpt.execute(
                preview_mov_path,
                camera=camera_shape_name,
                resolution=(512, 512),
                image_sequence_dir_path=image_sequence_dir_path
            )
            l_p.do_update()


class MoCapFbxMotionGenerateAutoProcess(object):
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def execute(self):
        fbx_path = self._kwargs.get('fbx_path')
        motion_json_path = self._kwargs.get('motion_json_path')
        if not fbx_path:
            raise RuntimeError()

        if bsc_storage.StgPath.get_is_file(fbx_path) is False:
            raise RuntimeError()

        with bsc_log.LogProcessContext.create(maximum=2) as l_p:

            # 1. import fbx
            qsm_mya_core.SceneFile.new()
            qsm_mya_core.SceneFile.import_fbx(fbx_path, namespace='mocap')

            # mark fbx flag, check is mixamo
            namespaces = _cor_tsf_resource.TransferResource.find_mocap_namespaces()
            if namespaces:
                mocap_namespace = namespaces[0]
            else:
                raise RuntimeError(
                    'no valid namespace is found.'
                )
            l_p.do_update()

            # 2. create sketch and export motion json
            transfer_handle = _cor_trf_handle.MocapTransferHandle(mocap_namespace)
            transfer_handle.setup()
            transfer_handle.connect_to_mocap()
            transfer_handle.export_mocap_to(motion_json_path)
            l_p.do_update()

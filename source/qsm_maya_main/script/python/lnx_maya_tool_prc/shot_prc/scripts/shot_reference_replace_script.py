# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

import qsm_maya.adv as qsm_mya_adv

import qsm_maya.motion as qsm_mya_motion

import qsm_maya.handles.general.scripts as qsm_mya_hdl_gnl_scripts

import lnx_maya_montage.scripts as qsm_mya_lzy_mtg_scripts


class ShotReferenceReplace(object):
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    @classmethod
    def find_valid_camera(cls):
        cameras = qsm_mya_core.Cameras.get_non_defaults()
        if cameras:
            for i in cameras:
                if i.startswith('CAM_'):
                    return i
            return cameras[0]

    def execute(self):
        file_path = self._kwargs.get('file_path')
        cache_path = self._kwargs.get('cache_path')

        if not file_path:
            raise RuntimeError()

        reference_replace_map = self._kwargs.get('reference_replace_map')
        if not reference_replace_map:
            raise RuntimeError()

        directory_path = bsc_storage.StgFileOpt(cache_path).directory_path

        with bsc_log.LogProcessContext.create(maximum=4) as l_p:

            # 1. open file
            qsm_mya_core.SceneFile.new()
            qsm_mya_core.SceneFile.open(file_path)
            l_p.do_update()

            # 2. replace reference
            camera = self.find_valid_camera()
            if not camera:
                raise RuntimeError()

            references = qsm_mya_core.References.get_all_loaded()
            if not references:
                raise RuntimeError()

            for i in references:
                i_file_path = qsm_mya_core.Reference.get_file(i)
                if i_file_path in reference_replace_map:
                    i_file_path_tgt = reference_replace_map[i_file_path]
                    if i_file_path == i_file_path_tgt:
                        continue

                    i_namespace = qsm_mya_core.Reference.get_namespace(i)

                    i_json_path = '{}/{}.jsz'.format(
                        directory_path, i_namespace.replace(':', '__')
                    )
                    if bsc_storage.StgPath.get_is_file(i_json_path) is False:
                        qsm_mya_lzy_mtg_scripts.AdvChrMotionExportOpt(i_namespace).execute(
                            i_json_path, frame_range=qsm_mya_core.Frame.get_frame_range()
                        )

                    qsm_mya_core.Reference.unload(i)
                    qsm_mya_core.Reference.hide_foster_parent(i)

                    i_namespace_tgt = qsm_mya_core.SceneFile.reference_file(
                        i_file_path_tgt, namespace=bsc_storage.StgFileOpt(i_file_path_tgt).name_base
                    )

                    start_frame, end_frame = qsm_mya_core.Frame.get_frame_range()
                    qsm_mya_lzy_mtg_scripts.AdvChrMotionImportOpt(i_namespace_tgt).execute(
                        i_json_path, start_frame=start_frame
                    )

                    qsm_mya_core.Frame.to_start()

                    i_adv_opt_tgt = qsm_mya_adv.AdvChrOpt(i_namespace_tgt)
                    i_adv_opt_tgt.move_main_control_to_toe()
            l_p.do_update()

            # 3. create preview
            video_path = '{}/{}.mov'.format(directory_path, bsc_storage.StgFileOpt(file_path).name_base)
            qsm_mya_hdl_gnl_scripts.PlayblastOpt.execute(
                video_path,
                camera=camera,
                # use render
                resolution=qsm_mya_core.RenderSettings.get_resolution(),
                # ignore light and shadow
                texture_enable=True, light_enable=False, shadow_enable=False
            )
            l_p.do_update()

            # 4. save file
            qsm_mya_core.SceneFile.save_to(cache_path)
            l_p.do_update()

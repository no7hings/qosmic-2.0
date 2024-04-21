# coding:utf-8

def export_camera_usd(camera_usd_file_path, frame_range, samples=[0], camera_root="camera_grp"):
    # noinspection PyUnresolvedReferences
    import paper_maya.toolset.utl.cache_exporters.usd_exporter as pusd
    exporter = pusd.UsdExporter()
    exporter.enable_animation(frame_range, samples)
    exporter.do_export(camera_root, camera_usd_file_path)


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxresolver.core as rsv_core

    import qsm_hook_maya.rsv.objects as mya_rsv_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFileMtd.get_is_exists(any_scene_file_path) is True:
            mya_dcc_objects.Scene.open_file(any_scene_file_path)
            #
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                with_camera_main_abc = hook_option_opt.get('with_camera_main_abc') or False
                if with_camera_main_abc is True:
                    a = mya_rsv_objects.RsvDccCameraHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    )
                    a.do_export_asset_camera_abc()

                    camera_usd_rsv_unit = a._rsv_task.get_rsv_unit(keyword='asset-camera-main-usd-file')
                    camera_usd_file_path = camera_usd_rsv_unit.get_result(version=rsv_scene_properties.get('version'))

                    frame_range = hook_option_opt.get_as_array('camera_main_frame_range')
                    export_camera_usd(
                        camera_usd_file_path,
                        frame_range=[int(f) for f in frame_range],
                        camera_root=rsv_scene_properties.get('dcc.camera_root')
                    )
                #
                create_camera_persp_abc = hook_option_opt.get('create_camera_persp_abc') or False
                if create_camera_persp_abc is True:
                    pass
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

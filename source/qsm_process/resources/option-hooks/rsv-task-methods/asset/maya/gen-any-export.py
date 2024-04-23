# coding:utf-8


def export_camera_usd(camera_usd_file_path, frame_range, samples=[0], camera_root="camera_grp"):
    # noinspection PyUnresolvedReferences
    import paper_maya.toolset.utl.cache_exporters.usd_exporter as pusd
    exporter = pusd.UsdExporter()
    exporter.enable_animation(frame_range, samples)
    exporter.do_export(camera_root, camera_usd_file_path)


def main(session):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxresolver.core as rsv_core

    import qsm_prc_maya.rsv.objects as mya_rsv_objects
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    cmds.stackTrace(state=1)

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFileOpt(any_scene_file_path).get_is_exists() is True:
            mya_dcc_objects.Scene.open_file(any_scene_file_path)
            #
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                if hook_option_opt.get_as_boolean('with_render_texture') is True:
                    mya_rsv_objects.RsvDccTextureHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    ).do_export_asset_render_texture()
                elif hook_option_opt.get_as_boolean('with_preview_texture') is True:
                    mya_rsv_objects.RsvDccTextureHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    ).execute_preview_texture_export()
                #
                if hook_option_opt.get_as_boolean('with_scene') is True:
                    mya_rsv_objects.RsvDccSceneHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).do_export_asset_scene()
                #
                if hook_option_opt.get_as_boolean('with_look_yml') is True:
                    mya_rsv_objects.RsvDccLookHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    ).execute_asset_look_yml_export()
                #
                if hook_option_opt.get_as_boolean('with_camera_abc') is True:
                    mya_rsv_objects.RsvDccCameraHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).do_export_asset_camera_abc()
                #
                if hook_option_opt.get_as_boolean('with_camera_usd') is True:
                    a = mya_rsv_objects.RsvDccCameraHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    )
                    camera_usd_rsv_unit = a._rsv_task.get_rsv_unit(keyword='asset-camera-main-usd-file')
                    camera_usd_file_path = camera_usd_rsv_unit.get_result(version=rsv_scene_properties.get('version'))

                    frame_range = hook_option_opt.get_as_array('camera_main_frame_range') or [1, 1]
                    export_camera_usd(
                        camera_usd_file_path,
                        frame_range=[int(f) for f in frame_range],
                        camera_root=rsv_scene_properties.get('dcc.camera_root')
                    )
            else:
                raise RuntimeError(
                    bsc_log.Log.trace_method_error(
                        session.name,
                        'file: "{}" is not available'.format(any_scene_file_path)
                    )
                )
        else:
            bsc_log.Log.trace_method_warning(
                session.name,
                'file: "{}" is non-exists'.format(any_scene_file_path)
            )
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

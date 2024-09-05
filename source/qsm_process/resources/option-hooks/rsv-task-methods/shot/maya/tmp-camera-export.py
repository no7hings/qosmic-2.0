# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxresolver.core as rsv_core

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFileMtd.get_is_exists(any_scene_file_path) is True:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                rsv_task = resolver.get_rsv_task_by_any_file_path(any_scene_file_path)
                workspace = rsv_scene_properties.get('workspace')
                version = rsv_scene_properties.get('version')
                if workspace == rsv_scene_properties.get('workspaces.release'):
                    keyword_0 = '{branch}-maya-scene-file'
                elif workspace == rsv_scene_properties.get('workspaces.temporary'):
                    keyword_0 = '{branch}-temporary-maya-scene-file'
                else:
                    raise TypeError()
                #
                cache_frames = hook_option_opt.get('cache_frames')
                frame_range = bsc_core.BscTextOpt(cache_frames).to_frame_range()
                #
                keyword_0 = keyword_0.format(**rsv_scene_properties.value)
                maya_scene_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
                maya_scene_file_path = maya_scene_file_rsv_unit.get_result(version=version)
                if bsc_storage.StgPathOpt(maya_scene_file_path).get_is_exists() is True:
                    mya_dcc_objects.Scene.open_file(maya_scene_file_path)
                    # usd
                    with_camera_usd = hook_option_opt.get('with_camera_usd') or False
                    if with_camera_usd is True:
                        set_camera_usd_export(rsv_task, rsv_scene_properties, frame_range)
                    # camera abc
                    with_camera_abc = hook_option_opt.get('with_camera_abc') or False
                    if with_camera_abc is True:
                        set_camera_abc_export(rsv_task, rsv_scene_properties, frame_range)
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def set_camera_usd_export(rsv_task, rsv_scene_properties, frame_range):
    import lxbasic.log as bsc_log

    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == rsv_scene_properties.get('workspaces.release'):
        keyword_0 = '{branch}-release-version-dir'
    elif workspace == rsv_scene_properties.get('workspaces.temporary'):
        keyword_0 = '{branch}-temporary-version-dir'
    else:
        raise TypeError()
    #
    keyword_0 = keyword_0.format(**rsv_scene_properties.value)
    version_directory_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_0
    )
    version_directory_path = version_directory_rsv_unit.get_result(version=version)
    # noinspection PyUnresolvedReferences
    from papyUsd.maya import MayaUsdTaskExport
    #
    bsc_log.Log.trace_method_result(
        'usd export', 'frame-range="{}-{}"'.format(*frame_range)
    )
    #
    MayaUsdTaskExport.MayaUsdTaskExport(
        version_directory_path,
        None,
        frame_range
    ).camera()


def set_camera_abc_export(rsv_task, rsv_scene_properties, frame_range):
    pass


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

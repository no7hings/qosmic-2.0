# coding:utf-8


def main(session):
    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxresolver.core as rsv_core

    import lxmaya.core as mya_core

    mya_core.MyaUtil.set_stack_trace_enable(True)

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFileMtd.get_is_exists(any_scene_file_path) is True:
            mya_dcc_objects.Scene.open_file(any_scene_file_path)
            #
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                rsv_task = resolver.get_rsv_task_by_any_file_path(any_scene_file_path)
                # scene
                with_scene = hook_option_opt.get('with_scene') or False
                if with_scene is True:
                    do_export_asset_scene(rsv_task, rsv_scene_properties)
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def do_export_asset_scene(rsv_task, rsv_scene_properties):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxgeneral.dcc.objects as gnl_dcc_objects

    import lxmaya.dcc.objects as mya_dcc_objects
    #
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == rsv_scene_properties.get('workspaces.release'):
        keyword_0 = '{branch}-maya-scene-file'
    elif workspace == rsv_scene_properties.get('workspaces.temporary'):
        keyword_0 = '{branch}-temporary-maya-scene-file'
    else:
        raise TypeError()
    #
    keyword_0 = keyword_0.format(**rsv_scene_properties.value)
    #
    maya_scene_file_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_0
    )
    maya_scene_file_path = maya_scene_file_rsv_unit.get_result(version=version)

    test_directory_path = '/l/temp/shanshui/pg_repo/zero_test/ani_temp_tool/anim_farm'
    test_directory = gnl_dcc_objects.StgDirectory(test_directory_path)
    if test_directory.get_is_exists() is True:
        bsc_core.BscEnviron.set_python_add(
            test_directory_path
        )
        py_module = bsc_core.PyModule('do_save_ani_maya_file_0')
        if py_module.get_is_exists():
            # noinspection PyUnresolvedReferences
            import do_save_ani_maya_file_0
            #
            do_save_ani_maya_file_0.save_pub_maya_cmd(maya_scene_file_path)
            #
            mya_dcc_objects.Scene.save_to_file(maya_scene_file_path)
        else:
            raise RuntimeError(
                bsc_log.Log.trace_error(
                    'python-module="{}"'
                )
            )
    else:
        raise RuntimeError(
            bsc_log.Log.trace_error(
                'directory="{}" is non-exists'.format(test_directory_path)
            )
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

# coding:utf-8


def main(session):
    def setup_fnc_():
        import lxbasic.storage as bsc_storage

        import lxgeneral.dcc.core as gnl_dcc_core

        gnl_dcc_core.OcioSetup(
            bsc_storage.StgPathMapper.map_to_current(
                '/l/packages/pg/third_party/ocio/aces/1.2'
            )
        ).set_run()

        import lxarnold.startup as and_startup

        and_startup.MtoaSetup(
            bsc_storage.StgPathMapper.map_to_current(
                '/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019'
            )
        ).set_run()

    def execute_fnc_(directory_path_, output_directory_path_):
        directory = gnl_dcc_objects.StgDirectory(directory_path_)
        if directory.get_is_exists() is True:
            if recursion_enable is True:
                file_paths = directory.get_all_file_paths(ext_includes=ext_includes)
            else:
                file_paths = directory.get_file_paths(ext_includes=ext_includes)
            #
            gnl_dcc_objects.StgDirectory(
                output_directory_path_
            ).set_create()
            #
            with bsc_log.LogProcessContext.create(
                maximum=len(file_paths), label=session.name, use_as_progress_bar=True
            ) as l_p:
                for i_file_path in file_paths:
                    l_p.do_update()
                    if gnl_dcc_objects.StgTexture._get_unit_is_exists_as_tgt_ext_by_src_(
                            i_file_path,
                            target_ext,
                            output_directory_path_
                    ) is False or force_enable is True:
                        i_cmd = gnl_dcc_objects.StgTexture._get_unit_create_cmd_as_ext_tgt_by_src_force_(
                            i_file_path,
                            target_ext,
                            output_directory_path_,
                            width
                        )
                        if i_cmd:
                            bsc_core.TrdCommandPool.do_pool_wait()
                            bsc_core.TrdCommandPool.set_start(i_cmd)
        else:
            raise RuntimeError(
                bsc_log.Log.trace_method_error(
                    '{} run'.format(session.name),
                    'directory="{}" is non-exists'.format(directory_path_)
                )
            )

    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxgeneral.dcc.objects as gnl_dcc_objects

    hook_option_opt = session.option_opt

    setup_fnc_()

    directory_path = hook_option_opt.get('directory')
    output_directory_path = hook_option_opt.get('output_directory')

    directory_paths = hook_option_opt.get_as_array('directories')
    output_directory_paths = hook_option_opt.get_as_array('output_directories')

    recursion_enable = hook_option_opt.get_as_boolean('recursion_enable')
    force_enable = hook_option_opt.get_as_boolean('force_enable')

    ext_includes = hook_option_opt.get_as_array('ext_includes')
    target_ext = hook_option_opt.get('target_ext')
    width = hook_option_opt.get('width')

    if directory_path and output_directory_path:
        execute_fnc_(directory_path, output_directory_path)

    if directory_paths and output_directory_paths:
        for i_index, i_directory_path in enumerate(directory_paths):
            i_output_directory_path = output_directory_paths[i_index]
            execute_fnc_(i_directory_path, i_output_directory_path)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

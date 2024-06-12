# coding:utf-8


def main(session):
    import collections

    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxsession.commands as ssn_commands

    import lxresolver.core as rsv_core

    resolver = rsv_core.RsvBase.generate_root()
    #
    hook_option_opt = session.option_opt
    option_hook_key = hook_option_opt.get('option_hook_key')
    #
    file_path = hook_option_opt.get('file')
    rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(file_path)
    rsv_task = resolver.get_rsv_task_by_any_file_path(file_path)
    #
    katana_render_hook_key = 'rsv-task-methods/asset/render/katana-render'
    rv_movie_convert_hook_key = 'rsv-task-methods/asset/rv/movie-convert'
    #
    variable_keys = [
        'camera',
        'layer',
        'light_pass',
        'look_pass',
        'quality'
    ]
    #
    variable_mapper = {
        'camera': 'cameras',
        'layer': 'layers',
        'light_pass': 'light_passes',
        'look_pass': 'look_passes',
        'quality': 'qualities',
    }
    variants_dic = collections.OrderedDict()
    for i_variable_key in variable_keys:
        variants_dic[i_variable_key] = hook_option_opt.get(
            variable_mapper[i_variable_key], as_array=True
        )
    #
    combinations = bsc_core.RawVariablesMtd.get_all_combinations(
        variants_dic
    )
    with bsc_log.LogProcessContext.create(
        maximum=len(combinations), label='cmb-render-create'
    ) as l_p:
        for i_seq, i_variants in enumerate(combinations):
            l_p.do_update()
            #
            i_option_hook_key = '-'.join(
                i_variants.values()
            )
            i_variable_name = '.'.join(
                i_variants.values()
            )
            i_renderer = 'renderer__{}'.format(
                '__'.join(['{}'.format(v) for k, v in i_variants.items()])
            )
            #
            i_camera = i_variants['camera']
            if i_camera in ['shot']:
                i_render_frames = hook_option_opt.get('render_shot_frames')
                i_render_frame_step = int(hook_option_opt.get('render_shot_frame_step'))
            else:
                i_render_frames = hook_option_opt.get('render_asset_frames')
                i_render_frame_step = int(hook_option_opt.get('render_asset_frame_step'))
            #
            if i_render_frame_step > 1:
                render_frame_range = bsc_core.RawTextOpt(i_render_frames).to_frame_range()
                i_render_frames_ = bsc_core.RawFrameRangeMtd.get(
                    render_frame_range, i_render_frame_step
                )
            else:
                i_render_frames_ = bsc_core.RawTextOpt(i_render_frames).to_frames()
            #
            i_batch_file_path = hook_option_opt.get('batch_file')
            i_file_path = hook_option_opt.get('file')
            i_user = hook_option_opt.get('user')
            i_time_tag = hook_option_opt.get('time_tag')
            #
            i_td_enable = hook_option_opt.get('td_enable') or False
            i_rez_beta = hook_option_opt.get('rez_beta') or False
            #
            i_render_output_directory_path = hook_option_opt.get('render_output_directory')

            i_render_file_path = hook_option_opt.get('render_file')

            i_image_path = '{}/main/{}/beauty.####.exr'.format(
                i_render_output_directory_path, i_variable_name
            )
            i_movie_file_path = '{}/main/{}.mov'.format(
                i_render_output_directory_path, i_variable_name
            )
            i_katana_render_hook_option_opt = bsc_core.ArgDictStringOpt(
                dict(
                    option_hook_key=katana_render_hook_key,
                    #
                    batch_file=i_batch_file_path,
                    # python option
                    file=i_file_path,
                    #
                    user=i_user, time_tag=i_time_tag,
                    #
                    td_enable=i_td_enable, rez_beta=i_rez_beta,
                    #
                    render_file=i_render_file_path,
                    render_output_directory=i_render_output_directory_path,
                    renderer=i_renderer,
                    #
                    render_frames=i_render_frames_,
                    #
                    option_hook_key_extend=[i_option_hook_key],
                    #
                    dependencies=[option_hook_key],
                )
            )
            #
            i_katana_render_session = ssn_commands.execute_option_hook_by_deadline(
                i_katana_render_hook_option_opt.to_string()
            )

            i_katana_render_ddl_job_id = i_katana_render_session.get_ddl_job_id()

            if i_katana_render_ddl_job_id:
                i_rv_movie_convert_hook_option_opt = bsc_core.ArgDictStringOpt(
                    option=dict(
                        option_hook_key=rv_movie_convert_hook_key,
                        #
                        file=i_file_path,
                        #
                        user=i_user, time_tag=i_time_tag,
                        td_enable=i_td_enable, rez_beta=i_rez_beta,
                        #
                        image_file=i_image_path,
                        movie_file=i_movie_file_path,
                        #
                        start_frame=i_render_frames_[0],
                        end_frame=i_render_frames_[-1],
                        #
                        option_hook_key_extend=[i_option_hook_key],
                        #
                        dependencies=[option_hook_key],
                        #
                        dependent_ddl_job_id_extend=[i_katana_render_ddl_job_id]
                    )
                )
                ssn_commands.execute_option_hook_by_deadline(
                    i_rv_movie_convert_hook_option_opt.to_string()
                )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

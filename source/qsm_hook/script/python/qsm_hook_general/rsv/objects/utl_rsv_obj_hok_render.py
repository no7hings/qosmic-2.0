# coding:utf-8
from qsm_hook_general.rsv import utl_rsv_obj_abstract


class RsvDccRenderHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccRenderHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)
    
    def do_create_asset_katana_render(self):
        import collections

        import lxbasic.log as bsc_log
        #
        import lxbasic.core as bsc_core
        #
        import lxsession.commands as ssn_commands
        #
        option_hook_key = self._hook_option_opt.get('option_hook_key')
        #
        katana_render_hook_key = 'rsv-task-methods/asset/render/katana-render'
        movie_convert_hook_key = 'rsv-task-methods/asset/rv/movie-convert'
        image_convert_hook_key = 'rsv-task-methods/oiio/image-convert'
        #
        video_composite_hook_key = 'rsv-task-methods/python/video-composite'
        shotgun_qc_export_hook_key = 'rsv-task-methods/shotgun/gen-shotgun-qc-export'
        #
        batch_file_path = self._hook_option_opt.get('batch_file')
        file_path = self._hook_option_opt.get('file')
        user = self._hook_option_opt.get('user')
        time_tag = self._hook_option_opt.get('time_tag')
        #
        td_enable = self._hook_option_opt.get_as_boolean('td_enable')
        rez_beta = self._hook_option_opt.get_as_boolean('rez_beta')
        #
        render_file_path = self.get_asset_katana_render_file()
        #
        render_output_directory_path = self.get_asset_katana_render_output_directory()
        #
        with_video_convert = self._hook_option_opt.get_as_boolean('with_video_convert')
        with_image_convert = self._hook_option_opt.get_as_boolean('with_image_convert')
        #
        layer_from_geometry_variant = self._hook_option_opt.get_as_boolean('layer_from_geometry_variant')
        layer_variant_mapper = {
            'hi': 'high',
            'shape': 'shape',
        }
        #
        if layer_from_geometry_variant is True:
            geometry_variant_names = self.get_asset_exists_geometry_variant_names()
            layers = [layer_variant_mapper[i] for i in geometry_variant_names]
            bsc_log.Log.trace_method_result(
                'load layer form geometry variant',
                'layers={}'.format(', '.join(map(lambda x: '"{}"'.format(x), layers)))
            )
            self._hook_option_opt.set('layers', layers)
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
            variants_dic[i_variable_key] = self._hook_option_opt.get_as_array(
                variable_mapper[i_variable_key]
            )
        #
        combinations = bsc_core.RawVariablesMtd.get_all_combinations(
            variants_dic
        )
        render_ddl_job_ids = []
        with bsc_log.LogProcessContext.create(maximum=len(combinations), label='cmb-render-create') as l_p:
            for i_seq, i_variants in enumerate(combinations):
                l_p.do_update()
                #
                i_key_extend = '-'.join(
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
                    i_render_frames = self._hook_option_opt.get('render_shot_frames')
                    i_render_frame_step = int(self._hook_option_opt.get_as_integer('render_shot_frame_step'))
                else:
                    i_render_frames = self._hook_option_opt.get('render_asset_frames')
                    i_render_frame_step = int(self._hook_option_opt.get_as_integer('render_asset_frame_step'))
                #
                if i_render_frame_step > 1:
                    render_frame_range = bsc_core.RawTextOpt(i_render_frames).to_frame_range()
                    i_render_frames_ = bsc_core.RawFrameRangeMtd.get(
                        render_frame_range, i_render_frame_step
                    )
                else:
                    i_render_frames_ = bsc_core.RawTextOpt(i_render_frames).to_frames()
                #
                i_katana_render_hook_option_opt = bsc_core.ArgDictStringOpt(
                    dict(
                        option_hook_key=katana_render_hook_key,
                        #
                        batch_file=batch_file_path,
                        # python option
                        file=file_path,
                        #
                        user=user, time_tag=time_tag,
                        #
                        td_enable=td_enable, rez_beta=rez_beta,
                        #
                        render_file=render_file_path,
                        render_output_directory=render_output_directory_path,
                        #
                        renderer=i_renderer,
                        #
                        render_frames=i_render_frames_,
                        #
                        option_hook_key_extend=[i_key_extend],
                        #
                        dependencies=[option_hook_key],
                    )
                )
                #
                i_katana_render_session = ssn_commands.execute_option_hook_by_deadline(
                    i_katana_render_hook_option_opt.to_string()
                )
                #
                i_render_ddl_job_id = i_katana_render_session.get_ddl_job_id()
                if i_render_ddl_job_id:
                    render_ddl_job_ids.append(i_render_ddl_job_id)
                    if with_video_convert is True:
                        i_image_file_path_src = '{}/main/{}/beauty.####.exr'.format(
                            render_output_directory_path, i_variable_name
                        )
                        i_movie_file_path_tgt = '{}/main/{}.mov'.format(
                            render_output_directory_path,
                            i_variable_name
                        )
                        i_movie_convert_hook_option_opt = bsc_core.ArgDictStringOpt(
                            option=dict(
                                option_hook_key=movie_convert_hook_key,
                                #
                                file=file_path,
                                #
                                user=user, time_tag=time_tag,
                                td_enable=td_enable, rez_beta=rez_beta,
                                #
                                image_file=i_image_file_path_src,
                                movie_file=i_movie_file_path_tgt,
                                #
                                start_frame=i_render_frames_[0],
                                end_frame=i_render_frames_[-1],
                                #
                                option_hook_key_extend=[i_key_extend],
                                dependencies=[option_hook_key],
                                dependent_ddl_job_id_extend=[i_render_ddl_job_id],
                            )
                        )
                        ssn_commands.execute_option_hook_by_deadline(
                            i_movie_convert_hook_option_opt.to_string()
                        )
                    #
                    if with_image_convert is True:
                        i_image_file_path_src = '{}/main/{}/beauty.{}.exr'.format(
                            render_output_directory_path,
                            i_variable_name,
                            str(i_render_frames_[0]).zfill(4)
                        )
                        i_image_file_path_tgt = '{}/main/{}.png'.format(
                            render_output_directory_path, i_variable_name
                        )
                        i_movie_convert_hook_option_opt = bsc_core.ArgDictStringOpt(
                            option=dict(
                                option_hook_key=image_convert_hook_key,
                                #
                                file=file_path,
                                #
                                user=user, time_tag=time_tag,
                                td_enable=td_enable, rez_beta=rez_beta,
                                #
                                image_file=i_image_file_path_src,
                                output_image_file=i_image_file_path_tgt,
                                #
                                option_hook_key_extend=[i_key_extend],
                                dependencies=[option_hook_key],
                                dependent_ddl_job_id_extend=[i_render_ddl_job_id],
                            )
                        )
                        ssn_commands.execute_option_hook_by_deadline(
                            i_movie_convert_hook_option_opt.to_string()
                        )
        #
        with_video_composite = self._hook_option_opt.get_as_boolean('with_video_composite')
        if with_video_composite is True:
            layers = self._hook_option_opt.get_as_array('layers')
            render_passes = self._hook_option_opt.get_as_array('render_passes')
            #
            video_composite_hook_option_opt = bsc_core.ArgDictStringOpt(
                option=dict(
                    option_hook_key=video_composite_hook_key,
                    #
                    file=file_path,
                    #
                    user=user, time_tag=time_tag,
                    td_enable=td_enable, rez_beta=rez_beta,
                    #
                    dependencies=[option_hook_key],
                    dependent_ddl_job_id_extend=render_ddl_job_ids,
                    #
                    with_video_mov=True,
                    #
                    composite_use_katana_video_all_mov=True,
                    #
                    layers=layers,
                    render_passes=render_passes
                )
            )
            video_composite_session = ssn_commands.execute_option_hook_by_deadline(
                video_composite_hook_option_opt.to_string()
            )
            video_composite_ddl_job_id = video_composite_session.get_ddl_job_id()
            if video_composite_ddl_job_id:
                with_shotgun_qc_export = self._hook_option_opt.get_as_boolean('with_shotgun_qc_export')
                if with_shotgun_qc_export is True:
                    shotgun_qc_export_hook_option_opt = bsc_core.ArgDictStringOpt(
                        option=dict(
                            option_hook_key=shotgun_qc_export_hook_key,
                            #
                            file=file_path,
                            #
                            user=user, time_tag=time_tag,
                            td_enable=td_enable, rez_beta=rez_beta,
                            #
                            dependencies=[option_hook_key],
                            dependent_ddl_job_id_extend=[video_composite_ddl_job_id],
                            #
                            create_shotgun_qc_task=True,
                            create_shotgun_qc_version=True,
                            #
                            with_qc_review_mov=True,
                            #
                            review_use_katana_video_all_mov=True,
                        )
                    )

                    ssn_commands.execute_option_hook_by_deadline(
                        shotgun_qc_export_hook_option_opt.to_string()
                    )

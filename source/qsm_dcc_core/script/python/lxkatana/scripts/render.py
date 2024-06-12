# coding:utf-8
import copy

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# katana
from .. import core as ktn_core
# katana dcc
from ..dcc import objects as ktn_dcc_objects


class ScpRenderLayer(object):
    VERSION_KEY = 'render_version'

    def __init__(self, obj_opt):
        self._obj_opt = obj_opt

        from . import macro_for_wsp as ktn_scp_macro_for_wsp

        scp = ktn_scp_macro_for_wsp.ScpWspRenderLayer(self._obj_opt._ktn_obj)

        self._variant = scp.get_variants()
        self._variant.pop(self.VERSION_KEY)

    @classmethod
    def _to_render_layer(cls, opt_opt):
        parent_opt = opt_opt.get_parent_opt()
        if parent_opt.get('type') == 'RenderLayer_Wsp':
            return parent_opt

    @classmethod
    def _parse_version(cls, version, pattern_opt, version_key):
        if version == 'new':
            return pattern_opt.get_new_version(version_key=version_key)
        elif version == 'latest':
            return pattern_opt.get_latest_version(version_key=version_key)
        else:
            return version

    def get_render_version(self, default_render_version):
        render_version_mode = self._obj_opt.get('parameters.render.version.mode')
        directory_p = self._obj_opt.get('parameters.render.output.directory')
        directory_p_opt = bsc_core.PtnStgParseOpt(directory_p)
        # check is valid
        if directory_p_opt.get_keys():
            directory_p_opt.update_variants(**self._variant)
            #
            if render_version_mode == 'default':
                version = self._parse_version(default_render_version, directory_p_opt, self.VERSION_KEY)
            elif render_version_mode == 'new':
                version = directory_p_opt.get_new_version(version_key=self.VERSION_KEY)
            elif render_version_mode == 'latest':
                version = directory_p_opt.get_latest_version(version_key=self.VERSION_KEY)
            elif render_version_mode == 'customize':
                version = self._obj_opt.get('parameters.render.version.customize')
            else:
                raise RuntimeError()
            return version
        return default_render_version

    def get_render_output_directory(self, default_render_version):
        directory_p = self._obj_opt.get('parameters.render.output.directory')
        directory_p_opt = bsc_core.PtnStgParseOpt(directory_p)
        # check is valid
        if directory_p_opt.get_keys():
            directory_p_opt.update_variants(**self._variant)
            version_kwargs = {}
            render_version = self.get_render_version(default_render_version)
            version_kwargs[self.VERSION_KEY] = render_version
            directory_p_opt.update_variants(**version_kwargs)
            return directory_p_opt.get_value()
        else:
            return directory_p_opt.get_value()

    def get_latest_render_output_image(self):
        # use primary pass
        directory_p = self._obj_opt.get('parameters.render.output.directory')
        directory_p_opt = bsc_core.PtnStgParseOpt(directory_p)
        # check is valid
        if directory_p_opt.get_keys():
            directory_p_opt.update_variants(**self._variant)
            results = directory_p_opt.get_match_results(sort=True)
            if results:
                directory = results[-1]
                variant = copy.copy(self._variant)
                image_sub_p = self._obj_opt.get('parameters.render.output.builtin.image_pattern')
                image_file_p = bsc_core.PtnStgParseOpt('{}{}'.format(directory, image_sub_p))
                variant.update(dict(aov='primary'))
                image_file_p.update_variants(**variant)
                return image_file_p.get_value()

    def get_render_output_directory_key(self):
        directory_p = self._obj_opt.get('parameters.render.output.directory')
        directory_p_opt = bsc_core.PtnStgParseOpt(directory_p)
        directory_p_opt.update_variants(**self._variant)
        return directory_p_opt.get_value()

    def get_render_frames(self, default_render_frames):
        render_frames_mode = self._obj_opt.get('parameters.render.frames.mode')
        if render_frames_mode == 'default':
            render_frames_string = default_render_frames
        elif render_frames_mode == 'customize':
            render_frames_string = self._obj_opt.get('parameters.render.frames.customize')
        else:
            raise RuntimeError()
        return render_frames_string


class ScpRenderBuild(object):
    KEY = 'render build'

    def __init__(self, session):
        self._session = session
        self._hook_option_opt = self._session.option_opt

    @classmethod
    def _parse_version(cls, version, pattern_opt, version_key):
        if version == 'new':
            return pattern_opt.get_new_version(version_key=version_key)
        elif version == 'latest':
            return pattern_opt.get_latest_version(version_key=version_key)
        else:
            return version

    @ktn_core.Modifier.undo_run
    def refresh_all_render_layers_output(self, default_render_version='new'):
        key = 'render process'

        from . import macro_for_wsp as ktn_scp_macro_for_wsp

        version_key = 'render_version'

        render_layers = ktn_core.NGNodesMtd.filter_nodes(
            filters=[
                ('node_type', 'is', 'Group'),
                ('type', 'in', {'RenderLayer_Wsp', 'RenderLayer_Wsp_Usr'})
            ]
        )
        for i_render_layer in render_layers:
            i_obj_opt = ktn_core.NGNodeOpt(i_render_layer)

            i_scp = ktn_scp_macro_for_wsp.ScpWspRenderLayer(i_render_layer)

            i_kwargs = i_scp.get_variants()
            i_kwargs.pop(version_key)
            i_render_version_mode = i_obj_opt.get('parameters.render.version.mode')
            i_directory_p = i_obj_opt.get('parameters.render.output.directory')
            i_directory_p_opt = bsc_core.PtnStgParseOpt(i_directory_p)
            # check is valid
            if i_directory_p_opt.get_keys():
                i_directory_p_opt.update_variants(**i_kwargs)
                #
                i_version_kwargs = {}
                if i_render_version_mode == 'default':
                    i_version = self._parse_version(default_render_version, i_directory_p_opt, version_key)
                elif i_render_version_mode == 'new':
                    i_version = i_directory_p_opt.get_new_version(version_key=version_key)
                elif i_render_version_mode == 'latest':
                    i_version = i_directory_p_opt.get_latest_version(version_key=version_key)
                elif i_render_version_mode == 'customize':
                    i_version = i_obj_opt.get('parameters.render.version.customize')
                else:
                    raise RuntimeError()
                #
                i_version_kwargs[version_key] = i_version
                i_directory_p_opt.update_variants(**i_version_kwargs)
                # check is valid
                if not i_directory_p_opt.get_keys():
                    i_result = i_directory_p_opt.get_value()
                    #
                    i_obj_opt.set('parameters.render.output.directory', i_result)
                    #
                    bsc_log.Log.trace_method_result(
                        key,
                        'node: "{}"'.format(
                            i_obj_opt.get_path()
                        )
                    )
                    # create directory
                    bsc_storage.StgPermissionMtd.create_directory(
                        i_result
                    )
                else:
                    bsc_log.Log.trace_method_error(
                        key,
                        'node: "{}" is failed'.format(
                            i_obj_opt.get_path()
                        )
                    )
            else:
                bsc_log.Log.trace_method_warning(
                    key,
                    'node: "{}" not any variant for convert, ignore'.format(
                        i_obj_opt.get_path()
                    )
                )

    @classmethod
    def _to_render_layer(cls, opt_opt):
        parent_opt = opt_opt.get_parent_opt()
        if parent_opt.get('type') == 'RenderLayer_Wsp':
            return parent_opt

    def copy_file(self):
        file_path = self._hook_option_opt.get('file')

        render_file_path = bsc_storage.StgFileOpt(
            file_path
        ).get_render_file_path()
        #
        bsc_storage.StgPermissionMtd.copy_to_file(
            file_path,
            render_file_path
        )
        self._hook_option_opt.set(
            'render_file', render_file_path
        )

    def pre_process(self):
        render_file_path = self._hook_option_opt.get('render_file')

        ktn_dcc_objects.Scene.open_file(render_file_path)

        default_render_version = self._hook_option_opt.get('default_render_version')

        self.refresh_all_render_layers_output(
            default_render_version=default_render_version
        )

        ktn_dcc_objects.Scene.save_file()

    def build_render_jobs(self):
        render_file_path = self._hook_option_opt.get('render_file')
        ktn_dcc_objects.Scene.open_file(render_file_path)
        self._build_render_jobs(
            hook_option_opt=self._hook_option_opt
        )

    @classmethod
    def _build_render_jobs(cls, hook_option_opt):
        import lxsession.commands as ssn_commands

        auto_convert_mov = hook_option_opt.get_as_boolean('auto_convert_mov')

        default_render_frames = hook_option_opt.get('default_render_frames')

        render_nodes = hook_option_opt.get_as_array(
            'render_nodes'
        )
        option_hook_key = hook_option_opt.get('option_hook_key')
        batch_name = hook_option_opt.get('batch_name')
        batch_file_path = hook_option_opt.get('batch_file')
        file_path = hook_option_opt.get('file')
        render_file_path = hook_option_opt.get('render_file')
        user = hook_option_opt.get('user')
        time_tag = hook_option_opt.get('time_tag')
        td_enable = hook_option_opt.get('td_enable')
        rez_beta = hook_option_opt.get('rez_beta')
        #
        katana_render_hook_key = 'rsv-project-methods/katana/render'
        rv_video_comp_hook_key = 'rsv-project-methods/rv/video-comp'
        with bsc_log.LogProcessContext.create_as_bar(maximum=len(render_nodes), label=cls.KEY) as l_p:
            for i_render_node in render_nodes:
                l_p.do_update()
                if ktn_core.NGNodeOpt._get_is_exists_(i_render_node) is True:
                    i_render_node_opt = ktn_core.NGNodeOpt(i_render_node)
                    i_render_layer_opt = cls._to_render_layer(i_render_node_opt)
                    if i_render_layer_opt is not None:
                        i_render_frames_mode = i_render_layer_opt.get('parameters.render.frames.mode')
                        if i_render_frames_mode == 'default':
                            i_render_frames_string = default_render_frames
                        elif i_render_frames_mode == 'customize':
                            i_render_frames_string = i_render_layer_opt.get('parameters.render.frames.customize')
                        else:
                            raise RuntimeError()
                    else:
                        i_render_frames_string = default_render_frames
                    #
                    i_render_output_image_path = ktn_core.KtnStageOpt(
                        i_render_node_opt._ktn_obj
                    ).get(
                        '/root.renderSettings.outputs.primary.locationSettings.renderLocation'
                    )
                    if i_render_output_image_path is None:
                        raise RuntimeError(
                            bsc_log.Log.trace_method_error(
                                'aov layer "primary" is not found'
                            )
                        )
                    #
                    i_render_output_directory_path = bsc_storage.StgFileOpt(
                        i_render_output_image_path
                    ).get_directory_path()
                    i_render_output_directory_opt = bsc_storage.StgDirectoryOpt(
                        i_render_output_directory_path
                    )
                    i_render_layer_name = i_render_output_directory_opt.get_name()
                    i_render_layer_name = i_render_layer_name.replace('.', '/')
                    i_video_directory_path = bsc_core.PthNodeOpt(i_render_output_directory_path).get_parent_path()
                    # etc.
                    i_video_file_name = bsc_core.PthNodeOpt(i_render_output_directory_path).get_name()
                    i_vedio_file_path = '{}/{}.mov'.format(i_video_directory_path, i_video_file_name)
                    #
                    i_render_frames = bsc_core.RawTextOpt(i_render_frames_string).to_frames()
                    #
                    i_katana_render_hook_option_opt = bsc_core.ArgDictStringOpt(
                        dict(
                            option_hook_key=katana_render_hook_key,
                            #
                            batch_name=batch_name,
                            #
                            batch_file=batch_file_path,
                            file=file_path,
                            #
                            user=user, time_tag=time_tag,
                            td_enable=td_enable, rez_beta=rez_beta,
                            #
                            katana_version=hook_option_opt.get('katana_version'),
                            render_file=render_file_path,
                            render_output_directory=i_render_output_directory_path,
                            render_node=i_render_node,
                            #
                            render_frames=i_render_frames,
                            #
                            option_hook_key_extend=[i_render_node, 'image'],
                            option_hook_key_over=[i_render_layer_name, 'image'],
                            #
                            dependencies=[option_hook_key],
                        )
                    )
                    i_katana_render_session = ssn_commands.execute_option_hook_by_deadline(
                        i_katana_render_hook_option_opt.to_string()
                    )
                    #
                    if auto_convert_mov is True:
                        i_katana_render_ddl_job_id = i_katana_render_session.get_ddl_job_id()
                        i_rv_movie_convert_hook_option_opt = bsc_core.ArgDictStringOpt(
                            option=dict(
                                option_hook_key=rv_video_comp_hook_key,
                                #
                                batch_name=batch_name,
                                #
                                batch_file=batch_file_path,
                                file=file_path,
                                #
                                user=user, time_tag=time_tag,
                                td_enable=td_enable, rez_beta=rez_beta,
                                #
                                image_file=i_render_output_image_path,
                                video_file=i_vedio_file_path,
                                #
                                render_output_directory=i_render_output_directory_path,
                                #
                                start_frame=i_render_frames[0],
                                end_frame=i_render_frames[-1],
                                #
                                option_hook_key_extend=[i_render_node, 'movie'],
                                option_hook_key_over=[i_render_layer_name, 'movie'],
                                #
                                dependencies=[option_hook_key],
                                #
                                dependent_ddl_job_id_extend=[i_katana_render_ddl_job_id]
                            )
                        )
                        ssn_commands.execute_option_hook_by_deadline(
                            i_rv_movie_convert_hook_option_opt.to_string()
                        )
                else:
                    bsc_log.Log.trace_method_warning(
                        cls.KEY,
                        'render-node: "{}" is non-exists'.format(i_render_node)
                    )

    def execute(self):
        self.copy_file()
        self.pre_process()
        self.build_render_jobs()

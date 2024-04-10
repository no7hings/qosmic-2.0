# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from lxutil.rsv import utl_rsv_obj_abstract


class RsvUtilityOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvUtilityOpt, self).__init__(rsv_scene_properties, hook_option_opt)


class RsvRecyclerHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvRecyclerHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    #
    def set_texture_recycles(self):
        directory_paths_src = self._hook_option_opt.get_as_array('recycles_texture_directories')
        if directory_paths_src:
            keyword = 'asset-source-texture-version-dir'

            variant = 'outsource'
            version = self._rsv_scene_properties.get('version')
            #
            directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
                keyword=keyword
            )
            directory_path_tgt = directory_rsv_unit_tgt.get_result(
                version=version, variants_extend=dict(variant=variant)
            )

            directory_path_src = directory_paths_src[0]

            directory_path_opt_src = bsc_storage.StgDirectoryOpt(directory_path_src)
            directory_path_opt_src.map_to_current()
            if directory_path_opt_src.get_is_exists() is True:
                directory_path_opt_src.copy_to_directory(
                    directory_path_tgt
                )
                bsc_log.Log.trace_method_result(
                    'asset texture recycles',
                    u'directory="{}" >> directory="{}"'.format(
                        directory_path_src, directory_path_tgt
                    )
                )
            else:
                bsc_log.Log.trace_method_warning(
                    'asset texture recycles',
                    u'directory="{}" is non-exists'.format(
                        directory_path_src
                    )
                )

    def set_maya_recycles(self):
        import lxbasic.fnc.objects as bsc_fnc_objects

        import lxmaya.dcc.objects as mya_dcc_objects

        import lxmaya.core as mya_core

        mya_core.MyaUtil.set_stack_trace_enable(True)

        keyword_0 = 'asset-source-maya-scene-src-file'
        file_paths_src = self._hook_option_opt.get_as_array('recycles_maya_files')
        if file_paths_src:
            file_path_src = file_paths_src[0]
            file_path_opt_src = bsc_storage.StgFileOpt(file_path_src)
            file_path_opt_src.map_to_current()
            if file_path_opt_src.get_is_exists() is True:
                version = self._rsv_scene_properties.get('version')

                file_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
                    keyword=keyword_0
                )
                file_path_tgt = file_rsv_unit_tgt.get_result(
                    version=version
                )

                bsc_fnc_objects.FncExporterForDotMa(
                    option=dict(
                        file_path_src=file_path_src,
                        file_path_tgt=file_path_tgt
                    )
                ).execute()

                bsc_log.Log.trace_method_result(
                    'asset maya recycles',
                    u'file="{}" '.format(
                        file_path_tgt
                    )
                )
                # repath texture first
                repath_maya_texture_enable = self._hook_option_opt.get_as_boolean('repath_maya_texture_enable')
                if repath_maya_texture_enable is True:
                    mya_dcc_objects.Scene.open_file(file_path_tgt)
                    self.set_maya_texture_repath()
                    mya_dcc_objects.Scene.save_file()
                # repath xgen last
                repath_maya_xgen_enable = self._hook_option_opt.get_as_boolean('repath_maya_xgen_enable')
                if repath_maya_xgen_enable is True:
                    self.set_maya_xgen_repath()
                #
                convert_maya_to_katana_enable = self._hook_option_opt.get_as_boolean('convert_maya_to_katana_enable')
                if convert_maya_to_katana_enable is True:
                    self.set_maya_ass_export()
            else:
                bsc_log.Log.trace_method_warning(
                    'asset maya recycles',
                    u'file="{}" is non-exists'.format(
                        file_path_src
                    )
                )

    def set_xgen_recycles(self):
        import lxmaya.core as mya_core

        mya_core.MyaUtil.set_stack_trace_enable(True)

        variant = 'outsource'
        version = self._rsv_scene_properties.get('version')

        keyword = 'asset-source-maya-xgen-cache-dir'

        directory_paths_src = self._hook_option_opt.get_as_array('recycles_xgen_cache_directories')
        if directory_paths_src:
            directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
                keyword=keyword
            )
            directory_path_tgt = directory_rsv_unit_tgt.get_result(
                version=version, variants_extend=dict(variant=variant)
            )
            #
            directory_path_src = directory_paths_src[0]
            directory_path_opt_src = bsc_storage.StgDirectoryOpt(directory_path_src)
            directory_path_opt_src.map_to_current()
            if directory_path_opt_src.get_is_exists() is True:
                directory_path_opt_src.copy_to_directory(
                    directory_path_tgt
                )
                bsc_log.Log.trace_method_result(
                    'asset xgen cache recycles',
                    u'directory="{}" >> directory="{}"'.format(
                        directory_path_src, directory_path_tgt
                    )
                )
            else:
                bsc_log.Log.trace_method_warning(
                    'asset xgen cache recycles',
                    u'directory="{}" is non-exists'.format(
                        directory_path_src
                    )
                )

    def set_sp_recycles(self):
        keyword = 'asset-source-sp-scene-src-dir'
        file_paths_src = self._hook_option_opt.get_as_array('recycles_sp_files')
        if file_paths_src:
            variant = 'outsource'
            version = self._rsv_scene_properties.get('version')

            directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
                keyword=keyword
            )
            directory_path_tgt = directory_rsv_unit_tgt.get_result(
                version=version, variants_extend=dict(variant=variant)
            )
            for i_file_path_src in file_paths_src:
                i_file_path_opt_src = bsc_storage.StgFileOpt(i_file_path_src)
                i_file_path_opt_src.map_to_current()
                if i_file_path_opt_src.get_is_exists() is True:
                    i_file_path_opt_src.copy_to_directory(
                        directory_path_tgt
                    )
                    bsc_log.Log.trace_method_result(
                        'asset sp recycles',
                        u'file="{}" >> directory="{}"'.format(
                            i_file_path_opt_src, directory_path_tgt
                        )
                    )
                else:
                    bsc_log.Log.trace_method_warning(
                        'asset sp recycles',
                        u'file="{}" is non-exists'.format(
                            i_file_path_src
                        )
                    )

    def set_zb_recycles(self):
        keyword = 'asset-source-zbrush-scene-src-dir'
        file_paths_src = self._hook_option_opt.get_as_array('recycles_zb_files')
        if file_paths_src:
            variant = 'outsource'
            version = self._rsv_scene_properties.get('version')

            directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
                keyword=keyword
            )
            directory_path_tgt = directory_rsv_unit_tgt.get_result(
                version=version, variants_extend=dict(variant=variant)
            )
            for i_file_path_src in file_paths_src:
                i_file_path_opt_src = bsc_storage.StgFileOpt(i_file_path_src)
                # map path to current platform first
                i_file_path_opt_src.map_to_current()
                if i_file_path_opt_src.get_is_exists() is True:
                    i_file_path_opt_src.copy_to_directory(
                        directory_path_tgt
                    )
                    bsc_log.Log.trace_method_result(
                        'asset zb recycles',
                        u'file="{}" >> directory="{}"'.format(
                            i_file_path_opt_src, directory_path_tgt
                        )
                    )
                else:
                    bsc_log.Log.trace_method_warning(
                        'asset zb recycles',
                        u'file="{}" is non-exists'.format(
                            i_file_path_src
                        )
                    )

    # maya
    def set_maya_xgen_repath(self):
        import lxbasic.fnc.objects as bsc_fnc_objects

        import lxmaya.core as mya_core

        mya_core.MyaUtil.set_stack_trace_enable(True)

        variant = 'outsource'
        version = self._rsv_scene_properties.get('version')
        step = self._rsv_scene_properties.get('step')
        if step == 'grm':
            keyword_0 = 'asset-source-maya-xgen-cache-main-dir'
        else:
            keyword_0 = 'asset-source-maya-xgen-cache-dir'
        keyword_1 = 'asset-source-maya-scene-src-dir'
        keyword_2 = 'asset-source-maya-scene-src-file'

        xgen_main_directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        xgen_main_directory_path_tgt = xgen_main_directory_rsv_unit_tgt.get_result(
            version=version, variants_extend=dict(variant=variant)
        )

        xgen_project_directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        xgen_project_directory_path_tgt = xgen_project_directory_rsv_unit_tgt.get_result(
            version='latest'
        )

        maya_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_2
        )
        maya_scene_file_path = maya_scene_file_rsv_unit.get_result(
            version=version
        )

        if bsc_storage.StgDirectoryOpt(xgen_main_directory_path_tgt).get_is_exists() is False:
            directory_path_0 = xgen_main_directory_rsv_unit_tgt.get_exists_result(
                version='latest', variants_extend=dict(variant=variant)
            )
            if directory_path_0:
                bsc_log.Log.trace_method_warning(
                    'asset xgen repath',
                    u'directory="{}" is not found, use "{}" instance'.format(
                        xgen_main_directory_path_tgt, directory_path_0

                    )
                )
                xgen_main_directory_path_tgt = directory_path_0
            else:
                return False

        e = bsc_fnc_objects.FncExporterForDotXgen

        xgen_collection_file_paths = e._find_scene_xgen_collection_file_paths(
            maya_scene_file_path
        )
        for i_xgen_collection_file_path in xgen_collection_file_paths:
            i_xgen_collection_name = e._get_xgen_collection_name(i_xgen_collection_file_path)

            e._repath_xgen_collection_file_to(
                i_xgen_collection_file_path,
                xgen_project_directory_path_tgt,
                # convert to collection directory
                '{}/collections'.format(xgen_main_directory_path_tgt),
                i_xgen_collection_name,
            )

    def set_maya_texture_repath(self):
        import lxbasic.dcc.scripts as bsc_dcc_scripts

        import lxmaya.dcc.objects as mya_dcc_objects

        import lxmaya.core as mya_core

        mya_core.MyaUtil.set_stack_trace_enable(True)

        keyword = 'asset-source-texture-dir'

        variant = 'outsource'
        version = self._rsv_scene_properties.get('version')

        directory_rsv_unit_tgt = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )

        directory_path_tgt = directory_rsv_unit_tgt.get_exists_result(
            version=version, variants_extend=dict(variant=variant)
        )
        if directory_path_tgt:
            bsc_dcc_scripts.ScpDccTextures(
                mya_dcc_objects.TextureReferences(
                    option=dict(
                        with_reference=False
                    )
                )
            ).auto_search_from(
                [
                    directory_path_tgt
                ]
            )
        else:
            bsc_log.Log.trace_method_warning(
                'texture search',
                'texture directory is not found'
            )
        #
        bsc_dcc_scripts.ScpDccTextures(
            mya_dcc_objects.TextureReferences(
                option=dict(
                    with_reference=False
                )
            )
        ).auto_repath_tx_to_original()

    def set_maya_ass_export(self):
        import lxmaya.fnc.objects as mya_fnc_objects

        keyword = 'asset-source-maya-ass-file'

        variant = 'outsource'
        version = self._rsv_scene_properties.get('version')

        root = self._rsv_scene_properties.get('dcc.root')

        ass_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )

        ass_file_path = ass_file_rsv_unit.get_result(
            version=version, variants_extend=dict(variant=variant)
        )

        mya_fnc_objects.FncExporterForLookAss(
            option=dict(
                file=ass_file_path,
                location=root,
                texture_use_environ_map=True,
            )
        ).execute()

    # katana
    def set_katana_create(self):
        import lxkatana.dcc.objects as ktn_dcc_objects

        keyword = 'asset-source-katana-scene-src-file'

        version = self._rsv_scene_properties.get('version')

        katana_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        katana_scene_src_file_path = katana_scene_src_file_rsv_unit.get_result(
            version='{}__outsource'.format(version)
        )
        # save first
        ktn_dcc_objects.Scene.save_to_file(katana_scene_src_file_path)

        self.set_katana_load_workspace()

        self.set_katana_import_ass()

        ktn_dcc_objects.Scene.save_to_file(katana_scene_src_file_path)

    def set_katana_load_workspace(self):
        import lxkatana.dcc.objects as ktn_dcc_objects

        r = self._resolver

        project = self._rsv_scene_properties.get('project')

        rsv_task = r.get_rsv_task(
            project=project,
            asset='surface_workspace',
            step='srf',
            task='surfacing'
        )

        if rsv_task:
            rsv_unit = rsv_task.get_rsv_unit(
                keyword='asset-source-katana-scene-src-file'
            )
            file_path = rsv_unit.get_result(
                version='latest'
            )

            ms = [
                (ktn_dcc_objects.Scene.import_from_file, (file_path,)),
                (ktn_dcc_objects.AssetWorkspaceOld().set_all_executes_run, ()),
                (ktn_dcc_objects.AssetWorkspaceOld().set_variables_registry, ())
            ]

            with bsc_log.LogProcessContext.create(maximum=len(ms), label='execute workspace load method') as g_p:
                for i_m, i_as in ms:
                    g_p.do_update()
                    if i_as:
                        i_m(*i_as)
                    else:
                        i_m()

    def set_katana_import_ass(self):
        import lxkatana.fnc.objects as ktn_fnc_objects

        keyword = 'asset-source-maya-ass-file'

        variant = 'outsource'
        version = self._rsv_scene_properties.get('version')

        ass_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword
        )
        ass_file_path = ass_file_rsv_unit.get_result(
            version=version, variants_extend=dict(variant=variant)
        )

        ktn_fnc_objects.FncImporterForLookAssOld(
            option=dict(
                file=ass_file_path,
                location='/root/materials',
                look_pass='default'
            )
        ).set_run()


# noinspection PyUnusedLocal
class RsvVedioComposite(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvVedioComposite, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_video_mov_composite(self):
        import itertools

        import collections

        rsv_scene_properties = self._rsv_scene_properties

        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-katana-render-video-all-mov-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-katana-render-video-all-mov-file'
        else:
            raise TypeError()

        render_output_directory_path = self.get_asset_katana_render_output_directory()
        video_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        video_file_path = video_file_rsv_unit.get_result(
            version=version
        )

        layer_from_geometry_variant = self._hook_option_opt.get_as_boolean('layer_from_geometry_variant')
        layers = self._hook_option_opt.get_as_array('layers')
        render_passes = self._hook_option_opt.get_as_array('render_passes')

        render_output_file_path_pattern = '{directory}/main/{camera}.{layer}.{light_pass}.{look_pass}.{quality}/{render_pass}.{frame}.exr'

        p = bsc_core.PtnParseOpt(render_output_file_path_pattern)
        p.update_variants(directory=render_output_directory_path)

        dict_ = collections.OrderedDict()
        for i_layer, i_render_pass in itertools.product(layers, render_passes):
            i_p = p.update_variants_to(
                layer=i_layer, render_pass=i_render_pass
            )
            i_matchers = i_p.get_matches()
            for j_match in i_matchers:
                j_option = {}
                j_file_path = j_match['result']
                j_file_opt = bsc_storage.StgFileOpt(j_file_path)
                i_f_name_new, i_numbers = bsc_storage.StgFileMtdForMultiply.get_number_args(
                    j_file_opt.name, '*.%04d.exr'
                )
                i_f_new = '{}/{}'.format(j_file_opt.directory_path, i_f_name_new)
                j_option['name'] = i_render_pass
                j_option['image_foreground'] = '/l/resource/td/asset/image/foreground-v001/{}-{}.png'.format(
                    i_layer, i_render_pass
                )
                dict_[i_f_new] = j_option
        # resize use fit
        for k, i_v in dict_.items():
            i_f_src = k
            i_f_opt_src = bsc_storage.StgFileOpt(k)
            i_f_tgt = '{}/resize/{}'.format(i_f_opt_src.directory_path, i_f_opt_src.name)
            i_f_opt_tgt = bsc_storage.StgFileOpt(i_f_tgt)
            i_v['image_resize'] = i_f_tgt
            i_f_opt_tgt.create_directory()
            bsc_storage.ImgOiioMtd.fit_to(i_f_src, i_f_tgt, (2048, 2048))
            bsc_log.Log.trace_method_result(
                'image resize',
                u'file="{}"'.format(
                    i_f_tgt
                )
            )
        # create background
        for k, i_v in dict_.items():
            i_name = i_v['name']
            i_f_src = k
            i_f_opt_src = bsc_storage.StgFileOpt(k)
            i_f_tgt = '{}/background/{}.exr'.format(i_f_opt_src.directory_path, i_name)
            i_f_opt_tgt = bsc_storage.StgFileOpt(i_f_tgt)
            i_v['image_background'] = i_f_tgt
            i_f_opt_tgt.create_directory()
            bsc_storage.ImgOiioMtd.create_as_flat_color(i_f_tgt, (2048, 2048), (.25, .25, .25, 1))
            bsc_log.Log.trace_method_result(
                'image background create',
                u'file="{}"'.format(
                    i_f_tgt
                )
            )
        # add background
        for k, i_v in dict_.items():
            i_f_src = k
            i_f_opt_src = bsc_storage.StgFileOpt(k)
            i_f_tgt = '{}/base/{}'.format(i_f_opt_src.directory_path, i_f_opt_src.name)
            i_f_opt_tgt = bsc_storage.StgFileOpt(i_f_tgt)
            i_v['image_base'] = i_f_tgt
            i_resize = i_v['image_resize']
            i_background = i_v['image_background']
            i_f_opt_tgt.create_directory()
            bsc_storage.ImgOiioMtd.over_by(i_resize, i_background, i_f_tgt, (0, 0))
            bsc_log.Log.trace_method_result(
                'image background add',
                u'file="{}"'.format(
                    i_f_tgt
                )
            )
        # add foreground
        for k, i_v in dict_.items():
            i_f_src = k
            i_f_opt_src = bsc_storage.StgFileOpt(k)
            i_f_tgt = '{}/final/{}'.format(i_f_opt_src.directory_path, i_f_opt_src.name)
            i_f_opt_tgt = bsc_storage.StgFileOpt(i_f_tgt)
            i_v['image_final'] = i_f_tgt
            i_base = i_v['image_base']
            i_foreground = i_v['image_foreground']
            i_f_opt_tgt.create_directory()
            bsc_storage.ImgOiioMtd.over_by(i_foreground, i_base, i_f_tgt, (0, 0))
            bsc_log.Log.trace_method_result(
                'image foreground add',
                u'file="{}"'.format(
                    i_f_tgt
                )
            )

        images_final = [v['image_final'] for k, v in dict_.items()]

        bsc_storage.VdoRvioOpt(
            option=dict(
                input=' '.join(['"{}"'.format(i) for i in images_final]),
                output=video_file_path
            )
        ).set_convert_to_vedio()

# coding:utf-8
from qsm_prc_general.rsv import utl_rsv_obj_abstract

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgeneral.dcc.objects as gnl_dcc_objects

import lxmaya.core as mya_core

import lxmaya.dcc.objects as mya_dcc_objects

import lxmaya.fnc.objects as mya_fnc_objects


class RsvDccSceneHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccSceneHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def do_export_asset_scene(self):
        key = 'asset scene export'
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        step = rsv_scene_properties.get('step')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        camera_root = rsv_scene_properties.get('dcc.camera_root')
        pathsep = rsv_scene_properties.get('dcc.pathsep')
        #
        if step in ['cam']:
            location = camera_root
        else:
            location = root
        #
        mya_location = bsc_core.PthNodeOpt(location).translate_to(
            pathsep=pathsep
        ).to_string()
        mya_group = mya_dcc_objects.Group(
            mya_location
        )
        if mya_group.get_is_exists() is True:
            if workspace == rsv_scene_properties.get('workspaces.release'):
                keyword_0 = 'asset-maya-scene-file'
            elif workspace == rsv_scene_properties.get('workspaces.temporary'):
                keyword_0 = 'asset-temporary-maya-scene-file'
            else:
                raise TypeError()
            #
            scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_0
            )
            scene_file_path = scene_file_rsv_unit.get_result(version=version)
            mya_fnc_objects.FncExporterForScene(
                option=dict(
                    file=scene_file_path,
                    location=location,
                    #
                    with_xgen_collection=True,
                    with_set=True,
                    #
                    ext_extras=self._hook_option_opt.get('ext_extras', as_array=True)
                )
            ).execute()
            return scene_file_path
        else:
            raise RuntimeError(
                bsc_log.Log.trace_method_error(
                    key,
                    u'obj="{}" is non-exists'.format(mya_group.path)
                )
            )

    def set_asset_root_property_refresh(self):
        task = self._rsv_scene_properties.get('task')
        version = self._rsv_scene_properties.get('version')
        root = self._rsv_scene_properties.get('dcc.root')

        mya_root_dag_opt = bsc_core.PthNodeOpt(root).translate_to(
            pathsep='|'
        )
        mya_root = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if mya_root.get_is_exists() is True:
            mya_core.CmdObjOpt(mya_root.path).create_customize_attribute(
                'pg_{}_version'.format(task),
                version
            )

    def set_asset_camera_scene_src_create(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        project = rsv_scene_properties.get('project')
        asset = rsv_scene_properties.get('asset')
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        pathsep = rsv_scene_properties.get('dcc.pathsep')
        camera_root = rsv_scene_properties.get('dcc.camera_root')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-maya-scene-src-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-maya-scene-src-file'
        else:
            raise TypeError()
        #
        orig_file_path = '/l/resource/td/asset/maya/asset-camera.ma'
        orig_file_path = bsc_storage.StgPathMapper.map_to_current(orig_file_path)

        scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_src_file_path = scene_src_file_rsv_unit.get_result(version=version)
        orig_file = gnl_dcc_objects.StgFile(orig_file_path)
        if orig_file.get_is_exists() is True:
            orig_file.copy_to_file(scene_src_file_path, replace=True)
            #
            scene_src_file = gnl_dcc_objects.StgFile(scene_src_file_path)
            if scene_src_file.get_is_exists() is True:
                mya_dcc_objects.Scene.open_file(scene_src_file_path)
                camera_location = camera_root
                mya_camera_location = bsc_core.PthNodeOpt(camera_location).translate_to(pathsep).to_string()
                mya_camera_group = mya_dcc_objects.Group(mya_camera_location)
                if mya_camera_group.get_is_exists() is True:
                    mya_fnc_objects.FncBuilderForAssetOld(
                        option=dict(
                            project=project,
                            asset=asset,
                            #
                            with_model_geometry=True,
                            render_resolution=(2048, 2048),
                        )
                    ).set_run()
                    mya_root = bsc_core.PthNodeOpt(root).translate_to(pathsep).to_string()
                    mya_group = mya_dcc_objects.Group(mya_root)
                    if mya_group.get_is_exists() is True:
                        mya_dcc_objects.Scene.set_current_frame(4)
                        for i in mya_camera_group.get_all_shape_paths(include_obj_type=['camera']):
                            i_camera = mya_dcc_objects.Camera(i)
                            i_camera.set_display_()
                            i_camera.set_frame_to(
                                mya_group.path,
                                percent=.5
                            )
                    else:
                        raise RuntimeError(
                            bsc_log.Log.trace_method_error(
                                'camera scene create',
                                u'obj="{}" is non-exists'.format(mya_root)
                            )
                        )
                else:
                    raise RuntimeError(
                        bsc_log.Log.trace_method_error(
                            'camera scene create',
                            u'obj="{}" is non-exists'.format(mya_camera_location)
                        )
                    )
                mya_dcc_objects.Scene.save_file()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()

    def set_asset_snapshot_preview_export(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        root = rsv_scene_properties.get('dcc.root')
        pathsep = rsv_scene_properties.get('dcc.pathsep')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-preview-mov-file'
            keyword_1 = 'asset-review-mov-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-preview-mov-file'
            keyword_1 = 'asset-temporary-review-mov-file'
        else:
            raise TypeError()

        preview_mov_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        preview_mov_file_path = preview_mov_file_rsv_unit.get_result(
            version=version
        )

        mya_root = bsc_core.PthNodeOpt(root).translate_to(pathsep).to_string()

        mya_fnc_objects.FncExporterForPreview(
            option=dict(
                file=preview_mov_file_path,
                root=mya_root,
                use_render=False,
                convert_to_dot_mov=True,
            )
        ).execute()

        create_review_link = self._hook_option_opt.get('create_review_link') or False
        if create_review_link is True:
            review_mov_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_1
            )
            review_mov_file_path = review_mov_file_rsv_unit.get_result(
                version=version
            )
            preview_mov_file = gnl_dcc_objects.StgFile(
                preview_mov_file_path
            )
            review_mov_file = gnl_dcc_objects.StgFile(review_mov_file_path)
            if preview_mov_file.get_is_exists() is True:
                if review_mov_file.get_is_exists() is False:
                    preview_mov_file.link_to(
                        review_mov_file.path
                    )

    def set_asset_preview_scene_src_create(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        project = rsv_scene_properties.get('project')
        asset = rsv_scene_properties.get('asset')
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-maya-scene-src-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-maya-scene-src-file'
        else:
            raise TypeError()

        scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_src_file_path = scene_src_file_rsv_unit.get_result(version=version)
        #
        mya_fnc_objects.FncBuilderForAssetOld(
            option=dict(
                project=project,
                asset=asset,
                #
                with_model_geometry=True,
                #
                with_surface_look=True,
                with_surface_geometry_uv_map=True,
                #
                geometry_var_names=['hi'],
            )
        ).set_run()
        mya_dcc_objects.Scene.save_to_file(scene_src_file_path)

    def do_create_asset_scene_src(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        project = rsv_scene_properties.get('project')
        asset = rsv_scene_properties.get('asset')
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-maya-scene-src-file'
            keyword_1 = 'asset-maya-scene-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-maya-scene-src-file'
            keyword_1 = 'asset-temporary-maya-scene-file'
        else:
            raise TypeError()

        scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_src_file_path = scene_src_file_rsv_unit.get_result(version=version)

        with_build = self._hook_option_opt.get_as_boolean('with_build')
        if with_build is True:
            mya_fnc_objects.FncBuilderForAssetNew(
                option=dict(
                    # resource
                    project=self._rsv_task.get('project'),
                    asset=self._rsv_task.get('asset'),
                    # data
                    with_geometry=True,
                    with_geometry_uv_map=True,
                    with_look=True,
                    # key
                    with_model=self._hook_option_opt.get_as_boolean('with_model_geometry'),
                    with_model_dynamic=self._hook_option_opt.get_as_boolean('with_model_dynamic'),
                    # model
                    model_space='release',
                    model_elements=[
                        'renderable',
                    ],
                    #
                    with_groom=self._hook_option_opt.get_as_boolean('with_groom_geometry'),
                    with_groom_grow=True,
                    # groom
                    groom_space='release',
                    groom_elements=[
                        'renderable'
                    ],
                    #
                    with_surface=(
                            self._hook_option_opt.get_as_boolean('with_surface_look')
                            or self._hook_option_opt.get_as_boolean('with_surface_geometry_uv_map')
                    ),
                    # surface
                    surface_space='release',
                    surface_elements=[
                        'renderable'
                    ]
                )
            ).execute()
        #
        mya_dcc_objects.Scene.save_to_file(scene_src_file_path)
        #
        if self._hook_option_opt.get_as_boolean('with_scene_link') is True:
            scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_1
            )
            scene_file_path = scene_file_rsv_unit.get_result(version=version)
            bsc_storage.StgFileOpt(scene_file_path).create_directory()
            bsc_storage.StgPathLinkMtd.link_file_to(
                scene_src_file_path, scene_file_path
            )

    def set_asset_texture_bake_create(self):
        key = 'asset texture bake create'

        import lxsession.commands as ssn_commands

        option_hook_key = self._hook_option_opt.get('option_hook_key')
        bake_option_hook_key = 'rsv-task-methods/asset/maya/gen-texture-bake'
        bake_convert_option_hook_key = 'rsv-task-methods/asset/maya/gen-texture-bake-convert'

        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')

        mya_root_dag_opt = bsc_core.PthNodeOpt(root).translate_to(
            pathsep=pathsep
        )
        mya_group = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if mya_group.get_is_exists() is True:
            bake_resolution = self._hook_option_opt.get('bake_resolution', as_integer=True)
            with_work_scene_src_link = self._hook_option_opt.get('with_work_scene_src_link') or False
            #
            mesh_paths = mya_group.get_all_shape_paths(include_obj_type='mesh')
            bake_option_opt = bsc_core.ArgDictStringOpt(
                option=dict(
                    option_hook_key=bake_option_hook_key,
                    #
                    batch_file=self._hook_option_opt.get('batch_file'), file=self._hook_option_opt.get('file'),
                    #
                    user=self._hook_option_opt.get('user'), time_tag=self._hook_option_opt.get('time_tag'),
                    #
                    td_enable=self._hook_option_opt.get('td_enable'), rez_beta=self._hook_option_opt.get('rez_beta'),
                    #
                    bake_location=root,
                    bake_indices=list(range(len(mesh_paths))),
                    bake_resolution=bake_resolution,
                    #
                    dependencies=[option_hook_key],
                )
            )
            bake_session = ssn_commands.execute_option_hook_by_deadline(
                bake_option_opt.to_string()
            )
            bake_ddl_job_id = bake_session.get_ddl_job_id()
            if bake_ddl_job_id:
                bake_convert_option_opt = bsc_core.ArgDictStringOpt(
                    option=dict(
                        option_hook_key=bake_convert_option_hook_key,
                        #
                        batch_file=self._hook_option_opt.get('batch_file'), file=self._hook_option_opt.get('file'),
                        #
                        user=self._hook_option_opt.get('user'), time_tag=self._hook_option_opt.get('time_tag'),
                        #
                        td_enable=self._hook_option_opt.get('td_enable'),
                        rez_beta=self._hook_option_opt.get('rez_beta'),
                        #
                        with_texture_bake_convert=True,
                        bake_resolution=bake_resolution,
                        with_work_scene_src_link=with_work_scene_src_link,
                        #
                        dependencies=[option_hook_key],
                        #
                        dependent_ddl_job_id_extend=[bake_ddl_job_id]
                    )
                )
                ssn_commands.execute_option_hook_by_deadline(
                    bake_convert_option_opt.to_string()
                )
        else:
            raise RuntimeError(
                bsc_log.Log.trace_method_error(
                    key,
                    u'obj="{}" is non-exists'.format(mya_group.path)
                )
            )

    def set_asset_texture_bake(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        root = rsv_scene_properties.get('dcc.root')
        pathsep = rsv_scene_properties.get('dcc.pathsep')

        mya_root_dag_opt = bsc_core.PthNodeOpt(root).translate_to(
            pathsep=pathsep
        )
        mya_group = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if mya_group.get_is_exists() is True:
            workspace = rsv_scene_properties.get('workspace')
            version = rsv_scene_properties.get('version')
            #
            if workspace == rsv_scene_properties.get('workspaces.release'):
                keyword_0 = 'asset-texture-dir'
            elif workspace == rsv_scene_properties.get('workspaces.temporary'):
                keyword_0 = 'asset-temporary-texture-dir'
            else:
                raise RuntimeError()
            #
            texture_tgt_directory_tgt_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_0
            )
            texture_directory_path_tgt = texture_tgt_directory_tgt_unit.get_result(
                version=version
            )
            start_index, end_index = self._hook_option_opt.get('start_index'), self._hook_option_opt.get('end_index')
            #
            mesh_paths = mya_group.get_all_shape_paths(include_obj_type='mesh')
            all_indices = list(range(len(mesh_paths)))
            include_indices = all_indices[int(start_index):int(end_index)+1]
            bake_resolution = self._hook_option_opt.get('bake_resolution', as_integer=True)
            #
            mya_fnc_objects.TextureBaker(
                option=dict(
                    directory=texture_directory_path_tgt,
                    location=root,
                    include_indices=include_indices,
                    resolution=bake_resolution,
                    aa_samples=3
                )
            ).set_run()

    def set_asset_texture_bake_convert(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        root = self._rsv_scene_properties.get('dcc.root')
        pathsep = self._rsv_scene_properties.get('dcc.pathsep')

        mya_root_dag_opt = bsc_core.PthNodeOpt(root).translate_to(
            pathsep=pathsep
        )
        mya_group = mya_dcc_objects.Group(
            mya_root_dag_opt.get_value()
        )
        if mya_group.get_is_exists() is True:
            workspace = rsv_scene_properties.get('workspace')
            version = rsv_scene_properties.get('version')
            #
            if workspace == rsv_scene_properties.get('workspaces.release'):
                keyword_0 = 'asset-maya-scene-file'
                keyword_1 = 'asset-texture-dir'
            elif workspace == rsv_scene_properties.get('workspaces.temporary'):
                keyword_0 = 'asset-temporary-maya-scene-file'
                keyword_1 = 'asset-temporary-texture-dir'
            else:
                raise TypeError()
            #
            scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_0
            )
            scene_file_path = scene_file_rsv_unit.get_result(version=version)
            #
            texture_tgt_directory_tgt_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_1
            )
            texture_directory_path_tgt = texture_tgt_directory_tgt_unit.get_result(
                version=version
            )
            #
            bake_resolution = self._hook_option_opt.get('bake_resolution', as_integer=True)
            #
            mya_fnc_objects.TextureBaker(
                option=dict(
                    directory=texture_directory_path_tgt,
                    location=root,
                    resolution=bake_resolution,
                )
            ).set_convert_run()
            #
            mya_dcc_objects.Scene.save_to_file(
                scene_file_path
            )

    def set_asset_work_scene_src_link(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-maya-scene-file'
            keyword_1 = 'asset-source-maya-scene-src-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-maya-scene-file'
            keyword_1 = 'asset-source-maya-scene-src-file'
        else:
            raise TypeError()
        #
        scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        scene_file_path = scene_file_rsv_unit.get_result(version=version)

        work_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        latest_work_scene_src_file_path = work_scene_src_file_rsv_unit.get_result(
            version='latest'
        )
        if latest_work_scene_src_file_path:
            if bsc_storage.StgPathLinkMtd.get_is_link_source_to(
                    scene_file_path, latest_work_scene_src_file_path
            ) is False:
                new_work_scene_src_file_path = work_scene_src_file_rsv_unit.get_result(
                    version='new'
                )
                #
                gnl_dcc_objects.StgFile(
                    scene_file_path
                ).link_to(new_work_scene_src_file_path)
            else:
                bsc_log.Log.trace_method_warning(
                    'preview work-scene-src link create',
                    u'link="{}" >> "{}" is exists'.format(
                        scene_file_path, latest_work_scene_src_file_path
                    )
                )
        else:
            new_work_scene_src_file_path = work_scene_src_file_rsv_unit.get_result(
                version='new'
            )
            gnl_dcc_objects.StgFile(
                scene_file_path
            ).link_to(new_work_scene_src_file_path)


class RsvDccShotSceneHookOpt(utl_rsv_obj_abstract.AbsRsvObjHookOpt):
    def __init__(self, rsv_scene_properties, hook_option_opt=None):
        super(RsvDccShotSceneHookOpt, self).__init__(rsv_scene_properties, hook_option_opt)

    def set_asset_shot_scene_open(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        asset_shot = self._hook_option_opt.get('shot')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-shot-maya-scene-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-shot-maya-scene-file'
        else:
            raise TypeError()
        #
        asset_shot_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        asset_shot_scene_file_path = asset_shot_scene_file_rsv_unit.get_exists_result(
            version=version,
            variants_extend=dict(
                asset_shot=asset_shot
            )
        )
        if asset_shot_scene_file_path is not None:
            mya_dcc_objects.Scene.open_file(
                asset_shot_scene_file_path
            )
        else:
            raise RuntimeError()

    def set_asset_shot_scene_src_copy(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        asset_shot = self._hook_option_opt.get('shot')
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-shot-maya-scene-src-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-shot-maya-scene-src-file'
        else:
            raise TypeError()
        #
        rsv_project = self._rsv_task.get_rsv_project()
        rsv_shot = rsv_project.get_rsv_resource(
            shot=asset_shot
        )
        #
        shot_scene_file_rsv_unit = rsv_shot.get_available_rsv_unit(
            task=['final_layout', 'animation', 'blocking', 'rough_layout'],
            keyword='shot-maya-scene-file',
        )
        shot_scene_file_path = shot_scene_file_rsv_unit.get_result(
            version='latest',
        )
        #
        asset_shot_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        asset_shot_scene_src_file_path = asset_shot_scene_src_file_rsv_unit.get_result(
            version=version,
            variants_extend=dict(
                asset_shot=asset_shot
            )
        )
        #
        gnl_dcc_objects.StgFile(
            shot_scene_file_path
        ).copy_to_file(
            asset_shot_scene_src_file_path
        )

    def set_asset_shot_scene_export(self):
        rsv_scene_properties = self._rsv_scene_properties
        #
        asset_shot = self._hook_option_opt.get('shot')
        shot_asset = self._hook_option_opt.get('shot_asset')
        #
        workspace = rsv_scene_properties.get('workspace')
        version = rsv_scene_properties.get('version')
        #
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-shot-maya-scene-src-file'
            keyword_1 = 'asset-shot-maya-scene-file'
            keyword_2 = 'asset-maya-scene-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-shot-maya-scene-src-file'
            keyword_1 = 'asset-temporary-shot-maya-scene-file'
            keyword_2 = 'asset-temporary-maya-scene-file'
        else:
            raise TypeError()
        #
        asset_shot_scene_src_file_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        asset_shot_scene_src_file_path = asset_shot_scene_src_file_rsv_unit.get_exists_result(
            version=version,
            variants_extend=dict(
                asset_shot=asset_shot
            )
        )
        if asset_shot_scene_src_file_path:
            mya_dcc_objects.Scene.open_file(asset_shot_scene_src_file_path)
            #
            asset_maya_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_2
            )
            asset_maya_scene_file_path = asset_maya_scene_file_rsv_unit.get_exists_result(
                version=version
            )
            if asset_maya_scene_file_path:
                self._set_shot_asset_rig_replace_(shot_asset, asset_maya_scene_file_path)
            else:
                raise RuntimeError()
            #
            asset_shot_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword_1
            )
            asset_shot_scene_file_path = asset_shot_scene_file_rsv_unit.get_result(
                version=version,
                variants_extend=dict(
                    asset_shot=asset_shot
                )
            )
            mya_dcc_objects.Scene.save_to_file(
                asset_shot_scene_file_path
            )
        else:
            raise RuntimeError()

    @classmethod
    def _set_shot_asset_rig_replace_(cls, namespace, file_path):
        reference_dict = mya_dcc_objects.References().get_reference_dict_()
        if namespace in reference_dict:
            namespace, root, obj = reference_dict[namespace]
            obj.do_replace(file_path)
        else:
            raise RuntimeError(
                bsc_log.Log.trace_method_error(
                    'usd export',
                    'namespace="{}" is non-exists'.format(namespace)
                )
            )

    # TODO need support for pg_namespace
    @classmethod
    def get_shot_asset_dict(cls):
        dict_ = {}
        r = cls.generate_resolver()
        reference_raw = mya_dcc_objects.References().get_reference_raw()
        for i_obj, i_namespace, i_file_path in reference_raw:
            i_rsv_task = r.get_rsv_task_by_any_file_path(
                i_file_path
            )
            i_root = i_obj.get_content_obj_paths()[0]
            if i_rsv_task is not None:
                dict_[i_root] = i_namespace, i_rsv_task
        return dict_

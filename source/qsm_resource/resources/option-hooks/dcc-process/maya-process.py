# coding:utf-8

def lib_fbx_to_usd_fnc(option_opt):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxmaya.fnc.objects as mya_fnc_objects

    fbx_file_path = option_opt.get('fbx')
    fbx_file_opt = bsc_storage.StgFileOpt(fbx_file_path)
    if fbx_file_opt.get_is_file() is True:
        usd_file_path = option_opt.get('usd')
        usd_file_opt = bsc_storage.StgFileOpt(usd_file_path)
        #
        use_update_mode = option_opt.get('use_update_mode')
        if use_update_mode is True:
            if fbx_file_opt.get_timestamp_is_same_to(
                usd_file_path
            ) is True:
                bsc_log.Log.trace_method_warning(
                    'fbx to usd',
                    'non changed update for "{}"'.format(
                        usd_file_path
                    )
                )
                return
        # import fbx
        mya_fnc_objects.FncImporterForGeometryFbx(
            option=dict(
                file=option_opt.get('fbx')
            )
        ).execute()

        location = '/geometries'

        meshes = mya_dcc_objects.Nodes(['mesh']).get_objs()
        if meshes:
            group = mya_dcc_objects.Group(bsc_core.BscNodePathOpt(location).translate_to('|').get_path())
            group.set_create('transform')
            #
            for i in mya_dcc_objects.Nodes(['mesh']).get_objs():
                i.get_parent().set_parent(group)
            #
            usd_file_path = option_opt.get('usd')
            #
            bsc_storage.StgFileOpt(usd_file_path).create_directory()
            #
            mya_fnc_objects.FncExporterForGeometryUsd(
                option=dict(
                    file=usd_file_path,
                    location=location,
                    #
                    default_prim_path=location,
                    #
                    with_mesh_uv=True,
                    with_mesh=True,
                    with_curve=True,
                    #
                    with_mesh_subset=True,
                )
            ).execute()
            #
            if usd_file_opt.get_is_file() is True:
                usd_file_opt.set_modify_time(
                    fbx_file_opt.get_mtime()
                )
        else:
            bsc_log.Log.trace_method_warning(
                'fbx-to-usd',
                'no mesh found in scene'
            )
    else:
        bsc_log.Log.trace_method_warning(
            'fbx-to-usd',
            'file="{}" is non-exists'.format(fbx_file_path)
        )


def lib_scene_src_to_scene_fnc(option_opt):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxgeneral.dcc.scripts as gnl_dcc_scripts

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxmaya.fnc.objects as mya_fnc_objects

    import lxmaya.scripts as mya_scripts

    type_path = option_opt.get('type_path')
    type_opt = bsc_core.BscNodePathOpt(type_path)
    type_name = type_opt.get_name()
    category_opt = type_opt.get_parent()
    category_path = category_opt.get_path()
    category_name = category_opt.get_name()
    resource_path = option_opt.get('resource_path')
    resource_name = option_opt.get('resource_name')
    version_name = option_opt.get('version_name')
    prefix_name = 'lib__{}_{}'.format(resource_name, version_name)
    scene_maya_src_file_path = option_opt.get('scene_maya_src_file')
    scene_maya_src_file_opt = bsc_storage.StgFileOpt(scene_maya_src_file_path)
    #
    rename_geometry = option_opt.get_as_boolean('rename_geometry')
    rename_look = option_opt.get_as_boolean('rename_look')
    split_mesh = option_opt.get_as_boolean('split_mesh')
    if scene_maya_src_file_opt.get_is_file() is True:
        mya_dcc_objects.Scene.open_file(
            scene_maya_src_file_opt.get_path()
        )
        location = '/geometries'
        meshes = mya_dcc_objects.Nodes(['mesh']).get_objs()
        if not meshes:
            return
        #
        group = mya_dcc_objects.Group(bsc_core.BscNodePathOpt(location).translate_to('|').get_path())
        group.set_create('transform')
        # collection geometry
        for seq, i_mesh in enumerate(mya_dcc_objects.Nodes(['mesh']).get_objs()):
            if rename_geometry is True:
                i_mesh.get_parent().set_rename('mesh_{}'.format(str(seq+1).zfill(3)))
                i_mesh.set_rename('mesh_{}Shape'.format(str(seq+1).zfill(3)))
                i_mesh._update_path_()
            #
            i_mesh.get_parent().set_parent(group)
        # scale
        scale = option_opt.get_as_float('scale')
        if scale is not None:
            group.set('scale', (scale, scale, scale))
            group.make_identity()
        # rename shader graph
        if rename_look is True:
            mya_scripts.ScpLibraryLook(location).rename_look(prefix_name)
        #
        texture_search_directory_path = '/production/library/resource/share/texture/plant-unorganized/tx'
        #
        gnl_dcc_scripts.ScpDccTextures(
            mya_dcc_objects.TextureReferences(
                option=dict(
                    with_reference=False
                )
            )
        ).auto_search_from(
            [
                texture_search_directory_path
            ],
            recursion_enable=True
        )
        # split mesh
        if split_mesh is True:
            mya_scripts.ScpLibraryLook(location).split_meshes_by_subsets({'lib_resource_type': type_path})
        # # texture search data
        # json_file_opt = bsc_storage.StgFileOpt(
        #     '/production/library/resource/.data/3d_plant_proxy/texture-search.json'
        # )
        # texture_search_data = json_file_opt.set_read() or {}
        # texture_search_data[resource_path] = {}
        # #
        # texture_data = mya_scripts.ScpLibraryLook(location).get_texture_search_data(category_name, type_name)
        # if texture_data:
        #     texture_search_data[resource_path] = texture_data
        # json_file_opt.set_write(texture_search_data)
        # auto group
        if option_opt.get_as_boolean('auto_group_component') is True:
            mya_scripts.ScpLibraryLook(location).auto_group_by_component(category_path, resource_path)
        #
        if option_opt.get_as_boolean('with_scene_maya') is True:
            maya_scene_file_path = option_opt.get('scene_maya_file')
            maya_scene_file_opt = bsc_storage.StgFileOpt(maya_scene_file_path)
            bsc_storage.StgFileOpt(maya_scene_file_path).create_directory()
            #
            mya_fnc_objects.FncExporterForScene(
                option=dict(
                    file=maya_scene_file_path,
                    location=location,
                )
            ).execute()
            #
            if maya_scene_file_opt.get_is_file() is True:
                maya_scene_file_opt.set_modify_time(
                    scene_maya_src_file_opt.get_mtime()
                )
    else:
        bsc_log.Log.trace_warning(
            'file="{}" is non-exists'.format(scene_maya_src_file_path)
        )


def lib_scene_to_geometry_fnc(option_opt):
    import lxbasic.log as bsc_log

    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxmaya.fnc.objects as mya_fnc_objects

    scene_maya_file_path = option_opt.get('scene_maya_file')
    scene_file_opt = bsc_storage.StgFileOpt(scene_maya_file_path)

    if scene_file_opt.get_is_file() is True:
        mya_dcc_objects.Scene.open_file(
            scene_file_opt.get_path()
        )

        location = '/geometries'

        if option_opt.get_as_boolean('with_geometry_usd') is True:
            geometry_usd_file_path = option_opt.get('geometry_usd_file')
            geometry_usd_file_opt = bsc_storage.StgFileOpt(geometry_usd_file_path)
            #
            bsc_storage.StgFileOpt(geometry_usd_file_path).create_directory()
            #
            mya_fnc_objects.FncExporterForGeometryUsd(
                option=dict(
                    file=geometry_usd_file_path,
                    location=location,
                    #
                    default_prim_path=location,
                    #
                    with_mesh_uv=True,
                    with_mesh=True,
                    with_curve=True,
                    #
                    with_mesh_subset=True,
                    with_material_assign=True,
                    #
                    auto_plant_display_color=True,
                    #
                    port_match_patterns=['lib_*']
                )
            ).execute()

            if geometry_usd_file_opt.get_is_file() is True:
                geometry_usd_file_opt.set_modify_time(
                    scene_file_opt.get_mtime()
                )

        if option_opt.get_as_boolean('with_geometry_abc') is True:
            geometry_abc_file_path = option_opt.get('geometry_abc_file')
            geometry_abc_file_opt = bsc_storage.StgFileOpt(geometry_abc_file_path)

            bsc_storage.StgFileOpt(geometry_abc_file_path).create_directory()

            mya_fnc_objects.FncExporterForGeometryAbc(
                file_path=geometry_abc_file_path,
                root=location,
                attribute_prefix=['lib'],
                option={
                    'writeFaceSets': True
                }
            ).set_run()

            if geometry_abc_file_opt.get_is_file() is True:
                geometry_abc_file_opt.set_modify_time(
                    scene_file_opt.get_mtime()
                )
    else:
        bsc_log.Log.trace_warning(
            'file="{}" is non-exists'.format(scene_maya_file_path)
        )


def lib_scene_to_proxy_fnc(option_opt):
    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxmaya.fnc.objects as mya_fnc_objects

    import lxmaya.scripts as mya_scripts

    resource_name = option_opt.get('resource')
    version = option_opt.get('version')
    prefix_name = 'lib__{}_{}'.format(resource_name, version)
    scene_maya_file_path = option_opt.get('scene_maya_file')
    scene_file_opt = bsc_storage.StgFileOpt(scene_maya_file_path)
    #
    create_user_datas = option_opt.get_as_boolean('create_user_datas')
    if scene_file_opt.get_is_file() is True:
        mya_dcc_objects.Scene.open_file(
            scene_file_opt.get_path()
        )
        location = '/geometries'

        if option_opt.get_as_boolean('with_proxy_ass') is True:
            proxy_ass_file_path = option_opt.get('proxy_ass_file')
            ass_file_opt = bsc_storage.StgFileOpt(proxy_ass_file_path)

            if create_user_datas is True:
                mya_scripts.ScpLibraryLook.create_user_datas(prefix_name)

            bsc_storage.StgFileOpt(proxy_ass_file_path).create_directory()

            mya_fnc_objects.FncExporterForLookAss(
                option=dict(
                    file=proxy_ass_file_path,
                    location=location,
                    texture_use_environ_map=True,
                )
            ).execute()
            #
            if ass_file_opt.get_is_file() is True:
                ass_file_opt.set_modify_time(
                    scene_file_opt.get_mtime()
                )


def lib_scene_to_look_fnc(option_opt):
    import lxbasic.storage as bsc_storage

    import lxbasic.resource as bsc_resource

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxmaya.scripts as mya_scripts

    scene_maya_file_path = option_opt.get('scene_maya_file')
    scene_file_opt = bsc_storage.StgFileOpt(scene_maya_file_path)
    #
    if scene_file_opt.get_is_file() is True:
        mya_dcc_objects.Scene.open_file(
            scene_file_opt.get_path()
        )

        category_name = option_opt.get('category_name')
        type_name = option_opt.get('type_name')
        resource_name = option_opt.get('resource_name')
        location = '/geometries'

        texture_directory_path = option_opt.get('texture_directory')
        if option_opt.get_as_boolean('with_look_preview_usd') is True:
            look_preview_json_file_path = option_opt.get('look_preview_json_file')
            look_preview_json_file_opt = bsc_storage.StgFileOpt(look_preview_json_file_path)
            look_data = mya_scripts.ScpLibraryLook(location).get_look_preview_data(texture_directory_path, resource_name)
            if look_data:
                bsc_storage.StgFileOpt(look_preview_json_file_path).set_write(
                    look_data
                )
            #
            if look_preview_json_file_opt.get_is_exists() is True:
                look_data = look_preview_json_file_opt.set_read()
                r = bsc_resource.RscExtendJinja.get_result(
                    'usda/look/preview-material-diffuse',
                    look_data
                )
                look_preview_usd_file_path = option_opt.get('look_preview_usd_file')
                look_preview_usd_file_opt = bsc_storage.StgFileOpt(look_preview_usd_file_path)
                look_preview_usd_file_opt.set_write(r)
                #
                if look_preview_usd_file_opt.get_is_file() is True:
                    look_preview_usd_file_opt.set_modify_time(
                        scene_file_opt.get_mtime()
                    )


def collection_and_repath_texture(option_opt):
    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxmaya.fnc.objects as mya_fnc_objects

    file_path = option_opt.get('file')
    file_opt = bsc_storage.StgFileOpt(file_path)
    #
    mya_dcc_objects.Scene.open_file(file_path)
    #
    texture_directory_path = option_opt.get('texture_directory')
    mya_fnc_objects.FncGeneralTextureExporter(
        option=dict(
            directory=texture_directory_path,
            location='/master',
            fix_name_blank=True,
            copy_source=True,
        )
    ).execute()
    #
    look_yml_directory_path = option_opt.get('look_yml_directory')
    look_yml_file_path = '{}/{}.yml'.format(look_yml_directory_path, file_opt.get_name_base())
    mya_fnc_objects.FncExporterForLookYml(
        option=dict(
            file=look_yml_file_path,
            locations=['/master/mod/hi']
        )
    ).execute()
    #
    scene_directory_path = option_opt.get('scene_directory')
    scene_maya_file_path = '{}/{}.ma'.format(scene_directory_path, file_opt.get_name_base())
    mya_dcc_objects.Scene.save_to_file(scene_maya_file_path)


def register_texture_search(option_opt):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxbasic.database as bsc_database

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxmaya.scripts as mya_scripts

    resource_path = option_opt.get('resource_path')
    version_path = '{}/v0001'.format(resource_path)
    path_opt = bsc_core.BscNodePathOpt(version_path)
    cs = path_opt.get_components()
    category_group = cs[-2].get_name()
    dtb_opt = bsc_database.DtbOptForResource.generate(category_group)

    json_file_opt = bsc_storage.StgFileOpt(
        '/production/library/resource/.data/3d_plant_proxy/texture-search.json'
    )

    texture_search_data = json_file_opt.set_read() or {}

    dtb_version = dtb_opt.get_dtb_version(version_path)
    if dtb_version:
        dtb_version_opt = bsc_database.DtbNodeOptForRscVersion(
            dtb_opt, dtb_version
        )

        scene_maya_file_path = dtb_version_opt.get_exists_file('maya-scene-file')
        if scene_maya_file_path:
            mya_dcc_objects.Scene.open_file(scene_maya_file_path)

            location = '/geometries'

            dtb_types = dtb_version_opt.get_types()
            dtb_type_path = dtb_types[0].path
            dtb_type_path_opt = bsc_core.BscNodePathOpt(dtb_type_path)

            category_name = dtb_type_path_opt.get_parent().get_name()
            type_name = dtb_type_path_opt.get_name()

            texture_data = mya_scripts.ScpLibraryLook(location).get_texture_search_data(category_name, type_name)
            if texture_data:
                texture_search_data[resource_path] = texture_data
    else:
        texture_search_data[resource_path] = {}

    json_file_opt.set_write(texture_search_data)


def main(session):
    # noinspection PyUnresolvedReferences
    from maya import cmds
    cmds.stackTrace(state=1)
    #
    option_opt = session.get_option_opt()
    key = option_opt.get('method')
    if key == 'fbx-to-usd':
        lib_fbx_to_usd_fnc(option_opt)
    #
    elif key == 'scene-src-to-scene':
        lib_scene_src_to_scene_fnc(option_opt)
    #
    elif key == 'scene-to-geometry':
        lib_scene_to_geometry_fnc(option_opt)
    elif key == 'scene-to-proxy':
        lib_scene_to_proxy_fnc(option_opt)
    elif key == 'scene-to-look':
        lib_scene_to_look_fnc(option_opt)
    elif key == 'register-texture-search':
        register_texture_search(option_opt)
    elif key == 'collection-and-repath-texture':
        collection_and_repath_texture(option_opt)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

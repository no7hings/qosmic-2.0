# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxresolver.core as rsv_core
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    cmds.stackTrace(state=1)

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
                    keyword_0 = 'asset-maya-scene-file'
                elif workspace == rsv_scene_properties.get('workspaces.temporary'):
                    keyword_0 = 'asset-temporary-maya-scene-file'
                else:
                    raise TypeError()
                #
                maya_scene_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
                maya_scene_file_path = maya_scene_file_rsv_unit.get_result(version=version)
                if bsc_storage.StgPathOpt(maya_scene_file_path).get_is_exists() is True:
                    mya_dcc_objects.Scene.open_file(maya_scene_file_path)
                    #
                    with_hair_xgen = hook_option_opt.get('with_hair_xgen') or False
                    if with_hair_xgen is True:
                        set_hair_xgen_export(rsv_task, rsv_scene_properties)
                    # cache/usd/xgen.usda
                    with_hair_xgen_usd = hook_option_opt.get('with_hair_xgen_usd') or False
                    if with_hair_xgen_usd is True:
                        set_hair_xgen_usd_export(rsv_task, rsv_scene_properties)
                else:
                    raise RuntimeError()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def set_hair_xgen_export(rsv_task, rsv_scene_properties):
    import lxbasic.core as bsc_core

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxmaya.fnc.objects as mya_fnc_objects

    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    pathsep = rsv_scene_properties.get('dcc.pathsep')
    location = '{}/hair'.format(root)
    mya_location = mya_dcc_objects.Group(
        bsc_core.PthNodeOpt(location).translate_to(
            pathsep
        ).to_string()
    )
    if mya_location.get_is_exists() is True:
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-release-version-dir'
            keyword_1 = 'asset-geometry-xgen-collection-dir'
            keyword_2 = 'asset-geometry-xgen-glow-dir'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-version-dir'
            keyword_1 = 'asset-temporary-geometry-xgen-collection-dir'
            keyword_2 = 'asset-temporary-geometry-xgen-glow-dir'
        else:
            raise TypeError()

        version_directory_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
        version_directory_path = version_directory_rsv_unit.get_result(version=version)

        xgen_collection_directory_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_1)
        xgen_collection_directory_path_tgt = xgen_collection_directory_rsv_unit.get_result(version=version)

        grow_mesh_directory_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_2)
        grow_mesh_directory_path = grow_mesh_directory_rsv_unit.get_result(version=version)
        #
        mya_fnc_objects.XgenExporter(
            option=dict(
                xgen_project_directory=version_directory_path,
                xgen_collection_directory=xgen_collection_directory_path_tgt,
                grow_mesh_directory=grow_mesh_directory_path,
                #
                location=location,
                #
                with_xgen_collection=True,
                with_grow_mesh_abc=True,
            )
        ).set_run()
    else:
        raise RuntimeError(
            bsc_log.Log.trace_method_error(
                'xgen export',
                u'obj="{}" is non-exists'.format(mya_location.path)
            )
        )


def set_hair_xgen_usd_export(rsv_task, rsv_scene_properties):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxgeneral.fnc.objects as gnl_fnc_objects

    import lxmaya.dcc.objects as mya_dcc_objects

    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    pathsep = rsv_scene_properties.get('dcc.pathsep')
    location = '{}/hair'.format(root)

    mya_location = mya_dcc_objects.Group(
        bsc_core.PthNodeOpt(location).translate_to(
            pathsep
        ).to_string()
    )
    if mya_location.get_is_exists() is True:
        if workspace == rsv_scene_properties.get('workspaces.release'):
            keyword_0 = 'asset-maya-scene-file'
            keyword_1 = 'asset-xgen-usd-file'
        elif workspace == rsv_scene_properties.get('workspaces.temporary'):
            keyword_0 = 'asset-temporary-maya-scene-file'
            keyword_1 = 'asset-temporary-xgen-usd-file'
        else:
            raise TypeError()

        xgen_usd_file_rsv_unit = rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        xgen_usd_file_path = xgen_usd_file_rsv_unit.get_result(
            version=version
        )
        maya_scene_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
        maya_scene_file_path = maya_scene_file_rsv_unit.get_result(version=version)

        gnl_fnc_objects.FncExporterForDotXgenUsda(
            dict(
                file=xgen_usd_file_path,
                location=location,
                maya_scene_file=maya_scene_file_path,
            )
        ).set_run()
    else:
        raise RuntimeError(
            bsc_log.Log.trace_method_error(
                'xgen export',
                u'obj="{}" is non-exists'.format(mya_location.path)
            )
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

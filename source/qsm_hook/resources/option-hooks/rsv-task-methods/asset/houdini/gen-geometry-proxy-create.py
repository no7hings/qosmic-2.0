# coding:utf-8


def main(session):
    import lxhoudini.dcc.objects as hou_dcc_objects
    #
    import lxresolver.core as rsv_core

    import qsm_hook_houdini.rsv.objects as hou_rsv_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        resolver = rsv_core.RsvBase.generate_root()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            with_geometry_proxy_usd = hook_option_opt.get('with_geometry_proxy_usd') or False
            if with_geometry_proxy_usd is True:
                hou_dcc_objects.Scene.new_file()
                opt = hou_rsv_objects.RsvDccUtilityHookOpt(
                    rsv_scene_properties,
                    hook_option_opt
                )
                set_asset_geometry_proxy_usd_export(opt)
            #
            with_geometry_proxy_abc = hook_option_opt.get('with_geometry_proxy_abc') or False
            if with_geometry_proxy_abc is True:
                hou_dcc_objects.Scene.new_file()
                opt = hou_rsv_objects.RsvDccUtilityHookOpt(
                    rsv_scene_properties,
                    hook_option_opt
                )
                set_asset_geometry_proxy_abc_export(opt)
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def set_asset_geometry_proxy_usd_export(self):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    rsv_scene_properties = self._rsv_scene_properties

    workspace = rsv_scene_properties.get('workspace')
    role = rsv_scene_properties.get('role')
    version = rsv_scene_properties.get('version')

    if workspace == rsv_scene_properties.get('workspaces.release'):
        keyword_1 = 'asset-geometry-usd-var-file'
        keyword_2 = 'asset-geometry-proxy-usd-var-file'
    elif workspace == rsv_scene_properties.get('workspaces.temporary'):
        keyword_1 = 'asset-temporary-geometry-usd-var-file'
        keyword_2 = 'asset-temporary-geometry-proxy-usd-var-file'
    else:
        raise RuntimeError()

    geometry_usd_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
        keyword=keyword_1
    )
    geometry_usd_hi_file_path = geometry_usd_var_file_rsv_unit.get_result(
        version=version, variants_extend=dict(var='hi')
    )

    geometry_proxy_usd_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
        keyword=keyword_2
    )

    geometry_proxy_usd_low_file_path = geometry_proxy_usd_var_file_rsv_unit.get_result(
        version=version, variants_extend=dict(var='low')
    )
    geometry_proxy_usd_shell_file_path = geometry_proxy_usd_var_file_rsv_unit.get_result(
        version=version, variants_extend=dict(var='shell')
    )

    if bsc_storage.StgFileOpt(geometry_usd_hi_file_path).get_is_exists() is True:
        if role in ['asb', 'scn']:
            pass
        else:
            cmd_0 = 'hython -m process.houHdaProcess -hda reducemesh -i "{}" -o "{}"'.format(
                geometry_usd_hi_file_path,
                geometry_proxy_usd_low_file_path
            )
            bsc_core.PrcBaseMtd.execute_with_result(
                cmd_0
            )
            cmd_1 = 'hython -m process.houHdaProcess -hda reducemesh -m 2 -i "{}" -o "{}"'.format(
                geometry_usd_hi_file_path,
                geometry_proxy_usd_shell_file_path
            )
            bsc_core.PrcBaseMtd.execute_with_result(
                cmd_1
            )


def set_asset_geometry_proxy_abc_export(self):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    rsv_scene_properties = self._rsv_scene_properties

    workspace = rsv_scene_properties.get('workspace')
    role = rsv_scene_properties.get('role')
    version = rsv_scene_properties.get('version')

    if workspace == rsv_scene_properties.get('workspaces.release'):
        keyword_1 = 'asset-geometry-usd-var-file'
        keyword_2 = 'asset-geometry-proxy-abc-var-file'
    elif workspace == rsv_scene_properties.get('workspaces.temporary'):
        keyword_1 = 'asset-temporary-geometry-usd-var-file'
        keyword_2 = 'asset-temporary-geometry-proxy-abc-var-file'
    else:
        raise RuntimeError()

    geometry_usd_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
        keyword=keyword_1
    )
    geometry_usd_hi_file_path = geometry_usd_var_file_rsv_unit.get_result(
        version=version, variants_extend=dict(var='hi')
    )

    geometry_proxy_abc_var_file_rsv_unit = self._rsv_task.get_rsv_unit(
        keyword=keyword_2
    )

    geometry_proxy_abc_low_file_path = geometry_proxy_abc_var_file_rsv_unit.get_result(
        version=version, variants_extend=dict(var='low')
    )
    geometry_proxy_abc_shell_file_path = geometry_proxy_abc_var_file_rsv_unit.get_result(
        version=version, variants_extend=dict(var='shell')
    )

    if bsc_storage.StgFileOpt(geometry_usd_hi_file_path).get_is_exists() is True:
        if role in ['asb', 'scn']:
            pass
        else:
            cmd_0 = 'hython -m process.houHdaProcess -hda reducemesh -i "{}" -o "{}"'.format(
                geometry_usd_hi_file_path,
                geometry_proxy_abc_low_file_path
            )
            bsc_core.PrcBaseMtd.execute_with_result(
                cmd_0
            )
            cmd_1 = 'hython -m process.houHdaProcess -hda reducemesh -m 2 -i "{}" -o "{}"'.format(
                geometry_usd_hi_file_path,
                geometry_proxy_abc_shell_file_path
            )
            bsc_core.PrcBaseMtd.execute_with_result(
                cmd_1
            )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

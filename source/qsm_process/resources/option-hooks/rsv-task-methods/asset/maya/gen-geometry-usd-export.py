# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import qsm_prc_maya.rsv.objects as mya_rsv_objects

    import lxresolver.core as rsv_core
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    cmds.stackTrace(state=1)

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFile.get_is_exists(any_scene_file_path) is True:
            mya_dcc_objects.Scene.open_file(any_scene_file_path)
            #
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                with_geometry_usd = hook_option_opt.get('with_geometry_usd') or False
                if with_geometry_usd is True:
                    opt = mya_rsv_objects.RsvDccGeometryHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    )
                    do_export_asset_geometry_usd(opt)
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def do_export_asset_geometry_usd(self):
    rsv_scene_properties = self._rsv_scene_properties

    workspace = rsv_scene_properties.get('workspace')
    role = rsv_scene_properties.get('role')
    version = rsv_scene_properties.get('version')

    if workspace == rsv_scene_properties.get('workspaces.release'):
        keyword = 'asset-cache-usd-dir'
    elif workspace == rsv_scene_properties.get('workspaces.temporary'):
        keyword = 'asset-temporary-cache-usd-dir'
    else:
        raise RuntimeError()

    file_path = self._hook_option_opt.get('file')

    geometry_usd_directory_rsv_unit = self._rsv_task.get_rsv_unit(
        keyword=keyword
    )

    geometry_usd_directory_path = geometry_usd_directory_rsv_unit.get_result(
        version=version
    )
    # noinspection PyUnresolvedReferences
    from production.usd.maya_asset import export_mod_usd
    #
    export_mod_usd.AssetExport().export_mod(
        file_path,
        # geometry_usd_directory_path
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

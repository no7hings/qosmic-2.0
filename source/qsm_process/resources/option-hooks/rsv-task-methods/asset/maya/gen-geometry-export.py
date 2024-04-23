# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxmaya.dcc.objects as mya_dcc_objects

    import lxresolver.core as rsv_core

    import qsm_prc_maya.rsv.objects as mya_rsv_objects
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    cmds.stackTrace(state=1)

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFileMtd.get_is_exists(any_scene_file_path) is True:
            mya_dcc_objects.Scene.open_file(any_scene_file_path)
            #
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                with_geometry_usd = hook_option_opt.get('with_geometry_usd') or False
                if with_geometry_usd is True:
                    mya_rsv_objects.RsvDccGeometryHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).do_export_asset_geometry_usd()
                #
                with_geometry_uv_map_usd = hook_option_opt.get('with_geometry_uv_map_usd') or False
                if with_geometry_uv_map_usd is True:
                    mya_rsv_objects.RsvDccGeometryHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).do_export_asset_geometry_uv_map_usd()
                #
                with_geometry_abc = hook_option_opt.get('with_geometry_abc') or False
                if with_geometry_abc is True:
                    mya_rsv_objects.RsvDccGeometryHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).set_asset_geometry_abc_export()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

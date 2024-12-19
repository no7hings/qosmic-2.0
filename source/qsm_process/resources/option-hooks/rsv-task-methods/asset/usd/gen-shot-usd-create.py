# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxresolver.core as rsv_core

    import lxusd.rsv.objects as usd_rsv_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFile.get_is_exists(any_scene_file_path) is True:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                #
                with_shot_asset_component_usd = hook_option_opt.get('with_shot_asset_component_usd') or False
                if with_shot_asset_component_usd is True:
                    usd_rsv_objects.RsvUsdHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).create_asset_shot_asset_component_usd()
                #
                with_shot_set_usd = hook_option_opt.get('with_shot_set_usd') or False
                if with_shot_set_usd is True:
                    usd_rsv_objects.RsvUsdHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).create_set_asset_shot_set_usd()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

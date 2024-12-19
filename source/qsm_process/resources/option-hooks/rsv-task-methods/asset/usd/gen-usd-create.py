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
                with_geometry_display_color_usd = hook_option_opt.get_as_boolean('with_geometry_display_color_usd')
                if with_geometry_display_color_usd is True:
                    usd_rsv_objects.RsvUsdHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).create_set_asset_display_color_usd()
                #
                with_geometry_user_property_usd = hook_option_opt.get_as_boolean('with_geometry_user_property_usd')
                if with_geometry_user_property_usd is True:
                    usd_rsv_objects.RsvUsdHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).create_asset_user_property_usd()
                #
                with_component_usd = hook_option_opt.get_as_boolean('with_component_usd')
                if with_component_usd is True:
                    usd_rsv_objects.RsvUsdHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).create_set_asset_component_usd()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

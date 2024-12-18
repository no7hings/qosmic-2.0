# coding:utf-8


def main(session):
    import qsm_prc_katana.rsv.objects as ktn_rsv_objects
    #
    import lxresolver.core as rsv_core

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        resolver = rsv_core.RsvBase.generate_root()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            if hook_option_opt.get_as_boolean('create_scene_src') is True:
                ktn_rsv_objects.RsvDccSceneHookOpt(
                    rsv_scene_properties,
                    hook_option_opt,
                ).do_create_asset_scene_src()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

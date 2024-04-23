# coding:utf-8


def main(session):
    import lxresolver.core as rsv_core

    import lxshotgun.rsv.scripts as rsv_stg_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        resolver = rsv_core.RsvBase.generate_root()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            with_review_mov = hook_option_opt.get('with_review_mov') or False
            if with_review_mov is True:
                rsv_stg_objects.RsvShotgunHookOpt(
                    rsv_scene_properties,
                    hook_option_opt
                ).execute_review_mov_export()
            #
            with_validation_info = hook_option_opt.get('with_validation_info') or False
            if with_validation_info is True:
                rsv_stg_objects.RsvShotgunHookOpt(
                    rsv_scene_properties,
                    hook_option_opt
                ).execute_validation_info_export()
            #
            create_shotgun_task = hook_option_opt.get('create_shotgun_task') or False
            if create_shotgun_task is True:
                rsv_stg_objects.RsvShotgunHookOpt(
                    rsv_scene_properties,
                    hook_option_opt
                ).create_stg_task()
            # create version
            create_shotgun_version = hook_option_opt.get('create_shotgun_version') or False
            if create_shotgun_version is True:
                rsv_stg_objects.RsvShotgunHookOpt(
                    rsv_scene_properties,
                    hook_option_opt
                ).create_stg_version()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

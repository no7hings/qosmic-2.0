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
            # new
            if hook_option_opt.get_as_boolean('with_new_registry_json') is True:
                rsv_stg_objects.RsvShotgunHookOpt(
                    rsv_scene_properties,
                    hook_option_opt
                ).execute_new_registry_json_create()

            if hook_option_opt.get_as_boolean('with_new_dependency') is True:
                rsv_stg_objects.RsvShotgunHookOpt(
                    rsv_scene_properties,
                    hook_option_opt
                ).execute_new_dependency_create()
            # shotgun
            if hook_option_opt.get_as_boolean('with_shotgun_file') is True:
                rsv_stg_objects.RsvShotgunHookOpt(
                    rsv_scene_properties,
                    hook_option_opt
                ).execute_shotgun_file_export()

            if hook_option_opt.get_as_boolean('with_shotgun_dependency') is True:
                rsv_stg_objects.RsvShotgunHookOpt(
                    rsv_scene_properties,
                    hook_option_opt
                ).set_dependency_export()
            # link version
            if hook_option_opt.get_as_boolean('with_version_link') is True:
                rsv_stg_objects.RsvShotgunHookOpt(
                    rsv_scene_properties,
                    hook_option_opt
                ).execute_version_link()
            # lock last
            if hook_option_opt.get_as_boolean('with_version_lock') is True:
                rsv_stg_objects.RsvShotgunHookOpt(
                    rsv_scene_properties,
                    hook_option_opt
                ).execute_version_lock()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxresolver.core as rsv_core

    import lxshotgun.rsv.scripts as rsv_stg_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFile.get_is_exists(any_scene_file_path) is True:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                create_shotgun_qc_task = hook_option_opt.get_as_boolean('create_shotgun_qc_task')
                if create_shotgun_qc_task is True:
                    rsv_stg_objects.RsvShotgunHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    ).create_qc_stg_task()
                #
                create_shotgun_qc_version = hook_option_opt.get_as_boolean('create_shotgun_qc_version')
                if create_shotgun_qc_version is True:
                    rsv_stg_objects.RsvShotgunHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    ).create_qc_stg_version()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

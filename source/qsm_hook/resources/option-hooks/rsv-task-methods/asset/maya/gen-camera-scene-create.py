# coding:utf-8


def main(session):
    import lxresolver.core as rsv_core

    import qsm_hook_maya.rsv.objects as mya_rsv_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        resolver = rsv_core.RsvBase.generate_root()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            create_scene_src = hook_option_opt.get('create_scene_src') or False
            if create_scene_src is True:
                mya_rsv_objects.RsvDccSceneHookOpt(
                    rsv_scene_properties,
                    hook_option_opt,
                ).set_asset_camera_scene_src_create()
            #
            with_work_scene_src = hook_option_opt.get('with_work_scene_src') or False
            if with_work_scene_src is True:
                pass
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
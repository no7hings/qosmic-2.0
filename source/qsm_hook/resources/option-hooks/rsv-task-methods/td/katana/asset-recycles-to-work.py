# coding:utf-8


def main(session):
    import lxresolver.core as rsv_core

    import qsm_hook_general.rsv.objects as gnl_rsv_objects

    hook_option_opt = session.option_opt

    file_path = hook_option_opt.get('file')

    r = rsv_core.RsvBase.generate_root()

    rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(file_path)

    if rsv_scene_properties:
        convert_maya_to_katana_enable = hook_option_opt.get_as_boolean('convert_maya_to_katana_enable')
        if convert_maya_to_katana_enable is True:
            gnl_rsv_objects.RsvRecyclerHookOpt(
                rsv_scene_properties, hook_option_opt
            ).set_katana_create()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

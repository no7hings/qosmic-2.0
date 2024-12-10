# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxresolver.core as rsv_core

    import qsm_prc_general.rsv.objects as gnl_rsv_objects

    import lxsession.commands as ssn_commands

    hook_option_opt = session.option_opt

    recycles_maya_file_paths = hook_option_opt.get_as_array('recycles_maya_files')

    file_path = hook_option_opt.get('file')

    r = rsv_core.RsvBase.generate_root()

    rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(file_path)

    if rsv_scene_properties:
        if recycles_maya_file_paths is not None:
            # recycles xgen and texture first
            # xgen
            recycles_xgen_enable = hook_option_opt.get_as_boolean('recycles_xgen_enable')
            if recycles_xgen_enable is True:
                gnl_rsv_objects.RsvRecyclerHookOpt(
                    rsv_scene_properties, hook_option_opt
                ).set_xgen_recycles()
            # texture
            recycles_texture_enable = hook_option_opt.get_as_boolean('recycles_texture_enable')
            if recycles_texture_enable is True:
                gnl_rsv_objects.RsvRecyclerHookOpt(
                    rsv_scene_properties, hook_option_opt
                ).set_texture_recycles()
            # sp and zb
            recycles_sp_enable = hook_option_opt.get_as_boolean('recycles_sp_enable')
            if recycles_sp_enable is True:
                gnl_rsv_objects.RsvRecyclerHookOpt(
                    rsv_scene_properties, hook_option_opt
                ).set_sp_recycles()
            recycles_zb_enable = hook_option_opt.get_as_boolean('recycles_zb_enable')
            if recycles_zb_enable is True:
                gnl_rsv_objects.RsvRecyclerHookOpt(
                    rsv_scene_properties, hook_option_opt
                ).set_zb_recycles()
            # recycles maya last, need repath
            recycles_maya_enable = hook_option_opt.get_as_boolean('recycles_maya_enable')
            if recycles_maya_enable is True:
                gnl_rsv_objects.RsvRecyclerHookOpt(
                    rsv_scene_properties, hook_option_opt
                ).set_maya_recycles()
            #
            convert_maya_to_katana_enable = hook_option_opt.get_as_boolean('convert_maya_to_katana_enable')
            if convert_maya_to_katana_enable is True:
                option_opt = bsc_core.ArgDictStringOpt(
                    option=dict(
                        option_hook_key='rsv-task-methods/td/katana/asset-recycles-to-work',
                        #
                        file=file_path,
                        #
                        user=hook_option_opt.get('user'),
                        time_tag=hook_option_opt.get('time_tag'),
                        # convert
                        convert_maya_to_katana_enable=hook_option_opt.get('convert_maya_to_katana_enable'),
                        #
                        td_enable=hook_option_opt.get('td_enable'),
                        test_flag=hook_option_opt.get('test_flag'),
                    )
                )
                #
                ssn_commands.execute_option_hook_by_deadline(
                    option=option_opt.to_string()
                )
        else:
            raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

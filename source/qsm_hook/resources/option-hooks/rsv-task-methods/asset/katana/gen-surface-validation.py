# coding:utf-8


def main(session):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxresolver.core as rsv_core

    import qsm_hook_general.rsv.objects as gnl_rsv_objects

    import lxkatana.core as ktn_core

    import lxkatana.dcc.objects as ktn_dcc_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    validation_checker = session.get_validation_checker()
    validation_checker.set_data_restore()

    if any_scene_file_path is not None:
        resolver = rsv_core.RsvBase.generate_root()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            if ktn_core.KtnUtil.get_is_ui_mode():
                bsc_log.Log.trace_method_result(
                    'surface validation running',
                    'mode="ui-mode"'
                )
            else:
                bsc_log.Log.trace_method_result(
                    'surface validation running',
                    'mode="command"'
                )
                ktn_dcc_objects.Scene.open_file(any_scene_file_path)
            #
            hook_opt = gnl_rsv_objects.RsvDccValidationHookOpt(rsv_scene_properties, hook_option_opt)
            #
            method_args = [
                ('with_shotgun_check', hook_opt.execute_shotgun_check, (validation_checker,)),
                #
                ('with_scene_check', hook_opt.execute_katana_scene_check, (validation_checker,)),
                #
                ('with_geometry_check', hook_opt.execute_katana_geometry_check, (validation_checker,)),
                ('with_geometry_topology_check', hook_opt.execute_katana_geometry_topology_check, (validation_checker,)),
                #
                ('with_look_check', hook_opt.execute_katana_look_check, (validation_checker,)),
                #
                ('with_texture_check', hook_opt.execute_katana_texture_check, (validation_checker,)),
                ('with_texture_workspace_check', hook_opt.execute_katana_texture_workspace_check, (validation_checker,)),
            ]
            method_args_valid = [
                i for i in method_args if hook_option_opt.get_as_boolean(i[0]) is True
            ]
            if method_args_valid:
                with bsc_log.LogProcessContext.create(
                    maximum=len(method_args_valid),
                    label='execute check method'
                ) as g_p:
                    for i_key, i_fnc, i_args in method_args_valid:
                        g_p.do_update()
                        #
                        i_fnc(*i_args)
            #
            validation_checker.set_data_record()
        else:
            raise RuntimeError(
                'option-hook execute',
                u'file="{}" is not available'.format(
                    any_scene_file_path
                )
            )
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

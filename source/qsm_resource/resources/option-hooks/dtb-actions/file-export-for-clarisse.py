# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxsession.commands as ssn_command

    import lxgui.core as gui_core

    dtb_opt = session.get_database_opt()

    if dtb_opt:
        option_opt = session.option_opt
        resource_path = option_opt.get('resource')
        file_type_path = option_opt.get('file_type')
        file_path = option_opt.get('file')
        dtb_types = dtb_opt.get_resource_type_paths(
            resource_path
        )
        type_path = dtb_types[0]

        type_path_opt = bsc_core.BscNodePathOpt(type_path)
        type_path_opt = type_path_opt.to_dcc()
        resource_path_opt = bsc_core.BscNodePathOpt(resource_path)
        resource_path_opt = resource_path_opt.to_dcc()
        file_type_path_opt = bsc_core.BscNodePathOpt(file_type_path)
        file_type_path_opt = file_type_path_opt.to_dcc()

        resource_location = '{}/{}'.format(
            type_path_opt.to_string(),
            resource_path_opt.get_name()
        )

        location = '/library{}/{}{}'.format(
            type_path_opt.to_string(),
            resource_path_opt.get_name(),
            file_type_path_opt.to_string()
        )

        ssn_command.execute_option_hook(
            bsc_core.ArgDictStringOpt(
                dict(
                    option_hook_key='dtb-actions/any-file-to-clarisse-new',
                    location=location,
                    resource_location=resource_location,
                    file_type=file_type_path,
                    file_type_name=file_type_path_opt.get_name(),
                    file=file_path,
                    port=gui_core.GuiHistory.get_latest('tool-panels.clarisse-socket-connection.port')
                )
            ).to_string()
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

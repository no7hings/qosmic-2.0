# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.core as gui_core


class ScpImport(object):
    def __init__(self, session, dtb_opt, dtb_resource, file_type_path, port):
        self.__session = session
        self.__dtb_opt = dtb_opt
        self.__dtb_resource = dtb_resource
        self.__file_type_path = file_type_path
        self.__port = port

    def execute(self):
        import lxbasic.database as bsc_database

        import lxsession.commands as ssn_command

        dtb_opt = self.__dtb_opt

        resource_path = self.__dtb_resource.path
        version_path = '{}/v0001'.format(resource_path)
        dtb_version = self.__dtb_opt.get_dtb_version(version_path)
        dtb_version_opt = bsc_database.DtbNodeOptForRscVersion(dtb_opt, dtb_version)
        file_type_path = self.__file_type_path
        if file_type_path == '/geometry/abc':
            file_path = dtb_version_opt.get_geometry_abc_file()
        elif file_type_path == '/geometry/usd':
            file_path = dtb_version_opt.get_geometry_usd_file()
        elif file_type_path == '/geometry/fbx':
            file_path = dtb_version_opt.get_geometry_fbx_file()
        else:
            raise TypeError()

        if file_path is not None:
            dtb_types = dtb_opt.get_resource_type_paths(
                resource_path
            )
            type_path = dtb_types[0]

            type_path_opt = bsc_core.BscPathOpt(type_path)
            type_path_opt = type_path_opt.to_dcc()
            resource_path_opt = bsc_core.BscPathOpt(resource_path)
            resource_path_opt = resource_path_opt.to_dcc()
            file_type_path_opt = bsc_core.BscPathOpt(file_type_path)
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
                        port=self.__port
                    )
                ).to_string()
            )


def main(session):
    def ok_fnc_():
        import lxgeneral.dcc.core as gnl_dcc_core

        _kwargs = o.to_dict()
        _file_type_key = o.get('file_type')
        _port = o.get('port')

        if gnl_dcc_core.SocketConnectForClarisse(_port).get_is_valid() is True:
            _file_type_path = file_type_path_mapper[_file_type_key]
            with w.gui_progressing(maximum=len(dtb_resources)) as g_p:
                for _i_dtb_resource in dtb_resources:
                    ScpImport(session, dtb_opt, _i_dtb_resource, _file_type_path, _port).execute()
                    g_p.do_update()

    file_type_path_mapper = {
        'ABC': '/geometry/abc',
        'USD': '/geometry/usd',
        'FBX': '/geometry/fbx'
    }

    # get checked resources
    window = session.get_window()
    gui_resource_opt = window._gui_resource_opt
    dtb_resources = gui_resource_opt.get_checked_or_selected_db_resources()
    if not dtb_resources:
        gui_core.GuiDialog.create(
            label=window.get_window_title(),
            sub_label='{}'.format(session.gui_name),
            content='check or select one or more items and retry',
            status=gui_core.GuiDialog.ValidationStatus.Warning,
            #
            ok_label='Close',
            #
            no_visible=False, cancel_visible=False
        )
        return
    #
    dtb_opt = session.get_database_opt()
    session.reload_configure()
    if dtb_opt:
        base_variants = dict(root=dtb_opt.get_stg_root())
        #
        geometry_abc_file_p = dtb_opt.get_pattern(keyword='geometry-abc-file')
        geometry_abc_file_p_o = bsc_core.PtnStgParseOpt(geometry_abc_file_p)
        geometry_abc_file_p_o.update_variants(**base_variants)
        #
        window = session.get_window()
        w = gui_core.GuiDialog.create(
            label=window.get_window_title(),
            sub_label='{}, {} Resources is Checked'.format(session.gui_name, len(dtb_resources)),
            status=gui_core.GuiDialog.ValidationStatus.Active,
            content=session.configure.get('build.content'),
            #
            options_configure=session.configure.get('build.node.options'),
            #
            ok_method=ok_fnc_,
            ok_label='Apply and Close',
            ok_visible=True,
            no_visible=False,
            #
            cancel_label='Close',
            #
            show=False,
            #
            window_size=session.gui_configure.get('size'),
            #
            parent=window.widget if window else None,
            #
            use_exec=False,
            use_window_modality=False,
            use_thread=False
        )

        o = w.get_options_node()

        w.set_window_show()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

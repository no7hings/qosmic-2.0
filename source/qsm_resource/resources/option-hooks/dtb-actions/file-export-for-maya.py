# coding:utf-8


def main(session):
    import lxbasic.dcc.core as bsc_dcc_core
    #
    window = session.get_window()
    dtb_opt = session.get_database_opt()

    if dtb_opt:
        option_opt = session.option_opt
        resource_path = option_opt.get('resource')
        file_type = option_opt.get('file_type')
        file_path = option_opt.get('file')
        dtb_types = dtb_opt.get_resource_type_paths(
            resource_path
        )
        type_path = dtb_types[0]
        data = dict(
            resource_type=type_path,
            resource=resource_path,
            file_type=file_type,
            file=file_path,
        )
        cmd = """import lxmaya.scripts as mya_scripts;mya_scripts.ScpMayaNetImport({}).execute()""".format(str(data))
        bsc_dcc_core.SocketConnectForMaya().run(cmd)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

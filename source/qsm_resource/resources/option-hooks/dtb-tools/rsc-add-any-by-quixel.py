# coding:utf-8


def main(session):
    def yes_fnc_():
        _quixel_json_files = o.get('quixel_json_files')
        with w.gui_progressing(maximum=len(_quixel_json_files)) as _g_p:
            _scp = lib_scripts.ScpResourcesAddByQuixel()
            for _i_quixel_json_file in _quixel_json_files:
                _g_p.do_update()
                _scp.add_resource_by_any_json(_i_quixel_json_file)
            #
            # _scp.accept()

    def show_quixel_json_files_fnc_():
        _directory_path_src = o.get('directory')
        _quixel_json_files = bsc_storage.StgDirectoryOpt(
            _directory_path_src
        ).get_all_file_paths(
            ext_includes=['.json']
        )
        if o.get('ignore_exists') is True:
            _quixel_json_files = [
                _i for _i in _quixel_json_files
                if lib_scripts.ScpResourcesAddByQuixel._check_resource_exists(_i) is False
            ]
        o.set('quixel_json_files', _quixel_json_files)

    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxgui.core as gui_core

    import lxtool.library.scripts as lib_scripts

    dtb_opt = session.get_database_opt()
    if dtb_opt:
        window = session.get_window()
        w = gui_core.GuiDialog.create(
            label=window.get_window_title(),
            sub_label=session.gui_name,
            status=gui_core.GuiDialog.ValidationStatus.Active,
            content=(
                '1. add quixel json files, you can use "a or b" or "a and b"\n'
                '    a. choose a "directory" and press "show all quixel json files" in "quixel json files";\n'
                '    b. add files in "quixel json files";\n'
                '2. press "add resources" to continue'
            ),
            #
            options_configure=session.configure.get('build.node.options'),
            #
            # yes_label='Confirm',
            yes_visible=False,
            no_visible=False,
            cancel_label='Close',
            #
            show=False,
            #
            window_size=session.gui_configure.get('size'),
            #
            parent=window.widget if window else None,
            #
            use_exec=False,
            #
            # use_window_modality=False
        )

        o = w.get_options_node()

        o.get_port('show_all_quixel_json_files').set(show_quixel_json_files_fnc_)
        o.get_port('add_resources').set(yes_fnc_)

        w.set_window_show()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

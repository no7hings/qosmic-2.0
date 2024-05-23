# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxbasic.database as bsc_database

    import lxarnold.scripts as and_scripts

    import lxgui.core as gui_core

    import lxgui.proxy.abstracts as gui_prx_abstracts

    class CreateMtd(gui_prx_abstracts.AbsQtThreadProcessBase):
        def __init__(self):
            super(CreateMtd, self).__init__(session.name, w, button)

        def build_for_data(self):
            _file_paths = files_p.get_all(check_only=True)
            #
            _with_acescg_exr = o.get('with_acescg_exr')
            _with_acescg_tx = o.get('with_acescg_tx')
            #
            _use_update_mode = o.get('use_update_mode')
            #
            _scp = and_scripts.ScpTextureCreate()
            # _scp.setup()
            with w.gui_progressing(maximum=len(_file_paths)) as _g_p:
                for _i_texture_original_src_file_path in _file_paths:
                    _g_p.do_update()
                    #
                    _i_texture_original_src_file_opt = bsc_storage.StgFileOpt(_i_texture_original_src_file_path)
                    _i_variants = texture_original_src_directory_p_o.get_variants(
                        _i_texture_original_src_file_opt.get_directory_path()
                    )
                    #
                    _i_texture_acescg_src_directory_path = texture_acescg_src_directory_pattern_opt.update_variants_to(
                        **_i_variants
                    ).get_value()
                    bsc_storage.StgPermissionMtd.create_directory(_i_texture_acescg_src_directory_path)
                    #
                    _i_texture_acescg_tx_directory_path = texture_acescg_tx_directory_pattern_opt.update_variants_to(
                        **_i_variants
                    ).get_value()
                    bsc_storage.StgPermissionMtd.create_directory(_i_texture_acescg_tx_directory_path)
                    #
                    _i_texture_acescg_src_exr_file_path = '{}/{}.exr'.format(
                        _i_texture_acescg_src_directory_path, _i_texture_original_src_file_opt.name_base
                    )
                    _i_texture_acescg_tx_file_path = '{}/{}.tx'.format(
                        _i_texture_acescg_tx_directory_path, _i_texture_original_src_file_opt.name_base
                    )
                    #
                    self.append_cmd(
                        (
                            _scp.generate_exr_create_cmd_as_acescg(
                                _i_texture_original_src_file_path, _i_texture_acescg_src_exr_file_path,
                                use_update_mode=_use_update_mode
                            ),
                            _scp.generate_tx_create_cmd_as_acescg(
                                _i_texture_acescg_src_exr_file_path, _i_texture_acescg_tx_file_path,
                                use_update_mode=_use_update_mode
                            ),
                        )
                    )

    def get_all_file_paths_fnc_():
        _list = []
        _formats = map(lambda x: str(x).strip(), o.get('deduplication_priority_formats').split(','))
        #
        with w.gui_progressing(maximum=len(dtb_resources)) as _g_p:
            for _i_dtb_resource in dtb_resources:
                _g_p.do_update()
                #
                _i_dtb_resource_opt = bsc_database.DtbNodeOpt(dtb_opt, _i_dtb_resource)
                #
                _i_dtb_version = _i_dtb_resource_opt.get_as_node('version')
                _i_dtb_version_opt = bsc_database.DtbNodeOpt(dtb_opt, _i_dtb_version)
                _i_version_directory_path = _i_dtb_version_opt.get('location')
                #
                _i_directory_stg_path = '{}{}'.format(_i_version_directory_path, '/texture/original/src')
                _i_directory_opt = bsc_storage.StgDirectoryOpt(_i_directory_stg_path)
                _i_file_paths = _i_directory_opt.get_file_paths(ext_includes=map(lambda x: '.{}'.format(x), _formats))
                _list.extend(_i_file_paths)
        return _list

    def deduplication_fnc_():
        _formats = map(lambda x: str(x).strip(), o.get('deduplication_priority_formats').split(','))
        _file_paths_as_dd = bsc_storage.StgPathMtd.deduplication_files_by_formats(
            file_paths, _formats
        )
        files_p.set_unchecked_by_include_paths(_file_paths_as_dd)
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
        #
        base_variants = dict(root=dtb_opt.get_stg_root())
        #
        texture_original_src_directory_p = dtb_opt.get_pattern(keyword='texture-original-src-dir')
        texture_original_src_directory_p_o = bsc_core.PtnStgParseOpt(texture_original_src_directory_p)
        texture_original_src_directory_p_o.update_variants(**base_variants)
        #
        texture_acescg_src_directory_pattern = dtb_opt.get_pattern(keyword='texture-acescg-src-dir')
        texture_acescg_src_directory_pattern_opt = bsc_core.PtnStgParseOpt(texture_acescg_src_directory_pattern)
        texture_acescg_src_directory_pattern_opt.update_variants(**base_variants)
        #
        texture_acescg_tx_directory_pattern = dtb_opt.get_pattern(keyword='texture-acescg-tx-dir')
        texture_acescg_tx_directory_pattern_opt = bsc_core.PtnStgParseOpt(texture_acescg_tx_directory_pattern)
        texture_acescg_tx_directory_pattern_opt.update_variants(**base_variants)
        #
        w = gui_core.GuiDialog.create(
            label=window.get_window_title(),
            sub_label='{}'.format(session.gui_name),
            status=gui_core.GuiDialog.ValidationStatus.Active,
            content=session.configure.get('build.content'),
            #
            options_configure=session.configure.get('build.node.options'),
            #
            ok_visible=False,
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
            use_window_modality=False
        )
        o = w.get_options_node()

        scp = and_scripts.ScpTextureCreate()
        # scp.setup()
        button = o.get_port('execute')
        mtd = CreateMtd()
        button.set(mtd.execute)

        w.set_window_show()

        file_paths = get_all_file_paths_fnc_()
        files_p = o.get_port('files')
        files_p.set(file_paths)

        deduplication_fnc_()
        o.set('deduplication', deduplication_fnc_)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

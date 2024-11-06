# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxgeneral.dcc.core as gnl_dcc_core

import lxbasic.storage as bsc_storage

import lxbasic.database as bsc_database

import lxgui.core as gui_core

import lxgui.proxy.abstracts as gui_prx_abstracts


def main(session):
    class CreateMtd(gui_prx_abstracts.AbsQtThreadProcessBase):
        def __init__(self):
            super(CreateMtd, self).__init__(session.name, w, button)

        def build_for_data(self):
            _file_paths = files_p.get_all(check_only=True)
            _use_update_mode = o.get('use_update_mode')
            with w.gui_progressing(maximum=len(_file_paths)) as _g_p:
                for _i_fbx_file_path in _file_paths:
                    _g_p.do_update()
                    #
                    _i_fbx_file_opt = bsc_storage.StgFileOpt(_i_fbx_file_path)
                    #
                    _i_variants = geometry_fbx_directory_p_o.get_variants(_i_fbx_file_opt.get_directory_path())
                    #
                    _i_usd_directory_path = geometry_usd_directory_p_o.update_variants_to(**_i_variants).get_value()
                    _i_usd_file_path = '{}/{}.usd'.format(_i_usd_directory_path, _i_fbx_file_opt.get_name_base())
                    if _use_update_mode is True:
                        if _i_fbx_file_opt.get_timestamp_is_same_to(_i_usd_file_path) is True:
                            bsc_log.Log.trace_method_warning(
                                'fbx to usd',
                                'non changed update for "{}"'.format(
                                    _i_usd_file_path
                                )
                            )
                            continue
                    #
                    self.append_cmd(
                        gnl_dcc_core.MayaProcess.generate_cmd_script(
                            'method=fbx-to-usd&fbx={}&usd={}&use_update_mode={}'.format(
                                _i_fbx_file_path,
                                _i_usd_file_path,
                                _use_update_mode,
                            )
                        )
                    )

    def get_all_file_paths_fnc_():
        _list = []
        with w.gui_progressing(maximum=len(dtb_resources)) as _g_p:
            for _i_dtb_resource in dtb_resources:
                _g_p.do_update()
                _i_dtb_resource_opt = bsc_database.DtbNodeOpt(dtb_opt, _i_dtb_resource)
                #
                _i_dtb_version = _i_dtb_resource_opt.get_as_node('version')
                _i_storage_dtb_path = '{}/{}'.format(_i_dtb_version.path, 'geometry_fbx_directory')
                _i_directory_stg_path = dtb_opt.get_property(
                    _i_storage_dtb_path, 'location'
                )
                _i_fbx_directory_opt = bsc_storage.StgDirectoryOpt(_i_directory_stg_path)
                _i_fbx_file_paths = _i_fbx_directory_opt.get_file_paths(ext_includes=['.fbx'])
                _list.extend(_i_fbx_file_paths)
        return _list
    # get checked resources
    window = session.find_window()
    gui_resource_opt = window._gui_asset_prx_unit
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
    dtb_opt = session.get_database_opt(disable_new_connection=True)
    session.reload_configure()
    if dtb_opt:
        base_variants = dict(root=dtb_opt.get_stg_root())
        #
        geometry_fbx_directory_p = dtb_opt.get_pattern(keyword='geometry-fbx-dir')
        geometry_fbx_directory_p_o = bsc_core.BscStgParseOpt(geometry_fbx_directory_p)
        geometry_fbx_directory_p_o.update_variants(**base_variants)
        #
        geometry_usd_directory_p = dtb_opt.get_pattern(keyword='geometry-usd-dir')
        geometry_usd_directory_p_o = bsc_core.BscStgParseOpt(geometry_usd_directory_p)
        geometry_usd_directory_p_o.update_variants(**base_variants)
        #
        window = session.find_window()
        w = gui_core.GuiDialog.create(
            label=window.get_window_title(),
            sub_label='{}, {} Resources is Checked'.format(session.gui_name, len(dtb_resources)),
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

        file_paths = get_all_file_paths_fnc_()

        files_p = o.get_port('files')
        files_p.set(file_paths)

        button = o.get_port('execute')
        mtd = CreateMtd()
        button.set(mtd.execute)

        w.show_window_auto()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.dcc.core as bsc_dcc_core

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
                for _i_scene_maya_file_path in _file_paths:
                    _g_p.do_update()
                    #
                    _i_dtb_version_opt = version_opt_mapper[_i_scene_maya_file_path]
                    #
                    _i_scene_maya_file_opt = bsc_storage.StgFileOpt(_i_scene_maya_file_path)
                    #
                    _i_geometry_usd_file_path = _i_dtb_version_opt.get_file('geometry-usd-file')
                    if _use_update_mode is True:
                        if _i_scene_maya_file_opt.get_timestamp_is_same_to(_i_geometry_usd_file_path) is True:
                            bsc_log.Log.trace_method_warning(
                                'scene to usd',
                                'non changed update for "{}"'.format(
                                    _i_geometry_usd_file_path
                                )
                            )
                            continue
                    #
                    _i_geometry_abc_file_path = _i_dtb_version_opt.get_file('geometry-abc-file')
                    #
                    self.append_cmd(
                        bsc_dcc_core.MayaProcess.generate_command(
                            bsc_core.ArgDictStringOpt(
                                option=dict(
                                    method='scene-to-geometry',
                                    scene_maya_file=_i_scene_maya_file_path,
                                    #
                                    with_geometry_usd=o.get('with_geometry_usd'),
                                    geometry_usd_file=_i_geometry_usd_file_path,
                                    #
                                    with_geometry_abc=o.get('with_geometry_abc'),
                                    geometry_abc_file=_i_geometry_abc_file_path,
                                    use_update_mode=_use_update_mode,
                                )
                            ).to_string()
                        )
                    )

    def get_all_file_paths_fnc_():
        _dict = {}
        _list = []
        with w.gui_progressing(maximum=len(dtb_resources)) as _g_p:
            for _i_dtb_resource in dtb_resources:
                _g_p.do_update()
                _i_dtb_resource_opt = bsc_database.DtbNodeOpt(dtb_opt, _i_dtb_resource)
                #
                _i_dtb_version = _i_dtb_resource_opt.get_as_node('version')
                _i_dtb_version_opt = bsc_database.DtbNodeOptForRscVersion(dtb_opt, _i_dtb_version)
                _i_scene_maya_file_path = _i_dtb_version_opt.get_exists_file('scene-maya-file')
                if _i_scene_maya_file_path:
                    _i_types = _i_dtb_version_opt.get_types()
                    _dict[_i_scene_maya_file_path] = _i_dtb_version_opt
                    _list.append(_i_scene_maya_file_path)
        return _list, _dict
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
            yes_label='Close',
            #
            no_visible=False, cancel_visible=False
        )
        return
    #
    dtb_opt = session.get_database_opt(disable_new_connection=True)
    session.reload_configure()
    if dtb_opt:
        window = session.get_window()
        w = gui_core.GuiDialog.create(
            label=window.get_window_title(),
            sub_label='{}, {} Resources is Checked'.format(session.gui_name, len(dtb_resources)),
            status=gui_core.GuiDialog.ValidationStatus.Active,
            content=session.configure.get('build.content'),
            #
            options_configure=session.configure.get('build.node.options'),
            #
            yes_visible=False,
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

        button = o.get_port('execute')
        mtd = CreateMtd()
        button.set(mtd.execute)

        w.set_window_show()

        file_paths, version_opt_mapper = get_all_file_paths_fnc_()
        files_p = o.get_port('files')
        files_p.set(file_paths)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
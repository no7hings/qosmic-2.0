# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.core as gui_core


def main(session):
    def ok_fnc_():
        import lxgeneral.dcc.core as gnl_dcc_core

        s_c = gnl_dcc_core.SocketConnectForMaya()
        if s_c.is_valid():
            print 'AAA'

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
    dtb_opt = session.get_database_opt()
    session.reload_configure()
    if dtb_opt:
        base_variants = dict(root=dtb_opt.get_stg_root())
        #
        proxy_ass_file_p = dtb_opt.get_pattern(keyword='proxy-ass-file')
        proxy_ass_file_p_o = bsc_core.BscStgParseOpt(proxy_ass_file_p)
        proxy_ass_file_p_o.update_variants(**base_variants)
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
        button = o.get_port('execute')
        button.set(ok_fnc_)

        w.show_window_auto()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

# coding:utf-8


def main(session):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxgui.proxy.core as gui_prx_core

    import lxtool.kit.gui.widgets as kit_gui_widgets

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
        kit_gui_widgets.DesktopToolKit, session=session
    )

    shell_start_m = bsc_core.EnvBaseMtd.get('shell_start_m')
    shell_start_s = bsc_core.EnvBaseMtd.get('shell_start_s')
    if shell_start_m and shell_start_s:
        end_m = bsc_core.SysBaseMtd.get_minute()
        end_s = bsc_core.SysBaseMtd.get_second()
        #
        bsc_log.Log.trace_method_result(
            'window show',
            'cost: {}s'.format(
                (end_m - int(shell_start_m))*60+(end_s-int(shell_start_s))
            )
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

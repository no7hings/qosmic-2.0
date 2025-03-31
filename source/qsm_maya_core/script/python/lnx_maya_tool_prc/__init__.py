# coding:utf-8


def do_reload():
    import lxbasic.core as bsc_core

    bsc_core.PyReloader2(
        [
            'lxbasic', 'lxsession',
            'qsm_general', 'lnx_scan', 'lnx_shark', 'lnx_screw',
            'qsm_maya', 'lnx_maya_tool_prc'
        ]
    ).do_reload()

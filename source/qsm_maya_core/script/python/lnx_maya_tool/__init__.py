# coding:utf-8


def do_reload():
    import lxbasic.core as bsc_core

    bsc_core.PyReloader2(
        [
            'lxbasic', 'lxsession', 'lxgui',

            'qsm_general', 'lnx_scan', 'lnx_screw', 'lnx_shark', 'qsm_lazy', 'qsm_lazy_tool',
            'qsm_maya', 'lnx_maya_gui', 'lnx_maya_tool_prc', 'lnx_maya_tool',
        ]
    ).do_reload()

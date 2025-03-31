# coding:utf-8


def do_reload():
    import lxbasic.core as bsc_core

    bsc_core.PyReloader2(
        [
            'lxbasic', 'lxsession', 'lxgui',

            'qsm_general', 'lnx_scan', 'lnx_screw', 'lnx_shark', 'qsm_lazy', 'qsm_lazy_tool', 'lnx_wotrix',
            'qsm_maya', 'lnx_maya_gui', 'qsm_maya_lazy', 'qsm_maya_lazy_tool', 'lnx_maya_wotrix',
        ]
    ).do_reload()

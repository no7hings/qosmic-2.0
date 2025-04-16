# coding:utf-8


def do_reload():
    import lxbasic.core as bsc_core

    bsc_core.PyReloader2(
        [
            'lxbasic', 'lxsession', 'lxgui',

            'qsm_general', 'lnx_screw', 'lnx_parsor', 'lnx_dcc_tool_prc', 'lnx_dcc_tool',
            'lnx_wotrix', 'lnx_wotrix_tasks',
            'qsm_maya', 'lnx_maya_gui',
            'lnx_maya_wotrix', 'lnx_maya_wotrix_tasks',
        ]
    ).do_reload()

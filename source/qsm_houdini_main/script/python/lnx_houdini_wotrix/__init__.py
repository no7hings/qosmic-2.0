# coding:utf-8


def do_reload():
    import lxbasic.core as bsc_core

    bsc_core.PyReloader2(
        [
            'lxbasic', 'lxsession', 'lxgui',

            'qsm_general', 'lnx_screw', 'lnx_shark', 'lnx_dcc_tool_prc', 'lnx_dcc_tool', 'lnx_wotrix',
            'lnx_houdini', 'lnx_houdini_wotrix',
        ]
    ).do_reload()

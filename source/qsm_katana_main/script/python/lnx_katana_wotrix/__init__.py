# coding:utf-8


def do_reload():
    import lxbasic.core as bsc_core

    bsc_core.PyReloader2(
        [
            'lxbasic', 'lxsession', 'lxgui',

            'qsm_general', 'lnx_screw', 'lnx_parsor', 'lnx_dcc_tool_prc', 'lnx_dcc_tool',
            'lnx_wotrix', 'lnx_wotrix_tasks',
            'lnx_katana',
            'lnx_katana_wotrix', 'lnx_katana_wotrix_tasks',
        ]
    ).do_reload()

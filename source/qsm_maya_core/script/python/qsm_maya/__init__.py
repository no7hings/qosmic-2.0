# coding:utf-8


def do_reload():
    import lxbasic.core as bsc_core

    bsc_core.PyReloader2(
        [
            'lxbasic', 'lxsession', 'lxgui',
            'qsm_general', 'lnx_parsor', 'lnx_screw',
            'qsm_maya'
        ]
    ).do_reload()

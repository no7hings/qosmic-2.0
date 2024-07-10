# coding:utf-8


def do_reload():
    import lxbasic.core as bsc_core

    bsc_core.PyReloader2(
        [
            'lxbasic', 'lxsession',
            'qsm_general',
            'qsm_maya', 'qsm_maya_lazy'
        ]
    ).do_reload()

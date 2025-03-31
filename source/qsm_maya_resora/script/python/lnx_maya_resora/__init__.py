# coding:utf-8


def do_reload():
    import lxbasic.core as bsc_core

    bsc_core.PyReloader2(
        [
            'lxbasic', 'lxsession', 'lxgui',

            'qsm_general', 'lnx_scan', 'qsm_lazy', 'qsm_lazy_tool',
            'qsm_maya', 'lnx_maya_gui',
            'lnx_screw', 'lnx_resora', 'lnx_resora_extra',
            'lnx_maya_resora',
        ]
    ).do_reload()

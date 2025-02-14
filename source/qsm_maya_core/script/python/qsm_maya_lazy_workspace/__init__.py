# coding:utf-8


def do_reload():
    import lxbasic.core as bsc_core

    bsc_core.PyReloader2(
        [
            'lxbasic', 'lxsession', 'lxgui',

            'qsm_general', 'qsm_scan', 'qsm_screw', 'qsm_shark', 'qsm_lazy', 'qsm_lazy_tool', 'qsm_lazy_workspace',
            'qsm_maya', 'qsm_maya_gui', 'qsm_maya_lazy', 'qsm_maya_lazy_tool', 'qsm_maya_lazy_workspace',
        ]
    ).do_reload()

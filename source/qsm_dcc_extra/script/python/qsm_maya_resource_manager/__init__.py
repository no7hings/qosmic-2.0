# coding:utf-8


def do_reload():
    import lxbasic.core as bsc_core

    bsc_core.PyReloader2(
        [
            'lxbasic', 'lxgui',
            'qsm_general', 'qsm_gui',
            'qsm_maya', 'qsm_maya_gui',
            'qsm_maya_resource_manager',
        ]
    ).do_reload()

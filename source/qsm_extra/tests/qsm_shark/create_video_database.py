import qsm_lazy.screw.core as qsm_lzy_scr_core

import lxbasic.resource as bsc_resource


if __name__ == '__main__':
    stage = qsm_lzy_scr_core.Stage(
        'video'
    )

    # stage.connect()
    stage.initialize()

    stage.build()
    # stage.build_test('node')

    # print stage.create_node_root_group()
    # print stage.get_node('/a')
    # print stage.create_node_group('/node_template')
    # print stage.create_node('/node_template/test1')

    # stage.test()

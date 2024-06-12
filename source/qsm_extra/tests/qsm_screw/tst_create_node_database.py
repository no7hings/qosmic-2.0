import qsm_screw.core as qsm_scr_core

import lxbasic.resource as bsc_resource


if __name__ == '__main__':
    stage = qsm_scr_core.Stage(
        'Z:/libraries/screw/.database/node.db'
    )

    stage.connect()
    stage.initialize()

    stage.build(
        bsc_resource.RscExtendConfigure.get_as_content('screw/node')
    )
    stage.build_test('node')

    # print stage.create_node_root_group()
    # print stage.get_node('/a')
    # print stage.create_node_group('/node_template')
    # print stage.create_node('/node_template/test1')

    # stage.test()

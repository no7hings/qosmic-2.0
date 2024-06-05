import qsm_screw.core as qsm_scr_core

import lxbasic.resource as bsc_resource


if __name__ == '__main__':
    stage = qsm_scr_core.Stage(
        'Z:/libraries/screw/.database/easy-template.db'
    )

    stage.connect()
    stage.initialize()

    stage.build(
        bsc_resource.RscExtendConfigure.get_as_content('entity/easy-template')
    )
    stage.build_test('node')

    print stage.find_all(
        'Type', filters=[('category', 'is', 'group')]
    )

    # print stage.create_node_root()
    # print stage.get_node('/a')
    # print stage.create_node_group('/node_template')
    # print stage.create_node('/node_template/test1')

    # stage.test()

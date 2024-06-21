import qsm_screw.core as qsm_scr_core

import lxbasic.resource as bsc_resource


if __name__ == '__main__':

    for i in [
        'maya_node',
        # 'maya_node_graph',
    ]:

        stage = qsm_scr_core.Stage(
            i
        )
        stage.initialize()
        stage.build()

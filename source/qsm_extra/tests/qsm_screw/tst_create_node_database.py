import qsm_lazy.core as qsm_lzy_core

import lxbasic.resource as bsc_resource


if __name__ == '__main__':

    for i in [
        'maya_cfx',
        # 'maya_layout',
        # 'maya_motion',
        # 'maya_scene',
    ]:

        stage = qsm_lzy_core.Stage(
            i
        )
        stage.initialize()
        stage.build()

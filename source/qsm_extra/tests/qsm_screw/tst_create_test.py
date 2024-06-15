import qsm_screw.core as qsm_scr_core

import lxbasic.resource as bsc_resource


if __name__ == '__main__':

    stage = qsm_scr_core.Stage(
        'test'
    )
    #
    stage.connect()
    stage.build()

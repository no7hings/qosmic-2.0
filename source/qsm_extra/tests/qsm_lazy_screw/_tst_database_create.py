import qsm_screw.core as qsm_scr_core

import lxbasic.resource as bsc_resource


if __name__ == '__main__':

    for i in [
        # 'maya_cfx',
        # 'maya_layout',
        # 'maya_motion',
        # 'maya_scene',
        # 'motion_test',
        # 'asset_test',
        # 'audio_test',
        'video_test',
    ]:

        stage = qsm_scr_core.Stage(
            i
        )
        stage.build()

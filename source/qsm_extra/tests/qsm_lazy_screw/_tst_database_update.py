import qsm_lazy.screw.core as qsm_lzy_scr_core

import lxbasic.resource as bsc_resource


if __name__ == '__main__':

    for i in [
        # 'maya_cfx',
        # 'maya_layout',
        # 'maya_motion',
        # 'maya_scene',
        'asset_test',
        'motion_test',
        'video_test',
        'audio_test'
    ]:

        stage = qsm_lzy_scr_core.Stage(
            i
        )
        stage.update_types()

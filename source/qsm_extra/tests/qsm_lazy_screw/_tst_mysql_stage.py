import qsm_lazy.screw.core as qsm_lzy_scr_core


if __name__ == '__main__':

    for i_key in [
        # 'maya_cfx',
        # 'maya_layout',
        # 'maya_motion',
        # 'maya_scene',
        'motion_test',
        'asset_test'
    ]:
        stage_sqlite = qsm_lzy_scr_core.Stage(
            i_key, 'sqlite'
        )

        stage_mysql = qsm_lzy_scr_core.Stage(
            i_key, 'mysql'
        )
        stage_mysql.initialize()

        stage_mysql.copy_from(stage_sqlite)

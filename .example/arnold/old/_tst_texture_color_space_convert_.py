# coding:utf-8
import lxbasic.core as bsc_core

import lxarnold.startup as and_startup

# s = and_startup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019')
# s.set_run()
# # xgen lib
# s.add_environ_fnc('LD_LIBRARY_PATH', '/l/packages/pg/prod/maya/2019.2/platform-linux/Application/plug-ins/xgen/lib')
# s.add_environ_fnc('LD_LIBRARY_PATH', '/l/packages/pg/prod/maya/2019.2/platform-linux/Application/lib')

bsc_core.EnvBaseMtd.set(
    'OCIO', '/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'
)

if __name__ == '__main__':
    import lxarnold.core as and_core

    import lxbasic.core as bsc_core

    # i_cmd = and_core.AndTextureOpt.generate_format_convert_as_aces_command(
    #     '/data/e/myworkspace/td/lynxi/script/python/.resources/assets/library/light/stinson-beach.exr',
    #     '/data/e/myworkspace/td/lynxi/script/python/.resources/assets/library/light/acescg/src/stinson-beach.exr',
    #     'Utility - Linear - sRGB',
    #     'ACES - ACEScg'
    # )
    #
    # bsc_core.PrcBaseMtd.execute_as_block(
    #     i_cmd
    # )

    # i_cmd = and_core.AndTextureOpt.generate_create_tx_as_acescg_command(
    #     '/data/e/myworkspace/td/lynxi/script/python/.resources/assets/library/light/acescg/src/stinson-beach.exr',
    #     '/data/e/myworkspace/td/lynxi/script/python/.resources/assets/library/light/acescg/tx/stinson-beach.tx',
    #     'ACES - ACEScg',
    #     'ACES - ACEScg'
    # )
    #
    # bsc_core.PrcBaseMtd.execute_as_block(
    #     i_cmd
    # )

    i_cmd = and_core.AndTextureOpt.generate_format_convert_as_aces_command(
        '/data/e/myworkspace/td/lynxi/script/python/.resources/assets/library/txr/acescg/src/albedo.exr',
        '/data/e/myworkspace/td/lynxi/script/python/.resources/assets/library/txr/acescg/jpg/albedo.png',
        'ACES - ACEScg',
        'ACES - ACEScg'
    )

    bsc_core.PrcBaseMtd.execute_as_block(
        i_cmd
    )



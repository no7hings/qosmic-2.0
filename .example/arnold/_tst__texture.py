# coding:utf-8
import os

import lxarnold.startup as and_startup

and_startup.MtoaSetup('/data/e/workspace/lynxi/resource/module/linux/arnold').set_run()

os.environ['OCIO'] = '/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'

import lxarnold.core as and_core

import lxbasic.core as bsc_core

c = and_core.AndTextureOpt.generate_create_exr_as_acescg_command(
    file_path_src='/l/resource/srf/hdri/test_2/other/other/tomoco_studio_1k.acescg.exr',
    file_path_tgt='/l/resource/srf/hdri/test_2/other/other/tomoco_studio_1k.exr',
    color_space_src='ACES - ACEScg',
    color_space_tgt='linear'
)


print bsc_core.PrcBaseMtd.execute_with_result(
    c
)

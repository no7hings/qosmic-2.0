# coding:utf-8
import lxarnold.startup as and_startup

and_startup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

import os

os.environ['OCIO'] = '/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'

import lxarnold.core as and_core


f = '/l/prod/cjd/work/assets/chr/huayao/srf/surfacing/texture/cloth_04.opacity.1001.exr'

i_0 = and_core.AndImageOpt(f)

print i_0._info


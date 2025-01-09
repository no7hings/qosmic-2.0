# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxarnold.startup as and_startup

and_startup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

d_p = '/data/e/myworkspace/td/lynxi/script/python/.setup/arnold/shaders'


f = '/data/e/myworkspace/td/lynxi/script/python/.setup/arnold/shaders/osl_string_to_int.osl'

bsc_storage.OslFileMtd.compile(
    f
)

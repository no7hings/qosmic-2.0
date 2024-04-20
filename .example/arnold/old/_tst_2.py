# coding:utf-8
import lxbasic.dcc.objects as bsc_dcc_objects

import lxarnold.startup as and_startup

and_startup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

d_p = '/data/e/myworkspace/td/lynxi/script/python/.setup/arnold/shaders'

d = bsc_dcc_objects.StgDirectory(d_p)

for i_f_p in d.get_child_file_paths():
    i_f = bsc_dcc_objects.StgFile(i_f_p)
    if i_f.ext == '.osl':
        pass

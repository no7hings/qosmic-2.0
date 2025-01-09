# coding:utf-8
import lxbasic.log as bsc_log

import time

c = 10

print '■'

with bsc_log.LogProcessContext.create(maximum=c, label='test', use_as_progress_bar=True) as l_p:
    for i in range(c):
        # time.sleep(1)
        l_p.do_update()


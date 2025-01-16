# coding:utf-8

import lxbasic.core as bsc_core

import lxbasic.web as bsc_web

import qsm_lazy_backstage.worker as lzy_bks_worker

ts = []

time_tag = bsc_core.BscSystem.get_time_tag()
for i_index in range(15):
    i_cmd_script = r'rez-env python27 -- python -c "import time; time.sleep(5); print \"{}\""'.format(i_index)
    i_t = bsc_core.ThreadWorker.generate(i_cmd_script, i_index)
    # i_t.status_changed.connect_to(status_changed_fnc_)
    # i_t.finished.connect_to(finished_fnc_)
    # i_t.failed.connect_to(failed_fnc_)
    ts.append(i_t)

[x.do_wait_for_start() for x in ts]

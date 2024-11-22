# coding:utf-8
import qsm_lazy.backstage.process as lzy_bks_process


rtc = lzy_bks_process.TaskProcess(
    r'rez-env python27 -- python -c "import time; time.sleep(10); print \"B\"; print \"C\"; print \"{}\";raise RuntimeError()"'.format(
        u'错误'.encode('utf-8')
    )
).execute()

print rtc

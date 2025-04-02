# coding:utf-8
import lnx_backstage.worker as lzy_bks_worker


rtc = lzy_bks_worker.TaskSubprocess(
    r'rez-env python27 -- python -c "import time; time.sleep(10); print \"B\"; print \"C\"; print \"{}\";raise RuntimeError()"'.format(
        u'错误'.encode('utf-8')
    )
).execute()

print rtc

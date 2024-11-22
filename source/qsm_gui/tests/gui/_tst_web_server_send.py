# coding:utf-8
import lxbasic.web as bsc_web

import qsm_lazy.backstage.process as lzy_bks_process

skt = bsc_web.WebSocket(
    lzy_bks_process.NoticeWebServerBase.HOST, lzy_bks_process.NoticeWebServerBase.PORT
)

if skt.connect() is True:
    for i in range(2):
        i_options = dict(
            title='通知',
            message='拍屏结束了, 是否打开视频',
            ok_python_script='import os; os.startfile("Z:/temeporaries/dongchangbao/rig-test/test.mov")',
            status='normal'
        )

        skt.send(
            i_options
        )

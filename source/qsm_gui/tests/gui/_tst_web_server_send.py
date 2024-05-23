# coding:utf-8
import lxbasic.web as bsc_web

skt = bsc_web.WebSocket()

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

# coding:utf-8
import lxbasic.web as bsc_web

import qsm_lazy.backstage.worker as lzy_bks_worker

skt = bsc_web.WebSocket(
    lzy_bks_worker.NoticeWebServerBase.HOST, 12306
)

print skt.is_valid()

if skt.connect() is True:
    skt.send(
        'import maya.mel as mel; mel.eval("polyCube -w 1 -h 1 -d 1 -sx 1 -sy 1 -sz 1 -ax 0 1 0 -cuv 4 -ch 1;")'
    )



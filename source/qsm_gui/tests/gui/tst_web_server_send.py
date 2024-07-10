# coding:utf-8
import lxbasic.web as bsc_web

import qsm_task.process as qsm_tsk_process

skt = bsc_web.WebSocket(
    qsm_tsk_process.NoticeWebServerBase.HOST, 12306
)

print skt.is_valid()

if skt.connect() is True:
    skt.send(
        'import maya.mel as mel; mel.eval("polyCube -w 1 -h 1 -d 1 -sx 1 -sy 1 -sz 1 -ax 0 1 0 -cuv 4 -ch 1;")'
    )



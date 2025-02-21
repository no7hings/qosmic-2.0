# coding:utf-8
import os

os.environ['PATH'] += ';Y:/deploy/rez-packages/external/ffmpeg/6.0/platform-windows/bin'

import lxbasic.cv.core as bsc_cv_core

bsc_cv_core.VideoCaptureOpt(
    u'X:/videos/测试/测试.mp4'
).create_thumbnail(
    u'X:/videos/测试/测试.png'
)

# coding:utf-8
import os

os.environ['PATH'] += ';Y:/deploy/rez-packages/external/ffmpeg/6.0/platform-windows/bin'

import lxbasic.audio.core as c

c.AudioCaptureOpt(
    u'Z:/temporaries/tst_wav/测试.mp3'
).create_thumbnail(
    u'Z:/temporaries/tst_wav/测试.png', replace=True
)

c.AudioCaptureOpt(
    u'Z:/temporaries/tst_wav/测试.mp3'
).create_compress(
    u'Z:/temporaries/tst_wav/测试-small.mp3', replace=True
)
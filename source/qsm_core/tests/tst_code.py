# coding:utf-8
import lxbasic.web as bsc_web

import lxbasic.core as bsc_core

c = u'Z:/projects/QSM_TST/source/shots/A001_002 测试/A001_001_001/user.shared/cfx.cfx_cloth/main/maya/scenes/playblast/A001_001_001.cfx.cfx_cloth.main.v010.v015.mov'

a = bsc_web.UrlValue.quote(c)
print(a)
b = bsc_web.UrlValue.unquote(a)
print(b)


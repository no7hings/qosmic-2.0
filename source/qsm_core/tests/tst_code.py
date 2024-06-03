# coding:utf-8
import lxbasic.web as bsc_web

import lxbasic.core as bsc_core

c = u'Z:/temeporaries/dongchangbao/playblast_tool/董昌宝/test.export.v009.ma'

a = bsc_web.UrlValue.quote(c)
print a
b = bsc_web.UrlValue.unquote(a)
print b

print bsc_web.UrlValue.unquote('Z%3A%2Ftemeporaries%2Fdongchangbao%2Fplayblast_tool%2F%E8%91%A3%E6%98%8C%E5%AE%9D%2Ftest.export.v010.ma')

o = bsc_core.ArgDictStringOpt(
    'option_hook_key=dcc-process/maya-cache-process&method=playblast&file=Z%3A%2Ftemeporaries%2Fdongchangbao%2Fplayblast_tool%2F%E8%91%A3%E6%98%8C%E5%AE%9D%2Ftest.export.v010.ma&movie=Z%3A%2Ftemeporaries%2Fdongchangbao%2Fplayblast_tool%2F%E8%91%A3%E6%98%8C%E5%AE%9D%2Ftest.export.v010.mov&camera=|persp|perspShape&start_frame=0&end_frame=32&frame_step=1&width=1280&height=720&texture_enable=True&light_enable=False&shadow_enable=False'
)

print bsc_web.UrlValue.unquote(o.get('file'))

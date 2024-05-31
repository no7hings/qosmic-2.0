# coding:utf-8
import lxbasic.web as bsc_web

c = u'Z:/temeporaries/dongchangbao/playblast_tool/董昌宝/test.export.v009.ma'

a = bsc_web.UrlValue.quote(c)
print a
b = bsc_web.UrlValue.unquote(a)
print b

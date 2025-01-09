# coding:utf-8
from urllib import quote, unquote

d = u'测试'

print repr(d.encode('utf-8'))

d_0 = quote(d.encode('utf-8'))

print d_0

print unquote(d_0)


print unquote('aaaa')

import re

print re.sub(r'(<[^>]+>)|(&[\#a-zA-Z0-9]+;)', '', '^&%')


print unquote('///B2///E2///CA///D4'.replace('///', '%'))

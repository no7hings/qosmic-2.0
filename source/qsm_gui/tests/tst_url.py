# coding:utf-8
import urllib

import urlparse

d = dict(
    title='通知',
    message='拍屏结束了',
    command='abc',
    status='normal'
)


d_ = urllib.urlencode(d)
print d_

print urlparse.parse_qs(d_)
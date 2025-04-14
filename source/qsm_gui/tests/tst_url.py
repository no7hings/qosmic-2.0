# coding:utf-8
from __future__ import print_function

import urllib

# noinspection PyUnresolvedReferences
from six.moves.urllib.parse import parse_qs, unquote

d = dict(
    title='通知',
    message='拍屏结束了',
    command='abc',
    status='normal'
)


d_ = urllib.urlencode(d)
print(d_)

print(parse_qs(d_))

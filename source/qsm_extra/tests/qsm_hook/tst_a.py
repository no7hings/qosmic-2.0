# coding:utf-8
from __future__ import print_function

import urllib

HOST = 'localhost'
PORT = 9527

_ = urllib.urlopen(
    'http://{host}:{port}/query?status'.format(
        **dict(
            host=HOST,
            port=PORT,
        )
    )
)

if _:
    print(_.read())

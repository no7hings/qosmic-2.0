# coding:utf-8
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
    print _.read()

# coding:utf-8
import os


class SyncServer(object):
    if os.environ.get('QSM_DEV') == '1':
        HOST = 'localhost'
    else:
        HOST = '10.33.4.90'

    PORT = 12308
    PORT_BACKUP = 12309

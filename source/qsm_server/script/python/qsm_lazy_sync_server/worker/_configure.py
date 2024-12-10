# coding:utf-8
import getpass


class SyncServer(object):
    if getpass.getuser() == 'nothings':
        HOST = 'localhost'
    else:
        HOST = '10.33.4.90'
    PORT = 12308

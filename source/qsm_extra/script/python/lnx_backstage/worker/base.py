# coding:utf-8


class BackstageServerBase(object):
    HOST = 'localhost'
    PORT = 12306


class TaskWebServerBase(object):
    NAME = 'Qosmic Task Web Server'
    LOCALHOST = 'localhost'
    HOST = 'localhost'
    PORT = 12307


class NoticeWebServerBase(object):
    NAME = 'Qosmic Notice Web Server'
    HOST = 'localhost'
    # do not use 12308, it is use for sync server
    PORT = 12310

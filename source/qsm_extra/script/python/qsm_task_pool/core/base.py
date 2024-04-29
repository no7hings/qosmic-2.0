# coding:utf-8
import time

import datetime

import uuid

import getpass

import socket


class Util(object):
    CONNECTION = None

    DATE_TAG_FORMAT = '%Y_%m%d'

    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def get_host_name(cls):
        return socket.gethostname()

    @classmethod
    def get_user_name(cls):
        return getpass.getuser()
    
    @classmethod
    def get_date_tag(cls):
        timestamp = time.time()
        return time.strftime(
            cls.DATE_TAG_FORMAT,
            time.localtime(timestamp)
        )

    @classmethod
    def new_uuid(cls):
        return str(uuid.uuid1()).upper()

    @classmethod
    def get_utc_time(cls):
        utc_now = datetime.datetime.utcnow()
        return utc_now.strftime(
            cls.TIME_FORMAT
        )

    @classmethod
    def get_time(cls):
        return time.strftime(
            cls.TIME_FORMAT,
            time.localtime(time.time())
        )


class TaskProperties(dict):
    class Keys(object):
        ID = 'id'
        Name = 'name'
        Time = 'time'
        UtcTime = 'utc_time'

        HostName = 'host_name'
        UserName = 'user_name'

        Priority = 'priority'

        SubmitTime = 'submit_time'
        StartTime = 'start_time'
        FinishTime = 'finish_time'

        All = [
            ID, Name,
            HostName, UserName,
            Priority,
            # SubmitTime, StartTime, FinishTime
        ]

    def __init__(self, *args, **kwargs):
        super(TaskProperties, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        return self.__getitem__(key)

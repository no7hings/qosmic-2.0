# coding:utf-8
import os

import enum


class BscColorSpaces(object):
    SRGB = 'sRGB'
    LINEAR = 'linear'
    RAW = 'raw'


class BasProcessStatus(enum.IntEnum):
    Unknown = 0
    Started = 1
    Running = 2
    Waiting = 3
    Completed = 4
    Suspended = 5
    Failed = 6
    Stopped = 7
    Error = 8
    Killed = 9
    Finished = 10

    @classmethod
    def to_mapper(cls):
        return {
            int(i): str(i).split('.')[-1].lower() for i in [
                cls.Unknown, cls.Started, cls.Running, cls.Waiting,
                cls.Completed, cls.Suspended, cls.Failed, cls.Stopped,
                cls.Error, cls.Killed, cls.Finished
            ]
        }


class BscSubProcessStatus(enum.EnumMeta):
    """
    0 正常结束
    1 sleep
    2 子进程不存在
    -15 kill
    None 在运行
    """
    Unknown = 2
    # sleep
    Failed = 1
    Completed = 0
    Running = None
    # kill
    Stopped = 5
    Error = -15


class BscPlatformCfg(object):
    Windows = 'windows'
    Linux = 'linux'
    #
    All = [
        Windows,
        Linux
    ]


class BscApplicationCfg(object):
    Python = 'python'
    #
    Maya = 'maya'
    Houdini = 'houdini'
    Katana = 'katana'
    Nuke = 'nuke'
    Clarisse = 'clarisse'
    #
    Lynxi = 'lynxi'
    #
    All = [
        Python,
        #
        Maya,
        Houdini,
        Katana,
        Nuke,
        Clarisse,
        #
        Lynxi
    ]


class BscSystemCfg(object):
    All = []
    for i_p in BscPlatformCfg.All:
        for i_a in BscApplicationCfg.All:
            All.append('{}-{}'.format(i_p, i_a))

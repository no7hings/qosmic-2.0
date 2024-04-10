# coding:utf-8
import enum


class DdlJobStatus(enum.IntEnum):
    """
    Stat (Status)
    0 = Unknown
    1 = Active
    2 = Suspended
    3 = Completed
    4 = Failed
    6 = Pending
    """
    Unknown = 0
    Active = 1
    Suspended = 2
    Completed = 3
    Failed = 4
    Pending = 6


class DdlTaskStatus(enum.IntEnum):
    """
    Stat (Status)
    1 = Unknown
    2 = Queued
    3 = Suspended
    4 = Rendering
    5 = Completed
    6 = Failed
    8 = Pending
    """
    Unknown = 1
    Queued = 2
    Suspended = 3
    Rendering = 4
    Completed = 5
    Failed = 6
    Pending = 8


class DdlOnTaskTimeout(object):
    """
    Timeout (OnTaskTimeout)
    0 = Both
    1 = Error
    2 = Notify
    """
    KEY = 'Timeout'


class DdlOnJobComplete(object):
    """
    OnComp (OnJobComplete)
    0 = Archive
    1 = Delete
    2 = Nothing
    """
    KEY = 'OnComp'


class DdlScheduledType(object):
    """
    Schd (ScheduledType)
    0 = None
    1 = Once
    2 = Daily
    """
    KEY = 'Schd'

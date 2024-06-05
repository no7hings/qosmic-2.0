# coding:utf-8
from peewee import *

import datetime

import uuid

__all__ = [
    'Node',
    'Type',
    'Tag',
    'Assign',
    'Property',
    'Connection',
]


class _Entity(Model):
    enable = BooleanField(default=True)

    uuid = UUIDField(default=uuid.uuid1)

    ctime = TimestampField(default=datetime.datetime.now)
    mtime = TimestampField(default=datetime.datetime.now)

    metadata = FixedCharField(default='{}')

    category = CharField(default='')
    type = CharField(default='')

    kind = CharField(default='')

    path = CharField(default='', unique=True)


class _Prim(_Entity):
    gui_name = CharField(default='')
    gui_name_chs = CharField(default='')

    gui_description = CharField(default='')
    gui_description_chs = CharField(default='')

    gui_icon_name = CharField(default='')


class Node(_Prim):
    """
    node
    """
    gui_icon_name = CharField(default='database/object')


class Type(_Prim):
    """
    type is node
    """
    gui_icon_name = CharField(default='database/object')


class Tag(_Prim):
    """
    tag is node
    """
    gui_icon_name = CharField(default='database/tag')


class _Relationship(_Entity):
    source = CharField(default='')
    target = CharField(default='')

    active = BooleanField(default=True)


class Assign(_Relationship):
    """
    relationship for node
    """
    category = CharField(default='assign')


class Property(_Entity):
    """
    for node extend
    """
    node = CharField(default='')
    port = CharField(default='')
    value = CharField(default='')


class Connection(_Relationship):
    """
    relationship for properties
    """
    category = CharField(default='connection')

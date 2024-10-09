# coding:utf-8
import getpass

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


class _Obj(Model):
    """
    basic model
    """
    enable = BooleanField(default=True)

    trash = BooleanField(default=False)
    lock = BooleanField(default=False)

    permission = CharField(default='*')

    uuid = UUIDField(default=uuid.uuid1)

    ctime = TimestampField(default=datetime.datetime.now)
    mtime = TimestampField(default=datetime.datetime.now)
    user = CharField(default=getpass.getuser)

    metadata = FixedCharField(default='{}')

    category = CharField(default='')
    type = CharField(default='')

    kind = CharField(default='')

    color = CharField(default='FFFFFF')

    path = CharField(default='', unique=True)


class _Prim(_Obj):
    gui_name = CharField(default='')
    gui_name_chs = CharField(default='')

    gui_description = CharField(default='')
    gui_description_chs = CharField(default='')

    gui_icon_name = CharField(default='')


class Node(_Prim):
    """
    node is primitive
    """
    gui_icon_name = CharField(default='database/object')


class Type(_Prim):
    """
    type is primitive
    """
    gui_icon_name = CharField(default='database/type')


class Tag(_Prim):
    """
    tag is primitive
    """
    gui_icon_name = CharField(default='database/tag')


class _Relationship(_Obj):
    source = CharField(default='')
    target = CharField(default='')

    active = BooleanField(default=True)


class Assign(_Relationship):
    """
    relationship for node
    """
    category = CharField(default='assign')


class Property(_Obj):
    """
    for node extend
    """
    category = CharField(default='property')

    node = CharField(default='')
    port = CharField(default='')
    value = TextField(default='')


class Connection(_Relationship):
    """
    relationship for properties
    """
    category = CharField(default='connection')


class ActionLog(Model):
    ctime = TimestampField(default=datetime.datetime.now)
    user = CharField(default=getpass.getuser)

    entity_type = CharField(default='')
    entity_path = CharField(default='')

    action = CharField(default='')

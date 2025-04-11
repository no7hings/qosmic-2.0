# coding:utf-8
from peewee import *

import datetime

import uuid


class _Prim(Model):
    """
    basic model
    """
    uuid = UUIDField(default=uuid.uuid1)
    ctime = TimestampField(default=datetime.datetime.now)
    mtime = TimestampField(default=datetime.datetime.now)

    name = CharField(default='')


class _Entity(_Prim):
    gui_name = CharField(default='')
    gui_name_chs = CharField(default='')

    description = TextField(default='')
    description_chs = TextField(default='')

    image = BlobField(default='')

    status = CharField(default='default')


class BaseStep(_Prim):
    gui_name = CharField(default='')
    gui_name_chs = CharField(default='')


class BaseTask(_Prim):
    gui_name = CharField(default='')
    gui_name_chs = CharField(default='')

    step = ForeignKeyField(BaseStep, backref='bs')


# role
class Role(_Prim):
    gui_name = CharField(default='')
    gui_name_chs = CharField(default='')


class User(_Prim):
    gui_name = CharField(default='')
    gui_name_chs = CharField(default='')


# project
class Project(_Entity):
    category = CharField(default='')


# asset
class Asset(_Entity):
    project = ForeignKeyField(Project, backref='bs')
    role = ForeignKeyField(Role, backref='bs')


# episode
class Episode(_Entity):
    project = ForeignKeyField(Project, backref='bs')


# sequence
class Sequence(_Entity):
    project = ForeignKeyField(Project, backref='bs')
    episode = ForeignKeyField(Episode, backref='bs')


# shot
class Shot(_Entity):
    project = ForeignKeyField(Project, backref='bs')
    episode = ForeignKeyField(Episode, backref='bs')
    sequence = ForeignKeyField(Sequence, backref='bs')


# task
class Task(BaseTask):
    resource_type = CharField(default='')

    asset = ForeignKeyField(Asset, backref='bs')
    episode = ForeignKeyField(Episode, backref='bs')
    sequence = ForeignKeyField(Sequence, backref='bs')
    shot = ForeignKeyField(Shot, backref='bs')


# version
class Version(_Prim):
    task = ForeignKeyField(Task, backref='bs')
    number = IntegerField(default=0)

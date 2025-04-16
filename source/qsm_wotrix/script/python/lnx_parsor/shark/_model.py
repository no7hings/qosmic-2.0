# coding:utf-8
from peewee import *

import datetime

import uuid

import getpass


class _Prim(Model):
    """
    basic model
    """
    enable = BooleanField(default=True)

    trash = BooleanField(default=False)
    lock = BooleanField(default=False)

    uuid = UUIDField(default=uuid.uuid1)
    ctime = TimestampField(default=datetime.datetime.now)
    mtime = TimestampField(default=datetime.datetime.now)

    user = CharField(default=getpass.getuser)

    name = CharField(default='')


class _Entity(_Prim):
    gui_name = CharField(default='')
    gui_name_chs = CharField(default='')

    description = TextField(default='')
    description_chs = TextField(default='')

    image = BlobField(default='')

    status = CharField(default='default')


class User(_Entity):
    login = TextField(default='')


# project
class Project(_Entity):
    category = CharField(default='')


# resource type
class ResourceType(_Entity):
    project = ForeignKeyField(Project, backref='bs')


# step
class Step(_Entity):
    project = ForeignKeyField(Project, backref='bs')
    resource_type = ForeignKeyField(ResourceType, backref='bs')


# role
class Role(_Entity):
    project = ForeignKeyField(Project, backref='bs')


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
class Task(_Entity):
    resource_type = CharField(default='')

    project = ForeignKeyField(Project, backref='bs')
    asset = ForeignKeyField(Asset, backref='bs')
    episode = ForeignKeyField(Episode, backref='bs')
    sequence = ForeignKeyField(Sequence, backref='bs')
    shot = ForeignKeyField(Shot, backref='bs')

    step = ForeignKeyField(Step, backref='bs')

    @property
    def entity(self):
        if self.resource_type == 'project':
            return ForeignKeyField(Project, backref='bs')
        elif self.resource_type == 'asset':
            return ForeignKeyField(Asset, backref='bs')
        return


# version
class Version(_Entity):
    task = ForeignKeyField(Task, backref='bs')
    number = IntegerField(default=0)

# coding:utf-8
import datetime

import time

import json

import os.path

import random

import peewee

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from .. import database as _database


class Entity(dict):
    def __init__(self, entity_type, *args, **kwargs):
        self.entity_type = entity_type
        super(Entity, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self.__getitem__(item)  # = self[item]

    def __str__(self):
        return '{}(type="{}", path="{}", id="{}")'.format(
            self.entity_type, self.type, self.path, self.id
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def to_string(self, *args):
        if args:
            keys = args
        else:
            keys = self.keys()
            keys.sort()
        return '\n'.join(['{}: {}'.format(x, bsc_core.auto_string(self[x])) for x in keys])


class Stage(object):
    Node = _database.Node
    Type = _database.Type
    Tag = _database.Tag
    Assign = _database.Assign
    Property = _database.Property
    Connection = _database.Connection

    class EntityTypes:
        Node = _database.Node.__name__
        Type = _database.Type.__name__
        Tag = _database.Tag.__name__
        Assign = _database.Assign.__name__
        Property = _database.Property.__name__
        Connection = _database.Connection.__name__

    ALL = [
        Node,
        Type,
        Tag,
        Assign,
        Property,
        Connection
    ]

    PATHSEP = '/'

    TIME_TAGS = [
        'today',
        'yesterday',
        'earlier_this_week',
        'last_week',
        'earlier_this_month',
        'last_month',
        'earlier_this_year',
        'long_time_ago',
    ]

    @classmethod
    def to_expression_str(cls, entity_type, filters):
        list_ = []
        for i_key, i_opt, i_value in filters:
            if i_opt == 'is':
                i_fnc_ = '__eq__'
            elif i_opt == 'is not':
                i_fnc_ = '__ne__'
            elif i_opt == 'in':
                i_fnc_ = 'in_'
            elif i_opt == 'contains':
                i_fnc_ = 'contains'
            elif i_opt == 'startswith':
                i_fnc_ = 'startswith'
            elif i_opt == 'endswith':
                i_fnc_ = 'endswith'
            else:
                raise RuntimeError()

            i_value_ = json.dumps(i_value)
            #
            list_.append('(self.{}.{}.{}({}))'.format(entity_type, i_key, i_fnc_, i_value_))
        return ' & '.join(list_)

    @classmethod
    def to_dtb_entity(cls, entity_type):
        if entity_type not in cls.__dict__:
            raise RuntimeError()
        return cls.__dict__[entity_type]

    @classmethod
    def to_entity(cls, entity_type, data):
        return Entity(entity_type, data)

    def __init__(self, dtb_path):
        self._dtb_path = dtb_path
        self._dtb = peewee.SqliteDatabase(dtb_path, thread_safe=True)

    @property
    def dtb(self):
        return self._dtb

    def connect(self):
        for i in self.ALL:
            # noinspection PyUnresolvedReferences
            i._meta.database = self._dtb
        return self._dtb

    def close(self):
        self._dtb.close()

    def initialize(self):
        directory_path = os.path.dirname(self._dtb_path)
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

        self._dtb.create_tables(
            self.ALL
        )

    def build(self, configure):
        if configure is None:
            raise RuntimeError()

        type_data = configure.get('entities.types')
        for k, v in type_data.items():
            self.create_entity(
                self.EntityTypes.Type, k, **v
            )

        tag_data = configure.get('entities.tags')
        for k, v in tag_data.items():
            self.create_entity(
                self.EntityTypes.Tag, k, **v
            )

        node_data = configure.get('entities.nodes')
        for k, v in node_data.items():
            self.create_entity(
                self.EntityTypes.Node, k, **v
            )

    def build_test(self, asset_type):
        # self.create_node_root_group()
        # self.create_node_group('/{}'.format(asset_type))

        random.seed(0)
        type_paths = [
            x.path for x in self.find_all(
                self.EntityTypes.Type,
                filters=[
                    ('type', 'is', 'node'),
                    ('kind', 'is not', 'builtin')
                ]
            )
        ]
        tag_paths = [
            x.path for x in self.find_all(
                self.EntityTypes.Tag,
                filters=[
                    ('type', 'is', 'node'),
                    ('kind', 'is not', 'builtin')
                ]
            )
        ]

        today = datetime.datetime.today()
        maximum = int(time.mktime(today.timetuple()))
        start_of_year = today.replace(month=1, day=1)
        minimum = int(time.mktime(start_of_year.timetuple()))

        ctimes = range(minimum, maximum)

        for i in range(500):
            i_node_path = '/{}/test_{}'.format(asset_type, i)

            self.create_node(i_node_path, ctime=random.choice(ctimes))
            if i % 3:
                for j in range(2):
                    j_type_path = random.choice(type_paths)
                    self.create_assign(i_node_path, j_type_path, type='type_assign')

            if i % 2:
                for j in range(2):
                    j_tag_path = random.choice(tag_paths)
                    self.create_assign(i_node_path, j_tag_path, type='tag_assign')

            self.create_parameter(
                i_node_path,
                'video',
                'Z:/temeporaries/dongchangbao/playblast_tool/test.export.v004.mov'
            )
            self.create_parameter(
                i_node_path,
                'thumbnail',
                'Z:/temeporaries/dongchangbao/playblast_tool/test.export.v004.png'
            )

    def find_one(self, entity_type, filters):
        dtb_entity = self.__class__.__dict__[entity_type]
        e_str = self.to_expression_str(
            entity_type, filters
        )
        _ = dtb_entity.select().where(
            eval(e_str)
        )
        if _.exists():
            return self.to_entity(entity_type, _.first().__data__)

    def find_all(self, entity_type, filters=None):
        dtb_entity = self.__class__.__dict__[entity_type]
        if filters:
            e_str = self.to_expression_str(
                 entity_type, filters
            )
            _ = dtb_entity.select().where(
                eval(e_str)
            )
        else:
            _ = dtb_entity.select()
        if _.exists():
            return map(lambda x: self.to_entity(entity_type, x.__data__), _)
        return []

    def is_entity_exists(self, entity_type, path):
        dtb_entity = self.to_dtb_entity(entity_type)
        return dtb_entity.select().where(dtb_entity.path == path).exists()

    def get_entity(self, entity_type, path):
        dtb_entity = self.to_dtb_entity(entity_type)
        _ = dtb_entity.select().where(dtb_entity.path == path)
        if _.exists():
            return self.to_entity(entity_type, _.first().__data__)

    def create_entity(self, entity_type, path, **kwargs):
        if self.is_entity_exists(entity_type, path) is True:
            return self.get_entity(entity_type, path)

        dtb_entity = self.to_dtb_entity(entity_type)
        name = path.split(self.PATHSEP)[-1]
        gui_name = bsc_core.RawTextMtd.to_prettify(name, capitalize=True)
        options = dict(
            path=path,
            gui_name=gui_name,
        )
        options.update(**kwargs)
        _ = dtb_entity.create(**options)
        _.save()
        return self.to_entity(entity_type, _.__data__)

    def create_node_root_group(self, **kwargs):
        options = dict(
            path='/', category='group', type='root', gui_icon_name='database/all'
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Node, **options
        )

    def create_node_group(self, path, **kwargs):
        options = dict(
            path=path, category='group', type='group', gui_icon_name='database/group'
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Node, **options
        )

    def create_node(self, path, **kwargs):
        options = dict(
            path=path, category='node', type='node', gui_icon_name='database/object'
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Node, **options
        )

    def create_assign(self, path_source, path_target, **kwargs):
        path = '{}->{}'.format(path_source, path_target)
        options = dict(
            path=path,
            source=path_source,
            target=path_target
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Assign,
            **options
        )

    def create_property(self, node, port, value, **kwargs):
        path = '{}.{}'.format(node, port)
        options = dict(
            path=path,
            node=node,
            port=port,
            value=value,
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Property,
            **options
        )

    def create_parameter(self, node, port, value, **kwargs):
        return self.create_property(node, port, value, type='parameter', **kwargs)

    def get_node(self, path):
        return self.get_entity(
            self.EntityTypes.Node, path
        )

    def is_node_exists(self, path):
        return self.Node.select().where(self.Node.path == path).exists()

    def find_all_by_ctime_tag(self, entity_type, tag='today', filters=None):
        today = datetime.date.today()
        yesterday = today-datetime.timedelta(days=1)
        start_of_week = today-datetime.timedelta(days=today.weekday())
        start_of_last_week = start_of_week-datetime.timedelta(days=7)
        end_of_last_week = start_of_week-datetime.timedelta(seconds=1)
        start_of_month = today.replace(day=1)
        start_of_last_month = (start_of_month-datetime.timedelta(days=1)).replace(day=1)
        end_of_last_month = start_of_month-datetime.timedelta(seconds=1)
        start_of_year = today.replace(month=1, day=1)
        dtb_entity = self.__class__.__dict__[entity_type]

        conditions = {
            #
            'today': '(dtb_entity.ctime >= today) & (dtb_entity.ctime < today+datetime.timedelta(days=1))',
            # yesterday <= ctime < today
            'yesterday': '(dtb_entity.ctime >= yesterday) & (dtb_entity.ctime < today)',
            # start_of_week <= ctime < yesterday
            'earlier_this_week': '(dtb_entity.ctime >= start_of_week) & (dtb_entity.ctime < yesterday)',
            #
            'last_week': '(dtb_entity.ctime >= start_of_last_week) & (dtb_entity.ctime <= end_of_last_week)',
            'earlier_this_month': '(dtb_entity.ctime >= start_of_month) & (dtb_entity.ctime < end_of_last_week)',
            'last_month': '(dtb_entity.ctime >= start_of_last_month) & (dtb_entity.ctime <= end_of_last_month)',
            'earlier_this_year': '(dtb_entity.ctime >= start_of_year) & (dtb_entity.ctime < end_of_last_month)',
            'long_time_ago': '(dtb_entity.ctime < start_of_year)'
        }
        if filters:
            _ = dtb_entity.select().where(
                eval(conditions[tag] + '&' + self.to_expression_str(entity_type, filters))
            )
        else:
            _ = dtb_entity.select().where(
                eval(conditions[tag])
            )
        if _.exists():
            return map(lambda x: self.to_entity(entity_type, x.__data__), _)
        return []




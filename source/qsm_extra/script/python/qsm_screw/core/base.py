# coding:utf-8
import json
import random

import peewee

import lxbasic.core as bsc_core

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

    def to_string(self):
        keys = self.keys()
        keys.sort()
        return '\n'.join(['{}: {}'.format(i, bsc_core.auto_string(self[i])) for i in keys])


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

    def __init__(self, path):
        self._dtb = peewee.SqliteDatabase(path, thread_safe=True)

    @property
    def dtb(self):
        return self._dtb

    def connect(self):
        for i in self.ALL:
            # noinspection PyUnresolvedReferences
            i._meta.database = self._dtb
        return self._dtb

    def initialize(self):
        self._dtb.create_tables(
            self.ALL
        )

    def build(self, configure):
        if configure is None:
            raise RuntimeError()

        types_data = configure.get('entities.types')
        for k, v in types_data.items():
            self.create_entity(
                self.EntityTypes.Type, k, **v
            )

        tags_data = configure.get('entities.tags')
        for k, v in tags_data.items():
            self.create_entity(
                self.EntityTypes.Tag, k, **v
            )

    def build_test(self, asset_type):
        self.create_node_root()
        self.create_node_group('/{}'.format(asset_type))

        random.seed(0)
        type_paths = [x.path for x in self.find_all(self.EntityTypes.Type, filters=[('type', 'is', 'node')])]

        for i in range(200):
            i_node_path = '/{}/test_{}'.format(asset_type, i)
            self.create_node(i_node_path)
            for j in range(2):
                j_type_path = random.choice(type_paths)
                self.create_assign(i_node_path, j_type_path, type='type_assign')

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

    def find_all(self, entity_type, filters):
        dtb_entity = self.__class__.__dict__[entity_type]
        e_str = self.to_expression_str(
             entity_type, filters
        )
        _ = dtb_entity.select().where(
            eval(e_str)
        )
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

    def create_node_root(self, **kwargs):
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

    def get_node(self, path):
        return self.get_entity(
            self.EntityTypes.Node, path
        )

    def is_node_exists(self, path):
        return self.Node.select().where(self.Node.path == path).exists()

    def test(self):

        # for i in self.find_all(
        #     'Node', ('type', 'in', ['node']), ('path', 'startswith', '/test/')
        # ):
        #     print i
        # #
        # # print
        #
        # print self.find_one(
        #     'Node', ('type', 'in', ['node']), ('path', 'startswith', '/test/')
        # )
        print self.get_entity(
            'Node', '/'
        )





# coding:utf-8
import peewee

import json

import threading

import _my_sql

import abc_

import _base

import _model


class Entity(dict):
    def __init__(self, entity_type, *args, **kwargs):
        self.entity_type = entity_type
        super(Entity, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self.__getitem__(item)  # = self[item]

    def __str__(self):
        return '{}(id="{}", name="{}")'.format(
            self.entity_type, self.id, self.name
        )

    def __repr__(self):
        return '\n'+self.__str__()


class Database(abc_.AbsBase):
    LOCK = threading.Lock()
    
    @classmethod
    def _to_expression_str(cls, entity_type, filters):
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
            # when value is bool do not use json.dumps
            if isinstance(i_value, bool):
                i_value_ = i_value
            else:
                i_value_ = json.dumps(i_value)

            list_.append('(self.{}.{}.{}({}))'.format(entity_type, i_key, i_fnc_, i_value_))
        return ' & '.join(list_)

    @classmethod
    def _to_entity(cls, entity_type, data):
        return Entity(entity_type, data)

    def _to_dtb_entity_type(self, entity_type):
        # fixme: reconnect for timeout?
        if self._dtb.is_closed():
            self._dtb.connect()
        if entity_type not in self.__dict__:
            raise RuntimeError()
        return self.__dict__[entity_type]

    def __init__(self, database_type, database_name):
        # todo: use only one instance?
        self._database_name = database_name

        self._database_name = self._to_database_key(database_type, database_name)
        
        self._dtb = peewee.MySQLDatabase(
            self._database_name,
            **self._get_mysql_options()
        )

        self.connect()

    def create_entity(self, entity_type, **kwargs):
        dtb_entity_type = self._to_dtb_entity_type(entity_type)
        options = {}
        options.update(**kwargs)
        with self.LOCK:
            _ = dtb_entity_type.create(**options)
            _.save()
            return self._to_entity(entity_type, _.__data__)
    
    def find_one(self, entity_type, filters):
        dtb_entity_type = self._to_dtb_entity_type(entity_type)
        e_str = self._to_expression_str(
            entity_type, filters
        )
        _ = dtb_entity_type.select().where(
            eval(e_str)
        )
        if _.exists():
            return self._to_entity(entity_type, _.first().__data__)

    def connect(self):
        self.BaseStep = _base.generate_entity_type_models(_model.BaseStep, self._dtb)
        self.BaseTask = _base.generate_entity_type_models(_model.BaseTask, self._dtb)

        self.Project = _base.generate_entity_type_models(_model.Project, self._dtb)
        self.Role = _base.generate_entity_type_models(_model.Role, self._dtb)
        self.Asset = _base.generate_entity_type_models(_model.Asset, self._dtb)
        self.Episode = _base.generate_entity_type_models(_model.Episode, self._dtb)
        self.Sequence = _base.generate_entity_type_models(_model.Sequence, self._dtb)
        self.Shot = _base.generate_entity_type_models(_model.Shot, self._dtb)
        self.Task = _base.generate_entity_type_models(_model.Task, self._dtb)
        self.Version = _base.generate_entity_type_models(_model.Version, self._dtb)
        
        self.All = [
            self.BaseStep,
            self.BaseTask,

            self.Project,
            self.Role,
            self.Asset,
            self.Episode,
            self.Sequence,
            self.Shot,

            self.Task,
            self.Version,
        ]

    def initialize(self):
        # create database when is non-exists
        _my_sql.MySql.create_database(
            self._get_mysql_options(), self._database_name
        )
        # build all entity type for project
        _base.build_entity_types(
            self.All, self._dtb
        )

    def build(self, **kwargs):
        self.initialize()

        self.create_entity(
            self.EntityTypes.Project, name=self._database_name, **kwargs
        )

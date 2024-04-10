# coding:utf-8
from __future__ import print_function

import six

import sqlite3

import threading

import Queue


class DtbSqlThread(threading.Thread):
    STACK = []
    MAXIMUM = 256
    EVENT = threading.Event()
    LOCK = threading.Lock()

    def __init__(self, database):
        super(DtbSqlThread, self).__init__()
        self._db = database
        self._reqs = Queue.Queue()

    def run(self):
        cnt = sqlite3.Connection(self._db)
        cnt.row_factory = AbsDtbSqlBaseOpt.dict_factory
        csr = cnt.cursor()
        while True:
            cmd, args, res = self._reqs.get()
            if cmd == '--close--':
                break
            elif cmd == '--commit--':
                cnt.commit()
            #
            csr.execute(cmd, args)
            if res:
                for i in csr:
                    res.put(i)
                #
                res.put('--no more--')
        #
        cnt.close()

    def execute(self, cmd, args=None, res=None):
        self._reqs.put(
            (cmd, args or tuple(), res)
        )

    def select(self, cmd, args=None):
        res = Queue.Queue()
        self.execute(cmd, args, res)
        while True:
            rec = res.get()
            if rec == '--no more--':
                break
            yield rec

    def commit(self):
        self.execute('--commit--')

    def close(self):
        self.execute('--close--')


class DtbDict(dict):
    def __init__(self, *args, **kwargs):
        super(DtbDict, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self.__getitem__(item)  # = self[item]

    def to_string(self):
        keys = self.keys()
        keys.sort()
        return '\n'.join(['{}: {}'.format(i, self[i]) for i in keys])


class AbsDtbSqlBaseOpt(object):
    TYPE_MAPPER = {
        'string': 'text',
        'integer': 'integer',
        'float': 'real',
        'boolean': 'integer',
        'json': 'blob',
        'list': 'blob',
        'timestamp': 'timestamp'
    }

    DEBUGGER_ENABLE = False
    DEBUGGER_PRINT_MAXIMUM = 200

    def __init__(self, database, connection):
        self._dtb = database
        self._cnt = connection

    @classmethod
    def dict_factory(cls, cursor, row):
        dict_ = DtbDict()
        for i_index, i_column in enumerate(cursor.description):
            dict_[i_column[0]] = row[i_index]
        return dict_

    @classmethod
    def create_connection_from_db(cls, database):
        return sqlite3.connect(database)

    def get_connection(self):
        return self._cnt

    def accept(self):
        return self._cnt.commit()

    def close(self):
        return self._cnt.close()

    def _print_execute_cmd(self, cmd):
        if len(cmd) > self.DEBUGGER_PRINT_MAXIMUM:
            print('database execute: {} ...'.format(cmd[:self.DEBUGGER_PRINT_MAXIMUM]))
        else:
            print('database execute: {}'.format(cmd))

    def _execute_cmd(self, cmd, args=None):
        if self.DEBUGGER_ENABLE is True:
            self._print_execute_cmd(cmd)
        #
        csr = self._cnt.cursor()
        if args:
            csr.execute(cmd, args)
        else:
            csr.execute(cmd)
        return csr

    def _execute_cmd_as_new_connection(self, cmd, args=None):
        if self.DEBUGGER_ENABLE is True:
            self._print_execute_cmd(cmd)
        #
        cnt = self.create_connection_from_db(self._dtb)
        cnt.row_factory = AbsDtbSqlBaseOpt.dict_factory
        csr = cnt.cursor()
        if args:
            csr.execute(cmd, args)
        else:
            csr.execute(cmd)
        return csr


class DtbSqlTableOpt(AbsDtbSqlBaseOpt):
    def __init__(self, database, connection, name):
        super(DtbSqlTableOpt, self).__init__(database, connection)
        self._name = name

    def create(self, options):
        def get_string_fnc_(options_):
            _list = []
            for _k, _v in options_.items():
                _i_l = ['"{}"'.format(_k)]
                if 'type' in _v:
                    _i_t = _v['type']
                    _i_t_ = self.TYPE_MAPPER[_i_t]
                    _i_l.append(_i_t_)
                if 'args' in _v:
                    _i_a = _v['args']
                    _i_l.append(' '.join(_i_a))
                _list.append(' '.join(_i_l))
            return ', '.join(_list)

        options_string = get_string_fnc_(options)
        cmd = (
            'create table if not exists {name}({options})'
        ).format(**dict(name=self._name, options=options_string))
        return self._execute_cmd(cmd)

    @classmethod
    def _to_filters_(cls, **kwargs):
        list_ = []
        for i_k, i_v in kwargs.items():
            list_.append(
                (i_k, 'is', i_v)
            )
        return list_

    def get_is_exists(self, **kwargs):
        _ = self.get_one(
            filters=self._to_filters_(**kwargs),
            new_connection=False
        )
        cmd = (
            'where exists'
        )
        return _ is not None

    def delete(self):
        cmd = 'drop table if exists {name}'.format(
            **dict(name=self._name)
        )
        return self._execute_cmd(cmd)

    def add(self, **kwargs):
        def get_string_fnc_(kwargs_):
            _key_list = []
            _value_list = []
            for _i_k, _i_v in kwargs_.items():
                _key_list.append('"{}"'.format(_i_k))
                if isinstance(_i_v, str):
                    _value_list.append('"{}"'.format(_i_v))
                elif isinstance(_i_v, unicode):
                    _value_list.append('"{}"'.format(_i_v.decode('utf-8')))
                else:
                    _value_list.append(_i_v)
            return ', '.join(_key_list), ', '.join(_value_list)

        #
        keys_string, values_string = get_string_fnc_(kwargs)
        cmd = (
            'insert or ignore into {name}({keys}) values({values})'
        ).format(**dict(name=self._name, keys=keys_string, values=values_string))
        return self._execute_cmd(cmd)

    def update(self, **kwargs):
        def get_string_fnc_(kwargs_):
            _property_list = []
            for _i_k, _i_v in kwargs_.items():
                if isinstance(_i_v, str):
                    _i_value_string = '"{}"'.format(_i_v)
                elif isinstance(_i_v, unicode):
                    _i_value_string = '"{}"'.format(_i_v.decode('utf-8'))
                else:
                    _i_value_string = _i_v
                _property_list.append(
                    '{} = {}'.format('"{}"'.format(_i_k), _i_value_string)
                )
            return ', '.join(_property_list)

        #
        id_ = kwargs.pop('id')
        properties_string = get_string_fnc_(kwargs)
        cmd = (
            'update {name} set {properties} where id = {id}'
        ).format(**dict(name=self._name, properties=properties_string, id=id_))
        return self._execute_cmd(cmd)

    def get_one(self, filters, new_connection=True):
        def get_string_fnc_(filters_):
            _key_list = []
            _value_list = []
            for _i_k, _i_c, _i_v in filters_:
                if isinstance(_i_v, str):
                    _i_v_ = '"{}"'.format(_i_v)
                elif isinstance(_i_v, unicode):
                    _i_v_ = '"{}"'.format(_i_v.decode('utf-8'))
                else:
                    _i_v_ = _i_v
                if _i_c == 'is':
                    _i_c_ = '='
                else:
                    _i_c_ = '='
                #
                _value_list.append('{}{}{}'.format('"{}"'.format(_i_k), _i_c_, _i_v_))
            return ' and '.join(_value_list)

        condition_string = get_string_fnc_(filters)

        cmd = (
            'select * from {name} where {values}'
        ).format(
            **dict(name=self._name, values=condition_string)
        )
        if new_connection is True:
            csr = self._execute_cmd_as_new_connection(cmd)
        else:
            csr = self._execute_cmd(cmd)
        return csr.fetchone()

    def get_all(self, filters=None, new_connection=True):
        def get_string_fnc_(filters_):
            _key_list = []
            _value_list = []
            for _i_k, _i_c, _i_v in filters_:
                if _i_c == 'is':
                    _i_c_ = ' = '
                elif _i_c == 'in':
                    _i_c_ = ' in '
                elif _i_c == 'startswith':
                    _i_c_ = ' like '
                    if not isinstance(_i_v, six.string_types):
                        raise TypeError()
                    _i_v += '%'
                else:
                    _i_c_ = ' = '
                #
                if isinstance(_i_v, str):
                    _i_v_ = '"{}"'.format(_i_v)
                elif isinstance(_i_v, unicode):
                    _i_v_ = '"{}"'.format(_i_v.decode('utf-8'))
                elif isinstance(_i_v, (list, set)):
                    _i_v_list = []
                    for _j_v in _i_v:
                        if isinstance(_j_v, str):
                            _j_v_ = '"{}"'.format(_j_v)
                        elif isinstance(_j_v, unicode):
                            _j_v_ = '"{}"'.format(_j_v.decode('utf-8'))
                        else:
                            _j_v_ = _j_v
                        #
                        _i_v_list.append(_j_v_)
                    _i_v_ = '({})'.format(', '.join(_i_v_list))
                else:
                    _i_v_ = _i_v
                #
                _value_list.append('{}{}{}'.format('"{}"'.format(_i_k), _i_c_, _i_v_))
            return ' and '.join(_value_list)

        if filters:
            condition_string = get_string_fnc_(filters)
            cmd = (
                'select * from {name} where {values}'
            ).format(
                **dict(name=self._name, values=condition_string)
            )
        else:
            cmd = (
                'select * from {name}'
            ).format(
                **dict(name=self._name)
            )
        if new_connection is True:
            csr = self._execute_cmd_as_new_connection(cmd)
        else:
            csr = self._execute_cmd(cmd)
        return csr.fetchall()

    def _get_command_for_find_one(self, **kwargs):
        def get_string_fnc_(kwargs_):
            _key_list = []
            _value_list = []
            for _i_k, _i_v in kwargs_.items():
                if isinstance(_i_v, str):
                    _i_v_ = '"{}"'.format(_i_v)
                elif isinstance(_i_v, unicode):
                    _i_v_ = '"{}"'.format(_i_v.decode('utf-8'))
                else:
                    _i_v_ = _i_v
                #
                _value_list.append('{} = {}'.format(_i_k, _i_v_))
            return ' and '.join(_value_list)

        condition_string = get_string_fnc_(kwargs)

        return (
            'select * from {name} where {values}'
        ).format(
            **dict(name=self._name, values=condition_string)
        )

    def get_one_(self, **kwargs):
        csr = self._execute_cmd(self._get_command_for_find_one(**kwargs))
        return csr.fetchone()

    def get_one_as_new_connection(self, **kwargs):
        csr = self._execute_cmd_as_new_connection(self._get_command_for_find_one(**kwargs))
        return csr.fetchone()

    def _get_command_for_find_all(self, **kwargs):
        def get_string_fnc_(kwargs_):
            _key_list = []
            _value_list = []
            for _i_k, _i_v in kwargs_.items():
                if isinstance(_i_v, str):
                    _i_v_ = '"{}"'.format(_i_v)
                elif isinstance(_i_v, unicode):
                    _i_v_ = '"{}"'.format(_i_v.decode('utf-8'))
                else:
                    _i_v_ = _i_v
                #
                _value_list.append('{} = {}'.format(_i_k, _i_v_))
            return ' and '.join(_value_list)

        if kwargs:
            condition_string = get_string_fnc_(kwargs)

            return (
                'select * from {name} where {values}'
            ).format(
                **dict(name=self._name, values=condition_string)
            )
        else:
            return (
                'select * from {name}'
            ).format(
                **dict(name=self._name)
            )

    def get_all_(self, **kwargs):
        csr = self._execute_cmd(self._get_command_for_find_all(**kwargs))
        return csr.fetchall()

    def get_all_as_new_connection(self, **kwargs):
        csr = self._execute_cmd_as_new_connection(self._get_command_for_find_all(**kwargs))
        return csr.fetchall()


class DtbSqlConnectionOpt(AbsDtbSqlBaseOpt):
    def __init__(self, database, connection):
        super(DtbSqlConnectionOpt, self).__init__(database, connection)
        self._cnt.row_factory = self.dict_factory

    @classmethod
    def create_from_database(cls, database):
        cnt = cls.create_connection_from_db(database)
        return cls(database, cnt)

    @classmethod
    def create_from_memory(cls):
        return cls(sqlite3.connect(":memory:", check_same_thread=False))

    def get_table_opt(self, name):
        return DtbSqlTableOpt(self._dtb, self._cnt, name)

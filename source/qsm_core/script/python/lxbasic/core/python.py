# coding:utf-8
import six

import sys

import os

import pkgutil

import importlib

import types

import imp

import lxbasic.log as bsc_log


class PyModule(object):
    def __init__(self, *args):
        _ = args[0]
        if isinstance(_, types.ModuleType):
            self._module = _
        else:
            module_name = _
            _ = pkgutil.find_loader(module_name)
            if _:
                self._module = importlib.import_module(module_name)
            else:
                self._module = None
        #
        self._module_name = None
        self._file_path_pyc = None
        self._file_path_py = None
        #
        if self._module is not None:
            self._module_name = self._module.__name__
            if hasattr(self._module, '__file__') is True:
                self._file_path_pyc = self._module.__file__
                self._file_path_py = self._get_py_(self._file_path_pyc)

    def get_module(self):
        return self._module

    @property
    def module(self):
        return self._module

    @property
    def name(self):
        return self._module_name

    @property
    def file(self):
        return self._file_path_pyc

    @staticmethod
    def _get_py_(file_path_pyc):
        _ = os.path.splitext(file_path_pyc)
        return '{}.py'.format(_[0])

    def get_pyc_timestamp(self):
        if os.path.isfile(self._file_path_pyc):
            return os.stat(self._file_path_pyc).st_mtime

    def get_parent(self):
        if self.get_is_package() is True:
            return None
        module_name = '.'.join(self.name.split('.')[:-1])
        return self.__class__(sys.modules[module_name])

    def get_contain_modules(self):
        return [
            self.__class__(i)
            for i in self.module.__dict__.values()
            if isinstance(i, types.ModuleType)
        ]

    def get_child_modules(self):
        """
        :return: list(instance(PyModule))
        """
        lis = []
        for i in self.get_contain_modules():
            if i.get_is_package() is False:
                if i.get_parent() == self:
                    lis.append(i)
        return lis

    def get_all_child_modules(self):
        def _rcs_fnc(lis_, module_):
            _child_modules = module_.get_child_modules()
            lis.append(module_)
            if _child_modules:
                for _child_module in _child_modules:
                    _rcs_fnc(lis_, _child_module)

        lis = []
        _rcs_fnc(lis, self)
        return lis

    def get_require_modules(self):
        lis = []
        for i in self.get_contain_modules():
            if i.get_is_package() is True:
                lis.append(i)
            else:
                if i.get_parent() != self:
                    lis.append(i)
        return lis

    def get_is_package(self):
        return '.' not in self.name

    def set_reload(self):
        if self.module is not None:
            _ = pkgutil.find_loader(self.name)
            if _:
                module = importlib.import_module(self.name)
                # noinspection PyUnresolvedReferences
                imp.reload(module)
                #
                bsc_log.Log.trace_method_result(
                    'python reload', 'module="{}", file="{}"'.format(
                        self.name, self.file
                    )
                )

    def set_help_print(self):
        # noinspection PyUnresolvedReferences
        help(self.module)

    def set_help_write(self, directory):
        if os.path.isdir(directory) is False:
            os.makedirs(directory)
        #
        file_path = '{}/{}'.format(directory, self._module_name)
        out = sys.stdout
        sys.stdout = open(file_path, "w")
        # noinspection PyUnresolvedReferences
        help(self.module)
        sys.stdout.close()
        sys.stdout = out

    def _test(self):
        for i in self.get_child_modules():
            i._test()

    def get_method(self, key):
        if self._module is not None:
            return self._module.__dict__[key]

    def get_is_exists(self):
        return self._module is not None

    def __str__(self):
        return '{}(name="{}", file_path="{}")'.format(
            self.__class__.__name__,
            self.name,
            self.file
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if other is not None:
            return self.name == other.name
        return False

    def __ne__(self, other):
        return self.name != other.name


class PyReloader(object):
    def __init__(self, *args):
        _ = args[0]
        if isinstance(_, six.string_types):
            self._module_names = [_]
        elif isinstance(_, (tuple, list)):
            self._module_names = _

    def ge_modules(self):
        lis = []
        for i_name in self._module_names:
            _ = pkgutil.find_loader(i_name)
            if _:
                lis.append(
                    PyModule(importlib.import_module(i_name))
                )
        return lis

    @classmethod
    def set_module_load(cls, module_name):
        _ = pkgutil.find_loader(module_name)
        if _:
            return PyModule(
                importlib.import_module(module_name)
            )

    def get_require_module_names(self):
        def _rcs_fnc(source_module_, target_module_):
            _source_module_name = source_module_.name
            if _source_module_name not in all_module_names:
                # collection stack
                all_module_names.append(_source_module_name)
                # collection require
                if target_module_ is not None:
                    _target_module_name = target_module_.name
                    if _source_module_name not in require_module_names:
                        require_module_names.append(_source_module_name)
                    if _target_module_name not in require_module_names:
                        require_module_names.append(_target_module_name)

                    _source_index = require_module_names.index(_source_module_name)
                    _target_index = require_module_names.index(_target_module_name)
                    if _source_index > _target_index:
                        require_module_names.remove(_source_module_name)
                        require_module_names.insert(_target_index, _source_module_name)
                else:
                    if _source_module_name not in require_module_names:
                        require_module_names.append(_source_module_name)
                #
                _require_modules = source_module_.get_contain_modules()
                if _require_modules:
                    for _require_module in _require_modules:
                        _require_module_name = _require_module.name
                        #
                        if _require_module_name in filter_module_names:
                            #
                            _source_module, _target_module = _require_module, source_module_
                            _rcs_fnc(_source_module, _target_module)

        all_modules = []
        all_module_names = []
        require_module_names = []

        for module in self.ge_modules():
            all_modules.extend(module.get_all_child_modules())

        filter_module_names = [i.name for i in all_modules]

        for module in all_modules:
            _rcs_fnc(module, None)

        return require_module_names

    def get_require_connections(self):
        def _rcs_fnc(source_module_, target_module_):
            _source_module_name = source_module_.name
            if _source_module_name not in all_module_names:
                # collection stack
                all_module_names.append(_source_module_name)
                _require_modules = source_module_.get_contain_modules()
                if _require_modules:
                    for _require_module in _require_modules:
                        _require_module_name = _require_module.name
                        #
                        if _require_module_name in filter_module_names:
                            #
                            _source_module, _target_module = _require_module, source_module_
                            _rcs_fnc(_source_module, _target_module)
                # collection connection
                if target_module_ is not None:
                    _target_module_name = target_module_.name
                    _connection = _source_module_name, _target_module_name
                    if _connection not in require_connections:
                        require_connections.append(_connection)

        all_modules = []
        all_module_names = []
        require_connections = []

        for module in self.ge_modules():
            all_modules.extend(module.get_all_child_modules())

        filter_module_names = [i.name for i in all_modules]

        for module in all_modules:
            _rcs_fnc(module, None)

        return require_connections

    def get_requires_graph(self):
        list_ = [
            'graph LR\n'
        ]
        connections = self.get_require_connections()
        for i in connections:
            i_module_name, i_required_module_name = i
            i_module_node_name = i_module_name.replace('.', '_')
            i_module_node_text = '{}["{}"]\n'.format(i_module_node_name, i_module_name)
            if i_module_node_text not in list_:
                list_.append(i_module_node_text)
            #
            i_required_module_node_name = i_required_module_name.replace('.', '_')
            i_c = len(i_required_module_name.split('.'))
            if i_c == 1:
                i_required_module_node_text = '{}(("{}"))\n'.format(i_required_module_node_name, i_required_module_name)
            else:
                i_required_module_node_text = '{}["{}"]\n'.format(i_required_module_node_name, i_required_module_name)
            if i_required_module_node_text not in list_:
                list_.append(i_required_module_node_text)

            list_.append('{0} --> {1}\n'.format(i_module_node_name, i_required_module_node_name))

        return ''.join(list_)

    def set_reload(self):
        for i_module_name in self.get_require_module_names():
            _ = pkgutil.find_loader(i_module_name)
            if _:
                module = PyModule(i_module_name)
                module.set_reload()

    def test_(self):
        pass

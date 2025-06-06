# coding:utf-8
import sys

import os


class BscEnviron(object):
    PYTHON_VERSION_KEY = 'QSM_PYTHON_VERSION'

    # todo, rename to QSM_GUI_LANGUAGE
    GUI_LANGUAGE_KEY = 'QSM_UI_LANGUAGE'

    # use for version
    CORE_BASE_KEY = 'QSM_CORE_BASE'

    DEPLOY_ROOT_KEY = 'QSM_DEPLOY_ROOT'
    PROJECT_ROOT_KEY = 'QSM_PROJECT_ROOT'
    LIBRARY_ROOT_KEY = 'QSM_LIBRARY_ROOT'

    # cache
    CACHE_ROOT_KEY = 'QSM_CACHE_ROOT'
    LOCAL_CACHE_ROOT_KEY = 'QSM_CACHE_LOCAL_ROOT'

    # todo: use 0, 1 instance
    TRUE = 'true'
    FALSE = 'false'
    
    @classmethod
    def get_python_version(cls):
        return cls.get(cls.PYTHON_VERSION_KEY)

    @classmethod
    def get_test_flag(cls):
        _ = cls.get('QSM_TEST')
        if _ == '1':
            return True
        return False

    @classmethod
    def get_devlop_flag(cls):
        _ = cls.get('QSM_TEST')
        if _ == '-1':
            return True
        return False

    @classmethod
    def get_data_paths(cls):
        pass

    @classmethod
    def get(cls, key):
        return os.environ.get(key)

    @classmethod
    def get_as_array(cls, key):
        if key in os.environ:
            _ = os.environ[key]
            if _:
                return _.split(os.pathsep)
        return []

    @classmethod
    def set(cls, key, value):
        os.environ[key] = value

    @classmethod
    def append(cls, key, value):
        if key in os.environ:
            v = os.environ[key]
            if value not in v:
                os.environ[key] += os.pathsep+value
        else:
            os.environ[key] = value

    @classmethod
    def set_python_add(cls, path):
        python_paths = sys.path
        if path not in python_paths:
            sys.path.insert(0, path)

    @classmethod
    def get_qt_thread_enable(cls):
        # bug is fixed, remove this
        # if _base.BscApplication.get_is_maya():
        #     return False
        return True

    @classmethod
    def append_lua_path(cls, path):
        # use for katana
        key = 'LUA_PATH'
        value = cls.get(key)
        if value:
            if path not in value:
                value += path+';'
                cls.set(key, value)

    @classmethod
    def find_all_executes(cls, name):
        _ = cls.get_as_array('PATH')
        list_ = []
        for i in _:
            i_f = '{}/{}'.format(i, name)
            if os.path.isfile(i_f):
                list_.append(i_f)
        return list_

    @classmethod
    def find_execute(cls, name):
        _ = cls.get_as_array('PATH')
        for i in _:
            i_f = '{}/{}'.format(i, name)
            if os.path.isfile(i_f):
                return i_f

    @classmethod
    def get_deploy_root(cls):
        _ = cls.get(cls.DEPLOY_ROOT_KEY)
        if _ is None:
            raise RuntimeError()
        return _

    @classmethod
    def get_project_root(cls):
        _ = cls.get(cls.PROJECT_ROOT_KEY)
        if _ is None:
            raise RuntimeError()
        return _

    @classmethod
    def get_cache_root(cls):
        _ = cls.get(cls.CACHE_ROOT_KEY)
        if _ is None:
            raise RuntimeError()
        return _

    @classmethod
    def get_local_cache_root(cls):
        _ = cls.get(cls.LOCAL_CACHE_ROOT_KEY)
        if _ is None:
            raise RuntimeError()
        return _

    @classmethod
    def get_library_root(cls):
        _ = cls.get(cls.LIBRARY_ROOT_KEY)
        if _ is None:
            raise RuntimeError()
        return _

    @classmethod
    def get_cache_temporary_root(cls):
        return '{}/temporary'.format(cls.get_cache_root())

    @classmethod
    def get_cache_qosmic_root(cls):
        return '{}/qosmic'.format(cls.get_cache_root())

    @classmethod
    def get_local_cache_temporary_root(cls):
        return '{}/temporary'.format(cls.get_local_cache_root())

    @classmethod
    def get_cache_session_root(cls):
        return '{}/session'.format(cls.get_cache_root())

    @classmethod
    def get_cache_database_root(cls):
        return '{}/database'.format(cls.get_cache_root())

    @classmethod
    def get_gui_language(cls):
        return cls.get(cls.GUI_LANGUAGE_KEY) or 'en_US'

    @classmethod
    def get_extend_version(cls):
        if cls.get_test_flag() is True:
            return 'BETA'
        elif cls.get_devlop_flag() is True:
            return 'ALPHA'

    @classmethod
    def get_core_version(cls):
        path = os.environ.get(cls.CORE_BASE_KEY)
        if path:
            _ = os.path.basename(path)
            # if _ == '99.99.99':
            #     return '0.0.0'
            return _
        return 'unknown'


class BscEnvironExtra(BscEnviron):
    SCHEME_KEY = 'QSM_SCHEME'

    TEST_FLAG_KEY = 'QSM_TEST'
    DEVLOP_FLAG = 'QSM_DEVELOP'

    @classmethod
    def get_scheme(cls):
        return cls.get(cls.SCHEME_KEY)

    @classmethod
    def set_test_flag(cls, boolean):
        if boolean is True:
            cls.set(cls.TEST_FLAG_KEY, cls.TRUE)
        else:
            cls.set(cls.TEST_FLAG_KEY, cls.FALSE)

    @classmethod
    def set_devlop_flag(cls, boolean):
        if boolean is True:
            cls.set(cls.DEVLOP_FLAG, cls.TRUE)
        else:
            cls.set(cls.DEVLOP_FLAG, cls.FALSE)


class BscEnvironOpt(object):
    def __init__(self, environs):
        self.__raw = environs

    def set(self, key, value):
        self.__raw[key] = value

    def append(self, key, value):
        if key in self.__raw:
            v = self.__raw[key]
            if value not in v:
                self.__raw[key] += os.pathsep+value
        else:
            self.__raw[key] = value

    def prepend(self, key, value):
        if key in self.__raw:
            v = self.__raw[key]
            if value not in v:
                self.__raw[key] = value+os.pathsep+self.__raw[key]
        else:
            self.__raw[key] = value

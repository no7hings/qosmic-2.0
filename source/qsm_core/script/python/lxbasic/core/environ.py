# coding:utf-8
import sys

import os


class BscEnviron(object):
    GUI_LANGUAGE_KEY = 'QSM_UI_LANGUAGE'
    DEPLOY_ROOT_KEY = 'QSM_DEPLOY_ROOT'

    PROJECT_ROOT_KEY = 'QSM_PROJECT_ROOT'
    CACHE_ROOT_KEY = 'QSM_CACHE_ROOT'
    LOCAL_CACHE_ROOT_KEY = 'QSM_CACHE_LOCAL_ROOT'
    LIBRARY_ROOT_KEY = 'QSM_LIBRARY_ROOT'
    
    STUDIO_KEY = 'QSM_STUDIO'

    TRUE = 'true'
    FALSE = 'false'

    @classmethod
    def get_is_beta_enable(cls):
        _ = cls.get('REZ_BETA')
        if _ == '1':
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
        # fixme: why disable in maya?
        # if _base.BscApplication.get_is_maya():
        #     return False
        return True

    @classmethod
    def append_lua_path(cls, path):
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
    def get_studio(cls):
        return cls.get(cls.STUDIO_KEY) or 'DEVELOP'


class BscEnvironExtra(BscEnviron):
    SCHEME_KEY = 'QSM_SCHEME'
    BETA_ENABLE_KEY = 'QSM_BETA_ENABLE'
    TD_ENABLE_KEY = 'QSM_TD_ENABLE'

    @classmethod
    def get_scheme(cls):
        return cls.get(cls.SCHEME_KEY)

    @classmethod
    def get_beta_enable(cls):
        _ = cls.get(cls.BETA_ENABLE_KEY)
        if str(_).lower() == cls.TRUE:
            return True
        return False

    @classmethod
    def set_beta_enable(cls, boolean):
        if boolean is True:
            cls.set(cls.BETA_ENABLE_KEY, cls.TRUE)
        else:
            cls.set(cls.BETA_ENABLE_KEY, cls.FALSE)

    @classmethod
    def get_is_td_enable(cls):
        _ = cls.get(cls.TD_ENABLE_KEY)
        if _ == cls.TRUE:
            return True
        return False

    @classmethod
    def set_td_enable(cls, boolean):
        if boolean is True:
            cls.set(cls.TD_ENABLE_KEY, cls.TRUE)
        else:
            cls.set(cls.TD_ENABLE_KEY, cls.FALSE)


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

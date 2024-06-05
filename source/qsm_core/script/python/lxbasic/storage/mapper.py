# coding:utf-8
import platform

import lxbasic.resource as bsc_resource

from lxbasic.core import base as bsc_cor_base

from . import base as _base


class StgPathMapper(object):
    PATHSEP = '/'

    MAPPER = None

    @staticmethod
    def get_platform_is_windows():
        return platform.system() == 'Windows'

    @staticmethod
    def get_platform_is_linux():
        return platform.system() == 'Linux'

    @classmethod
    def __generate_mapper(cls):
        if cls.MAPPER is None:
            cls.MAPPER = bsc_cor_base.StgPathMapDict(
                _base.StgFileOpt(
                    bsc_resource.RscExtendConfigure.get_yaml('storage/path-mapper')
                ).set_read()
            )

    @classmethod
    def map_to_current(cls, path):
        if path is not None:
            if cls.get_platform_is_windows():
                return cls.map_to_windows(path)
            elif cls.get_platform_is_linux():
                return cls.map_to_linux(path)
            return _base.StgPathOpt(path).__str__()
        return path

    @classmethod
    def map_to_windows(cls, path):
        cls.__generate_mapper()
        # clear first
        path = _base.StgPathOpt(path).__str__()
        if bsc_cor_base.BscStorage.get_path_is_linux(path):
            mapper_dict = cls.MAPPER._windows_dict
            for i_root_src, i_root_tgt in mapper_dict.items():
                if path == i_root_src:
                    return i_root_tgt
                elif path.startswith(i_root_src+cls.PATHSEP):
                    return i_root_tgt+path[len(i_root_src):]
            return path
        return path

    @classmethod
    def map_to_linux(cls, path):
        """
print Path.map_to_linux(
    'l:/a'
)
        :param path:
        :return:
        """
        cls.__generate_mapper()
        # clear first
        path = _base.StgPathOpt(path).__str__()
        if bsc_cor_base.BscStorage.get_path_is_windows(path):
            mapper_dict = cls.MAPPER._linux_dict
            for i_root_src, i_root_tgt in mapper_dict.items():
                if path == i_root_src:
                    return i_root_tgt
                elif path.startswith(i_root_src+cls.PATHSEP):
                    return i_root_tgt+path[len(i_root_src):]
            return path
        return path


class StgEnvPathMapper(object):
    MAPPER = None

    @classmethod
    def __generate_mapper(cls):
        if cls.MAPPER is None:
            cls.MAPPER = bsc_cor_base.StgEnvPathMapDict(
                _base.StgFileOpt(
                    bsc_resource.RscExtendConfigure.get_yaml('storage/path-environment-mapper')
                ).set_read()
            )

    @classmethod
    def map_to_path(cls, path, pattern='[KEY]'):
        """
        print(
            PathEnv.map_to_path(
                '[QSM_CACHE_ROOT]/nsa_dev/assets/chr/td_test/user/team.srf/extend/look/klf/v001/all.json',
                pattern='[KEY]'
            )
        )
        print(
            PathEnv.map_to_path(
                '${QSM_CACHE_ROOT}/nsa_dev/assets/chr/td_test/user/team.srf/extend/look/klf/v001/all.json',
                pattern='${KEY}'
            )
        )
        :param path:
        :param pattern:
        :return:
        """
        cls.__generate_mapper()
        path = _base.StgPathOpt(path).__str__()
        mapper_dict = cls.MAPPER._env_dict
        for i_env_key, i_root in mapper_dict.items():
            i_string = pattern.replace('KEY', i_env_key)
            if path == i_string:
                return i_root
            elif path.startswith(i_string+'/'):
                return i_root+path[len(i_string):]
        return path

    @classmethod
    def map_to_env(cls, path, pattern='[KEY]'):
        """
        print(
            PathEnv.map_to_env(
                '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/look/klf/v001/all.json',
                pattern='[KEY]'
            ),
        )
        print(
            PathEnv.map_to_env(
                '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/look/klf/v001/all.json',
                pattern='${KEY}'
            )
        )
        :param path:
        :param pattern:
        :return:
        """
        cls.__generate_mapper()
        path = _base.StgPathOpt(path).__str__()
        mapper_dict = cls.MAPPER._path_dict
        for i_root, i_env_key in mapper_dict.items():
            i_string = pattern.replace('KEY', i_env_key)
            if path == i_root:
                return i_string
            elif path.startswith(i_root+'/'):
                return i_string+path[len(i_root):]
        return path

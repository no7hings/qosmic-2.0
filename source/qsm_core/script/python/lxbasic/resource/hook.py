# coding:utf-8
import platform

import lxbasic.log as bsc_log

import lxbasic.content as bsc_content
# resource
from . import base as _base


class BscHook(object):
    BRANCH = 'hooks'

    @classmethod
    def get_yaml(cls, key, search_paths=None):
        return _base.BscResource.get(
            '{}/{}.yml'.format(cls.BRANCH, key), search_paths
        )

    @classmethod
    def get_python(cls, key, search_paths=None):
        return _base.BscResource.get(
            '{}/{}.py'.format(cls.BRANCH, key), search_paths
        )

    @classmethod
    def get_shell(cls, key, search_paths=None):
        if platform.system() == 'Linux':
            return _base.BscResource.get(
                '{}.sh'.format(key), search_paths
            )
        elif platform.system() == 'Windows':
            return _base.BscResource.get(
                '{}.bat'.format(key)
            )

    @classmethod
    def get_args(cls, key, search_paths=None):
        yaml_file_path = cls.get_yaml(key, search_paths)
        if yaml_file_path:
            configure = bsc_content.Content(value=yaml_file_path)
            type_ = configure.get('option.type')
            if type_:
                python_file_path = cls.get_python(key, search_paths)
                shell_file_path = cls.get_shell(key, search_paths)
                return type_, key, configure, yaml_file_path, python_file_path, shell_file_path

            bsc_log.Log.trace_warning(
                'hook file is not valid: "{}".'.format(yaml_file_path)
            )
            return None
        bsc_log.Log.trace_error(
            'hook file is not found: "{}".'.format(key)
        )
        return None


class BscOptionHook(BscHook):
    BRANCH = 'option-hooks'

# coding:utf-8
import platform

import lxbasic.log as bsc_log

import lxcontent.core as ctt_core
# resource
from . import base as rsc_cor_base


class RscHook(object):
    BRANCH = 'hooks'

    @classmethod
    def get_yaml(cls, key, search_paths=None):
        return rsc_cor_base.ExtendResource.get(
            '{}/{}.yml'.format(cls.BRANCH, key), search_paths
        )

    @classmethod
    def get_python(cls, key, search_paths=None):
        return rsc_cor_base.ExtendResource.get(
            '{}/{}.py'.format(cls.BRANCH, key), search_paths
        )

    @classmethod
    def get_shell(cls, key, search_paths=None):
        if platform.system() == 'Linux':
            return rsc_cor_base.ExtendResource.get(
                '{}.sh'.format(key), search_paths
            )
        elif platform.system() == 'Windows':
            return rsc_cor_base.ExtendResource.get(
                '{}.bat'.format(key)
            )

    @classmethod
    def get_args(cls, key):
        yaml_file_path = cls.get_yaml(key)
        if yaml_file_path:
            configure = ctt_core.Content(value=yaml_file_path)
            type_ = configure.get('option.type')
            if type_:
                python_file_path = cls.get_python(key)
                shell_file_path = cls.get_shell(key)
                return type_, key, configure, yaml_file_path, python_file_path, shell_file_path

            bsc_log.Log.trace_warning(
                'hook file is not valid: "{}"'.format(yaml_file_path)
            )
            return None
        bsc_log.Log.trace_error(
            'hook file is found: "{}"'.format(key)
        )
        return None

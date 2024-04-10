# coding:utf-8
import fnmatch

import lxresource as bsc_resource

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxcontent.core as ctt_core


class SsnUtil(object):
    HOST = 'localhost'
    PORT = 9527


class SsnHookMtd(object):
    @classmethod
    def set_cmd_run(cls, cmd):
        import urllib

        unique_id = bsc_core.UuidMtd.generate_new()

        hook_yml_file_path = bsc_storage.StgUserMtd.get_user_session_file(unique_id=unique_id)

        bsc_storage.StgFileOpt(hook_yml_file_path).set_write(
            dict(
                user=bsc_core.SysBaseMtd.get_user_name(),
                tiame=bsc_core.SysBaseMtd.get_time(),
                cmd=cmd,
            )
        )

        urllib.urlopen(
            'http://{host}:{port}/cmd-run?uuid={uuid}'.format(
                **dict(
                    host=SsnUtil.HOST,
                    port=SsnUtil.PORT,
                    uuid=unique_id
                )
            )
        )


class SsnHookEngineMtd(object):
    CONTENT = None

    @classmethod
    def _generate_content(cls):
        if cls.CONTENT is not None:
            return cls.CONTENT
        cls.CONTENT = ctt_core.Content(
            value=bsc_resource.RscExtendConfigure.get_yaml('session/hook-engine')
        )
        cls.CONTENT.do_flatten()
        return cls.CONTENT

    @classmethod
    def get_all(cls):
        c = cls._generate_content()
        return c.get_key_names_at('command') or []

    @classmethod
    def get_command(cls, hook_engine, **kwargs):
        c = cls._generate_content()
        _ = c.get(
            'command.{}'.format(hook_engine)
        )
        return _.format(**kwargs)


class SsnHookFileMtd(object):
    BRANCH = 'hooks'

    @classmethod
    def get_python(cls, key, search_paths=None):
        return bsc_resource.ExtendResource.get(
            '{}/{}.py'.format(cls.BRANCH, key), search_paths
        )

    @classmethod
    def get_shell(cls, key, search_paths=None):
        if bsc_core.SysPlatformMtd.get_is_linux():
            return bsc_resource.ExtendResource.get(
                '{}/{}.sh'.format(cls.BRANCH, key), search_paths
            )
        elif bsc_core.SysPlatformMtd.get_is_windows():
            return bsc_resource.ExtendResource.get(
                '{}/{}.bat'.format(cls.BRANCH, key), search_paths
            )

    @classmethod
    def get_yaml(cls, key, search_paths=None):
        return bsc_resource.ExtendResource.get(
            '{}/{}.yml'.format(cls.BRANCH, key), search_paths
        )

    @classmethod
    def get_command(cls, key):
        return bsc_resource.ExtendResource.get(
            '{}/{}.yml'.format(cls.BRANCH, key)
        )

    @classmethod
    def get_full_key(cls, key):
        return

    #
    @classmethod
    def get_hook_abs_path(cls, src_key, tgt_key):
        """
        for i in ['../shotgun/shotgun-create', '../maya/geometry-export', '../maya/look-export']:
            print SsnHookFileMtd.get_hook_abs_path(
                'rsv-task-methods/asset/usd/usd-create', i
            )

        rsv-task-methods/asset/shotgun/shotgun-create
        rsv-task-methods/asset/maya/geometry-export
        rsv-task-methods/asset/maya/look-export

        :param src_key: str(<hook-key>)
        :param tgt_key: str(<hook-key>)
        :return: str(<hook-key>)
        """
        if fnmatch.filter([tgt_key], '.*'):
            s_0 = tgt_key.split('.')[-1].strip()
            c_0 = tgt_key.count('.')
            ss_1 = src_key.split('/')
            c_1 = len(ss_1)
            if c_0 < c_1:
                return '{}{}'.format('/'.join(ss_1[:-c_0]), s_0)
            elif c_0 == c_1:
                return s_0
            else:
                raise ValueError(
                    'count of sep "." out of range'
                )
        return tgt_key

    @classmethod
    def get_extra_file(cls, key):
        directory_path = bsc_core.EnvBaseMtd.get_session_root()
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.session/extra/{}/{}{}'.format(
            directory_path, region, key, '.yml'
        )

    @classmethod
    def set_extra_data_save(cls, raw):
        key = bsc_core.UuidMtd.generate_new()
        file_path = cls.get_extra_file(key)
        bsc_storage.StgFileOpt(file_path).set_write(raw)
        return key

    @classmethod
    def get_extra_data(cls, key):
        file_path = cls.get_extra_file(key)
        return bsc_storage.StgFileOpt(file_path).set_read()


class SsnOptionHookFileMtd(SsnHookFileMtd):
    BRANCH = 'option-hooks'


class SsnHookServerMtd(object):
    @classmethod
    def get_key(cls, **kwargs):
        return bsc_core.UuidMtd.generate_by_text(
            bsc_core.ArgDictStringMtd.to_string(**kwargs)
        )

    @classmethod
    def get_file_path(cls, **kwargs):
        directory_path = bsc_core.EnvBaseMtd.get_session_root()
        key = cls.get_key(**kwargs)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.session/option-hook/{}/{}{}'.format(
            directory_path, region, key, '.yml'
        )

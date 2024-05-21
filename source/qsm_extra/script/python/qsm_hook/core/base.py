# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage


class HookBase(object):
    HOST = 'localhost'
    PORT = 9527

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

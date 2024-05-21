# coding:utf-8
import urllib

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from . import base as _base


class Hook(object):
    @classmethod
    def execute(cls, group, name, cmd_script):

        unique_id = bsc_core.UuidMtd.generate_new()
        hook_file_path = _base.HookBase.get_file_path(uuid=unique_id)

        bsc_storage.StgFileOpt(hook_file_path).set_write(
            dict(
                group=group,
                name=name,
                cmd_script=cmd_script,
                user=bsc_core.SysBaseMtd.get_user_name(),
                tiame=bsc_core.SysBaseMtd.get_time(exact=True),
            )
        )

        _ = urllib.urlopen(
            'http://{host}:{port}/hook?uuid={uuid}'.format(
                **dict(
                    host=_base.HookBase.HOST,
                    port=_base.HookBase.PORT,
                    uuid=unique_id
                )
            )
        )
        if _:
            print _.read()

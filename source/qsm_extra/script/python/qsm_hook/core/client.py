# coding:utf-8
import urllib

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from . import base as _base


class Hook(object):
    @classmethod
    def new_task(cls, group, name, cmd_script, completion_notice=None):
        user_name = bsc_core.SysBaseMtd.get_user_name()
        time_tag = bsc_core.SysBaseMtd.get_time_tag()

        unique_id = _base.HookBase.get_key(
            user=user_name,
            time=time_tag
        )
        hook_file_path = _base.HookBase.get_file_path(uuid=unique_id)

        bsc_storage.StgFileOpt(hook_file_path).set_write(
            dict(
                group=group,
                name=name,
                cmd_script=cmd_script,
                #
                user=bsc_core.SysBaseMtd.get_user_name(),
                time=time_tag,
                completion_notice=completion_notice
            )
        )

        _ = urllib.urlopen(
            'http://{host}:{port}/task?uuid={uuid}'.format(
                **dict(
                    host=_base.HookBase.HOST,
                    port=_base.HookBase.PORT,
                    uuid=unique_id
                )
            )
        )
        if _:
            print _.read()

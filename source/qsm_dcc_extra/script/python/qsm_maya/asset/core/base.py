# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage


class AssetCache(object):
    @classmethod
    def get_key(cls, file_path):
        return bsc_core.UuidMtd.generate_by_file(file_path)

    @classmethod
    def get_skin_proxy_file(cls, file_path):
        directory_path = bsc_core.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/skin-proxy/{}/{}{}'.format(
            directory_path, region, key, '.ma'
        )

    @classmethod
    def get_dynamic_gpu_directory(cls, user_name):
        directory_path = bsc_core.EnvBaseMtd.get_temporary_root()
        key = bsc_core.UuidMtd.generate_new()
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/dynamic-gpu/{}/{}/{}'.format(
            directory_path, user_name, region, key
        )

    @classmethod
    def get_dynamic_gpu(cls, file_path):
        directory_path = bsc_core.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/dynamic-gpu/{}/{}/gpu.{}'.format(
            directory_path, region, key, '.abc'
        )


class MayaCacheProcess(object):
    @classmethod
    def generate_command(cls, option):
        if bsc_core.SysApplicationMtd.get_is_maya():
            maya_version = bsc_core.SysApplicationMtd.get_maya_version()
        else:
            maya_version = '2019'
        # windows
        cmds = [
            'rez-env maya-{} qsm_dcc_main'.format(maya_version),
            (
                r'-- mayabatch -command '
                r'"python('
                r'\"import lxsession.commands as ssn_commands;'
                r'ssn_commands.execute_option_hook(option=\\\"{hook_option}\\\")\")"'
            ).format(
                hook_option='option_hook_key=dcc-process/maya-cache-process&' + option
            )
        ]
        return ' '.join(cmds)

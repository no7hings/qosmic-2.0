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
    def generate_skin_proxy_file(cls, file_path):
        root = bsc_core.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/skin-proxy/{}/{}.ma'.format(
            root, region, key
        )

    @classmethod
    def generate_dynamic_gpu_directory(cls, user_name):
        root = bsc_core.EnvBaseMtd.get_temporary_root()
        key = bsc_core.UuidMtd.generate_new()
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/dynamic-gpu/{}/{}/{}'.format(
            root, user_name, region, key
        )

    @classmethod
    def generate_animation_file(cls, user_name):
        root = bsc_core.EnvBaseMtd.get_temporary_root()
        key = bsc_core.UuidMtd.BASIC
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/animation/{}/{}/{}.json'.format(
            root, user_name, region, key
        )

    @classmethod
    def generate_unit_assembly_file(cls, file_path):
        root = bsc_core.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/unit-assembly/{}/{}/source.ma'.format(
            root, region, key
        )

    @classmethod
    def generate_gpu_instance_file(cls, file_path):
        root = bsc_core.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/unit-assembly/{}/{}/gpu.ma'.format(
            root, region, key
        )



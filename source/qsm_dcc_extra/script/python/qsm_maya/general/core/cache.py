# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage


class ResourceCacheNodes(object):
    SkinProxyRoot = '|__SKIN_PROXY__'
    SkinProxyName = 'skin_proxy_dgc'

    DynamicGpuRoot = '|__DYNAMIC_GPU__'
    DynamicGpuName = 'dynamic_gpu_dgc'
    
    UnitAssemblyRoot = '|__UNIT_ASSEMBLY__'
    UnitAssemblyName = 'unit_assembly_dgc'
    
    GpuInstanceRoot = '|__GPU_INSTANCE__'
    GpuInstanceName = 'gpu_instance_dgc'

    CfxClothRoot = '|__CFX_CLOTH__'
    CfxClothName = 'cfx_cloth_dgc'


class ResourceCache(object):
    @classmethod
    def get_key(cls, file_path):
        return bsc_core.BscUuid.generate_by_file(file_path)

    @classmethod
    def generate_skin_proxy_scene_file(cls, file_path):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = cls.get_key(file_path)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/skin-proxy/{}/{}.ma'.format(
            root, region, key
        )

    @classmethod
    def generate_skin_proxy_data_file(cls, file_path):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = cls.get_key(file_path)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/skin-proxy/{}/{}.json'.format(
            root, region, key
        )

    @classmethod
    def generate_dynamic_gpu_directory(cls, user_name, key=None):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        if key is None:
            key = bsc_core.BscUuid.generate_new()
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/dynamic-gpu/{}/{}/{}'.format(
            root, user_name, region, key
        )

    @classmethod
    def generate_animation_file(cls, user_name):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = bsc_core.BscUuid.BASIC
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/animation/{}/{}/{}.json'.format(
            root, user_name, region, key
        )

    @classmethod
    def generate_unit_assembly_file(cls, file_path):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = cls.get_key(file_path)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/scenery/{}/{}/unit_assembly.ma'.format(
            root, region, key
        )

    @classmethod
    def generate_gpu_instance_file(cls, file_path):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = cls.get_key(file_path)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/scenery/{}/{}/gpu_instance.ma'.format(
            root, region, key
        )

    @classmethod
    def generate_rig_geometry_data_file(cls, file_path, tag):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = cls.get_key(file_path)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/rig-geometry/{}/{}/{}.json'.format(
            root, region, key, tag
        )

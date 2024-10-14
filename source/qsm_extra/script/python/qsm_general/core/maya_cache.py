# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage


class MayaCache(object):
    class ApiVersions:
        UnitAssembly = 1.0

    @classmethod
    def get_key(cls, file_path, version=None):
        return bsc_core.BscUuid.generate_by_file(file_path, version)

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
    def generate_dynamic_gpu_directory(cls, key=None):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        if key is None:
            key = bsc_core.BscUuid.generate_new()
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/dynamic-gpu/{}/{}'.format(
            root, region, key
        )

    @classmethod
    def generate_dynamic_gpu_local_directory(cls, key=None):
        root = bsc_core.EnvBaseMtd.get_local_cache_temporary_root()
        if key is None:
            key = bsc_core.BscUuid.generate_new()
        date_tag = bsc_core.BscSystem.get_date_tag()
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/dynamic-gpu/{}/{}/{}'.format(
            root, date_tag, region, key
        )

    @classmethod
    def generate_character_motion_file(cls, user_name):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = bsc_core.BscUuid.BASIC
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/character-motion/{}/{}/{}.json'.format(
            root, user_name, region, key
        )

    @classmethod
    def generate_control_motion_file(cls, user_name):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = bsc_core.BscUuid.BASIC
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/control-motion/{}/{}/{}.json'.format(
            root, user_name, region, key
        )

    @classmethod
    def generate_asset_unit_assembly_file(cls, file_path, version=None):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = cls.get_key(file_path, version)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/scenery/{}/{}/unit_assembly.ma'.format(
            root, region, key
        )

    @classmethod
    def generate_asset_unit_assembly_file_new(cls, file_path, version=ApiVersions.UnitAssembly):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = cls.get_key(file_path, version)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/unit-assembly/{}/{}/scene.ma'.format(
            root, region, key
        )

    @classmethod
    def generate_asset_gpu_instance_file(cls, file_path, version=None):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = cls.get_key(file_path, version)
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

    @classmethod
    def generate_asset_rig_validation_result_file(cls, file_path, api_version=None):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = cls.get_key(file_path, api_version)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/rig-validation/{}/{}.json'.format(
            root, region, key
        )

    @classmethod
    def generate_asset_scenery_validation_result_file(cls, file_path, option_hash=None):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = cls.get_key(file_path, option_hash)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/scenery-validation/{}/{}.json'.format(
            root, region, key
        )

    @classmethod
    def generate_asset_mesh_count_file(cls, file_path, version=None):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = cls.get_key(file_path, version)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/mesh-count/{}/{}.json'.format(
            root, region, key
        )

    @classmethod
    def generate_asset_system_resource_usage_file(cls, file_path, version=None):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = cls.get_key(file_path, version)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/system-resource-usage/{}/{}.json'.format(
            root, region, key
        )
    
    @classmethod
    def generate_asset_snapshot_file(cls, file_path, version=None):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        key = cls.get_key(file_path, version)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.asset-cache/snapshot/{}/{}.jpg'.format(
            root, region, key
        )

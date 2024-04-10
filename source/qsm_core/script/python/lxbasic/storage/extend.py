# coding:utf-8
import uuid

from lxbasic.core import base as bsc_cor_base

from lxbasic.core import raw as bsc_cor_raw

from lxbasic.core import environ as bsc_cor_environ

from . import base as bsc_stg_base


class StgTmpBaseMtd(object):
    ROOT = '/l/temp'

    @classmethod
    def get_user_directory(cls, tag):
        return bsc_cor_base.StgBasePathMapMtd.map_to_current(
            '{root}/temporary/{tag}/{date_tag}-{user}'.format(
                **dict(
                    root=cls.ROOT,
                    date_tag=bsc_cor_base.SysBaseMtd.get_date_tag(),
                    user=bsc_cor_base.SysBaseMtd.get_user_name(),
                    tag=tag
                )
            )
        )

    @classmethod
    def get_cache_directory(cls, tag):
        return bsc_cor_base.StgBasePathMapMtd.map_to_current(
            '{root}/temporary/{tag}/{user}'.format(
                **dict(
                    root=cls.ROOT,
                    user=bsc_cor_base.SysBaseMtd.get_user_name(),
                    tag=tag
                )
            )
        )

    @classmethod
    def get_save_region(cls, unique_id):
        number = abs(uuid.UUID(unique_id).int)
        return bsc_cor_raw.RawIntegerOpt(number%4096).set_encode_to_36()


class StgTmpThumbnailMtd(object):
    @classmethod
    def get_key(cls, file_path):
        return bsc_cor_base.UuidMtd.generate_by_file(file_path)

    @classmethod
    def get_file_path_(cls, file_path, width=128, ext='.jpg'):
        directory_path = bsc_cor_environ.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.thumbnail/{}/{}/{}{}'.format(
            directory_path, region, key, width, ext
        )

    @classmethod
    def generate_for_qt_resize(cls, file_path, width=128, ext='.jpg'):
        directory_path = bsc_cor_environ.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.qt-thumbnail/{}/{}/{}{}'.format(
            directory_path, region, key, width, ext
        )


class StgTmpUsdMtd(object):
    @classmethod
    def generate_key(cls, file_paths):
        return bsc_cor_base.UuidMtd.generate_by_files(file_paths)

    @classmethod
    def generate_file_path(cls, file_paths):
        directory_path = bsc_cor_environ.EnvBaseMtd.get_temporary_root()
        key = cls.generate_key(file_paths)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.usd/{}/{}'.format(
            directory_path, region, key
        )


class StgTmpYamlMtd(object):
    @classmethod
    def get_key(cls, file_path):
        return bsc_cor_base.UuidMtd.generate_by_file(file_path)

    @classmethod
    def get_file_path(cls, file_path, tag='untitled'):
        directory_path = bsc_cor_environ.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.yml/{}/{}/{}{}'.format(
            directory_path, tag, region, key, '.yml'
        )


class StgTmpTextMtd(object):
    @classmethod
    def get_key(cls, file_path):
        return bsc_cor_base.UuidMtd.generate_by_file(file_path)

    @classmethod
    def get_file_path(cls, file_path, tag='untitled'):
        directory_path = bsc_cor_environ.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.txt/{}/{}/{}{}'.format(
            directory_path, tag, region, key, '.txt'
        )


class StgTmpInfoMtd(object):
    @classmethod
    def get_key(cls, file_path):
        return bsc_cor_base.UuidMtd.generate_by_file(file_path)

    @classmethod
    def get_file_path(cls, file_path, tag='untitled'):
        directory_path = bsc_cor_environ.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.info/{}/{}/{}{}'.format(
            directory_path, tag, region, key, '.txt'
        )


class DccTempCacheMtd(object):
    @classmethod
    def _to_file_path(cls, key, category):
        directory_path = bsc_cor_environ.EnvBaseMtd.get_database_root()
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/{}/{}/{}'.format(directory_path, category, region, key)

    @classmethod
    def get_key(cls, data):
        return bsc_cor_base.HashMtd.get_hash_value(
            data, as_unique_id=True
        )

    @classmethod
    def get_value(cls, key, category):
        file_path = cls._to_file_path(key, category)
        gzip_file = bsc_stg_base.StgGzipFileOpt(file_path, '.yml')
        if gzip_file.get_is_exists() is True:
            return gzip_file.set_read()

    @classmethod
    def set_value(cls, key, value, force, category):
        file_path = cls._to_file_path(key, category)
        gzip_file = bsc_stg_base.StgGzipFileOpt(file_path, '.yml')
        if gzip_file.get_is_exists() is False or force is True:
            gzip_file.set_write(value)
            return True


class DccTempCacheMtdForGeometryUv(object):
    @classmethod
    def get_value(cls, key):
        return DccTempCacheMtd.get_value(
            key,
            category='geometry/uv-map'
        )

    @classmethod
    def set_value(cls, key, value, force):
        return DccTempCacheMtd.set_value(
            key,
            value,
            force,
            category='geometry/uv-map'
        )

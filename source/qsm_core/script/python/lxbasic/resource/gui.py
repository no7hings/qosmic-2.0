# coding:utf-8
# resource
from . import base as _base


class RscExtendIcon(object):
    BRANCH = 'icons'

    DEFAULT_EXTENSIONS = {'.png', '.svg'}

    @classmethod
    def get(cls, key, file_format=None):
        if file_format is not None:
            result = _base.BscExtendResource.get(
                '{}/{}.{}'.format(cls.BRANCH, key, file_format)
            )
            if result is not None:
                return result
        return _base.BscExtendResource.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )

    @classmethod
    def find_all_keys_at(cls, group_name, ext_includes=None):
        return _base.BscExtendResource.find_all_file_keys_at(
            cls.BRANCH, group_name, ext_includes=ext_includes or cls.DEFAULT_EXTENSIONS
        )

    @classmethod
    def find_all_keys(cls, ext_includes=None):
        return _base.BscExtendResource.find_all_file_keys(
            cls.BRANCH, ext_includes=ext_includes or cls.DEFAULT_EXTENSIONS
        )


class RscExtendFont(object):
    BRANCH = 'fonts'

    DEFAULT_EXTENSIONS = {'.ttf', '.ttc'}

    @classmethod
    def get(cls, key):
        return _base.BscExtendResource.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )

    @classmethod
    def find_all_keys_at(cls, group_name):
        return _base.BscExtendResource.find_all_file_keys_at(
            cls.BRANCH, group_name, ext_includes=cls.DEFAULT_EXTENSIONS
        )

    @classmethod
    def find_all_keys(cls, ext_includes=None):
        return _base.BscExtendResource.find_all_file_keys(
            cls.BRANCH, ext_includes=ext_includes or cls.DEFAULT_EXTENSIONS
        )

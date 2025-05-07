# coding:utf-8
import lxbasic.resource as bsc_resource

import qsm_general.core as qsm_gnl_core

import _model


class AbsBase(object):
    class EntityTypes:
        User = _model.User.__name__
        Project = _model.Project.__name__
        Sequence = _model.Sequence.__name__

    DATABASE_ROOT_NAME = 'QSM'

    @classmethod
    def _to_database_key(cls, database_type, database_name):
        return '{}_{}_{}'.format(
            cls.DATABASE_ROOT_NAME, database_type, database_name
        )

    @classmethod
    def _get_mysql_configure(cls):
        if qsm_gnl_core.scheme_is_release():
            key = 'lazy/mysql_new'
        else:
            key = 'lazy/mysql'
        return bsc_resource.BscConfigure.get_as_content(key)

    @classmethod
    def _get_mysql_options(cls):
        cfg = cls._get_mysql_configure()
        return cfg.get('options')

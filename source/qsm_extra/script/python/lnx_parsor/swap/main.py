# coding:utf-8
import os

import sys

import lxbasic.core as bsc_core

from ..core import base as _cor_base


class Swap(object):
    STAGE_CACHE = None

    @classmethod
    def generate_root(cls, location='X:'):
        if cls.STAGE_CACHE:
            return cls.STAGE_CACHE.root(location)

        cgt_exe_paths = bsc_core.BscProcess.find_process_path_by_name(
            'CgTeamWork.exe'
        )
        if cgt_exe_paths:
            dir_path = os.path.dirname(cgt_exe_paths[0])
            py_path = '{}/base'.format(os.path.dirname(dir_path.replace('\\', '/')))
            if py_path not in sys.path:
                sys.path.append(py_path)

            # import here
            from .. import cgt as _cgt
            stage = _cgt.Stage()
            cls.STAGE_CACHE = stage
            return stage.root(location)

        # import here
        from .. import scan as _scan
        stage = _scan.Stage()
        cls.STAGE_CACHE = stage
        return stage.root(location)

    @staticmethod
    def set_sync_cache_flag(boolean):
        _cor_base.GlobalVar.SYNC_CACHE_FLAG = boolean


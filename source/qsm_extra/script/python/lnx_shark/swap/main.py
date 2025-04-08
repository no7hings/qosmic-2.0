# coding:utf-8
import os

import sys

import lxbasic.core as bsc_core

from .. import scan as _scan

from .. import cgt as _cgt


class Swap(object):
    @classmethod
    def generate_stage(cls):
        cgt_exe_path = bsc_core.BscProcess.find_process_path_by_name(
            'CgTeamWork.exe'
        )
        if cgt_exe_path:
            dir_path = os.path.dirname(cgt_exe_path)
            py_path = '{}/base'.format(os.path.dirname(dir_path))
            if py_path not in sys.path:
                sys.path.append(py_path)
            return _cgt.Stage()
        return _scan.Stage()


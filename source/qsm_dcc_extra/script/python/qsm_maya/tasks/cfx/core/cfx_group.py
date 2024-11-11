# coding:utf-8
import collections

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

from .... import core as _mya_core

from ... import _abc


class ShotCfxGroup(_abc.AbsGroupOpt):
    LOCATION = '|assets|cfx'

    def __init__(self, *args, **kwargs):
        super(ShotCfxGroup, self).__init__(*args, **kwargs)

# coding:utf-8
import os

os.environ['QSM_UI_LANGUAGE'] = 'chs'

import lxbasic.session as bsc_session

bsc_session.Hook.execute(
    '*/qsm-lazy-resource'
)

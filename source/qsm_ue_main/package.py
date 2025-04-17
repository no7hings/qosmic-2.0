# coding:utf-8
name = 'qsm_ue_core'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = [
    'qsm_dcc_main',
    # ue
    'qsm_ue_core',
]


def commands():
    env.QSM_UE_MAIN_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')
    # configure
    env.QSM_EXTEND_CONFIGURES.append('{root}/configures')
    # resource
    env.QSM_EXTEND_RESOURCES.append('{root}/resources')

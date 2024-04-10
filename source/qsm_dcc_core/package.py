# coding:utf-8
name = 'qsm_dcc_core'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = [
    'qsm_dcc_lib',
    'qsm_core',
]


def commands():
    # root
    env.QSM_DCC_CORE_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')


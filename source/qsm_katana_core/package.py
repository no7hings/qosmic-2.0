# coding:utf-8
name = 'qsm_katana_core'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = [
    'qsm_katana_lib',
]


def commands():
    env.QSM_KATANA_CORE_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')
    # configure
    env.QSM_EXTEND_CONFIGURES.append('{root}/configures')
    # resource
    env.QSM_EXTEND_RESOURCES.append('{root}/resources')

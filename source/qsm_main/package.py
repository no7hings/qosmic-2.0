# coding:utf-8
name = 'qsm_main'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = [
    'qsm_core',
    'qsm_gui',
    'qsm_resource',
]


def commands():
    # root
    env.QSM_MAIN_BASE = '{root}'
    env.PATH.append('{root}/script/bin')
    # python
    env.PYTHONPATH.append('{root}/script/python')


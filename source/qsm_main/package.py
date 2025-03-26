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
    'qsm_extra',
    # tools
    'qsm_resora',
    'qsm_nexsolve',
]


def commands():
    # root
    env.QSM_MAIN_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')


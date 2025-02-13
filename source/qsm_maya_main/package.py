# coding:utf-8
name = 'qsm_dcc_main'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = [
    # basic
    'qsm_main',
    # dcc
    'qsm_dcc_lib',
    'qsm_dcc_core',
    'qsm_dcc_gui',
    'qsm_dcc_resource',
    'qsm_dcc_extra',
    # maya
    'qsm_maya_core',
    'qsm_maya_core_lib',
]


def commands():
    env.QSM_DCC_MAIN_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')
    # startup in dcc
    # maya
    env.PYTHONPATH.append('{root}/startup/maya/scripts')


timestamp = 1639389924

format_version = 2

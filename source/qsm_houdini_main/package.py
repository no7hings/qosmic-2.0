# coding:utf-8
name = 'qsm_houdini_main'

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
    #
    'qsm_houdini_core',
    'qsm_houdini_core_lib',
]


def commands():
    env.QSM_DCC_MAIN_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')
    # startup in dcc
    # houdini-setup
    env.HOUDINI_PATH.append('{root}/startup/houdini;&')


timestamp = 1639389924

format_version = 2

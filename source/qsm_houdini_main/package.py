# coding:utf-8
name = 'qsm_houdini_main'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = [
    'qsm_dcc_main',
    # katana
    'qsm_houdini_core',
    'qsm_houdini_lib',
]


def commands():
    env.QSM_DCC_MAIN_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')
    # configure
    env.QSM_EXTEND_CONFIGURES.append('{root}/configures')
    # resource
    env.QSM_EXTEND_RESOURCES.append('{root}/resources')
    # houdini startup
    env.HOUDINI_PATH.append('{root}/startup/houdini;&')


timestamp = 1639389924

format_version = 2

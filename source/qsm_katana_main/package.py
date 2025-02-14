# coding:utf-8
name = 'qsm_katana_main'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = [
    'qsm_dcc_main',
    # maya
    'qsm_katana_core',
    'qsm_katana_lib',
]


def commands():
    env.QSM_DCC_MAIN_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')
    # configure
    env.QSM_EXTEND_CONFIGURES.append('{root}/configures')
    # resource
    env.QSM_EXTEND_RESOURCES.append('{root}/resources')
    # katana startup
    env.KATANA_RESOURCES.append('{root}/startup/katana')


timestamp = 1639389924

format_version = 2

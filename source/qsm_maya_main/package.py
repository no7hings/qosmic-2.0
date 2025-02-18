# coding:utf-8
name = 'qsm_maya_main'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = [
    'qsm_dcc_main',
    # maya
    'qsm_maya_core',
    'qsm_maya_lib',
    # tools
    'qsm_maya_resora',
]


def commands():
    env.QSM_DCC_MAIN_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')
    # configure
    env.QSM_EXTEND_CONFIGURES.append('{root}/configures')
    # resource
    env.QSM_EXTEND_RESOURCES.append('{root}/resources')
    # maya startup
    env.PYTHONPATH.append('{root}/startup/maya/scripts')


timestamp = 1639389924

format_version = 2

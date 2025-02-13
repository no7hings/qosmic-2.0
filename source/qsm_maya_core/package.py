# coding:utf-8
name = 'qsm_maya_core'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = [
    'qsm_maya_core_lib'
]


def commands():
    env.QSM_MAYA_CORE_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')
    # configure
    env.QSM_EXTEND_CONFIGURES.append('{root}/configures')
    # resource
    env.QSM_EXTEND_RESOURCES.append('{root}/resources')

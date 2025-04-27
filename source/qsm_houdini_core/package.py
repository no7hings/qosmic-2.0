# coding:utf-8
name = 'qsm_houdini_core'

version = '0.0.0'

description = 'package for houdini'

authors = ['']

tools = []

requires = [
    'qsm_houdini_lib',
]


def commands():
    env.QSM_HOUDINI_CORE_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')
    # configure
    env.QSM_EXTEND_CONFIGURES.append('{root}/configures')
    # resource
    env.QSM_EXTEND_RESOURCES.append('{root}/resources')

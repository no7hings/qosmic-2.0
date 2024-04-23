# coding:utf-8
name = 'qsm_process'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = []


def commands():
    env.QSM_PROCESS_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')
    # configure
    env.QSM_EXTEND_CONFIGURES.append('{root}/configures')
    # resource
    env.QSM_EXTEND_RESOURCES.append('{root}/resources')

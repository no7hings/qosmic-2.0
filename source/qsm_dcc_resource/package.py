# coding:utf-8
name = 'qsm_dcc_resource'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = []


def commands():
    env.QSM_DCC_RESOURCE_BASE = '{root}'
    # resources
    env.QSM_EXTEND_RESOURCES.append('{root}/resources')

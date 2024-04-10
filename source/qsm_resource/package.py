# coding:utf-8
name = 'qsm_resource'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = []


def commands():
    env.QSM_RESOURCE_BASE = '{root}'
    # resources
    env.QSM_EXTEND_RESOURCES.append('{root}/resources')

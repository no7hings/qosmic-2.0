# coding:utf-8
name = 'qsm_gui'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = [
    'qsm_core'
]


def commands():
    # root
    env.QSM_GUI_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')


timestamp = 1637923804

format_version = 2

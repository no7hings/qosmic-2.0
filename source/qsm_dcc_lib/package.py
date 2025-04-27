# coding:utf-8
name = 'qsm_dcc_lib'

version = '0.0.0'

description = ''

authors = ['']

tools = []


# requires = []
def requires():
    # todo: use this method to dynamic load requires package
    return []


def commands():
    # root
    env.QSM_DCC_LIB_BASE = '{root}'

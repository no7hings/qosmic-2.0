# coding:utf-8
name = 'qsm_lib'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = []


def commands():
    import platform
    # root
    env.QSM_LIB_BASE = '{root}'
    # resource
    env.QSM_EXTEND_RESOURCES.append('{root}/resources')
    # python
    env.PYTHONPATH.append('{root}/lib/python-2.7/site-packages')

    if platform.system() == 'Linux':
        env.PYTHONPATH.append('{root}/lib/linux-python-2.7/site-packages')
    else:
        env.PYTHONPATH.append('{root}/lib/windows-python-2.7/site-packages')


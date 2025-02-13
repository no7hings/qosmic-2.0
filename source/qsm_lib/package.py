# coding:utf-8
name = 'qsm_lib'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = []


def commands():
    import sys

    import os

    import platform
    # root
    env.QSM_LIB_BASE = '{root}'
    # resource
    env.QSM_EXTEND_RESOURCES.append('{root}/resources')
    # python
    if 'QSM_PYTHON_VERSION' in os.environ:
        if os.environ['QSM_PYTHON_VERSION'] == '3':
            if platform.system() == 'Linux':
                env.PYTHONPATH.append('{root}/lib/linux-python-3.10/site-packages')
            else:
                env.PYTHONPATH.append('{root}/lib/windows-python-3.10/site-packages')
        else:
            if platform.system() == 'Linux':
                env.PYTHONPATH.append('{root}/lib/linux-python-2.7/site-packages')
            else:
                env.PYTHONPATH.append('{root}/lib/windows-python-2.7/site-packages')
    else:
        env.PYTHONPATH.append('{root}/lib/python-2.7/site-packages')
        if platform.system() == 'Linux':
            env.PYTHONPATH.append('{root}/lib/linux-python-2.7/site-packages')
        else:
            env.PYTHONPATH.append('{root}/lib/windows-python-2.7/site-packages')


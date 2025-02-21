# coding:utf-8
name = 'qsm_maya_lib'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = []


def commands():
    import platform

    import os
    # root
    env.QSM_MAYA_LIB_BASE = '{root}'
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
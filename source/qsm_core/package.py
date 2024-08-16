# coding:utf-8
name = 'qsm_core'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = [
    'qsm_lib'
]


def commands():
    import platform
    #
    env.QSM_MARK = 'TRUE'
    # root
    env.QSM_CORE_BASE = '{root}'
    # scheme
    env.QSM_SCHEME = 'default'
    # configure
    env.QSM_EXTEND_CONFIGURES.append('{root}/configures')
    # python
    env.PYTHONPATH.append('{root}/script/python')
    # bin
    env.PATH.append('{root}/script/bin')
    if platform.system() == 'Linux':
        env.PATH.append('{root}/script/bin/linux')
    elif platform.system() == 'Windows':
        env.PATH.append('{root}/script/bin/windows')
    # log
    env.QSM_LOG_ROOT = '{}/.log'.format(
        env.QSM_DEPLOY_ROOT
    )
    # tool
    env.QSM_TOOLS.append(
        '{}/.tools'.format(
            env.QSM_DEPLOY_ROOT
        )
    )
    # configure
    env.QSM_EXTEND_CONFIGURES.append(
        '{}/.configures'.format(
            env.QSM_DEPLOY_ROOT
        )
    )
    # resource
    env.QSM_EXTEND_RESOURCES.append(
        '{}/.resources'.format(
            env.QSM_DEPLOY_ROOT
        )
    )
    #
    if platform.system() == 'Linux':
        pass
    elif platform.system() == 'Windows':
        # project
        env.QSM_PROJECT_ROOT = 'Z:/projects'
        # cache
        env.QSM_CACHE_ROOT = 'Z:/caches'
        env.QSM_CACHE_LOCAL_ROOT = 'D:/caches'
        # library
        env.QSM_LIBRARY_ROOT = 'Z:/libraries'

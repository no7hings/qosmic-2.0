# coding:utf-8
name = 'qsm_dcc_main'

version = '0.0.0'

description = ''

authors = ['']

tools = []

requires = [
    # basic
    'qsm_main',
    # dcc
    'qsm_dcc_lib',
    'qsm_dcc_core',
    'qsm_dcc_gui',
    'qsm_dcc_resource',
    'qsm_dcc_extra',
]


def commands():
    env.QSM_DCC_MAIN_BASE = '{root}'
    # python
    env.PYTHONPATH.append('{root}/script/python')
    # startup in dcc
    # maya
    env.PYTHONPATH.append('{root}/startup/maya/scripts')
    # houdini-setup
    env.HOUDINI_PATH.append('{root}/startup/houdini;&')
    # katana-setup
    env.KATANA_RESOURCES.append('{root}/startup/katana')
    # arnold-setup
    # env.ARNOLD_PLUGIN_PATH.append('{root}/script/python/.setup/arnold/shaders')
    # clarisse-setup
    # env.CLARISSE_STARTUP_SCRIPT.append('{root}/script/python/.setup/clarisse/startup_script.py')


timestamp = 1639389924

format_version = 2

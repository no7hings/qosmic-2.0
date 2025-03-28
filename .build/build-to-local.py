# coding:utf-8
from __future__ import print_function

import copy

import os

list_ = [
    (
        '@echo off\n'
        'pushd %~d0\n'
    )
]


class Main(object):
    ROOT = '/'.join(os.path.dirname(__file__.replace('\\', '/')).split('/')[:-1])

    PACKAGES = [
        'qsm_main',
        'qsm_core',
        'qsm_gui',
        'qsm_lib',
        'qsm_resource',
        'qsm_extra',

        'qsm_resora',
        'qsm_wotrix',
        'qsm_nexsolve',

        'qsm_dcc_main',
        'qsm_dcc_core',
        'qsm_dcc_gui',
        'qsm_dcc_lib',
        'qsm_dcc_resource',
        'qsm_dcc_extra',

        'qsm_maya_core',
        'qsm_maya_lib',
        'qsm_maya_resora',
        'qsm_maya_main',

        'qsm_houdini_core',
        'qsm_houdini_lib',
        'qsm_houdini_main',

        'qsm_katana_core',
        'qsm_katana_lib',
        'qsm_katana_main',
    ]

    @classmethod
    def generate(cls):
        options = dict(
            root=cls.ROOT.replace('/', '\\')
        )
        for i_package in cls.PACKAGES:
            i_options = copy.copy(options)
            i_options['package'] = i_package
            i_cmd = (
                'if exist %HOMEDRIVE%%HOMEPATH%\\packages\\{package} (\n'
                '    echo %HOMEDRIVE%%HOMEPATH%\\packages\\{package} is exists\n'
                ') else (\n'
                '    mkdir  %HOMEDRIVE%%HOMEPATH%\\packages\\{package}\n'
                ')\n'
                'if exist  %HOMEDRIVE%%HOMEPATH%\\packages\\{package}\\99.99.99 (\n'
                '    echo %HOMEDRIVE%%HOMEPATH%\\packages\\{package}\\99.99.99 is exists\n'
                ') else (\n'
                '    mklink /D %HOMEDRIVE%%HOMEPATH%\\packages\\{package}\\99.99.99 {root}\\source\\{package}\n'
                ')\n'
            ).format(
                **i_options
            )
            list_.append(
                i_cmd
            )
        list_.append(
            (
                'popd\n'
                'echo. & pause\n'
            )
        )

        return ''.join(
            list_
        )


if __name__ == '__main__':
    py_f = __file__
    bat_f = os.path.splitext(py_f)[0]+'.bat'
    with open(bat_f, 'w') as b:
        b.write(Main.generate())


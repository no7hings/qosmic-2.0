# coding:utf-8
import copy

import glob

import os

import lxbasic.storage as bsc_storage

list_ = [
    (
        '@echo off\n'
        'pushd %~d0\n'
    )
]


class Main(object):
    ROOT_USER = 'E:/myworkspace/qosmic-2.0/source'
    ROOT_RELEASE = 'Y:/deploy/rez-packages/internally/release'

    PACKAGE_USER = '{root_user}/{package}'
    PACKAGE_RELEASE = '{root_release}/{package}/{version}'

    PACKAGES = [
        'qsm_main',
        'qsm_core',
        'qsm_gui',
        # 'qsm_lib',
        'qsm_resource',
        'qsm_extra',
        #
        'qsm_dcc_main',
        'qsm_dcc_core',
        'qsm_dcc_gui',
        # 'qsm_dcc_lib',
        'qsm_dcc_resource',
        'qsm_dcc_extra',
    ]

    @classmethod
    def execute(cls):
        options = dict(
            root_user=cls.ROOT_USER,
            root_release=cls.ROOT_RELEASE
        )
        for i_package in cls.PACKAGES:
            i_options = copy.copy(options)
            i_options['package'] = i_package

            i_dir_user = cls.PACKAGE_USER.format(**i_options)
            if os.path.isdir(i_dir_user) is False:
                continue

            i_version_new = cls.get_version_new(i_options)

            i_options_release = copy.copy(i_options)
            i_options_release['version'] = i_version_new
            i_dir_release = cls.PACKAGE_RELEASE.format(**i_options_release)

            if os.path.isdir(i_dir_release) is True:
                continue

            bsc_storage.StgDirectoryMtd.do_thread_copy(
                i_dir_user, i_dir_release
            )

    @classmethod
    def get_version_new(cls, options):
        options_0 = copy.copy(options)
        options_0['version'] = '*'

        p = cls.PACKAGE_RELEASE.format(**options_0)
        _results = glob.glob(p)
        if not _results:
            return '0.0.1'

        _results.sort()

        result = _results[-1]
        result = result.replace('\\', '/')
        version_latest = result.split('/')[-1]
        return '0.0.{}'.format(int(version_latest.split('.')[-1])+1)


if __name__ == '__main__':
    Main.execute()


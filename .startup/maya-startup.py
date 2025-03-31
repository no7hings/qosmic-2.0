# coding:utf-8
from __future__ import print_function

import getpass

import sys

import copy

import glob

import os

import time

import json

import re


class Main(object):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    DEPLOY_ROOT = 'Y:/deploy'

    PROJECT_ROOT = 'Z:/projects'

    CACHE_ROOT = 'Z:/caches'
    CACHE_LOCAL_ROOT = 'D:/cache'

    LIBRARY_ROOT = 'Z:/libraries'

    PACKAGE_ROOT_DEVLOP = 'C:/Users/{user}/packages'
    PACKAGE_ROOT_RELEASE = 'Y:/deploy/rez-packages/internally/release'
    PACKAGE_ROOT_PRE_RELEASE = 'Y:/deploy/rez-packages/internally/pre-release'

    PACKAGE_DIR = '{package_root}/{package}/{version}'
    
    BUILD_ROOT_DEVLOP = 'Y:/deploy/.startup/build/devlop'
    BUILD_ROOT_RELEASE = 'Y:/deploy/.startup/build/release'
    BUILD_ROOT_PRE_RELEASE = 'Y:/deploy/.startup/build/pre-release'

    BUILD_JSON = '{build_root}/{version}/package.json'

    MARK_KEY = 'QSM_MARK'

    PACKAGE_DATA = {
        'qsm_main': {
            'QSM_MAIN_BASE': '{root}',
            'PYTHONPATH': ['{root}/script/python'],
        },
        'qsm_core': {
            'QSM_CORE_BASE': '{root}',
            'QSM_SCHEME': 'default',
            'PYTHONPATH': ['{root}/script/python'],
            'PATH': [
                '{root}/script/bin/windows',
                '{deploy_root}/.rez/build/windows/2.112.0/Scripts/rez'
            ],
            # server configure and resource
            'QSM_EXTEND_CONFIGURES': ['{deploy_root}/.configures', '{root}/configures'],
            'QSM_EXTEND_RESOURCES': ['{deploy_root}/.resources', '{root}/resources'],
            'QSM_LOG_ROOT': '{deploy_root}/.log',
            'QSM_TOOLS': ['{deploy_root}/.tools'],
            #
            'QSM_DEPLOY_ROOT': DEPLOY_ROOT,
            'QSM_PROJECT_ROOT': PROJECT_ROOT,
            'QSM_CACHE_ROOT': CACHE_ROOT,
            'QSM_CACHE_LOCAL_ROOT': CACHE_LOCAL_ROOT,
            'QSM_LIBRARY_ROOT': LIBRARY_ROOT,
            #
            'QSM_UI_LANGUAGE': 'chs',
            'REZ_CONFIGURE_FILE': '{deploy_root}/.rez/configure/windows/rezconfig.py'
        },
        'qsm_gui': {
            'QSM_GUI_BASE': '{root}',
            'PYTHONPATH': ['{root}/script/python'],
        },
        'qsm_lib': {
            'QSM_LIB_BASE': '{root}',
            'QSM_EXTEND_RESOURCES': ['{root}/resources'],
            'PYTHONPATH2': ['{root}/lib/python-2.7/site-packages', '{root}/lib/windows-python-2.7/site-packages'],
            'PYTHONPATH3': ['{root}/lib/python-3.10/site-packages', '{root}/lib/windows-python-3.10/site-packages']
        },
        'qsm_resource': {
            'QSM_RESOURCE_BASE': '{root}',
            'QSM_EXTEND_RESOURCES': ['{root}/resources'],
        },
        'qsm_extra': {
            'QSM_EXTRA_BASE': '{root}',
            'PYTHONPATH': ['{root}/script/python'],
            'QSM_EXTEND_CONFIGURES': ['{root}/configures'],
            'QSM_EXTEND_RESOURCES': ['{root}/resources'],
        },
        # new
        'qsm_resora': {
            'QSM_RESORA_BASE': '{root}',
            'PYTHONPATH': ['{root}/script/python'],
            'QSM_EXTEND_CONFIGURES': ['{root}/configures'],
            'QSM_EXTEND_RESOURCES': ['{root}/resources'],
        },
        'qsm_wotrix': {
            'QSM_WOTRIX_BASE': '{root}',
            'PYTHONPATH': ['{root}/script/python'],
            'QSM_EXTEND_CONFIGURES': ['{root}/configures'],
            'QSM_EXTEND_RESOURCES': ['{root}/resources'],
        },
        #
        'qsm_dcc_core': {
            'QSM_DCC_CORE_BASE': '{root}',
            'PYTHONPATH': ['{root}/script/python']
        },
        'qsm_dcc_gui': {
            'QSM_DCC_GUI_BASE': '{root}',
            'PYTHONPATH': ['{root}/script/python']
        },
        'qsm_dcc_lib': {
            'QSM_DCC_LIB_BASE': '{root}',
        },
        'qsm_dcc_resource': {
            'QSM_DCC_RESOURCE_BASE': '{root}',
            'QSM_EXTEND_RESOURCES': ['{root}/resources'],
        },
        'qsm_dcc_extra': {
            'QSM_DCC_EXTRA_BASE': '{root}',
            'PYTHONPATH': ['{root}/script/python'],
            'QSM_EXTEND_CONFIGURES': ['{root}/configures'],
            'QSM_EXTEND_RESOURCES': ['{root}/resources'],

        },
        'qsm_dcc_main': {
            'QSM_DCC_MAIN_BASE': '{root}',
            'PYTHONPATH': ['{root}/script/python', '{root}/startup/maya/scripts'],
            'QSM_EXTEND_CONFIGURES': ['{root}/configures'],
            'QSM_EXTEND_RESOURCES': ['{root}/resources'],
        },
        # maya package
        'qsm_maya_core': {
            'QSM_MAYA_CORE_BASE': '{root}',
            'PYTHONPATH': ['{root}/script/python'],
            'QSM_EXTEND_CONFIGURES': ['{root}/configures'],
            'QSM_EXTEND_RESOURCES': ['{root}/resources'],
        },
        'qsm_maya_lib': {
            'QSM_MAYA_LIB_BASE': '{root}',
            'PYTHONPATH2': ['{root}/lib/python-2.7/site-packages', '{root}/lib/windows-python-2.7/site-packages'],
            'PYTHONPATH3': ['{root}/lib/python-3.10/site-packages', '{root}/lib/windows-python-3.10/site-packages']
        },
        'qsm_maya_main': {
            'QSM_MAYA_MAIN_BASE': '{root}',
            'PYTHONPATH': ['{root}/script/python'],
            'QSM_EXTEND_CONFIGURES': ['{root}/configures'],
            'QSM_EXTEND_RESOURCES': ['{root}/resources'],
        },
        # tool package
        'qsm_maya_resora': {
            'QSM_MAYA_RESORA_BASE': '{root}',
            'PYTHONPATH': ['{root}/script/python'],
            'QSM_EXTEND_CONFIGURES': ['{root}/configures'],
            'QSM_EXTEND_RESOURCES': ['{root}/resources'],
        },
    }

    @classmethod
    def log(cls, result):
        sys.stdout.write(
            '{}         | {}\n'.format(time.strftime(
                cls.TIME_FORMAT, time.localtime(time.time())),
                result
            ),
        )

    @classmethod
    def get_test_flag(cls):
        return os.environ.get('QSM_TEST')

    @classmethod
    def to_number_embedded_args(cls, text):
        pieces = re.compile(r'(\d+)').split(text)
        pieces[1::2] = map(int, pieces[1::2])
        return pieces

    @classmethod
    def sort_by_number(cls, texts):
        texts.sort(key=lambda x: cls.to_number_embedded_args(x))
        return texts

    @classmethod
    def get_version_latest(cls, ptn, options):
        options_0 = copy.copy(options)
        options_0['version'] = '*'

        p = ptn.format(**options_0)

        _results = glob.glob(p)
        if not _results:
            return None

        _results = cls.sort_by_number(_results)

        result = _results[-1]
        result = result.replace('\\', '/')
        if os.path.isfile(result):
            result = os.path.dirname(result)

        return result.split('/')[-1]

    @classmethod
    def add_python(cls, value, variants):
        if isinstance(value, list) is False:
            value = [value]

        paths_exists = sys.path
        for i_value in value:
            i_value = i_value.format(**variants)
            if i_value not in paths_exists:
                sys.path.insert(0, i_value)
                cls.log(
                    'add python: {}'.format(i_value)
                )

    @classmethod
    def add_other(cls, key, value, variants):
        if isinstance(value, list):
            for i_value in value:
                i_value = i_value.format(**variants)
                cls.add_environ_fnc(key, i_value)
        else:
            value = value.format(**variants)
            cls.set_environ_fnc(key, value)

    @classmethod
    def set_environ_fnc(cls, key, value):
        if value is not None:
            os.environ[key] = value
            cls.log(
                'set environ: {} = {}'.format(key, value)
            )

    @classmethod
    def add_environ_fnc(cls, key, value):
        if value is not None:
            if key in os.environ:
                v = os.environ[key]
                if value not in v:
                    os.environ[key] += os.pathsep+value
                    cls.log(
                        'add environ: {} = {}'.format(key, value)
                    )
            else:
                os.environ[key] = value
                cls.log(
                    'set environ: {} = {}'.format(key, value)
                )

    @classmethod
    def load_package_fnc(cls, python_version='2'):
        """
        Using build json as a loading cache can effectively avoid package asynchrony caused by slow network speed.
        """
        if cls.MARK_KEY in os.environ:
            return

        cls.log(
            'startup maya'
        )

        if cls.get_test_flag() == '1':
            cls.log(
                'load as BETA'
            )
            variants = dict(
                deploy_root=cls.DEPLOY_ROOT,
                package_root=cls.PACKAGE_ROOT_PRE_RELEASE,
                build_root=cls.BUILD_ROOT_PRE_RELEASE
            )
        elif cls.get_test_flag() == '-1':
            cls.log(
                'load as DEVLOP'
            )
            variants = dict(
                deploy_root=cls.DEPLOY_ROOT,
                package_root=cls.PACKAGE_ROOT_DEVLOP.format(user=getpass.getuser()),
                build_root=cls.BUILD_ROOT_DEVLOP
            )
        else:
            cls.log(
                'load as RELEASE'
            )
            variants = dict(
                deploy_root=cls.DEPLOY_ROOT,
                package_root=cls.PACKAGE_ROOT_RELEASE,
                build_root=cls.BUILD_ROOT_RELEASE
            )

        build_data = cls.get_build_data(variants)

        for i_package, i_v in cls.PACKAGE_DATA.items():
            i_package_variants = copy.copy(variants)
            i_package_variants['package'] = i_package

            # when package in build data, read from data, other from latest version by glob
            if i_package in build_data:
                i_version_latest = build_data[i_package]['version']
                cls.log(
                    'load package from build json: {}'.format(i_package)
                )
            else:
                i_version_latest = cls.get_version_latest(cls.PACKAGE_DIR, i_package_variants)
                # ignore when is not found
                if i_version_latest is None:
                    continue

                cls.log(
                    'load package from storage scan: {}'.format(i_package)
                )

            i_package_variants_latest = copy.copy(i_package_variants)
            i_package_variants_latest['version'] = i_version_latest

            i_package_location = cls.PACKAGE_DIR.format(**i_package_variants_latest)

            if os.path.isdir(i_package_location) is False:
                sys.stderr.write('package location is not found: {}'.format(i_package_location))

            i_package_variants['root'] = i_package_location

            for j_key, j_value in i_v.items():
                if j_key == 'PYTHONPATH':
                    cls.add_python(j_value, i_package_variants)
                elif j_key == 'PYTHONPATH2':
                    if python_version == '2':
                        cls.add_python(j_value, i_package_variants)
                elif j_key == 'PYTHONPATH3':
                    if python_version == '3':
                        cls.add_python(j_value, i_package_variants)
                else:
                    cls.add_other(j_key, j_value, i_package_variants)

    @classmethod
    def get_build_data(cls, variants):
        """
        get build data from build json
        """
        build_variants = copy.copy(variants)
        build_version_latest = cls.get_version_latest(cls.BUILD_JSON, build_variants)
        if build_version_latest is None:
            return {}

        build_variants_latest = copy.copy(build_variants)
        build_variants_latest['version'] = build_version_latest

        build_json = cls.BUILD_JSON.format(**build_variants_latest)
        if os.path.isfile(build_json) is False:
            return {}

        with open(build_json) as j:
            # noinspection PyTypeChecker
            cls.log('load build data from: {}'.format(build_json))
            data = json.load(j)
            j.close()
            if isinstance(data, dict):
                return data
            return {}

    @classmethod
    def load_package_extend_fnc(cls):
        cls.log('add numpy')
        sys.path.insert(0, 'Y:/deploy/rez-packages/external/maya_numpy/1.9.2/platform-windows/python')
        cls.log('add opencv')
        sys.path.insert(0, 'Y:/deploy/rez-packages/external/maya_opencv/2.4.10/platform-windows')

    @classmethod
    def build_maya_environ(cls, python_version='2'):
        # noinspection PyUnresolvedReferences
        from maya import cmds

        import functools

        # use defer
        cmds.evalDeferred(
            functools.partial(cls.load_package_fnc, python_version)
        )
        
    @classmethod
    def build_maya_shelf_fnc(cls):
        import qsm_maya.gui as qsm_mya_gui
        qsm_mya_gui.MainShelf().create()

    @classmethod
    def build_maya_shelf(cls):
        # noinspection PyUnresolvedReferences
        from maya import cmds
        
        # use defer
        cmds.evalDeferred(cls.build_maya_shelf_fnc)

    @classmethod
    def test(cls):
        os.environ.pop('QSM_MARK')
        Main.load_package_fnc()

    @classmethod
    def build_all(cls):
        # noinspection PyUnresolvedReferences
        from maya import cmds

        version = str(cmds.about(apiVersion=1))[:4]

        # check maya version
        if version in {'2020'}:
            Main.build_maya_environ('2')
            Main.build_maya_shelf()
        # elif version in {'2022', '2023', '2024', '2025'}:
        #     Main.build_maya_environ('3')
        #     Main.build_maya_shelf()


if __name__ == '__main__':
    Main.build_all()

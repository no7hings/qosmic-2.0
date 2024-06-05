# coding:utf-8
import sys

import copy

import glob

import os

import time

import re


class Main(object):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    DEPLOY_ROOT = 'Y:/deploy'

    PROJECT_ROOT = 'Z:/projects'

    CACHE_ROOT = 'Z:/caches'

    LIBRARY_ROOT = 'Z:/libraries'

    ROOT_RELEASE = 'Y:/deploy/rez-packages/internally/release'

    PACKAGE_RELEASE = '{root_release}/{package}/{version}'

    MARK_KEY = 'QSM_MARK'

    DATA = {
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
            'QSM_EXTEND_CONFIGURES': ['{root}/configures'],
            'QSM_EXTEND_RESOURCES': ['{deploy_root}/.resources', '{root}/resources'],
            'QSM_LOG_ROOT': '{deploy_root}/.log',
            'QSM_TOOLS': ['{deploy_root}/.tools'],
            #
            'QSM_DEPLOY_ROOT': DEPLOY_ROOT,
            'QSM_PROJECT_ROOT': PROJECT_ROOT,
            'QSM_CACHE_ROOT': CACHE_ROOT,
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
            'PYTHONPATH': ['{root}/lib/python-2.7/site-packages', '{root}/lib/windows-python-2.7/site-packages']
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
        #
        'qsm_dcc_main': {
            'QSM_DCC_MAIN_BASE': '{root}',
            'PYTHONPATH': ['{root}/script/python', '{root}/startup/maya/scripts']
        },
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
    def to_number_embedded_args(cls, text):
        pieces = re.compile(r'(\d+)').split(text)
        pieces[1::2] = map(int, pieces[1::2])
        return pieces

    @classmethod
    def sort_by_number(cls, texts):
        texts.sort(key=lambda x: cls.to_number_embedded_args(x))
        return texts

    @classmethod
    def get_version_latest(cls, options):
        options_0 = copy.copy(options)
        options_0['version'] = '*'

        p = cls.PACKAGE_RELEASE.format(**options_0)

        _results = glob.glob(p)
        if not _results:
            return None

        _results = cls.sort_by_number(_results)

        result = _results[-1]
        result = result.replace('\\', '/')
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
    def execute(cls):
        if cls.MARK_KEY in os.environ:
            return

        cls.log(
            'startup maya from server'
        )
        variants = dict(
            deploy_root=cls.DEPLOY_ROOT,
            root_release=cls.ROOT_RELEASE
        )
        for i_k, i_v in cls.DATA.items():
            i_variants = copy.copy(variants)
            i_variants['package'] = i_k
            i_version_latest = cls.get_version_latest(
                i_variants
            )
            if i_version_latest is None:
                continue

            i_variants['version'] = i_version_latest

            i_root = cls.PACKAGE_RELEASE.format(**i_variants)

            if os.path.isdir(i_root) is False:
                raise RuntimeError()

            i_variants['root'] = i_root

            for j_key, j_value in i_v.items():
                if j_key == 'PYTHONPATH':
                    cls.add_python(j_value, i_variants)
                else:
                    cls.add_other(j_key, j_value, i_variants)

        os.environ[cls.MARK_KEY] = 'TRUE'

    @classmethod
    def create_shelves(cls):
        def fnc_():
            import qsm_maya.gui as qsm_mya_gui
            qsm_mya_gui.MainShelf().create()

        # noinspection PyUnresolvedReferences
        from maya import cmds

        cmds.evalDeferred(fnc_)


if __name__ == '__main__':
    Main.execute()
    Main.create_shelves()

# coding:utf-8
import collections

import json

import shutil

import sys

import copy

import re

import glob

import os

import threading

import time

import six

import subprocess

import functools


class RezPackage:

    PACKAGE_DIR_SOURCE = '{package_root_source}/{package}'
    PACKAGE_DIR = '{package_root}/{package}/{version}'

    BUILD_JSON = '{build_root}/{version}/package.json'

    PACKAGES = [
        # package, enable
        ('qsm_main', True),
        ('qsm_core', True),
        ('qsm_gui', True),
        ('qsm_lib', False),
        ('qsm_resource', True),
        ('qsm_extra', True),
        #
        ('qsm_resora', True),
        #
        ('qsm_dcc_main', True),
        ('qsm_dcc_core', True),
        ('qsm_dcc_gui', True),
        ('qsm_dcc_lib', False),
        ('qsm_dcc_resource', True),
        ('qsm_dcc_extra', True),
        # maya
        ('qsm_maya_core', True),
        ('qsm_maya_lib', False),
        ('qsm_maya_resora', True),
        ('qsm_maya_main', True),
        # houdini
        ('qsm_houdini_core', True),
        ('qsm_houdini_lib', False),
        ('qsm_houdini_main', True),
        # katana
        ('qsm_katana_core', False),
        ('qsm_katana_lib', False),
        ('qsm_katana_main', False),
    ]

    @classmethod
    def load_configure(cls):
        import lxbasic.resource as bsc_resource

        return bsc_resource.BscExtendConfigure.get_as_content(
            'lazy/sync'
        )

    @classmethod
    def copytree(cls, source, target):
        dir_path = os.path.dirname(target)
        if os.path.exists(dir_path) is False:
            os.makedirs(dir_path)

        cmd_args = [
            'xcopy',
            source.replace('/', '\\'),
            target.replace('/', '\\'),
            '/E',
            '/I',
            '/Y',
            '/C',
        ]

        cmd_args = [cmd.encode('mbcs') if isinstance(cmd, six.text_type) else cmd for cmd in cmd_args]

        cmd_script = ' '.join(cmd_args)
        s_p = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, unused_err = s_p.communicate()
        if s_p.returncode != 0:
            output_lines = output.splitlines()
            for i in output_lines:
                if i:
                    sys.stdout.write(i+'\n')

            raise subprocess.CalledProcessError(s_p.returncode, cmd_script)

        sys.stdout.write(
            u'copytree {} > {}\n'.format(source, target)
        )

    @classmethod
    def generate_sync_threads(cls, source, targets):
        ts = []
        for i_target in targets:
            i_t = threading.Thread(
                target=functools.partial(
                    cls.copytree,
                    source=source,
                    target=i_target
                )
            )
            ts.append(i_t)
        return ts

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
    def get_version_new(cls, ptn, options):
        options_0 = copy.copy(options)
        options_0['version'] = '*'

        p = ptn.format(**options_0)
        _results = glob.glob(p)
        if not _results:
            return '0.0.1'

        _results = cls.sort_by_number(_results)

        result = _results[-1]
        result = result.replace('\\', '/')
        if os.path.isfile(result):
            result = os.path.dirname(result)

        version_latest = result.split('/')[-1]
        return '0.0.{}'.format(int(version_latest.split('.')[-1])+1)

    @classmethod
    def get_version_latest(cls, ptn, options):
        options_0 = copy.copy(options)
        options_0['version'] = '*'

        p = ptn.format(**options_0)
        _results = glob.glob(p)
        if _results:
            _results = cls.sort_by_number(_results)

            result = _results[-1]
            result = result.replace('\\', '/')
            if os.path.isfile(result):
                result = os.path.dirname(result)

            return result.split('/')[-1]

    @classmethod
    def release_fnc(cls, package_root_source, package_root, package_root_sync, build_root, build_root_sync):
        variants = dict(
            package_root_source=package_root_source,
            package_root=package_root
        )

        ts = []

        build_data = collections.OrderedDict()

        # package
        for i_args in cls.PACKAGES:
            i_package, i_enable = i_args

            i_package_variants = copy.copy(variants)
            i_package_variants['package'] = i_package

            if i_enable is False:
                i_version_latest = cls.get_version_latest(cls.PACKAGE_DIR, i_package_variants)
                i_package_variants_latest = copy.copy(i_package_variants)
                i_package_variants_latest['version'] = i_version_latest
                i_package_location = cls.PACKAGE_DIR.format(**i_package_variants_latest)
                build_data[i_package] = dict(
                    version=i_version_latest,
                    location=i_package_location
                )
                continue

            i_dir_source = cls.PACKAGE_DIR_SOURCE.format(**i_package_variants)
            if os.path.isdir(i_dir_source) is False:
                continue

            i_version_new = cls.get_version_new(cls.PACKAGE_DIR, i_package_variants)

            i_package_variants_new = copy.copy(i_package_variants)
            i_package_variants_new['version'] = i_version_new
            i_package_location = cls.PACKAGE_DIR.format(**i_package_variants_new)

            if os.path.isdir(i_package_location) is True:
                continue

            build_data[i_package] = dict(
                version=i_version_new,
                location=i_package_location
            )
            cls.copytree(i_dir_source, i_package_location)

            if package_root_sync:
                i_dir_package_target_sync = [i_package_location.replace(package_root, x) for x in package_root_sync]
                i_ts = cls.generate_sync_threads(i_package_location, i_dir_package_target_sync)
                ts.extend(i_ts)

        if ts:
            for i in ts:
                i.start()
            for i in ts:
                i.join()

        # build json
        build_variants = dict(
            build_root=build_root
        )
        build_version_new = cls.get_version_new(cls.BUILD_JSON, build_variants)
        build_variants_new = copy.copy(build_variants)
        build_variants_new['version'] = build_version_new
        build_json_path = cls.BUILD_JSON.format(**build_variants_new)

        json_dir_path = os.path.dirname(build_json_path)
        if os.path.exists(json_dir_path) is False:
            os.makedirs(json_dir_path)

        with open(build_json_path, 'w') as j:
            json.dump(
                build_data,
                j,
                indent=4
            )
            sys.stdout.write('write json: {}\n'.format(build_json_path))

        # build json sync
        if build_root_sync:
            json_build_target_sync = [build_json_path.replace(build_root, x) for x in build_root_sync]
            for i in json_build_target_sync:
                i_dir = os.path.dirname(i)
                if os.path.exists(i_dir) is False:
                    os.makedirs(i_dir)

                shutil.copy2(build_json_path, i)
                sys.stdout.write('copy json: {} > {}\n'.format(build_json_path, i))

    @classmethod
    def release(cls, test=True):
        from . import sync as _sync

        cfg = cls.load_configure()

        studio = _sync.Sync().studio.get_current()

        rez_cfg = cfg.get('rez_package.{}'.format(studio))

        if rez_cfg:
            s = time.time()
            if test is True:
                sys.stdout.write('pre release is started.\n')
                package_root_source, package_root_pre_release, package_root_pre_release_sync = (
                    rez_cfg['package_root_source'],
                    rez_cfg['package_root_pre_release'],
                    rez_cfg['package_root_pre_release_sync']
                )
                build_root_pre_release, build_root_pre_release_sync = (
                    rez_cfg['build_root_pre_release'],
                    rez_cfg['build_root_pre_release_sync']
                )
                cls.release_fnc(
                    package_root_source, package_root_pre_release, package_root_pre_release_sync,
                    build_root_pre_release, build_root_pre_release_sync
                )
                sys.stdout.write('pre release is finished, cost {}s.\n'.format(round(time.time()-s, 3)))
            else:
                sys.stdout.write('release is started.\n')
                package_root_source, package_root_release, package_root_release_sync = (
                    rez_cfg['package_root_source'], 
                    rez_cfg['package_root_release'], 
                    rez_cfg['package_root_release_sync']
                )
                build_root_release, build_root_release_sync = (
                    rez_cfg['build_root_release'], 
                    rez_cfg['build_root_release_sync']
                )
                cls.release_fnc(
                    package_root_source, package_root_release, package_root_release_sync,
                    build_root_release, build_root_release_sync
                )
                sys.stdout.write('release is finished, cost {}s.\n'.format(round(time.time()-s, 3)))

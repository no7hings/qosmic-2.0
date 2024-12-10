# coding:utf-8
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

    PACKAGE_SOURCE = '{root_source}/{package}'
    PACKAGE_TARGET = '{root_target}/{package}/{version}'

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
    def load_configure(cls):
        import lxbasic.resource as bsc_resource

        return bsc_resource.RscExtendConfigure.get_as_content(
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
    def get_version_new(cls, options):
        options_0 = copy.copy(options)
        options_0['version'] = '*'

        p = cls.PACKAGE_TARGET.format(**options_0)
        _results = glob.glob(p)
        if not _results:
            return '0.0.1'

        _results = cls.sort_by_number(_results)

        result = _results[-1]
        result = result.replace('\\', '/')
        version_latest = result.split('/')[-1]
        return '0.0.{}'.format(int(version_latest.split('.')[-1])+1)

    @classmethod
    def release_fnc(cls, root_source, root_target, root_target_sync):
        options = dict(
            root_source=root_source,
            root_target=root_target
        )

        ts = []
        for i_package in cls.PACKAGES:
            i_options = copy.copy(options)
            i_options['package'] = i_package

            i_dir_source = cls.PACKAGE_SOURCE.format(**i_options)
            if os.path.isdir(i_dir_source) is False:
                continue

            i_version_new = cls.get_version_new(i_options)

            i_options_release = copy.copy(i_options)
            i_options_release['version'] = i_version_new
            i_dir_target = cls.PACKAGE_TARGET.format(**i_options_release)

            if os.path.isdir(i_dir_target) is True:
                continue

            cls.copytree(i_dir_source, i_dir_target)

            if root_target_sync:
                i_dir_target_sync = [i_dir_target.replace(root_target, x) for x in root_target_sync]
                i_ts = cls.generate_sync_threads(i_dir_target, i_dir_target_sync)
                ts.extend(i_ts)

        if ts:
            for i in ts:
                i.start()
            for i in ts:
                i.join()

    @classmethod
    def release(cls, test=True):
        from . import sync as _sync

        cfg = cls.load_configure()

        studio = _sync.Sync().studio.get_current()

        sub_cfg = cfg.get('rez_package.{}'.format(studio))

        if sub_cfg:
            s = time.time()
            if test is True:
                sys.stdout.write('pre release is started.\n')
                root_source, root_pre_release, root_pre_release_sync = (
                    sub_cfg['root_source'], sub_cfg['root_pre_release'], sub_cfg['root_pre_release_sync']
                )
                cls.release_fnc(
                    root_source, root_pre_release, root_pre_release_sync
                )
                sys.stdout.write('pre release is finished, cost {}s.\n'.format(round(time.time()-s, 3)))
            else:
                sys.stdout.write('release is started.\n')
                root_source, root_release, root_release_sync = (
                    sub_cfg['root_source'], sub_cfg['root_release'], sub_cfg['root_release_sync']
                )
                cls.release_fnc(
                    root_source, root_release, root_release_sync
                )
                sys.stdout.write('release is finished, cost {}s.\n'.format(round(time.time()-s, 3)))

# coding:utf-8
import sys

import collections

import six

import subprocess

import threading

import re

import lxbasic.core as bsc_core

import lxbasic.scan as bsc_scan


class MayaBin:
    @classmethod
    def generate_dict(cls):
        dict_ = collections.OrderedDict()

        ptn = 'C:/Program Files/Autodesk/Maya([0-9][0-9][0-9][0-9])/bin/maya.exe'
        regex = 'C:/Program Files/Autodesk/Maya[0-9][0-9][0-9][0-9]/bin/maya.exe'
        results = bsc_scan.ScanGlob.glob(regex)
        if results:
            results = bsc_core.BscTexts.sort_by_number(results)
            for i_result in results:
                i_r = re.search(ptn, i_result, re.DOTALL)
                if i_r:
                    i_version = i_r.group(1)
                    dict_[i_version] = i_result
        return dict_

    @classmethod
    def open_file(cls, bin_path, scene_path):
        def fnc_():
            _cmd_args = [
                '"{}"'.format(bin_path),
                '-file',
                '"{}"'.format(scene_path)
            ]
            _cmd_args = [cmd.encode('mbcs') if isinstance(cmd, six.text_type) else cmd for cmd in _cmd_args]
            _cmd_script = ' '.join(_cmd_args)
            _result = subprocess.Popen(_cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            _stdout, _stderr = _result.communicate()

            if _result.returncode != 0:
                sys.stderr.write(_stderr+'\n')
                return None

        scene_path = bsc_core.ensure_unicode(scene_path)
        # encode unicode
        if isinstance(scene_path, six.text_type):
            scene_path = scene_path.encode('mbcs')

        t = threading.Thread(
            target=fnc_
        )
        t.start()


class MayaTimeunit:
    TIMEUNIT_TO_FPS_DICT = {
        '12fps': 12,
        'game': 14,
        '16fps': 16,
        'film': 24,
        'pal': 25,
        'ntsc': 30,
        'show': 48,
        'palf': 50,
        'ntscf': 60
    }

    FPS_TO_TIMEUNIT_DICT = {v: k for k, v in TIMEUNIT_TO_FPS_DICT.items()}

    @classmethod
    def fps_to_timeunit(cls, fps):
        if fps in cls.FPS_TO_TIMEUNIT_DICT:
            return cls.FPS_TO_TIMEUNIT_DICT[fps]
        return '{}fps'.format(fps)

    @classmethod
    def timeunit_to_fps(cls, timeunit):
        if timeunit in cls.TIMEUNIT_TO_FPS_DICT:
            return cls.TIMEUNIT_TO_FPS_DICT[timeunit]
        return int(timeunit[:-3])


class DccFilePatterns(object):
    SceneSrcFile = '{directory}/source/scene.ma'
    # animation
    # geometry
    AniGeoCacheAbcFile = '{directory}/cache/abc/{namespace}.geometry.abc'
    AniGeoJsonFile = '{directory}/json/{namespace}.geometry.json'
    # control
    AniCtlCacheAbcFile = '{directory}/cache/abc/{namespace}.control.abc'
    AniCtlJsonFile = '{directory}/json/{namespace}.control.json'
    # CFX
    # cloth
    CfxClothAbcFile = '{directory}/abc/{namespace}.cloth.abc'
    CfxClothJsonFile = '{directory}/json/{namespace}.cloth.json'
    CfxClothMcxFile = '{directory}/mcx/{namespace}.cloth.mcx'

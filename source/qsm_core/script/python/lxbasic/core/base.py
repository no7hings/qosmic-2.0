# coding:utf-8
from __future__ import division

import json
import sys

import os

import six

import getpass

import time

import datetime

import platform

import re

import fnmatch

import subprocess

import uuid

import hashlib

import struct

import glob

import socket

import collections

from . import configure as _configure


class SysPlatformMtd(object):
    @staticmethod
    def get_is_linux():
        return platform.system() == 'Linux'

    @staticmethod
    def get_is_windows():
        return platform.system() == 'Windows'

    @staticmethod
    def get_current():
        if platform.system() == 'Windows':
            return _configure.BscPlatform.Windows
        elif platform.system() == 'Linux':
            return _configure.BscPlatform.Linux


class SysApplicationMtd(object):
    @classmethod
    def get_is_maya(cls):
        _ = os.environ.get('MAYA_APP_DIR')
        if _:
            return True
        return False

    @classmethod
    def get_maya_version(cls):
        string = ''
        if cls.get_is_maya():
            # noinspection PyUnresolvedReferences
            import maya.cmds as cmds
            # Str <Maya Version>
            string = str(cmds.about(apiVersion=1))[:4]
        return string

    @classmethod
    def get_is_houdini(cls):
        _ = os.environ.get('HIP')
        if _:
            return True
        return False

    @classmethod
    def get_is_katana(cls):
        _ = os.environ.get('KATANA_ROOT')
        if _:
            return True
        return False

    @classmethod
    def get_is_clarisse(cls):
        _ = os.environ.get('IX_PYTHON2HOME')
        if _:
            return True
        return False

    @classmethod
    def get_is_lynxi(cls):
        _ = os.environ.get('QSM_ROOT')
        if _:
            return True
        return False

    @classmethod
    def get_is_nuke(cls):
        pass

    @classmethod
    def get_is_dcc(cls):
        for i_fnc in [
            cls.get_is_maya,
            cls.get_is_houdini,
            cls.get_is_katana,
            cls.get_is_clarisse,
            cls.get_is_lynxi
        ]:
            if i_fnc() is True:
                return True
        return False

    @classmethod
    def get_current(cls):
        for i_fnc, i_app in [
            (cls.get_is_maya, _configure.BscApplication.Maya),
            (cls.get_is_houdini, _configure.BscApplication.Houdini),
            (cls.get_is_katana, _configure.BscApplication.Katana),
            (cls.get_is_clarisse, _configure.BscApplication.Clarisse),
            (cls.get_is_lynxi, _configure.BscApplication.Lynxi)
        ]:
            if i_fnc() is True:
                return i_app
        return _configure.BscApplication.Python

    @classmethod
    def test(cls):
        subprocess.check_output(
            ['', '-v'], shell=True
        ).strip()


class SysBaseMtd(object):
    Platform = _configure.BscPlatform
    Application = _configure.BscApplication

    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    TIME_FORMAT_EXACT = '%Y-%m-%d %H:%M:%S.%f'
    #
    TIME_TAG_FORMAT = '%Y_%m%d_%H%M_%S_%f'
    DATE_TAG_FORMAT = '%Y_%m%d'

    @classmethod
    def get_time(cls, exact=False):
        timestamp = time.time()
        if exact is True:
            return datetime.datetime.now().strftime(
                cls.TIME_FORMAT_EXACT
            )
        return time.strftime(
            cls.TIME_FORMAT,
            time.localtime(timestamp)
        )

    @classmethod
    def get_timestamp(cls):
        return time.time()

    @classmethod
    def get_year(cls):
        return time.localtime().tm_year

    @classmethod
    def get_minute(cls):
        return time.localtime().tm_min

    @classmethod
    def get_second(cls):
        return time.localtime().tm_sec

    @classmethod
    def get_time_tag(cls):
        return datetime.datetime.now().strftime(
            cls.TIME_TAG_FORMAT
        )

    @classmethod
    def get_date_tag(cls):
        timestamp = time.time()
        return time.strftime(
            cls.DATE_TAG_FORMAT,
            time.localtime(timestamp)
        )

    @classmethod
    def get_host(cls):
        return socket.gethostname()

    @classmethod
    def get_user_name(cls):
        return getpass.getuser()

    @classmethod
    def get_user_group_ids(cls):
        return os.getgroups()

    @staticmethod
    def get_is_linux():
        return platform.system() == 'Linux'

    @staticmethod
    def get_is_windows():
        return platform.system() == 'Windows'

    @staticmethod
    def get_platform():
        if platform.system() == 'Windows':
            return 'windows'
        elif platform.system() == 'Linux':
            return 'linux'

    #
    @classmethod
    def get_application(cls):
        return SysApplicationMtd.get_current()

    #
    @classmethod
    def get_home_directory(cls):
        if cls.get_is_windows():
            return os.environ.get('HOMEPATH')
        elif cls.get_is_linux():
            return os.environ.get('HOME')
        else:
            raise SystemError()

    @classmethod
    def get_environment(cls):
        dict_ = {}
        file_path = '{}/.qosmic/environment.txt'.format(cls.get_home_directory())
        if os.path.isfile(file_path) is True:
            with open(file_path) as f:
                raw = f.read()
                f.close()
                if raw:
                    for i in raw.split('\n'):
                        if i:
                            i_k, i_v = i.split('=', 1)
                            dict_[i_k] = i_v
        return dict_

    #
    @classmethod
    def get_system_includes(cls, system_keys):
        lis = []
        for i_system_key in system_keys:
            i_results = fnmatch.filter(
                _configure.BscSystem.All, i_system_key
            ) or []
            for j_system in i_results:
                if j_system not in lis:
                    lis.append(j_system)
        return lis

    @classmethod
    def get_current(cls):
        return '{}-{}'.format(
            cls.get_platform(),
            cls.get_application()
        )

    @classmethod
    def get_is_matched(cls, system_keys):
        return cls.get_current() in cls.get_system_includes(system_keys)

    #
    @classmethod
    def get(cls, key):
        dict_ = {
            'user': cls.get_user_name,
            'host': cls.get_host,
            'time_tag': cls.get_time_tag
        }
        if key in dict_:
            return dict_[key]()

    @classmethod
    def get_group_id(cls, group_name):
        import grp
        return grp.getgrnam(group_name).gr_gid

    @classmethod
    def get_group(cls, group_id):
        import grp
        return grp.getgrgid(group_id)

    @classmethod
    def trace(cls, text):
        return sys.stdout.write(text+'\n')

    @classmethod
    def trace_error(cls, text):
        return sys.stderr.write(text+'\n')


class StgBaseMtd(object):
    PATHSEP = '/'

    @staticmethod
    def get_platform_is_linux():
        return platform.system() == 'Linux'

    @staticmethod
    def get_platform_is_windows():
        return platform.system() == 'Windows'

    @classmethod
    def glob_fnc(cls, p_str):
        _ = glob.glob(
            p_str
        )
        if _:
            if cls.get_platform_is_windows():
                _ = map(lambda x: x.replace('\\', '/'), _)
            return _
        return []

    @classmethod
    def get_path_is_windows(cls, path):
        return not not re.findall(
            r'^[a-zA-Z]:(.*)', path
        )

    @classmethod
    def get_path_is_linux(cls, path):
        return not not re.findall(
            r'/(.*)', path
        )

    @classmethod
    def get_root(cls, path):
        if cls.get_path_is_windows(path):
            return path.split(cls.PATHSEP)[0]
        elif cls.get_path_is_linux(path):
            return cls.PATHSEP

    @classmethod
    def set_map_to_nas(cls, path):
        path = cls.clear_pathsep_to(path)
        if StgBaseMtd.get_path_is_linux(path):
            src_root = path[:2]
            if src_root == '/l':
                _ = '/ifs/data/cgdata'+path[len(src_root):]
                return _
            elif src_root == '/t':
                _ = '/hwshare001'+path[len(src_root):]
                return _
            else:
                return path

    @classmethod
    def convert_pathsep_to(cls, path):
        lis = []
        for i in path:
            i_r = repr(i)
            i_r_s = i_r.split("'")[1]
            i_r_s_c = len(i_r_s)
            if i_r_s_c == 1:
                lis.append(i)
            elif i_r_s_c == 2:
                if i_r_s == '\\\\':
                    lis.append('/')
                else:
                    lis.append('/'+i_r_s[-1])
            else:
                #
                if i_r_s in ['\\x07']:
                    lis.append('/a')
                elif i_r_s in ['\\x08']:
                    lis.append('/b')
                # hex
                elif i_r_s.startswith('\\x'):
                    hex_str = '0'+i_r_s[1:]
                    lis.append('/'+str(int(oct(int(hex_str, 16)))))
                # unicode
                elif i_r_s.startswith('\\u'):
                    lis.append(i_r_s)
        #
        return ''.join(lis).decode('unicode_escape')

    @classmethod
    def clear_pathsep_to(cls, path):
        path_ = cls.convert_pathsep_to(path)
        #
        _ = path_.split(cls.PATHSEP)
        new_path = cls.PATHSEP.join([i for i in _ if i])
        # etc: '/data/f/'
        if path_.endswith(cls.PATHSEP):
            new_path += '/'
        if path_.startswith(cls.PATHSEP):
            return cls.PATHSEP+new_path
        return new_path

    @classmethod
    def get_permission(cls, path):
        def get_str_fnc_(st_mode_):
            _mode_list = [
                #
                'd',
                # user
                # read, write, execute
                'r', 'w', 'x',
                # group
                'r', 'w', 'x',
                # other
                'r', 'w', 'x'
            ]
            _mode_b = bin(st_mode_)[-10:]
            _result = ''
            for _idx, _flg in enumerate(_mode_b):
                if _flg == '1':
                    _result += _mode_list[_idx]
                else:
                    _result += '-'
            return _result

        if os.path.exists(path) is True:
            s = os.stat(path)
            return get_str_fnc_(s.st_mode)

    @classmethod
    def get_user(cls, path):
        # noinspection PyBroadException
        if os.path.exists(path) is True:
            s = os.stat(path)
            uid = s.st_uid
            if StgBaseMtd.get_platform_is_linux():
                import pwd

                try:
                    user = pwd.getpwuid(uid)[0]
                    return user
                except KeyError:
                    return 'unknown'
        return 'unknown'

    @classmethod
    def get_group_name(cls, path):
        # noinspection PyBroadException
        if os.path.exists(path) is True:
            stat_info = os.stat(path)
            gid = stat_info.st_gid
            if StgBaseMtd.get_platform_is_linux():
                import grp

                group_name = grp.getgrgid(gid)[0]
                return group_name
        return None

    @classmethod
    def create_directory(cls, directory_path):
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

    @classmethod
    def get_relpath(cls, path_src, path_tgt):
        return os.path.relpath(path_src, path_tgt)

    @classmethod
    def get_file_realpath(cls, file_path_src, file_path_tgt):
        directory_path_src = os.path.dirname(file_path_src)
        return os.path.relpath(file_path_tgt, directory_path_src)

    @classmethod
    def get_is_exists(cls, path):
        return os.path.exists(path)

    @classmethod
    def get_is_file(cls, path):
        return os.path.isfile(path)

    @classmethod
    def get_is_directory(cls, path):
        return os.path.isdir(path)

    @classmethod
    def get_is_readable(cls, path):
        return os.access(path, os.R_OK)

    @classmethod
    def get_is_writable(cls, path):
        return os.access(path, os.W_OK)

    @classmethod
    def get_is_executable(cls, path):
        return os.access(path, os.X_OK)

    @classmethod
    def get_file_args(cls, file_path):
        directory_path = os.path.dirname(file_path)
        base = os.path.basename(file_path)
        name_base, ext = os.path.splitext(base)
        return directory_path, name_base, ext

    @classmethod
    def to_file_deduplication_mapper(cls, file_paths):
        dict_ = {}
        for i_path in file_paths:
            i_path_base = os.path.splitext(i_path)[0]
            dict_[i_path_base] = i_path
        return dict_

    @classmethod
    def deduplication_files_by_formats(cls, file_paths, formats):
        list_ = []
        dict_ = {}
        set_ = set()
        for i_file_path in file_paths:
            i_path_base, i_ext = os.path.splitext(i_file_path)
            i_format = i_ext[1:]
            set_.add(i_format)
            dict_.setdefault(i_path_base, []).append(i_format)
        #
        fs = [i for i in formats]
        [fs.append(i) for i in set_ if i not in fs]
        #
        for k, v in dict_.items():
            v.sort(key=fs.index)
            list_.append('{}.{}'.format(k, v[0]))
        return list_

    @classmethod
    def get_modify_timestamp(cls, path):
        return os.stat(path).st_mtime

    @classmethod
    def get_file_timestamp_is_same_to(cls, file_path_src, file_path_tgt):
        if file_path_src is not None and file_path_tgt is not None:
            if cls.get_is_file(file_path_src) is True and cls.get_is_file(file_path_tgt) is True:
                return int(cls.get_modify_timestamp(file_path_src)) == int(cls.get_modify_timestamp(file_path_tgt))
            return False
        return False

    @classmethod
    def rename_file_ext_to(cls, file_path, ext_tgt):
        return


class StgPathMapDict(object):
    def __init__(self, raw):
        self._raw = raw
        if StgBaseMtd.get_platform_is_windows() is True:
            p = 'windows'
        elif StgBaseMtd.get_platform_is_linux() is True:
            p = 'linux'
        else:
            raise TypeError()
        #
        self._windows_dict = self._generate_mapper_dict('windows')
        self._linux_dict = self._generate_mapper_dict('linux')
        #
        self._current_dict = self._generate_mapper_dict(p)

    def __contains__(self, item):
        return item in self._current_dict

    def __getitem__(self, item):
        return self._current_dict[item]

    def _generate_mapper_dict(self, platform_):
        dict_ = collections.OrderedDict()
        raw_platform = self._raw[platform_]
        for k, v in raw_platform.items():
            for i in v:
                dict_[i] = k
        return dict_


class StgEnvPathMapDict(object):
    def __init__(self, raw):
        self._raw = raw
        if StgBaseMtd.get_platform_is_windows() is True:
            p = 'windows'
        elif StgBaseMtd.get_platform_is_linux() is True:
            p = 'linux'
        else:
            raise TypeError()

        self._path_dict = self._generate_path_dict(p)
        self._env_dict = self._generate_env_dict(p)

    def _generate_path_dict(self, platform_):
        dict_ = collections.OrderedDict()
        raw_platform = self._raw[platform_]
        for k, v in raw_platform.items():
            for i in v:
                dict_[i] = k
        return dict_

    def _generate_env_dict(self, platform_):
        dict_ = collections.OrderedDict()
        raw_platform = self._raw[platform_]
        for k, v in raw_platform.items():
            dict_[k] = v[0]
        return dict_


class StgBasePathMapMtd(object):
    PATHSEP = '/'
    MAPPER = StgPathMapDict(
        {
            "windows": {},
            "linux": {}
        }
    )

    @classmethod
    def map_to_current(cls, path):
        if path is not None:
            if StgBaseMtd.get_platform_is_windows():
                return cls.map_to_windows(path)
            elif StgBaseMtd.get_platform_is_linux():
                return cls.map_to_linux(path)
            return StgBaseMtd.clear_pathsep_to(path)
        return path

    @classmethod
    def map_to_windows(cls, path):
        # clear first
        path = StgBaseMtd.clear_pathsep_to(path)
        if StgBaseMtd.get_path_is_linux(path):
            mapper_dict = cls.MAPPER._windows_dict
            for i_root_src, i_root_tgt in mapper_dict.items():
                if path == i_root_src:
                    return i_root_tgt
                elif path.startswith(i_root_src+cls.PATHSEP):
                    return i_root_tgt+path[len(i_root_src):]
            return path
        return path

    @classmethod
    def map_to_linux(cls, path):
        """
        print Path.map_to_linux(
            'l:/a'
        )
        :param path:
        :return:
        """
        # clear first
        path = StgBaseMtd.clear_pathsep_to(path)
        if StgBaseMtd.get_path_is_windows(path):
            mapper_dict = cls.MAPPER._linux_dict
            for i_root_src, i_root_tgt in mapper_dict.items():
                if path == i_root_src:
                    return i_root_tgt
                elif path.startswith(i_root_src+cls.PATHSEP):
                    return i_root_tgt+path[len(i_root_src):]
            return path
        return path


class HashMtd(object):
    @classmethod
    def get_pack_format(cls, max_value):
        o = 'q'
        if max_value < 128:
            o = 'b'
        elif max_value < 32768:
            o = 'h'
        elif max_value < 4294967296:
            o = 'i'
        return o

    @classmethod
    def get_hash_value(cls, raw, as_unique_id=False):
        s = hashlib.md5(
            str(raw)
        ).hexdigest()
        if as_unique_id is True:
            return UuidMtd.generate_by_hash_value(s)
        return s.upper()

    @classmethod
    def get_hash_key(cls, raw, as_unique_id=False):
        s = hashlib.md5(
            json.dumps(raw)
        ).hexdigest()
        if as_unique_id is True:
            return UuidMtd.generate_by_hash_value(s)
        return s.upper()

    @classmethod
    def get_hash_value_(cls, raw, as_unique_id=False):
        raw_str = str(raw)
        pack_array = [ord(i) for i in raw_str]
        #
        s = hashlib.md5(
            struct.pack('%s%s'%(len(pack_array), cls.get_pack_format(max(pack_array))), *pack_array)
        ).hexdigest()
        if as_unique_id is True:
            return UuidMtd.generate_by_hash_value(s)
        return s.upper()


class UuidMtd(object):
    BASIC = '4908BDB4-911F-3DCE-904E-96E4792E75F1'
    VERSION = 3.0

    @classmethod
    def _to_file_str(cls, file_path):
        file_path = StgBasePathMapMtd.map_to_linux(file_path)
        if os.path.isfile(file_path):
            timestamp = os.stat(file_path).st_mtime
            size = os.path.getsize(file_path)
            if isinstance(file_path, six.text_type):
                file_path = file_path.encode('utf-8')
            return 'file={}&timestamp={}&size={}&version={}'.format(file_path, timestamp, size, cls.VERSION)
        return 'file={}&version={}'.format(file_path, cls.VERSION)

    @classmethod
    def generate_new(cls):
        return str(uuid.uuid1()).upper()

    @classmethod
    def generate_by_text(cls, text):
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        return str(uuid.uuid3(uuid.UUID(cls.BASIC), str(text))).upper()

    @classmethod
    def generate_by_hash_value(cls, hash_value):
        return cls.generate_by_text(hash_value)

    @classmethod
    def generate_by_file(cls, file_path):
        file_str = cls._to_file_str(file_path)
        return str(
            uuid.uuid3(
                uuid.UUID(cls.BASIC),
                file_str
            )
        ).upper()

    @classmethod
    def generate_by_files(cls, file_paths, extra=None):
        file_strs = map(cls._to_file_str, file_paths)
        file_strs.sort()
        if isinstance(extra, (tuple, list)):
            file_strs.extend(extra)
        return str(
            uuid.uuid3(
                uuid.UUID(cls.BASIC),
                ';'.join(file_strs)
            )
        ).upper()


class ExceptionMtd(object):
    @classmethod
    def set_print(cls):
        import traceback
        #
        traceback.print_exc()

    @classmethod
    def print_stack(cls):
        import sys
        #
        import traceback
        #
        exc_type, exc_value, exc_stack = sys.exc_info()
        exc_texts = []
        value = '{}: "{}"'.format(exc_type.__name__, repr(exc_value))
        for seq, stk in enumerate(traceback.extract_tb(exc_stack)):
            i_file_path, i_line, i_fnc, i_fnc_line = stk
            exc_texts.append(
                '    file "{}" line {} in {}\n        {}'.format(i_file_path, i_line, i_fnc, i_fnc_line)
            )
        exc_texts.append(value)
        if exc_texts:
            sys.stdout.write('\n'.join(exc_texts)+'\n')

    @classmethod
    def get_stack(cls):
        import sys
        #
        import traceback

        #
        exc_type, exc_value, exc_stack = sys.exc_info()
        exc_texts = []
        value = '{}: "{}"'.format(exc_type.__name__, repr(exc_value))
        for seq, stk in enumerate(traceback.extract_tb(exc_stack)):
            i_file_path, i_line, i_fnc, i_fnc_line = stk
            exc_texts.append(
                u'    file "{}" line {} in {}\n        {}'.format(i_file_path, i_line, i_fnc, i_fnc_line)
            )

        exc_texts.append(value)
        return '\n'.join(exc_texts)

    @classmethod
    def get_stack_(cls):
        import sys
        #
        import traceback

        exc_texts = []
        exc_type, exc_value, exc_stack = sys.exc_info()
        if exc_type:
            value = '{}: "{}"'.format(exc_type.__name__, repr(exc_value))
            for seq, stk in enumerate(traceback.extract_tb(exc_stack)):
                i_file_path, i_line, i_fnc, i_fnc_line = stk
                exc_texts.append(
                    '{indent}file "{file}" line {line} in {fnc}\n{indent}{indent}{fnc_line}'.format(
                        **dict(
                            indent='    ',
                            file=i_file_path,
                            line=i_line,
                            fnc=i_fnc,
                            fnc_line=i_fnc_line
                        )
                    )
                )
            #
            exc_texts.append(value)
        return '\n'.join(exc_texts)


class FfmpegMtd(object):
    """
ffmpeg version 4.2.2 Copyright (c) 2000-2019 the FFmpeg developers
  built with gcc 4.8.5 (GCC) 20150623 (Red Hat 4.8.5-39)
  configuration: --prefix=/linux_home/wangting/ffmpeg_build --pkg-config-flags=--static --extra-cflags=-I/linux_home/wangting/ffmpeg_build/include --extra-ldflags=-L/linux_home/wangting/ffmpeg_build/lib --extra-libs=-lpthread --extra-libs=-lm --bindir=/linux_home/wangting/bin --enable-gpl --enable-libfdk_aac --enable-libfreetype --enable-libmp3lame --enable-libopus --enable-libvpx --enable-libx264 --enable-libx265 --enable-nonfree
  libavutil      56. 31.100 / 56. 31.100
  libavcodec     58. 54.100 / 58. 54.100
  libavformat    58. 29.100 / 58. 29.100
  libavdevice    58.  8.100 / 58.  8.100
  libavfilter     7. 57.100 /  7. 57.100
  libswscale      5.  5.100 /  5.  5.100
  libswresample   3.  5.100 /  3.  5.100
  libpostproc    55.  5.100 / 55.  5.100
Hyper fast Audio and Video encoder
usage: ffmpeg [options] [[infile options] -i infile]... {[outfile options] outfile}...

Getting help:
    -h      -- print basic options
    -h long -- print more options
    -h full -- print all options (including all format and codec specific options, very long)
    -h type=name -- print all options for the named decoder/encoder/demuxer/muxer/filter/bsf
    See man ffmpeg for detailed description of the options.

Print help / information / capabilities:
-L                  show license
-h topic            show help
-? topic            show help
-help topic         show help
--help topic        show help
-version            show version
-buildconf          show build configuration
-formats            show available formats
-muxers             show available muxers
-demuxers           show available demuxers
-devices            show available devices
-codecs             show available codecs
-decoders           show available decoders
-encoders           show available encoders
-bsfs               show available bit stream filters
-protocols          show available protocols
-filters            show available filters
-pix_fmts           show available pixel formats
-layouts            show standard channel layouts
-sample_fmts        show available audio sample formats
-colors             show available color names
-sources device     list sources of the input device
-sinks device       list sinks of the output device
-hwaccels           show available HW acceleration methods

Global options (affect whole program instead of just one file:
-loglevel loglevel  set logging level
-v loglevel         set logging level
-report             generate a report
-max_alloc bytes    set maximum size of a single allocated block
-y                  overwrite output files
-n                  never overwrite output files
-ignore_unknown     Ignore unknown stream types
-filter_threads     number of non-complex filter threads
-filter_complex_threads  number of threads for -filter_complex
-stats              print progress report during encoding
-max_error_rate maximum error rate  ratio of errors (0.0: no errors, 1.0: 100% errors) above which ffmpeg returns an error instead of success.
-bits_per_raw_sample number  set the number of bits per raw sample
-vol volume         change audio volume (256=normal)

Per-file main options:
-f fmt              force format
-c codec            codec name
-codec codec        codec name
-pre preset         preset name
-map_metadata outfile[,metadata]:infile[,metadata]  set metadata information of outfile from infile
-t duration         record or transcode "duration" seconds of audio/video
-to time_stop       record or transcode stop time
-fs limit_size      set the limit file size in bytes
-ss time_off        set the start time offset
-sseof time_off     set the start time offset relative to EOF
-seek_timestamp     enable/disable seeking by timestamp with -ss
-timestamp time     set the recording timestamp ('now' to set the current time)
-metadata string=string  add metadata
-program title=string:st=number...  add program with specified streams
-target type        specify target file type ("vcd", "svcd", "dvd", "dv" or "dv50" with optional prefixes "pal-", "ntsc-" or "film-")
-apad               audio pad
-frames number      set the number of frames to output
-filter filter_graph  set stream filtergraph
-filter_script filename  read stream filtergraph description from a file
-reinit_filter      reinit filtergraph on input parameter changes
-discard            discard
-disposition        disposition

Video options:
-vframes number     set the number of video frames to output
-r rate             set frame rate (Hz value, fraction or abbreviation)
-s size             set frame size (WxH or abbreviation)
-aspect aspect      set aspect ratio (4:3, 16:9 or 1.3333, 1.7777)
-bits_per_raw_sample number  set the number of bits per raw sample
-vn                 disable video
-vcodec codec       force video codec ('copy' to copy stream)
-timecode hh:mm:ss[:;.]ff  set initial TimeCode value.
-pass n             select the pass number (1 to 3)
-vf filter_graph    set video filters
-ab bitrate         audio bitrate (please use -b:a)
-b bitrate          video bitrate (please use -b:v)
-dn                 disable data

Audio options:
-aframes number     set the number of audio frames to output
-aq quality         set audio quality (codec-specific)
-ar rate            set audio sampling rate (in Hz)
-ac channels        set number of audio channels
-an                 disable audio
-acodec codec       force audio codec ('copy' to copy stream)
-vol volume         change audio volume (256=normal)
-af filter_graph    set audio filters

Subtitle options:
-s size             set frame size (WxH or abbreviation)
-sn                 disable subtitle
-scodec codec       force subtitle codec ('copy' to copy stream)
-stag fourcc/tag    force subtitle tag/fourcc
-fix_sub_duration   fix subtitles duration
-canvas_size size   set canvas size (WxH or abbreviation)
-spre preset        set the subtitle options to the indicated preset


    """

    @classmethod
    def get_ffmpeg_source(cls):
        return '/l/packages/pg/prod/ffmpeg/4.2.2/platform-linux/bin/ffmpeg'

    @classmethod
    def get_ffprobe_source(cls):
        return '/l/packages/pg/prod/ffmpeg/4.2.2/platform-linux/bin/ffprobe'

    @classmethod
    def create_image_cache(cls, input_file_path, output_file_path, frame_range, frame_step):
        data = map(
            lambda x: 'file \'{}\''.format(x), cls.completion_image_cache(input_file_path, frame_range, frame_step)
        )
        cache_directory_path = os.path.dirname(output_file_path)
        cache_name_base = os.path.splitext(os.path.basename(output_file_path))[0]
        cache_f = '{}/{}.{}.files'.format(cache_directory_path, cache_name_base, '{}-{}'.format(*frame_range))
        with open(cache_f, 'w') as f:
            f.write('\n'.join(data))
        return cache_f

    @classmethod
    def completion_image_cache(cls, file_path, frame_range, frame_step):
        list_ = []
        directory_path = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        s = re.findall('#', file_name)
        s_c = len(s)
        f_cur = None
        if isinstance(frame_step, int):
            for i in range(*frame_range):
                i_f = '{}/{}'.format(directory_path, file_name.replace('#'*s_c, str(i).zfill(s_c)))
                if (i-1) % frame_step == 0:
                    f_cur = i_f
                    list_.append(i_f)
                else:
                    if f_cur is not None:
                        list_.append(f_cur)
        else:
            for i in range(*frame_range):
                i_f = '{}/{}'.format(directory_path, file_name.replace('#'*s_c, str(i).zfill(s_c)))
                if os.path.isfile(i_f):
                    f_cur = i_f
                    list_.append(i_f)
                else:
                    if f_cur is not None:
                        list_.append(f_cur)
        return list_

    @classmethod
    def get_image_concat_command(cls, **kwargs):
        """
    cmd = FfmpegMtd.get_image_concat_command(
        input='/data/e/workspace/lynxi/test/maya/software-render/render/09/test/image/cam_full_body.####.jpg',
        output='/data/e/workspace/lynxi/test/maya/software-render/render/09/test/cam_full_body.mov',
        fps=24
    )

    PrcBaseMtd.execute_with_result(
        cmd
    )
        """
        start_frame = kwargs.pop('start_frame')
        end_frame = kwargs.pop('end_frame')
        return (
            '{bin}'
            ' -r {fps}'
            ' -f concat -safe 0 -i "{input}"'
            ' -vf "fps={fps}"'
            ' -c:v libx264'
            ' -pix_fmt yuv420p'
            ' -b:v 8000k'
            ' -y'
            ' "{output}"'
        ).format(
            bin=cls.get_ffmpeg_source(),
            input=cls.create_image_cache(
                kwargs.pop('input'),
                kwargs['output'],
                frame_range=(start_frame, end_frame),
                frame_step=kwargs.get('frame_step')
            ),
            **kwargs
        )

    @classmethod
    def create_vedio_cache(cls, input_file_paths, output_file_path):
        data = map(
            lambda x: 'file \'{}\''.format(x), input_file_paths
        )
        cache_directory_path = os.path.dirname(output_file_path)
        cache_name_base = os.path.splitext(os.path.basename(output_file_path))[0]
        cache_f = '{}/{}.files'.format(cache_directory_path, cache_name_base)
        with open(cache_f, 'w') as f:
            f.write('\n'.join(data))
        return cache_f

    @classmethod
    def get_vedio_concat_command(cls, **kwargs):
        input_ = kwargs.pop('input')
        kwargs['input'] = cls.create_vedio_cache(input_, kwargs.get('output'))
        return (
            '{bin}'
            ' -f concat -safe 0 -i "{input}"'
            ' -c:v copy'
            ' -y'
            ' "{output}"'
        ).format(
            bin=cls.get_ffmpeg_source(),
            **kwargs
        )


_HEXDIG = '0123456789ABCDEFabcdef'
_HEXTOCHR = dict((a+b, chr(int(a+b, 16))) for a in _HEXDIG for b in _HEXDIG)


class SPathMtd(object):
    """
    from urllib quote and unquote
    """
    ALWAYS_SAFE = (
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        'abcdefghijklmnopqrstuvwxyz'
        '0123456789'
    )
    SAFE_MAP = {}
    SAFE_QUOTERS = {}
    for i, c in zip(xrange(256), str(bytearray(xrange(256)))):
        SAFE_MAP[c] = c if (i < 128 and c in ALWAYS_SAFE) else '%{:02X}'.format(i)

    RE_ASCII = re.compile('([\x00-\x7f]+)')

    @classmethod
    def set_quote_to(cls, s, safe=''):
        # fastpath
        if not s:
            if s is None:
                raise TypeError('None object cannot be quoted')
            return s
        cache_key = (safe, cls.ALWAYS_SAFE)
        try:
            (quoter, safe) = cls.SAFE_QUOTERS[cache_key]
        except KeyError:
            safe_map = cls.SAFE_MAP.copy()
            safe_map.update([(c, c) for c in safe])
            quoter = safe_map.__getitem__
            safe = cls.ALWAYS_SAFE+safe
            cls.SAFE_QUOTERS[cache_key] = (quoter, safe)
        if not s.rstrip(safe):
            return s
        return ''.join(map(quoter, s))

    @classmethod
    def _get_is_unicode(cls, x):
        return isinstance(x, unicode)

    @classmethod
    def set_unquote_to(cls, s):
        """unquote('abc%20def') -> 'abc def'."""
        if cls._get_is_unicode(s):
            if '%' not in s:
                return s
            bits = cls.RE_ASCII.split(s)
            res = [bits[0]]
            append = res.append
            for i in range(1, len(bits), 2):
                append(cls.set_unquote_to(str(bits[i])).decode('latin1'))
                append(bits[i+1])
            return ''.join(res)

        bits = s.split('%')
        # fastpath
        if len(bits) == 1:
            return s
        res = [bits[0]]
        append = res.append
        for item in bits[1:]:
            try:
                append(_HEXTOCHR[item[:2]])
                append(item[2:])
            except KeyError:
                append('%')
                append(item)
        return ''.join(res)

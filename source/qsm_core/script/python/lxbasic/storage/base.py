# coding:utf-8
from __future__ import print_function

import parse

import time

import six

import os

import collections

if six.PY2:
    # python 2
    # noinspection PyCompatibility
    from xmlrpclib import ServerProxy as _ServerProxy
else:
    # python 3
    # noinspection PyCompatibility
    from xmlrpc.client import ServerProxy as _ServerProxy

import threading

import re

import fnmatch

import functools

import glob

import shutil

import json

import gzip

import zipfile

import hashlib

import uuid

import lxbasic.log as bsc_log

import lxbasic.content as bsc_content

from ..scan import base as _scan_base

from ..scan import glob_ as _scan_glob

from ..core import base as _cor_base

from ..core import raw as _cor_raw

from ..core import raw_for_dict as _cor_raw_for_dict

from ..core import path as _cor_path

from ..core import pattern as _cor_pattern

from ..core import time_ as _cor_time

from ..core import process as _cor_process

from ..core import thread_ as _cor_thread


class StgRpc(object):
    RPC_SERVER = '10.10.206.117'
    RPC_PORT = 58888
    PATHSEP = '/'

    LOG_KEY = 'rpc'

    @classmethod
    def get_client(cls, port_addition=0):
        return _ServerProxy(
            'http://{0}:{1}'.format(cls.RPC_SERVER, cls.RPC_PORT+port_addition)
        )

    @classmethod
    def create_directory(cls, directory_path, mode='775'):
        units = _cor_path.BscNodePath.get_dag_component_paths(directory_path)
        units.reverse()
        list_ = []
        for i_path in units:
            if i_path != cls.PATHSEP:
                if os.path.exists(i_path) is False:
                    list_.append(i_path)
        #
        for i in list_:
            cls._create_directory_fnc_(i, mode)

    @classmethod
    def _create_directory_fnc_(cls, directory_path, mode='775'):
        key = 'rpc create directory'
        if os.path.exists(directory_path) is False:
            timeout = 25
            cost_time = 0
            start_time = time.time()
            clt = cls.get_client()
            clt.mkdir(directory_path, mode)
            p = os.path.dirname(directory_path)
            while os.path.exists(directory_path) is False:
                cost_time = int(time.time()-start_time)
                if cost_time > timeout:
                    raise RuntimeError(
                        bsc_log.Log.trace_method_error(
                            key,
                            'path="{}" is timeout, cost time {}s'.format(directory_path, cost_time)
                        )
                    )
                #
                if _cor_base.BscSystem.get_is_linux():
                    os.system('ls {} > /dev/null'.format(p))
                #
                time.sleep(1)
            #
            bsc_log.Log.trace_method_result(
                key,
                'path="{}" is cost time {}s'.format(directory_path, cost_time)
            )
            # noinspection PyArgumentEqualDefault
            cls.change_owner(
                directory_path,
                user='artist', group='artists'
            )
        return True

    @classmethod
    def delete(cls, file_path):
        if os.path.exists(file_path) is True:
            timeout = 25
            cost_time = 0
            start_time = time.time()
            clt = cls.get_client()
            clt.rm_file(file_path)
            # delete, check is exists
            p = os.path.dirname(file_path)
            while os.path.exists(file_path) is True:
                cost_time = int(time.time()-start_time)
                if cost_time > timeout:
                    raise RuntimeError(
                        bsc_log.Log.trace_method_error(
                            'rpc delete',
                            'path="{}" is timeout, cost time {}s'.format(file_path, cost_time)
                        )
                    )
                #
                if _cor_base.BscSystem.get_is_linux():
                    os.system('ls {} > /dev/null'.format(p))
                #
                time.sleep(1)
            #
            bsc_log.Log.trace_method_result(
                'rpc delete',
                'path="{}" is completed, cost time {}s'.format(file_path, cost_time)
            )

    @classmethod
    def copy_to_file(cls, file_path_src, file_path_tgt, replace=False):
        key = 'rpc copy to file'
        if replace is True:
            if os.path.exists(file_path_tgt):
                pass
        #
        if os.path.exists(file_path_tgt) is False:
            directory_path_tgt = os.path.dirname(file_path_tgt)
            if os.path.exists(directory_path_tgt) is False:
                cls.create_directory(directory_path_tgt)

            timeout = 25
            cost_time = 0
            start_time = time.time()
            clt = cls.get_client()
            clt.copyfile(file_path_src, file_path_tgt)
            p = os.path.dirname(file_path_tgt)
            while os.path.exists(file_path_tgt) is False:
                cost_time = int(time.time()-start_time)
                if cost_time > timeout:
                    raise RuntimeError(
                        bsc_log.Log.trace_method_error(
                            key,
                            'path="{}" is timeout, cost time {}s'.format(file_path_tgt, cost_time)
                        )
                    )
                if _cor_base.BscSystem.get_is_linux():
                    os.system('ls {} > /dev/null'.format(p))
                #
                time.sleep(1)
            # noinspection PyArgumentEqualDefault
            cls.change_owner(
                file_path_tgt,
                user='artist', group='artists'
            )
            # noinspection PyArgumentEqualDefault
            cls.change_mode(
                file_path_tgt,
                mode='775'
            )
            #
            bsc_log.Log.trace_method_result(
                key,
                'path="{} >> {}", cost time {}s'.format(file_path_src, file_path_tgt, cost_time)
            )

    @classmethod
    def change_mode(cls, path, mode='775'):
        key = 'rpc change mode'
        if os.path.exists(path) is True:
            clt = cls.get_client()
            clt.chmod(path, mode)
            #
            if _cor_base.BscSystem.get_is_linux():
                p = os.path.dirname(path)
                os.system('ls {} > /dev/null'.format(p))
            #
            bsc_log.Log.trace_method_result(
                key,
                'path="{}", mode="{}"'.format(path, mode)
            )

    @classmethod
    def change_owner(cls, path, user='artist', group='artists'):
        key = 'rpc change owner'
        if os.path.exists(path) is True:
            clt = cls.get_client()
            clt.chown(path, user, group)
            p = os.path.dirname(path)
            if _cor_base.BscSystem.get_is_linux():
                os.system('ls {} > /dev/null'.format(p))
            bsc_log.Log.trace_method_result(
                key,
                'path="{}", user="{}", group="{}"'.format(path, user, group)
            )


class StgSsh(object):
    GROUP_ID_QUERY = {
        'cg_group': 20002,
        # 'cg_grp': 20002,
        'ani_grp': 20017,
        'rlo_grp': 20025,
        'flo_grp': 20026,
        'art_grp': 20010,
        'stb_grp': 20027,
        'cfx_grp': 20015,
        'efx_grp': 20016,
        'dmt_grp': 20020,
        'lgt_grp': 20018,
        'mod_grp': 20011,
        'grm_grp': 20012,
        'rig_grp': 20013,
        'srf_grp': 20014,
        'set_grp': 20023,
        'plt_grp': 20024,
        'edt_grp': 20028,
        #
        'coop_grp': 20032,
        #
        'td_grp': 20004,
    }
    CMD_QUERY = {
        'deny': 'chmod -R +a group {group_id} deny dir_gen_write,std_delete,delete_child,object_inherit,container_inherit "{path}"',
        'allow': 'chmod -R +a group {group_id} allow dir_gen_all,object_inherit,container_inherit "{path}"',
        'read_only': 'chmod -R +a group {group_id} allow dir_gen_read,dir_gen_execute,object_inherit,container_inherit "{path}"',
        'read_only-0': 'chmod -R +a group {group_id} allow dir_gen_read,dir_gen_execute,object_inherit,container_inherit "{path}"',
        'show_grp': 'ls -led "{path}"',
        'remove_grp': 'chmod -R -a# {index} "{path}"',
        'file_allow': 'chmod -R +a group {group_id} allow file_gen_all,object_inherit,container_inherit "{path}"',
    }
    GROUP_PATTERN = r' {index}: group:DIEZHI\{group} {context}'
    USER_PATTERN = r' {index}: user:DIEZHI\{user} {context}'
    #
    HOST = 'isilon.diezhi.local'
    USER = 'root'

    # noinspection PyAugmentAssignment
    class MakePassword(object):
        def __init__(self, key, s):
            self.key = key
            self.s = s

        def encrypt(self):
            b = bytearray(str(self.s).encode("utf-8"))
            n = len(b)
            c = bytearray(n*2)
            j = 0
            for i in range(0, n):
                b1 = b[i]
                b2 = b1 ^ self.key
                c1 = b2%16
                c2 = b2//16
                c1 = c1+65
                c2 = c2+65
                c[j] = c1
                c[j+1] = c2
                j = j+2
            return c.decode("utf-8")

        def decrypt(self):
            c = bytearray(str(self.s).encode("utf-8"))
            n = len(c)
            if n%2 != 0:
                return ""
            n = n//2
            b = bytearray(n)
            j = 0
            for i in range(0, n):
                c1 = c[j]
                c2 = c[j+1]
                j = j+2
                c1 = c1-65
                c2 = c2-65
                b2 = c2*16+c1
                b1 = b2^self.key
                b[i] = b1
            # noinspection PyBroadException
            try:
                return b.decode("utf-8")
            except Exception:
                return "failed"

    @classmethod
    def _set_nas_cmd_run_(cls, cmd):
        # noinspection PyUnresolvedReferences
        import paramiko

        #
        bsc_log.Log.trace_method_result(
            'nas-cmd-run',
            'command=`{}`'.format(cmd)
        )
        #
        password = StgSsh.MakePassword(120, 'KBHBOCCCMDMBKEBDCBKBLAKA')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=cls.HOST,
            username=cls.USER,
            password=password.decrypt().encode('utf-8'),
            timeout=10,
            allow_agent=False,
            look_for_keys=False
        )
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        result = stdout.read()
        ssh.close()
        return result

    @classmethod
    def _get_all_group_data_(cls, nas_path):
        kwargs = dict(
            path=nas_path
        )
        cmd = cls.CMD_QUERY['show_grp'].format(
            **kwargs
        )
        result = cls._set_nas_cmd_run_(cmd)
        # print(result)
        dict_ = collections.OrderedDict()
        if result is not None:
            for i in result.split('\n'):
                i_p = parse.parse(r' {index}: group:DIEZHI\{group} {context}', i)
                if i_p:
                    i_dict = i_p.named
                    if i_dict:
                        dict_[i_dict['group']] = (i_dict['index'], i_dict['context'])
        return dict_

    @classmethod
    def _get_all_group_data_1_(cls, nas_path):
        kwargs = dict(
            path=nas_path
        )
        cmd = cls.CMD_QUERY['show_grp'].format(
            **kwargs
        )
        result = cls._set_nas_cmd_run_(cmd)
        # print(result)
        list_ = []
        if result is not None:
            for i in result.split('\n'):
                i_p = parse.parse(cls.GROUP_PATTERN, i)
                if i_p:
                    i_dict = i_p.named
                    if i_dict:
                        list_.append(
                            (i_dict['group'], i_dict['index'], i_dict['context'])
                        )
        return list_

    @classmethod
    def _get_all_user_data_(cls, nas_path):
        kwargs = dict(
            path=nas_path
        )
        cmd = cls.CMD_QUERY['show_grp'].format(
            **kwargs
        )
        result = cls._set_nas_cmd_run_(cmd)
        # print(result)
        list_ = []
        if result is not None:
            for i in result.split('\n'):
                i_p = parse.parse(cls.USER_PATTERN, i)
                if i_p:
                    i_dict = i_p.named
                    if i_dict:
                        list_.append(
                            (i_dict['user'], i_dict['index'], i_dict['context'])
                        )
        return list_

    @classmethod
    def _get_all_data_(cls, nas_path):
        kwargs = dict(
            path=nas_path
        )
        cmd = cls.CMD_QUERY['show_grp'].format(
            **kwargs
        )
        result = cls._set_nas_cmd_run_(cmd)
        # print(result)
        list_ = []
        if result is not None:
            for i in result.split('\n'):
                i_p_0 = parse.parse(cls.USER_PATTERN, i)
                if i_p_0:
                    i_dict = i_p_0.named
                    if i_dict:
                        list_.append(
                            (i_dict['user'], i_dict['index'], i_dict['context'])
                        )
                else:
                    i_p_1 = parse.parse(cls.GROUP_PATTERN, i)
                    if i_p_1:
                        i_dict = i_p_1.named
                        if i_dict:
                            list_.append(
                                (i_dict['group'], i_dict['index'], i_dict['context'])
                            )
        return list_


class StgSshOpt(object):
    def __init__(self, path):
        self._path = path
        self._nas_path = _cor_base.BscStorage.set_map_to_nas(path)

    def remove_all_group(self):
        group_data = StgSsh._get_all_group_data_1_(self._nas_path)
        group_data.reverse()
        for i_group_name, i_index, i_content in group_data:
            if i_group_name in StgSsh.GROUP_ID_QUERY:
                i_kwargs = dict(
                    path=self._nas_path,
                    index=i_index
                )
                i_cmd = StgSsh.CMD_QUERY['remove_grp'].format(
                    **i_kwargs
                )
                StgSsh._set_nas_cmd_run_(i_cmd)

    def set_read_only_for_groups(self, group_names):
        for i_group_name in group_names:
            if i_group_name in StgSsh.GROUP_ID_QUERY:
                i_group_id = StgSsh.GROUP_ID_QUERY[i_group_name]
                i_kwargs = dict(
                    group_id=i_group_id,
                    path=self._nas_path,
                )
                i_cmd = StgSsh.CMD_QUERY['read_only'].format(
                    **i_kwargs
                )
                StgSsh._set_nas_cmd_run_(i_cmd)

    def set_just_read_only_for(self, group_names):
        self.remove_all_group()
        self.remove_all_user()
        self.set_read_only_for_groups(group_names)

    def get_all_group_data(self):
        return StgSsh._get_all_group_data_1_(self._nas_path)

    def get_all_user_data(self):
        return StgSsh._get_all_user_data_(self._nas_path)

    def remove_all_user(self):
        user_data = StgSsh._get_all_user_data_(self._nas_path)
        user_data.reverse()
        for i_user_name, i_index, i_content in user_data:
            # print(i_user_name, i_index)
            i_kwargs = dict(
                path=self._nas_path,
                index=i_index
            )
            i_cmd = StgSsh.CMD_QUERY['remove_grp'].format(
                **i_kwargs
            )
            StgSsh._set_nas_cmd_run_(i_cmd)

    def get_all_data(self):
        return StgSsh._get_all_data_(self._nas_path)


class StgUser(object):
    @classmethod
    def get_windows_home(cls):
        return '{}{}'.format(
            os.environ.get('HOMEDRIVE', 'c:'),
            os.environ.get('HOMEPATH', '/temp')
        ).replace('\\', '/')

    @classmethod
    def get_linux_home(cls):
        return '{}'.format(
            os.environ.get('HOME', '/temp')
        )

    @classmethod
    def get_home(cls):
        if _cor_base.BscSystem.get_is_windows():
            return cls.get_windows_home()
        elif _cor_base.BscSystem.get_is_linux():
            return cls.get_linux_home()
        else:
            raise SystemError()

    @classmethod
    def get_windows_user_directory(cls):
        return '{}{}/.qosmic'.format(
            os.environ.get('HOMEDRIVE', 'c:'),
            os.environ.get('HOMEPATH', '/temp')
        ).replace('\\', '/')

    @classmethod
    def get_linux_user_directory(cls):
        return '{}/.qosmic'.format(
            os.environ.get('HOME', '/temp')
        )

    @classmethod
    def get_user_directory(cls):
        if _cor_base.BscSystem.get_is_windows():
            return cls.get_windows_user_directory()
        elif _cor_base.BscSystem.get_is_linux():
            return cls.get_linux_user_directory()
        else:
            raise SystemError()

    @classmethod
    def get_user_temporary_directory(cls, create=False):
        date_tag = _cor_base.BscSystem.get_date_tag()
        _ = '{}/temporary/{}'.format(
            cls.get_user_directory(), date_tag
        )
        if create:
            _cor_base.BscStorage.create_directory(_)
        return _

    @classmethod
    def get_user_debug_directory(cls, tag=None, create=False):
        date_tag = _cor_base.BscSystem.get_date_tag()
        _ = '{}/debug/{}'.format(
            cls.get_user_directory(), date_tag
        )
        if tag is not None:
            _ = '{}/{}'.format(_, tag)
        if create:
            _cor_base.BscStorage.create_directory(_)
        return _

    @classmethod
    def get_user_batch_exception_directory(cls, tag, create=False):
        date_tag = _cor_base.BscSystem.get_date_tag()
        _ = '{}/batch-exception-log/{}'.format(
            cls.get_user_directory(), date_tag
        )
        if tag is not None:
            _ = '{}/{}'.format(_, tag)
        if create:
            _cor_base.BscStorage.create_directory(_)
        return _

    @classmethod
    def get_user_log_directory(cls):
        date_tag = _cor_base.BscSystem.get_date_tag()
        return '{}/log/{}.log'.format(
            cls.get_user_directory(), date_tag
        )

    @classmethod
    def get_user_history_cache_file(cls):
        return '{}/history.yml'.format(
            cls.get_user_directory()
        )

    @classmethod
    def get_user_session_directory(cls, create=False):
        date_tag = _cor_base.BscSystem.get_date_tag()
        _ = '{}/.session/{}'.format(
            cls.get_user_directory(), date_tag
        )
        if create:
            _cor_base.BscStorage.create_directory(_)
        return _

    @classmethod
    def get_user_hook_file(cls, unique_id=None):
        directory_path = cls.get_user_session_directory()
        if unique_id is None:
            unique_id = _cor_base.BscUuid.generate_new()
        return '{}/{}.yml'.format(directory_path, unique_id)


class StgExplorer(object):
    @classmethod
    def open_directory(cls, path):
        path = _cor_raw.ensure_string(path)
        if _cor_base.BscSystem.get_is_windows():
            # must replace '/' to '\\', when path is share like "//nas/test.text"
            cmd = 'explorer "{}"'.format(path.replace('/', '\\'))
        elif _cor_base.BscSystem.get_is_linux():
            cmd = 'gio open "{}"'.format(path)
        else:
            raise SystemError()

        t_0 = threading.Thread(
            target=functools.partial(
                _cor_process.BscProcess.execute, cmd, ignore_return_code=1
            )
        )
        t_0.setDaemon(True)
        t_0.start()

    @classmethod
    def open_directory_force(cls, path):
        path = _cor_raw.ensure_string(path)
        if os.path.exists(path) is False:
            path = StgExtra.get_exists_component(path)

        cls.open_directory(path)

    @classmethod
    def open_file(cls, path):
        path = _cor_base.ensure_unicode(path)
        path = _cor_base.ensure_mbcs(path)
        if _cor_base.BscSystem.get_is_windows():
            # must replace '/' to '\\', when path is share like "//nas/test.text"
            cmd = 'explorer /select,"{}"'.format(path.replace('/', '\\'))
        elif _cor_base.BscSystem.get_is_linux():
            cmd = 'nautilus "{}" --select'.format(path)
        else:
            raise SystemError()

        t_0 = threading.Thread(
            target=functools.partial(
                _cor_process.BscProcess.execute, cmd, ignore_return_code=1
            )
        )
        t_0.setDaemon(True)
        t_0.start()

    @classmethod
    def open(cls, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                cls.open_directory(path)
            elif os.path.isfile(path):
                cls.open_file(path)
        else:
            component = StgExtra.get_exists_component(path)
            if component:
                cls.open_directory(component)


class StgExtra(object):
    @classmethod
    def get_exists_component(cls, path):
        units = _cor_path.BscNodePath.get_dag_component_paths(path)
        for i in units:
            if os.path.exists(i):
                return i

    @classmethod
    def get_paths_by_fnmatch_pattern(cls, pattern, sort_by='number'):
        _ = glob.glob(pattern) or []
        if _:
            # fix windows path
            if _cor_base.BscSystem.get_is_windows():
                _ = map(lambda x: x.replace('\\', '/'), _)
            if len(_) > 1:
                # sort by number
                if sort_by == 'number':
                    _.sort(key=lambda x: _cor_raw.BscText.to_number_embedded_args(x))
        return _

    @classmethod
    def create_directory(cls, directory_path):
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)
            bsc_log.Log.trace_method_result(
                'create-directory',
                'directory="{}"'.format(directory_path)
            )


class StgPathLink(object):
    @classmethod
    def link_to(cls, path_src, path_tgt):
        if os.path.exists(path_tgt) is False:
            tgt_dir_path = os.path.dirname(path_tgt)
            src_rel_path = os.path.relpath(path_src, tgt_dir_path)
            os.symlink(src_rel_path, path_tgt)

    @classmethod
    def get_is_link_source_to(cls, path_src, path_tgt):
        tgt_dir_path = os.path.dirname(path_tgt)
        src_rel_path = os.path.relpath(path_src, tgt_dir_path)
        if os.path.islink(path_tgt):
            orig_src_rel_path = os.readlink(path_tgt)
            return src_rel_path == orig_src_rel_path
        return False

    @classmethod
    def get_rel_path(cls, path_src, path_tgt):
        tgt_dir_path = os.path.dirname(path_tgt)
        return os.path.relpath(path_src, tgt_dir_path)

    @classmethod
    def get_is_link(cls, path):
        return os.path.islink(path)

    @classmethod
    def get_link_source(cls, path_tgt):
        cur_path = path_tgt
        while True:
            if os.path.exists(cur_path):
                if os.path.islink(cur_path) is True:
                    cur_directory_path = os.path.dirname(cur_path)
                    os.chdir(cur_directory_path)
                    cur_path = os.path.abspath(os.readlink(cur_path))
                else:
                    break
            else:
                break
        return cur_path

    @classmethod
    def link_file_to(cls, path_src, path_tgt):
        if os.path.isfile(path_src):
            if os.path.islink(path_src):
                path_src = cls.get_link_source(path_src)
            #
            if os.path.exists(path_tgt) is False:
                tgt_dir_path = os.path.dirname(path_tgt)
                src_rel_path = os.path.relpath(path_src, tgt_dir_path)
                os.symlink(src_rel_path, path_tgt)


class StgPath(_cor_base.BscStorage):
    @classmethod
    def get_parent(cls, path):
        return _cor_path.BscNodePath.get_dag_parent_path(
            path
        )


class StgDirectory(object):

    @classmethod
    def get_file_paths(cls, directory_path, ext_includes=None):
        return _scan_base.ScanBase.get_file_paths(directory_path, ext_includes)

    @classmethod
    def get_all_file_paths(cls, directory_path, ext_includes=None):
        return _scan_base.ScanBase.get_all_file_paths(directory_path, ext_includes)

    @classmethod
    def get_directory_paths(cls, directory_path):
        return _scan_base.ScanBase.get_directory_paths(directory_path)

    @classmethod
    def get_all_directory_paths(cls, directory_path):
        return _scan_base.ScanBase.get_all_directory_paths(directory_path)

    @classmethod
    def get_file_relative_path(cls, directory_path, file_path):
        return os.path.relpath(file_path, directory_path)

    @classmethod
    def do_thread_copy(cls, src_directory_path, directory_path_tgt, excludes=None):
        def copy_fnc_(src_file_path_, tgt_file_path_):
            shutil.copy2(src_file_path_, tgt_file_path_)
            bsc_log.Log.trace_method_result(
                'file copy',
                'file="{}" >> "{}"'.format(src_file_path_, tgt_file_path_)
            )

        #
        src_directory_path = src_directory_path
        file_paths = _scan_base.ScanBase.get_all_file_paths(src_directory_path)
        #
        threads = []
        for i_src_file_path in file_paths:
            i_local_file_path = i_src_file_path[len(src_directory_path):]
            #
            if isinstance(excludes, (tuple, list)):
                is_match = False
                for j in excludes:
                    if fnmatch.filter([i_local_file_path], j):
                        is_match = True
                        break
                #
                if is_match is True:
                    continue
            #
            i_tgt_file_path = directory_path_tgt+i_local_file_path
            if os.path.exists(i_tgt_file_path) is False:
                i_tgt_dir_path = os.path.dirname(i_tgt_file_path)
                if os.path.exists(i_tgt_dir_path) is False:
                    os.makedirs(i_tgt_dir_path)
                #
                i_thread = _cor_thread.TrdFnc(
                    copy_fnc_, i_src_file_path, i_tgt_file_path
                )
                threads.append(i_thread)
                i_thread.start()
        #
        [i.join() for i in threads]

    @classmethod
    def find_file_paths(cls, glob_pattern):
        return _scan_glob.ScanGlob.glob(glob_pattern)


class StgDirectoryMtdForMultiply(object):
    @classmethod
    def get_all_multiply_file_dict(cls, directory_path, name_pattern):
        dict_ = collections.OrderedDict()
        _ = _scan_base.ScanBase.get_all_file_paths(directory_path)
        for i_file_path in _:
            i_opt = StgFileOpt(i_file_path)
            i_number_args = StgFileTiles.get_number_args(
                i_opt.name, name_pattern
            )
            if i_number_args:
                i_pattern, i_numbers = i_number_args
                if len(i_numbers) == 1:
                    i_relative_path_dir_path = StgDirectory.get_file_relative_path(
                        directory_path, i_opt.directory_path
                    )
                    i_key = '{}/{}'.format(
                        i_relative_path_dir_path, i_pattern
                    )
                    dict_.setdefault(
                        i_key, []
                    ).append(i_numbers[0])
        return dict_


class StgFile(object):
    @classmethod
    def get_directory(cls, file_path):
        return os.path.dirname(file_path)

    @classmethod
    def get_is_exists(cls, file_path):
        return os.path.isfile(file_path)

    @classmethod
    def get_ext(cls, file_path):
        return os.path.splitext(file_path)[-1]

    @classmethod
    def get_name_base(cls, file_path):
        return os.path.splitext(os.path.basename(file_path))[0]

    @classmethod
    def get_path_base(cls, file_path):
        return os.path.splitext(file_path)[0]


class StgFileTiles(object):
    """
    methods using for multiply file
    etc. "/tmp/image.1001.exr" convert to "/tmp/image.####.exr"
    """
    PATHSEP = _cor_pattern.BscFileTiles.PATHSEP
    P = '[0-9]'
    CACHE = dict()

    @classmethod
    def get_number_args(cls, file_name, name_pattern):
        new_file_name = file_name
        args = _cor_pattern.BscFileTiles.get_args(
            name_pattern
        )
        if args:
            re_pattern = _cor_pattern.BscFileTiles.to_re_style(name_pattern)
            results = re.findall(re_pattern, file_name)
            if results:
                if len(args) > 1:
                    numbers = results[0]
                else:
                    numbers = results
                #
                for i, (i_key, i_count) in enumerate(args):
                    new_file_name = new_file_name.replace(
                        numbers[i], i_key, 1
                    )
                return new_file_name, map(int, numbers)

    @classmethod
    def merge_to(cls, file_paths, name_patterns):
        list_ = []
        for i_file_path in file_paths:
            i_file_path = cls.convert_to(i_file_path, name_patterns)
            if i_file_path not in list_:
                list_.append(i_file_path)
        return list_

    @classmethod
    def convert_to(cls, file_path, name_patterns):
        """
        use for convert "/tmp/image.1001.exr" to "/tmp/image.####.exr"
        :param file_path:
        :param name_patterns: list[str, ...]
        etc. *.####.{format}, ext like "exr", "jpg"
        :return:
        """
        file_opt = StgFileOpt(file_path)
        for i_name_pattern in name_patterns:
            i_name_pattern = i_name_pattern.format(
                **dict(format=file_opt.get_format())
            )
            if _cor_pattern.BscFileTiles.is_valid(i_name_pattern):
                i_number_args = StgFileTiles.get_number_args(
                    file_opt.name, i_name_pattern
                )
                if i_number_args:
                    i_file_name, _ = i_number_args
                    i_file_path = '{}/{}'.format(file_opt.directory_path, i_file_name)
                    return i_file_path
        return file_path

    @classmethod
    def to_glob_pattern(cls, name_base):
        if name_base in cls.CACHE:
            return cls.CACHE[name_base]
        #
        name_base_new = name_base
        for i_keyword, i_re_format, i_count in _cor_pattern.BscFileTiles.RE_MULTIPLY_KEYS:
            i_results = re.finditer(i_re_format.format(i_keyword), name_base, re.IGNORECASE) or []
            for j_result in i_results:
                j_start, j_end = j_result.span()
                if i_count == -1:
                    s = cls.P
                else:
                    s = cls.P*i_count
                #
                name_base_new = name_base_new.replace(name_base[j_start:j_end], s, 1)
        cls.CACHE[name_base] = name_base_new
        return name_base_new

    @classmethod
    def get_tiles(cls, file_path):
        if os.path.isfile(file_path):
            return [file_path]

        name_base = os.path.basename(file_path)
        name_base_new = cls.to_glob_pattern(name_base)
        if name_base != name_base_new:
            directory_path = os.path.dirname(file_path)
            glob_pattern = cls.PATHSEP.join([directory_path, name_base_new])
            list_ = StgDirectory.find_file_paths(glob_pattern)
            return list_
        return []

    @classmethod
    def get_is_exists(cls, file_path):
        return not not cls.get_tiles(file_path)


class StgPathOpt(object):
    PATHSEP = '/'

    @classmethod
    def auto_unicode(cls, path):
        if not isinstance(path, six.text_type):
            return path.decode('utf-8')
        return path

    @classmethod
    def ensure_string(cls, s):
        if isinstance(s, six.text_type):
            if six.PY2:
                return s.encode('utf-8')
        elif isinstance(s, six.binary_type):
            if six.PY3:
                return s.decode('utf-8')
        return s

    def __init__(self, path, cleanup=True):
        # auto convert to unicode
        path = self.auto_unicode(path)

        if cleanup is True:
            self._path = _cor_base.BscStorage.clear_pathsep_to(path)
        else:
            self._path = path

        if self.get_is_windows():
            self._root = self._path.split(self.PATHSEP)[0]
        elif self.get_is_linux():
            self._root = self.PATHSEP
        else:
            self._root = '/'

        self.__gui = None

    def get_type_name(self):
        if self.get_is_file():
            return 'file'
        return 'directory'

    type_name = property(get_type_name)

    def get_type(self):
        return self.get_type_name()

    type = property(get_type)

    def get_path(self):
        return self._path

    path = property(get_path)

    def get_name(self):
        return os.path.basename(self.path)

    name = property(get_name)

    def get_root(self):
        return self._root

    root = property(get_root)

    @property
    def normcase_root(self):
        return os.path.normcase(self._root)

    @property
    def normcase_path(self):
        return os.path.normcase(self._path)

    def get_is_windows(self):
        return _cor_base.BscStorage.get_path_is_windows(self.get_path())

    def get_is_linux(self):
        return _cor_base.BscStorage.get_path_is_linux(self.get_path())

    def get_is_exists(self):
        return os.path.exists(self.get_path())

    def get_is_directory(self):
        return os.path.isdir(self.get_path())

    def get_is_file(self):
        return os.path.isfile(self.get_path())

    def show_in_system(self):
        if self.get_path():
            StgExplorer.open(self.get_path())

    def start_in_system(self):
        if self.get_path():
            # must replace '/' to '\\', when path is share like "//nas/test.text"
            os.startfile(self.get_path().replace('/', '\\'))

    def get_mtime(self):
        return os.stat(self._path).st_mtime

    def get_modify_time_tag(self):
        return _cor_time.BscTimestampOpt(
            self.get_mtime()
        ).get_as_tag()

    def get_modify_time(self):
        return _cor_time.BscTimestampOpt(
            self.get_mtime()
        ).get()

    def get_user(self):
        return _cor_base.BscStorage.get_user(self.get_path())

    def get_access_timestamp(self):
        return os.stat(self._path).st_atime

    def get_ctime(self):
        return os.stat(self._path).st_ctime

    def get_timestamp_is_same_to(self, file_path):
        if file_path is not None:
            if self.get_is_exists() is True and self.__class__(file_path).get_is_exists() is True:
                return int(self.get_mtime()) == int(self.__class__(file_path).get_mtime())
            return False
        return False

    def get_is_same_to(self, file_path):
        if file_path is not None:
            if self.get_is_exists() is True and self.__class__(file_path).get_is_exists() is True:
                return self.get_hash_value() == self.__class__(file_path).get_hash_value()
            return False
        return False

    def get_is_readable(self):
        return os.access(self._path, os.R_OK)

    def get_is_writeable(self):
        return os.access(self._path, os.W_OK)

    def get_is_executable(self):
        return os.access(self._path, os.X_OK)

    def map_to_current(self):
        self._path = _cor_base.StgBasePathMapMtd.map_to_current(self._path)
        return self._path

    def set_modify_time(self, timestamp):
        # noinspection PyBroadException
        try:
            os.utime(self.get_path(), (timestamp, timestamp))
        except Exception:
            _cor_base.BscException.set_print()
            bsc_log.Log.trace_error(
                'change modify time failed'
            )

    def get_component_paths(self):
        return _cor_path.BscNodePath.get_dag_component_paths(
            path=self.get_path(), pathsep=self.PATHSEP
        )

    def get_parent_path(self):
        return _cor_path.BscNodePath.get_dag_parent_path(
            path=self.get_path(), pathsep=self.PATHSEP
        )

    def get_ancestor_paths(self):
        return self.get_component_paths()[1:]

    def get_ancestors(self):
        return list(
            map(
                self.__class__, self.get_ancestor_paths()
            )
        )

    def get_path_prettify(self):
        p = self.get_path()
        pathsep = self.PATHSEP
        #
        _ = p.split(pathsep)
        if len(_) > 6:
            if _cor_base.BscStorage.get_path_is_windows(p):
                return six.u('{0}{2}...{2}{1}'.format(pathsep.join(_[:3]), pathsep.join(_[-3:]), pathsep))
            elif _cor_base.BscStorage.get_path_is_linux(p):
                return six.u('{0}{2}...{2}{1}'.format(pathsep.join(_[:2]), pathsep.join(_[-3:]), pathsep))
            return p
        return p

    def set_gui(self, gui):
        self.__gui = gui

    def get_gui(self):
        return self.__gui

    def get_hash_value(self):
        if os.path.isfile(self.get_path()):
            with open(self.get_path(), 'rb') as f:
                # noinspection PyDeprecation
                md5 = hashlib.md5()
                while True:
                    d = f.read(8096)
                    if not d:
                        break
                    md5.update(d)
                f.close()
                return str(md5.hexdigest()).upper()
        return 'D41D8CD98F00B204E9800998ECF8427E'

    def __str__(self):
        return self._path

    def __repr__(self):
        return self._path


class StgFileSearchOpt(object):
    LOG_KEY = 'file search'

    def __init__(self, ignore_name_case=False, ignore_ext_case=False, ignore_ext=False):
        self._ignore_name_case = ignore_name_case
        self._ignore_ext_case = ignore_ext_case
        self._ignore_ext = ignore_ext
        self._search_dict = collections.OrderedDict()

    def set_search_directories(self, directory_paths, recursion_enable=False):
        self._search_dict = collections.OrderedDict()
        for i in directory_paths:
            self.append_search_directory(i, recursion_enable=recursion_enable)
            bsc_log.Log.trace_method_result(
                self.LOG_KEY,
                'append search directory: "{}"'.format(i)
            )
        #
        self._set_key_sort_()

    def append_search_directory(self, directory_path, recursion_enable=False):
        if recursion_enable is True:
            _ = _scan_base.ScanBase.get_all_file_paths(directory_path)
        else:
            _ = StgDirectory.get_file_paths(directory_path)

        for i in _:
            i_directory_path, i_name_base, i_ext = _cor_base.BscStorage.get_file_args(i)
            if self._ignore_name_case is True:
                i_name_base = i_name_base.lower()
            if self._ignore_ext_case is True:
                i_ext = i_ext.lower()
            # noinspection PyBroadException
            try:
                self._search_dict[six.u('{}/{}{}').format(i_directory_path, i_name_base, i_ext)] = i
            except Exception:
                bsc_log.Log.trace_error(
                    six.u('file "{}" is not valid').format(i)
                )
        # sort
        self._set_key_sort_()

    def _set_key_sort_(self):
        self._search_dict = _cor_raw_for_dict.DictMtd.sort_string_key_to(self._search_dict)

    def get_result(self, file_path_src):
        name_src = os.path.basename(file_path_src)
        name_base_src, ext_src = os.path.splitext(name_src)
        name_base_pattern = _cor_pattern.BscFileTiles.to_fnmatch_style(name_base_src)

        if self._ignore_name_case is True:
            name_base_pattern = name_base_pattern.lower()

        if self._ignore_ext_case is True:
            ext_src = ext_src.lower()

        file_path_keys = self._search_dict.keys()

        match_pattern_0 = six.u('*/{}{}').format(name_base_pattern, ext_src)
        matches_0 = fnmatch.filter(
            file_path_keys, match_pattern_0
        )
        if matches_0:
            file_path_tgt = self._search_dict[matches_0[-1]]
            return file_path_tgt
        #
        if self._ignore_ext is True:
            match_pattern_1 = six.u('*/{}.*').format(name_base_pattern)
            matches_1 = fnmatch.filter(
                file_path_keys, match_pattern_1
            )
            if matches_1:
                file_path_tgt = self._search_dict[matches_1[-1]]
                return file_path_tgt


class StgDirectoryOpt(StgPathOpt):
    def __init__(self, path):
        super(StgDirectoryOpt, self).__init__(path)

    def __str__(self):
        return 'directory(path="{}")'.format(self.ensure_string(self._path))

    def __repr__(self):
        return self.__str__()

    def create_dag_fnc(self, path):
        return self.__class__(path)

    def set_create(self):
        _cor_base.BscStorage.create_directory(
            self.path
        )

    def do_create(self):
        _cor_base.BscStorage.create_directory(
            self.path
        )

    def get_file_paths(self, ext_includes=None):
        return StgDirectory.get_file_paths(
            self.path, ext_includes
        )

    def get_files(self, ext_includes=None):
        return list(
            map(
                StgFileOpt, self.get_file_paths(ext_includes)
            )
        )

    def get_all_file_paths(self, ext_includes=None):
        return _scan_base.ScanBase.get_all_file_paths(
            self.path, ext_includes
        )

    def get_all_files(self, ext_includes=None):
        return list(
            map(
                StgFileOpt, self.get_all_file_paths(ext_includes)
            )
        )

    def get_directory_paths(self):
        _ = _scan_base.ScanBase.get_directory_paths(
            self._path
        )
        return _

    def get_directories(self):
        return list(
            map(
                self.__class__, self.get_directory_paths()
            )
        )

    def get_all_directory_paths(self):
        return _scan_base.ScanBase.get_all_directory_paths(
            self._path
        )

    def get_all_directories(self):
        return list(
            map(
                self.__class__, self.get_all_directory_paths()
            )
        )

    def get_all_paths(self):
        return _scan_base.ScanBase.get_all_paths(
            self._path
        )

    def get_all(self):
        return list(
            map(
                lambda x: StgDirectoryOpt(x) if os.path.isdir(x) else StgFileOpt(x), self.get_all_paths()
            )
        )

    def get_child_names(self):
        return os.listdir(self.get_path()) or []

    def copy_all_files_to_directory(self, directory_path_tgt, replace=False):
        directory_path_src = self.path
        file_paths_src = self.get_all_file_paths()

        for index, i_file_path_src in enumerate(file_paths_src):
            i_relative_file_path = i_file_path_src[len(directory_path_src):]
            i_file_path_tgt = directory_path_tgt+i_relative_file_path
            #
            i_file_opt_src = StgFileOpt(i_file_path_src)
            i_file_opt_tgt = StgFileOpt(i_file_path_tgt)
            # create target directory first
            i_file_opt_tgt.create_directory()
            #
            _cor_thread.TrdMethod.do_pool_wait()
            _cor_thread.TrdMethod.set_start(
                i_file_opt_src.copy_to_file, index,
                i_file_path_tgt, replace=replace
            )

    def get_is_exists(self):
        return self.get_is_directory()

    def do_delete(self):
        path = self.get_path()
        if os.path.isdir(path):
            for i_location, _, i_file_names in os.walk(path, topdown=0):
                for j_name in i_file_names:
                    j_file_path = os.path.join(i_location, j_name).replace('\\', '/')
                    # file may not exist?
                    try:
                        os.remove(j_file_path)
                    except WindowsError:
                        pass
                try:
                    os.removedirs(i_location)
                except WindowsError:
                    pass


class StgFileOpt(StgPathOpt):
    def __init__(self, file_path, file_type=None):
        super(StgFileOpt, self).__init__(file_path)
        self._file_type = file_type

    def __str__(self):
        return 'file(path="{}")'.format(self.ensure_string(self._path))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if other is not None:
            if isinstance(other, six.text_type):
                return self._path == other
            elif isinstance(other, self.__class__):
                return self._path == other._path
        return False

    def get_directory_path(self):
        return os.path.dirname(self.path)

    directory_path = property(get_directory_path)

    def get_directory(self):
        return StgDirectoryOpt(self.get_directory_path())

    directory = property(get_directory)

    def get_type(self):
        return self.ext

    type = property(get_type)

    def get_format(self):
        return self.ext[1:]

    format = property(get_format)

    def get_path_base(self):
        return os.path.splitext(self.path)[0]

    @property
    def path_base(self):
        return os.path.splitext(self.path)[0]

    def get_name(self):
        return os.path.basename(self.path)

    name = property(get_name)

    def get_name_base(self):
        return os.path.splitext(os.path.basename(self.path))[0]

    name_base = property(get_name_base)

    def get_ext(self):
        if self._file_type is not None:
            return self._file_type
        return os.path.splitext(self.path)[-1]

    ext = property(get_ext)

    def get_format(self):
        return self.get_ext()[1:]

    def is_name_match_pattern(self, p):
        _ = _cor_pattern.BscFnmatch.filter([self.name], p)
        if _:
            return True
        return False
    
    def is_path_match_pattern(self, p):
        _ = _cor_pattern.BscFnmatch.filter([self.path], p)
        if _:
            return True
        return False

    def set_read(self):
        if os.path.exists(self.path):
            if self.get_ext() in {'.json'}:
                with open(self.path) as j:
                    # noinspection PyTypeChecker
                    raw = json.load(j, object_pairs_hook=collections.OrderedDict)
                    j.close()
                    return raw
            elif self.get_ext() in {'.yml'}:
                with open(self.path) as y:
                    raw = bsc_content.ContentYamlBase.load(y)
                    y.close()
                    return raw
            elif self.ext in {'.jsz'}:
                return StgGzipFileOpt(self._path, '.json').set_read()
            else:
                with open(self.path) as f:
                    raw = f.read()
                    f.close()
                    return raw

    def set_write(self, raw):
        directory = os.path.dirname(self.path)
        if os.path.isdir(directory) is False:
            # noinspection PyBroadException
            try:
                os.makedirs(directory)
            except Exception:
                _cor_base.BscException.set_print()
        if self.ext in {'.json'}:
            with open(self.path, 'w') as j:
                json.dump(
                    raw,
                    j,
                    indent=4
                )
        elif self.ext in {'.yml'}:
            with open(self.path, 'w') as y:
                bsc_content.ContentYamlBase.dump(
                    raw,
                    y,
                    indent=4,
                    default_flow_style=False,
                    allow_unicode=True,
                    # default_style='\'',
                )
        elif self.ext in {'.png'}:
            with open(self.path, 'wb') as f:
                f.write(raw)
        elif self.ext in {'.jsz'}:
            StgGzipFileOpt(self._path, '.json').set_write(raw)
        else:
            with open(self.path, 'w') as f:
                if isinstance(raw, six.text_type):
                    raw = raw.encode('utf-8')
                f.write(raw)

    def append(self, text):
        with open(self.path, 'a+') as f:
            text = _cor_raw.ensure_string(text)
            f.write('{}\n'.format(text))
            f.close()

    def create_directory(self):
        _cor_base.BscStorage.create_directory(
            self.get_directory_path()
        )

    def set_directory_repath_to(self, directory_path_tgt):
        return self.__class__(
            six.u('{}/{}').format(
                directory_path_tgt, self.get_name()
            )
        )

    def set_directory_repath_to_join_uuid(self, directory_path_tgt):
        directory_path_src = self.get_directory_path()
        uuid_key = _cor_base.BscUuid.generate_by_text(directory_path_src)
        return self.__class__(
            six.u('{}/{}/{}').format(
                directory_path_tgt, uuid_key, self.get_name()
            )
        )

    def set_ext_repath_to(self, ext_tgt):
        return self.__class__(
            '{}{}'.format(
                self.get_path_base(), ext_tgt
            )
        )

    def copy_to_file(self, file_path_tgt, replace=False):
        if replace is True:
            if os.path.exists(file_path_tgt):
                os.remove(file_path_tgt)
        #
        file_path_src = self.path
        if file_path_src == file_path_tgt:
            return
        #
        if os.path.exists(file_path_tgt) is False:
            directory_path_tgt = os.path.dirname(file_path_tgt)
            if os.path.exists(directory_path_tgt) is False:
                # noinspection PyBroadException
                try:
                    os.makedirs(directory_path_tgt)
                except Exception:
                    pass
            # noinspection PyBroadException
            try:
                shutil.copy2(file_path_src, file_path_tgt)
            except Exception:
                _cor_base.BscException.set_print()

    def copy_to_directory(self, directory_path_tgt, replace=False):
        file_path_tgt = six.u('{}/{}').format(
            directory_path_tgt, self.name
        )
        self.copy_to_file(
            file_path_tgt, replace=replace
        )
        return file_path_tgt

    def get_render_file_path(self):
        return '{directory}/.temporary/render/{time_tag}.{name_base}{ext}'.format(
            **dict(
                directory=self.get_directory_path(),
                name_base=self.get_name_base(),
                time_tag=self.get_modify_time_tag(),
                ext=self.get_ext()
            )
        )

    def get_size(self):
        if os.path.isfile(self.path):
            return os.path.getsize(self.path)
        return 0

    def get_size_as_gb(self):
        value = self.get_size()
        return value/(1024.0**3)

    def get_tag_as_36(self):
        timestamp = self.get_mtime()
        time_tag = _cor_raw.BscIntegerOpt(int(timestamp*10)).encode_to_36()
        size = self.get_size()
        size_tag = _cor_raw.BscIntegerOpt(int(size)).encode_to_36()
        return '{}{}'.format(time_tag, size_tag)

    @classmethod
    def new_file_fnc(cls):
        pass

    def get_is_exists(self):
        return self.get_is_file()

    def repath_to(self, new_path):
        os.rename(
            self.get_path(), new_path
        )

    def do_delete(self):
        os.remove(
            self.get_path()
        )

    def to_hash_uuid(self):
        return self.hash_to_uuid(
            self.calculate_file_hash(
                self.path
            )
        )
    
    @classmethod
    def hash_to_uuid(cls, hash_value):
        """Convert a hash value (as a hex string) to a UUID."""
        # Use the first 16 bytes (32 hex characters) of the hash value to create a UUID
        return str(uuid.UUID(hash_value[:32])).upper()

    @classmethod
    def calculate_file_hash(cls, file_path, hash_algorithm='md5', chunk_size=4096):
        """Calculate the hash value of a file using the specified hash algorithm."""

        # Create a hash object based on the specified algorithm
        hash_func = hashlib.new(hash_algorithm)

        # Open the file in binary mode and calculate hash
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hash_func.update(chunk)

        # Return the hex digest of the hash
        return hash_func.hexdigest()


# compress
class StgGzipFileOpt(StgFileOpt):
    def __init__(self, *args, **kwargs):
        super(StgGzipFileOpt, self).__init__(*args, **kwargs)

    def set_read(self):
        if self.get_is_file() is True:
            with gzip.GzipFile(
                mode='rb',
                fileobj=open(self.path, 'rb')
            ) as g:
                if self.get_ext() in {'.yml'}:
                    raw = bsc_content.ContentYamlBase.load(g)
                    g.close()
                    return raw
                elif self.get_ext() in {'.json'}:
                    raw = json.load(g, object_pairs_hook=collections.OrderedDict)
                    g.close()
                    return raw

    def set_write(self, raw):
        if os.path.isdir(self.directory_path) is False:
            os.makedirs(self.directory_path)
        # noinspection PyArgumentEqualDefault
        with gzip.GzipFile(
            filename=self.name+self.ext,
            mode='wb',
            compresslevel=9,
            fileobj=open(self.path, 'wb')
        ) as g:
            if self.get_ext() in {'.yml'}:
                bsc_content.ContentYamlBase.dump(
                    raw,
                    g,
                    indent=4,
                    default_flow_style=False,
                )
            elif self.get_ext() in {'.json'}:
                json.dump(
                    raw,
                    g,
                    indent=4
                )


class StgZipFileOpt(StgFileOpt):
    def __init__(self, file_path):
        super(StgZipFileOpt, self).__init__(file_path)

    def get_element_names(self):
        if self.get_is_exists() is True:
            file_path = self.get_path()
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path) as z:
                    return z.namelist()
        return []

    def extract_element_to(self, element_name, element_file_path):
        if self.get_is_exists() is True:
            file_path = self.get_path()
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path) as z:
                    directory_path = os.path.dirname(element_file_path)
                    f = z.extract(element_name, directory_path)
                    os.rename(f, element_file_path)


class StgRarFileOpt(StgFileOpt):
    def __init__(self, file_path):
        super(StgRarFileOpt, self).__init__(file_path)

    def get_element_names(self):
        from unrar import rarfile

        file_path = self.get_path()
        if rarfile.is_rarfile(file_path):
            with rarfile.RarFile(file_path) as r:
                return r.namelist()
        return []

    def extract_element_to(self, element_name, element_file_path):
        from unrar import rarfile

        file_path = self.get_path()
        if rarfile.is_rarfile(file_path):
            with rarfile.RarFile(file_path) as r:
                directory_path = os.path.dirname(element_file_path)
                f = r.extract(element_name, directory_path)
                os.rename(f, element_file_path)

    def extract_all_elements_to(self, directory_path):
        from unrar import rarfile

        file_path = self.get_path()
        if rarfile.is_rarfile(file_path):
            with rarfile.RarFile(file_path) as r:
                r.extractall(directory_path)


class StgPermissionDefaultMtd(object):
    @classmethod
    def create_directory(cls, path, mode):
        StgPath.create_directory(path)

    @classmethod
    def change_mode(cls, path, mode):
        pass

    @classmethod
    def change_owner(cls, path, user='artist', group='artists'):
        pass

    @classmethod
    def lock(cls, path):
        StgSshOpt(
            path
        ).set_just_read_only_for(
            ['cg_group', 'coop_grp']
        )

    @classmethod
    def unlock(cls, path):
        pass

    @classmethod
    def delete(cls, path):
        os.remove(path)

    @classmethod
    def lock_all_directories(cls, path):
        StgSshOpt(
            path
        ).set_just_read_only_for(
            ['cg_group', 'coop_grp']
        )

    @classmethod
    def unlock_all_directories(cls, path):
        pass

    @classmethod
    def lock_all_files(cls, path):
        pass

    @classmethod
    def unlock_all_files(cls, path):
        pass

    @classmethod
    def copy_to_file(cls, file_path_src, file_path_tgt, replace=False):
        StgFileOpt(file_path_src).copy_to_file(
            file_path_tgt, replace=replace
        )


class StgPermissionNewMtd(StgPermissionDefaultMtd):
    @classmethod
    def create_directory(cls, path, mode):
        StgRpc.create_directory(path)

    @classmethod
    def change_mode(cls, path, mode):
        StgRpc.change_mode(path, mode)

    @classmethod
    def change_owner(cls, path, user='artist', group='artists'):
        StgRpc.change_owner(path, user, group)

    @classmethod
    def lock(cls, path):
        StgRpc.change_mode(
            path, '555'
        )

    @classmethod
    def unlock(cls, path):
        StgRpc.change_mode(
            path, '775'
        )

    @classmethod
    def delete(cls, path):
        StgRpc.delete(
            path
        )

    @classmethod
    def lock_all_directories(cls, path):
        StgRpc.change_mode(
            path, '555'
        )
        ds = _scan_base.ScanBase.get_all_directory_paths(
            path
        )
        for i in ds:
            StgRpc.change_mode(
                i, '555'
            )

    @classmethod
    def unlock_all_directories(cls, path):
        StgRpc.change_mode(
            path, '775'
        )
        ds = _scan_base.ScanBase.get_all_directory_paths(
            path
        )
        for i in ds:
            StgRpc.change_mode(
                i, '775'
            )

    @classmethod
    def lock_all_files(cls, path):
        fs = _scan_base.ScanBase.get_all_file_paths(
            path
        )
        for i in fs:
            StgRpc.change_mode(
                i, '555'
            )

    @classmethod
    def unlock_all_files(cls, path):
        StgRpc.change_mode(
            path, '775'
        )
        ds = _scan_base.ScanBase.get_all_file_paths(
            path
        )
        for i in ds:
            StgRpc.change_mode(
                i, '775'
            )

    @classmethod
    def copy_to_file(cls, file_path_src, file_path_tgt, replace=False):
        if StgPermissionBaseMtd.get_scheme(file_path_src) == 'default':
            StgPermissionDefaultMtd.copy_to_file(file_path_src, file_path_tgt)
            cls.change_owner(file_path_tgt)
            cls.change_mode(file_path_tgt, '775')
        else:
            StgRpc.copy_to_file(
                file_path_src, file_path_tgt, replace=replace
            )


class StgPermissionBaseMtd(object):
    SCHEME_MAPPER = dict(
        windows={
            'default': ['l:', 'L:'],
            'new': ['z:', 'Z:', 'x:', 'X:']
        },
        linux={
            'default': ['/l'],
            'new': ['/production', '/job']
        }
    )
    MAP_DICT = {
        i: k for k, v in SCHEME_MAPPER[_cor_base.BscSystem.get_platform()].items() for i in v
    }
    METHOD_DICT = dict(
        default=StgPermissionDefaultMtd,
        new=StgPermissionNewMtd
    )

    @classmethod
    def get_mode(cls, user, group, other):
        query = [
            '---',  # 0
            '--x',  # 1
            '-w-',  # 2
            '-wx',  # 3
            'r--',  # 4
            'r-x',  # 5
            'rw-',  # 6
            'rwx',  # 7
        ]
        return str(query.index(user))+str(query.index(group))+str(query.index(other))

    @classmethod
    def get_scheme(cls, path):
        for k, v in cls.MAP_DICT.items():
            if path.startswith(k+'/'):
                return v
        return 'default'

    @classmethod
    def get_method(cls, path):
        return cls.METHOD_DICT[cls.get_scheme(path)]


class StgPermissionMtd(object):
    def __init__(self, path):
        self._path = path

    @classmethod
    def create_directory(cls, path, mode='775'):
        StgPermissionBaseMtd.get_method(
            path
        ).create_directory(path, mode)

    @classmethod
    def change_owner(cls, path, user='artist', group='artists'):
        StgPermissionBaseMtd.get_method(
            path
        ).change_owner(path, user, group)

    @classmethod
    def change_mode(cls, path, mode):
        StgPermissionBaseMtd.get_method(
            path
        ).change_mode(path, mode)

    @classmethod
    def lock(cls, path):
        StgPermissionBaseMtd.get_method(
            path
        ).lock(path)

    @classmethod
    def unlock(cls, path):
        StgPermissionBaseMtd.get_method(
            path
        ).unlock(path)

    @classmethod
    def delete(cls, path):
        StgPermissionBaseMtd.get_method(
            path
        ).delete(path)

    @classmethod
    def lock_all_directories(cls, path):
        StgPermissionBaseMtd.get_method(
            path
        ).lock_all_directories(path)

    @classmethod
    def unlock_all_directories(cls, path):
        StgPermissionBaseMtd.get_method(
            path
        ).unlock_all_directories(path)

    @classmethod
    def lock_all_files(cls, path):
        StgPermissionBaseMtd.get_method(
            path
        ).lock_all_files(path)

    @classmethod
    def unlock_all_files(cls, path):
        StgPermissionBaseMtd.get_method(
            path
        ).unlock_all_files(path)

    @classmethod
    def copy_to_file(cls, file_path_src, file_path_tgt, replace=False):
        StgPermissionBaseMtd.get_method(
            file_path_tgt
        ).copy_to_file(file_path_src, file_path_tgt, replace)


class StgTextureMtd(object):
    @classmethod
    def get_is_udim(cls, path):
        n = os.path.basename(path)
        return not not re.finditer(r'<udim>', n, re.IGNORECASE)

    @classmethod
    def get_udim_region_args(cls, path):
        d = os.path.dirname(path)
        n = os.path.basename(path)
        if os.path.isfile(path):
            return [(path, '1001')]
        r = re.finditer(r'<udim>', n, re.IGNORECASE) or []
        if r:
            list_ = []
            g_n = p_n = n
            for i_result in r:
                i_start, i_end = i_result.span()
                g_n = g_n.replace(n[i_start:i_end], '[0-9][0-9][0-9][0-9]', 1)
                p_n = p_n.replace(n[i_start:i_end], '{region}', 1)
            g_p = '/'.join([d, g_n])
            p_p = '/'.join([d, p_n])
            results = StgDirectory.find_file_paths(g_p)
            for i_result in results:
                i_p = parse.parse(
                    p_p, i_result
                )
                i_region = i_p['region']
                list_.append((i_result, i_region))
            return list_
        return []

    @classmethod
    def get_unit_paths(cls, path):
        if os.path.isfile(path):
            return [path]
        d = os.path.dirname(path)
        n = os.path.basename(path)
        r = re.finditer(r'<udim>', n, re.IGNORECASE) or []
        if r:
            g_n = n
            for i_result in r:
                i_start, i_end = i_result.span()
                g_n = g_n.replace(n[i_start:i_end], '[0-9][0-9][0-9][0-9]', 1)
            g_p = '/'.join([d, g_n])
            return StgDirectory.find_file_paths(g_p)
        return []


class StgTextureOpt(StgFileOpt):
    def __init__(self, *args, **kwargs):
        super(StgTextureOpt, self).__init__(*args, **kwargs)

    def get_units(self):
        return list(
            map(
                self.__class__, StgTextureMtd.get_unit_paths(self.get_path())
            )
        )

    def get_unit_paths(self):
        return StgTextureMtd.get_unit_paths(self.get_path())

    def get_udim_region_args(self):
        return StgTextureMtd.get_udim_region_args(self.get_path())

# coding:utf-8
import sys

import six

import os

import platform

import copy

import subprocess

import re

import threading

import functools

import lxbasic.log as bsc_log

from . import base as _base

from . import environ as _environ


class PrcBaseMtd(object):
    if platform.system().lower() == 'windows':
        # noinspection PyUnresolvedReferences
        NO_WINDOW = subprocess.STARTUPINFO()
        NO_WINDOW.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    else:
        NO_WINDOW = None

    ENVIRON_MARK = copy.copy(os.environ)

    @classmethod
    def _cmd_cleanup(cls, cmd):
        if platform.system() == 'Windows':
            parts = re.split(r'(".*?"|&&)', cmd)
            for i in range(0, len(parts), 2):
                parts[i] = re.sub(r'&', '^&', parts[i])
            return ''.join(parts)
        elif platform.system() == 'Linux':
            parts = re.split(r'(".*?"|&&)', cmd)
            for i in range(0, len(parts), 2):
                parts[i] = re.sub(r'&', r'\&', parts[i])
            return ''.join(parts)
        else:
            raise RuntimeError()

    @classmethod
    def _windows_trace(cls, text):
        text = text.decode('gbk', 'ignore')
        sys.stdout.write(text.encode('gbk'))

    @classmethod
    def _linux_trace(cls, text):
        text = text.decode('utf-8')
        text = text.replace(u'\u2018', "'").replace(u'\u2019', "'")
        sys.stdout.write(text.encode('utf-8'))

    @classmethod
    def _windows_error_trace(cls, text):
        text = text.decode('gbk', 'ignore')
        sys.stderr.write(text.encode('gbk'))

    @classmethod
    def _linux_error_trace(cls, text):
        text = text.decode('utf-8')
        text = text.replace(u'\u2018', "'").replace(u'\u2019', "'")
        sys.stderr.write(text.encode('utf-8'))

    @classmethod
    def _windows_decode(cls, text):
        return text.decode('gbk', 'ignore')

    @classmethod
    def _linux_decode(cls, text):
        return text.decode('utf-8')

    @classmethod
    def _windows_encode(cls, text):
        return text.encode('gbk')

    @classmethod
    def _linux_encode(cls, text):
        return text.encode('utf-8')

    @classmethod
    def get_environs(cls, **kwargs):
        environs_extend = kwargs.get('environs_extend', {})
        if environs_extend:
            environs_old = dict(os.environ)
            environs = {str(k): str(v) for k, v in environs_old.items()}
            env_opt = _environ.EnvContentOpt(environs)
            for k, v in environs_extend.items():
                if isinstance(v, six.string_types):
                    env_opt.set(
                        k, v
                    )
                    bsc_log.Log.trace_method_result(
                        'sub-process',
                        'environ set: "{}"="{}"'.format(k, v)
                    )
                elif isinstance(v, tuple):
                    i_v, i_opt = v
                    if i_opt == 'set':
                        env_opt.set(
                            k, v
                        )
                        bsc_log.Log.trace_method_result(
                            'sub-process',
                            'environ set: "{}"="{}"'.format(k, v)
                        )
                    elif i_opt == 'append':
                        env_opt.append(
                            k, i_v
                        )
                        bsc_log.Log.trace_method_result(
                            'sub-process',
                            'environ append: "{}"="{}"'.format(k, i_v)
                        )
                    elif i_opt == 'prepend':
                        env_opt.prepend(
                            k, i_v
                        )
                        bsc_log.Log.trace_method_result(
                            'sub-process',
                            'environ prepend: "{}"="{}"'.format(k, i_v)
                        )
            return environs
        return {str(k): str(v) for k, v in dict(os.environ).items()}

    @classmethod
    def get_clear_environs(cls, keys_exclude):
        environs_old = dict(os.environ)
        environs = {k: v for k, v in environs_old.items() if k not in keys_exclude}
        return environs

    @classmethod
    def check_command_clear_environ(cls, cmd):
        # todo, read form configure?

        # ps = [
        #     r'(.*)/paper-bin\s(.*)', r'paper\s(.*)',
        #     r'(.*)/windows/paper\s(.*)'
        # ]
        #
        # # print 'command is', cmd
        # for i_p in ps:
        #     if re.search(i_p, cmd) is not None:
        #         return True
        return False

    @classmethod
    def execute_as_trace(cls, cmd, **kwargs):
        if platform.system() == 'Windows':
            trace_fnc = cls._windows_trace
        elif platform.system() == 'Linux':
            trace_fnc = cls._linux_trace
        else:
            raise RuntimeError()

        clear_environ = kwargs.get('clear_environ', False)
        if clear_environ == 'auto':
            clear_environ = cls.check_command_clear_environ(cmd)
        #
        if clear_environ is True:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW,
                env=dict()
            )
        else:
            environs_extend = kwargs.get('environs_extend', {})
            if environs_extend:
                environs = cls.get_environs(**kwargs)
                s_p = subprocess.Popen(
                    cmd,
                    shell=True,
                    # close_fds=True,
                    universal_newlines=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    startupinfo=cls.NO_WINDOW,
                    env=environs
                )
            else:
                s_p = subprocess.Popen(
                    cmd,
                    shell=True,
                    # close_fds=True,
                    universal_newlines=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    startupinfo=cls.NO_WINDOW,
                )

        while True:
            return_line = s_p.stdout.readline()
            if return_line == '' and s_p.poll() is not None:
                break
            trace_fnc(return_line)

        retcode = s_p.poll()
        if retcode:
            raise subprocess.CalledProcessError(retcode, cmd)

        s_p.stdout.close()

    @classmethod
    def execute_as_trace_use_thread(cls, cmd, **kwargs):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.execute_as_trace,
                cmd=cmd,
                **kwargs
            )
        )
        t_0.start()

    @classmethod
    def execute(cls, cmd):
        s_p = subprocess.Popen(
            cmd,
            shell=True,
            # close_fds=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            startupinfo=cls.NO_WINDOW,
        )
        #
        output, unused_err = s_p.communicate()
        if s_p.returncode != 0:
            for i in output.decode('utf-8').splitlines():
                sys.stderr.write(i+'\n')
            raise subprocess.CalledProcessError(s_p.returncode, cmd)
        s_p.wait()
        return output.decode('utf-8').splitlines()

    @classmethod
    def execute_with_result_in_windows(cls, cmd, **kwargs):
        cmd = re.sub(r'(?<!&)&(?!&)', '^&', cmd)

        clear_environ = kwargs.get('clear_environ', False)
        if clear_environ == 'auto':
            clear_environ = cls.check_command_clear_environ(cmd)

        if clear_environ is True:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW,
                env=dict()
            )
        else:
            environs_extend = kwargs.get('environs_extend', {})
            if environs_extend:
                environs = cls.get_environs(**kwargs)
                s_p = subprocess.Popen(
                    cmd,
                    shell=True,
                    # close_fds=True,
                    universal_newlines=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    startupinfo=cls.NO_WINDOW,
                    env=environs
                )
            else:
                s_p = subprocess.Popen(
                    cmd,
                    shell=True,
                    # close_fds=True,
                    universal_newlines=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    startupinfo=cls.NO_WINDOW,
                )

        while True:
            next_line = s_p.stdout.readline()
            #
            return_line = next_line
            if return_line == '' and s_p.poll() is not None:
                break
            #
            return_line = return_line.decode('gbk', 'ignore')
            # noinspection PyBroadException
            try:
                print(return_line.encode('gbk').rstrip())
            except Exception:
                pass

        retcode = s_p.poll()
        if retcode:
            raise subprocess.CalledProcessError(retcode, cmd)

        s_p.stdout.close()

    @classmethod
    def execute_with_result_in_linux(cls, cmd, **kwargs):
        clear_environ = kwargs.get('clear_environ', False)
        if clear_environ == 'auto':
            clear_environ = cls.check_command_clear_environ(cmd)

        if clear_environ is True:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW,
                env=dict()
            )
        else:
            environs_extend = kwargs.get('environs_extend', {})
            if environs_extend:
                environs = cls.get_environs(**kwargs)
                s_p = subprocess.Popen(
                    cmd,
                    shell=True,
                    # close_fds=True,
                    universal_newlines=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    startupinfo=cls.NO_WINDOW,
                    env=environs
                )
            else:
                s_p = subprocess.Popen(
                    cmd,
                    shell=True,
                    # close_fds=True,
                    universal_newlines=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    startupinfo=cls.NO_WINDOW,
                )

        while True:
            next_line = s_p.stdout.readline()
            #
            return_line = next_line
            if return_line == '' and s_p.poll() is not None:
                break
            #
            return_line = return_line.decode('utf-8', 'ignore')
            return_line = return_line.replace(u'\u2018', "'").replace(u'\u2019', "'")
            # noinspection PyBroadException
            try:
                print(return_line.encode('utf-8').rstrip())
            except Exception:
                pass

        retcode = s_p.poll()
        if retcode:
            raise subprocess.CalledProcessError(retcode, cmd)

        s_p.stdout.close()

    @classmethod
    def execute_with_result(cls, cmd, **kwargs):
        if _base.SysBaseMtd.get_is_windows():
            cls.execute_with_result_in_windows(cmd, **kwargs)
        elif _base.SysBaseMtd.get_is_linux():
            cls.execute_with_result_in_linux(cmd, **kwargs)

    @classmethod
    def set_run(cls, cmd):
        _sp = subprocess.Popen(
            cmd,
            shell=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            startupinfo=cls.NO_WINDOW,
        )
        return _sp

    @classmethod
    def set_run_with_result_use_thread(cls, cmd, **kwargs):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.execute_with_result,
                cmd=cmd,
                **kwargs
            )
        )
        t_0.start()
        # t_0.join()

    @classmethod
    def execute_with_result_use_thread(cls, cmd, **kwargs):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.execute_with_result,
                cmd=cmd,
                **kwargs
            )
        )
        t_0.start()

    @classmethod
    def execute_as_block(cls, cmd, **kwargs):
        if platform.system() == 'Windows':
            decode_fnc = cls._windows_decode
            encode_fnc = cls._windows_encode
        elif platform.system() == 'Linux':
            decode_fnc = cls._linux_decode
            encode_fnc = cls._linux_encode
        else:
            raise RuntimeError()

        clear_environ = kwargs.get('clear_environ', False)
        if clear_environ == 'auto':
            clear_environ = cls.check_command_clear_environ(cmd)
        #
        return_dict = kwargs.get('return_dict', {})
        if clear_environ is True:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW,
                env=dict()
            )
        else:
            s_p = subprocess.Popen(
                cmd,
                shell=True,
                # close_fds=True,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                startupinfo=cls.NO_WINDOW,
            )
        #
        output, unused_err = s_p.communicate()
        #
        if s_p.returncode != 0:
            output = decode_fnc(output)
            output_lines = output.splitlines()
            for i in output_lines:
                if i:
                    sys.stdout.write(encode_fnc(i)+'\n')
            return_dict['results'] = output_lines
            raise subprocess.CalledProcessError(s_p.returncode, cmd)
        #
        s_p.wait()
        return_dict['results'] = output.splitlines()
        return output.splitlines()

    @classmethod
    def execute_use_thread(cls, cmd):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.execute,
                cmd=cmd
            )
        )
        t_0.start()

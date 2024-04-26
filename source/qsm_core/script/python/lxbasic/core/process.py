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
    def _windows_stdout(cls, text):
        text = text.decode('gbk', 'ignore')
        sys.stdout.write(text.encode('gbk'))

    @classmethod
    def _linux_stdout(cls, text):
        text = text.decode('utf-8')
        text = text.replace(u'\u2018', "'").replace(u'\u2019', "'")
        sys.stdout.write(text.encode('utf-8'))
    
    @classmethod
    def get_stdout_fnc(cls):
        if platform.system() == 'Windows':
            return cls._windows_stdout
        elif platform.system() == 'Linux':
            return cls._linux_stdout
        else:
            raise RuntimeError()
    
    @classmethod
    def _windows_stderr(cls, text):
        text = text.decode('gbk', 'ignore')
        sys.stderr.write(text.encode('gbk'))

    @classmethod
    def _linux_stderr(cls, text):
        text = text.decode('utf-8')
        text = text.replace(u'\u2018', "'").replace(u'\u2019', "'")
        sys.stderr.write(text.encode('utf-8'))
    
    @classmethod
    def _get_stderr_fnc(cls):
        if platform.system() == 'Windows':
            return cls._windows_stderr
        elif platform.system() == 'Linux':
            return cls._linux_stderr
        else:
            raise RuntimeError()

    @classmethod
    def _windows_decode_fnc(cls, text):
        return text.decode('gbk', 'ignore')

    @classmethod
    def _linux_decode_fnc(cls, text):
        return text.decode('utf-8')

    @classmethod
    def _windows_encode_fnc(cls, text):
        return text.encode('gbk')

    @classmethod
    def _linux_encode_fnc(cls, text):
        return text.encode('utf-8')

    @classmethod
    def get_decode_fnc(cls):
        if platform.system() == 'Windows':
            return cls._windows_decode_fnc
        elif platform.system() == 'Linux':
            return cls._linux_decode_fnc
        else:
            raise RuntimeError()

    @classmethod
    def get_encode_fnc(cls):
        if platform.system() == 'Windows':
            return cls._windows_encode_fnc
        elif platform.system() == 'Linux':
            return cls._linux_encode_fnc
        else:
            raise RuntimeError()

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
        trace_fnc = cls.get_stdout_fnc()

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
    def execute(cls, cmd, ignore_return_code=None):
        decode_fnc = cls.get_decode_fnc()
        encode_fnc = cls.get_encode_fnc()

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
            if ignore_return_code is not None:
                if s_p.returncode == ignore_return_code:
                    return output.splitlines()
            output = decode_fnc(output)
            output_lines = output.splitlines()
            for i in output_lines:
                if i:
                    sys.stdout.write(encode_fnc(i)+'\n')
            raise subprocess.CalledProcessError(s_p.returncode, cmd)
        s_p.wait()
        return output.splitlines()

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
        decode_fnc = cls.get_decode_fnc()
        encode_fnc = cls.get_encode_fnc()

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
                    sys.stderr.write(encode_fnc(i)+'\n')
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

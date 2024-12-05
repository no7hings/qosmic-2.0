# coding:utf-8
import functools

import sys

import os

import six

import subprocess


class TaskFnc:
    @classmethod
    def generate_fnc(cls, options):
        fnc = options['fnc']
        if fnc == 'symlink':
            return functools.partial(
                Mklink.symlink, **options['kwargs']
            )
        elif fnc == 'copytree':
            return functools.partial(
                XCopy.copytree, **options['kwargs']
            )
        elif fnc == 'sync':
            return functools.partial(
                Extend.sync, **options['kwargs']
            )


class Robocopy:
    """
    /E：复制所有子目录，包括空的子目录。
    /MIR：使目标文件夹完全镜像源文件夹（包括删除多余的文件）。
    /NP：不显示进度。
    /R:3：在遇到错误时重试3次。
    /W:5：每次重试间隔5秒。
    """
    @classmethod
    def generate_copytree_cmd_script(cls, source, target, replace=False):
        if replace is False:
            if os.path.exists(target):
                return
        else:
            # todo: add replace script
            pass

        dir_path = os.path.dirname(target)
        if os.path.exists(dir_path) is False:
            os.makedirs(dir_path)

        cmd_args = [
            'robocopy',
            source.replace('/', '\\'),
            target.replace('/', '\\'),
            '/E',
            '/MIR',
            '/NP'
        ]

        cmd_args = [cmd.encode('mbcs') if isinstance(cmd, six.text_type) else cmd for cmd in cmd_args]
        return ' '.join(cmd_args)

    @classmethod
    def copytree(cls, source, target, replace=False):
        cmd_script = cls.generate_copytree_cmd_script(source, target, replace)
        if cmd_script:
            s_p = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, unused_err = s_p.communicate()
            if s_p.returncode != 0:
                output_lines = output.splitlines()
                for i in output_lines:
                    if i:
                        sys.stdout.write(i+'\n')

                raise subprocess.CalledProcessError(s_p.returncode, cmd_script)


class XCopy:
    """
    /A	仅复制带存档属性的文件，并保留文件的存档属性。
    /M	仅复制带存档属性的文件，并在复制后清除存档属性。
    /D[:日期]	仅复制自指定日期之后更改的文件。如果未提供日期，则复制所有较新的文件。
    /S	复制目录及子目录，但不复制空目录。
    /E	复制目录及其所有子目录，包括空目录。
    /T	仅复制目录结构，不复制文件。如果搭配 /E，则会包含空目录。
    /K	复制文件时保留文件属性（如只读属性）。
    /R	覆盖目标中的只读文件。
    /H	复制隐藏文件和系统文件。
    /C	即使在复制过程中发生错误，仍继续进行。
    /I	如果目标不存在，且目标是目录，则假定目标是目录。
    /Y	覆盖已存在文件时不提示确认。
    /-Y	覆盖已存在文件时提示确认（默认行为）。
    /Q	复制时不显示文件名。
    /F	显示正在复制的文件的完整源和目标路径。
    """
    @classmethod
    def generate_copytree_cmd_script(cls, source, target, replace=False):
        if replace is False:
            if os.path.exists(target):
                return
        else:
            # use /Y
            pass

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
        return cmd_script

    @classmethod
    def copytree(cls, source, target, replace=False):
        cmd_script = cls.generate_copytree_cmd_script(source, target, replace)
        if cmd_script:
            s_p = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, unused_err = s_p.communicate()
            if s_p.returncode != 0:
                output_lines = output.splitlines()
                for i in output_lines:
                    if i:
                        sys.stdout.write(i+'\n')

                raise subprocess.CalledProcessError(s_p.returncode, cmd_script)


class Mklink:
    @classmethod
    def generate_symlink_cmd_script(cls, source, target, replace=False):
        if replace is False:
            if os.path.exists(target):
                return
        else:
            # windows
            if os.path.isdir(target):
                os.removedirs(target)

        dir_path = os.path.dirname(target)
        if os.path.exists(dir_path) is False:
            os.makedirs(dir_path)

        cmd_args = [
            'mklink',
            '/D',
            # link
            '"{}"'.format(target.replace('/', '\\')),
            # source
            '"{}"'.format(source.replace('/', '\\')),
        ]

        cmd_args = [cmd.encode('mbcs') if isinstance(cmd, six.text_type) else cmd for cmd in cmd_args]
        return ' '.join(cmd_args)

    @classmethod
    def symlink(cls, source, target, replace=False):
        cmd_script = cls.generate_symlink_cmd_script(source, target, replace)
        if cmd_script:
            s_p = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, unused_err = s_p.communicate()
            if s_p.returncode != 0:
                output_lines = output.splitlines()
                for i in output_lines:
                    if i:
                        sys.stdout.write(i+'\n')

                raise subprocess.CalledProcessError(s_p.returncode, cmd_script)


class Extend:
    @classmethod
    def sync(cls, source, targets, replace=False):
        for i_target in targets:
            XCopy.copytree(
                source, i_target, replace=replace
            )

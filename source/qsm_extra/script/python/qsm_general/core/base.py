# coding:utf-8
import sys

import os

import getpass

QSM_SCHEME = 'default' if getpass.getuser() == 'nothings' else 'new'

sys.stdout.write(
    'qosmic is initialization, scheme is "{}"\n'.format(QSM_SCHEME)
)


def scheme_is_new():
    return QSM_SCHEME == 'new'


def check_python_lib():
    file_path = 'C:/Windows/System32/python27.dll'
    if os.path.isfile(file_path) is False:
        import lxgui.core as gui_core

        gui_core.GuiDialog.create(
            '错误',
            content=(
                '流程安装错误，缺少文件“{file}”；\n'
                '请使用“\\\\10.33.4.90\\pipeline-root\\startup\\03-copy-python-lib.bat”进行单独安装；\n'
                '也可直接拷贝“\\\\10.33.4.90\\pipeline-root\\startup\\python_lib\\python27.dll”到“{file}”。'
            ).format(file=file_path),
            status=gui_core.GuiDialog.ValidationStatus.Error,
            no_label='关闭',
            ok_visible=False, no_visible=True, cancel_visible=False,
            window_size=(480, 320)
        )
        return False
    return True

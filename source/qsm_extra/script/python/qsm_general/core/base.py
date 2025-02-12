# coding:utf-8
import sys

import os

import getpass

QSM_SCHEME = 'default' if getpass.getuser() == 'nothings' else 'new'

sys.stdout.write(
    'qosmic: scheme is "{}"\n'.format(QSM_SCHEME)
)


def scheme_is_release():
    return QSM_SCHEME == 'new'


class QsmAsset(object):
    """
    this is shit.
    """
    CHARACTER_AND_PROP_ROLE_MASK = ['chr', 'prp']
    CHARACTER_AND_PROP_ROLE_MASK_NEW = ['CHA', 'PROP']

    CHARACTER_ROLE_MASK = ['chr']
    CHARACTER_ROLE_MASK_NEW = ['CHA']

    PROP_ROLE_MASK = ['prp']
    PROP_ROLE_MASK_NEW = ['PROP']

    SCENERY_ROLE_MASK = ['scn']
    SCENERY_ROLE_MASK_NEW = ['SCE']

    @classmethod
    def get_character_and_prop_role_mask(cls):
        if scheme_is_release():
            return cls.CHARACTER_AND_PROP_ROLE_MASK_NEW
        return cls.CHARACTER_AND_PROP_ROLE_MASK

    @classmethod
    def get_character_role_mask(cls):
        if scheme_is_release():
            return cls.CHARACTER_ROLE_MASK_NEW
        return cls.CHARACTER_ROLE_MASK

    @classmethod
    def get_prop_role_mask(cls):
        if scheme_is_release():
            return cls.PROP_ROLE_MASK_NEW
        return cls.PROP_ROLE_MASK

    @classmethod
    def get_scenery_role_mask(cls):
        if scheme_is_release():
            return cls.SCENERY_ROLE_MASK_NEW
        return cls.SCENERY_ROLE_MASK


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
            no_label='Close',
            ok_visible=False, no_visible=True, cancel_visible=False,
            window_size=(480, 320)
        )
        return False
    return True


class MySql(object):
    @classmethod
    def get_options(cls):
        if scheme_is_release():
            return dict(
                user='root',
                password='qosmic',
                host='10.33.4.90',
                port=3306
            )
        return dict(
            user='root',
            password='qosmic',
            host='localhost',
            port=3306
        )

# coding:utf-8
import os.path

from .wrap import *

import lxgui.core as gui_core


class SceneFile:
    @classmethod
    def is_dirty(cls):
        return hou.hipFile.hasUnsavedChanges()

    @classmethod
    def save_to(cls, file_path):
        # create directory
        dir_path = os.path.dirname(file_path)
        if os.path.exists(dir_path) is False:
            os.makedirs(dir_path)
        return hou.hipFile.save(file_path)

    @classmethod
    def get_current(cls):
        return hou.hipFile.path()

    @classmethod
    def open(cls, file_path, add_to_recent=False):
        return hou.hipFile.load(file_path)

    @classmethod
    def increment_and_save_with_dialog(cls, file_path, force=False):
        if cls.is_dirty() is True:
            cls.save_to(file_path)
            return True

        if force is True:
            cls.save_to(file_path)
            return True
        else:
            if gui_core.GuiUtil.language_is_chs():
                gui_core.GuiApplication.exec_message_dialog(
                    '沒有需要保存的更改。',
                    title='加存',
                    size=(320, 120),
                    status='warning',
                )
            else:
                gui_core.GuiApplication.exec_message_dialog(
                    'No changes to save.',
                    title='Increment and Save',
                    size=(320, 120),
                    status='warning',
                )
        return False

    @classmethod
    def open_with_dialog(cls, file_path):
        if cls.is_dirty() is True:
            if gui_core.GuiUtil.language_is_chs():
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'保存修改到: {}?'.format(
                        cls.get_current()
                    ),
                    title='保存文件？',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning'
                )
            else:
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'Save changes to: {}?'.format(
                        cls.get_current()
                    ),
                    title='Save Scene?',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning'
                )

            if result is True:
                cls.save_to(cls.get_current())
                cls.open(file_path, add_to_recent=True)
                return True
            elif result is False:
                cls.open(file_path, add_to_recent=True)
                return True
        else:
            cls.open(file_path, add_to_recent=True)
            return True
        return False

    @classmethod
    def new_with_dialog(cls):
        if cls.is_dirty() is True:
            if gui_core.GuiUtil.language_is_chs():
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'保存修改到: {}?'.format(
                        cls.get_current()
                    ),
                    title='保存文件？',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning',
                )
            else:
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'Save changes to: {}?'.format(
                        cls.get_current()
                    ),
                    title='Save Scene?',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning',
                )
            if result is True:
                cls.save_to(cls.get_current())
                cls.new()
                return True
            elif result is False:
                cls.new()
                return True
        else:
            cls.new()
            return True
        return False

    @classmethod
    def new(cls):
        hou.hipFile.clear(suppress_save_prompt=True)

    @classmethod
    def refresh(cls):
        pass


class Workspace:
    @classmethod
    def create(cls, directory_path):
        pass

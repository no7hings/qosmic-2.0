# coding:utf-8
import os

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core


class SceneFile(object):
    def __init__(self, root_model):
        self._root_model = root_model

        self._default_path = '{}/QSM/scenes/untitled.nxs_prj'.format(bsc_core.BscSystem.get_home_directory())
        self._current_path = self._default_path

        self._current_data = self._root_model.to_data()

    def is_dirty(self):
        return self._root_model.to_data() != self._current_data

    def get_current(self):
        return self._current_path

    def is_default(self):
        return self.get_current() == self._default_path

    def _set_current_path(self, file_path):
        self._current_path = file_path

    def _set_current_data(self, data):
        self._current_data = data

    def save_to(self, file_path):
        data = self._root_model.to_data()
        if data:
            bsc_storage.StgFileOpt(file_path).set_write(data)
            self._set_current_path(file_path)
            self._set_current_data(data)

    def save(self):
        self.save_to(self.get_current())

    def open(self, file_path):
        data = bsc_storage.StgFileOpt(file_path).set_read()
        if data:
            self._root_model.load_from_data(data)
            self._set_current_path(file_path)
            self._set_current_data(data)

    def new(self):
        self._current_path = self._default_path
        return self._root_model.restore()

    def new_with_dialog(self):
        if self.is_dirty() is True:
            if gui_core.GuiUtil.language_is_chs():
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'保存修改到: {}?'.format(
                        self.get_current()
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
                        self.get_current()
                    ),
                    title='Save Scene?',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning',
                )
            if result is True:
                self.save_to(self.get_current())
                self.new()
                return True
            elif result is False:
                self.new()
                return True
        else:
            self.new()
            return True
        return False

    def open_with_dialog(self, file_path):
        if self.is_dirty() is True:
            if gui_core.GuiUtil.language_is_chs():
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'保存修改到: {}?'.format(
                        self.get_current()
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
                        self.get_current()
                    ),
                    title='Save Scene?',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning'
                )

            if result is True:
                self.save_to(self.get_current())
                self.open(file_path)
                return True
            elif result is False:
                self.open(file_path)
                return True
        else:
            self.open(file_path)
            return True
        return False

    def save_as_with_dialog(self, file_path):
        # check file directory is changed, when changed save to.
        if os.path.abspath(file_path) == os.path.abspath(self.get_current()):
            if self.is_dirty() is True:
                self.save_to(file_path)
                return True

            if gui_core.GuiUtil.language_is_chs():
                gui_core.GuiApplication.exec_message_dialog(
                    '沒有需要保存的更改。',
                    title='保存文件',
                    size=(320, 120),
                    status='warning',
                )
            else:
                gui_core.GuiApplication.exec_message_dialog(
                    'No changes to save.',
                    title='Save Scene',
                    size=(320, 120),
                    status='warning',
                )
            return False
        self.save_to(file_path)
        return True

    def save_with_dialog(self):
        self.save_as_with_dialog(self.get_current())

    def close_with_dialog(self):
        if self.is_dirty() is True:
            if gui_core.GuiUtil.language_is_chs():
                result = gui_core.GuiApplication.exec_message_dialog(
                    u'保存修改到: {}?'.format(
                        self.get_current()
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
                        self.get_current()
                    ),
                    title='Save Scene?',
                    show_no=True,
                    show_cancel=True,
                    size=(320, 120),
                    status='warning'
                )
            if result is True:
                self.save_to(self.get_current())
                return True
        return False
# coding:utf-8
import six

import os

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# gui
from .... import core as _gui_core
# qt
from ....qt import core as _qt_core
# qt widgets
from ....qt.widgets import utility as _qt_wgt_utility

from ....qt.widgets.input import input_for_array as _qt_wgt_ipt_for_array
# proxy widgets
from .. import utility as _utility

from . import _input_base


# storage array
class PrxInputForStorageArray(_input_base.AbsPrxInput):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    QT_INPUT_WIDGET_CLS = _qt_wgt_ipt_for_array.QtInputForArray

    def __init__(self, *args, **kwargs):
        super(PrxInputForStorageArray, self).__init__(*args, **kwargs)
        self._history_key = None
        # drop
        self._qt_input_widget._set_input_entry_drop_enable_(True)
        # entry
        self._qt_input_widget._set_entry_enable_(True)
        self._qt_input_widget._set_resize_enable_(True)
        self._qt_input_widget._get_resize_handle_()._set_resize_target_(self._qt_widget)
        self._qt_input_widget._get_resize_handle_()._set_resize_minimum_(42)
        self._qt_input_widget._set_size_policy_height_fixed_mode_()
        self._qt_input_widget._get_entry_widget_()._set_entry_use_as_storage_(True)
        self._qt_input_widget._get_entry_widget_()._set_value_validation_fnc_(self._value_validation_fnc_)
        self._qt_input_widget._get_entry_widget_().entry_value_added.connect(self.update_history)
        self._qt_input_widget._get_choose_popup_widget_()._set_popup_auto_resize_enable_(True)
        self._qt_input_widget._set_value_choose_button_icon_file_path_(
            _gui_core.GuiIcon.get('history')
        )
        self._qt_input_widget._set_choose_button_state_icon_file_path_(
            _gui_core.GuiIcon.get('state/popup')
        )
        self._qt_input_widget._set_value_choose_button_name_text_('choose history')

        self.widget.setFixedHeight(_gui_core.GuiSize.InputHeightA)

        self._ext_filter = 'All File (*.*)'

        self._ext_includes = []

        self._open_button = _utility.PrxIconPressButton()
        self._qt_input_widget._add_input_button_(self._open_button.widget)
        self._open_button.connect_press_clicked_to(self.open_with_dialog_fnc)
        self._open_button.set_name('open file')
        self._open_button.set_icon_name('file/file')
        self._open_button.set_icon_frame_size(18, 18)
        self._open_button.set_tool_tip(
            [
                '"LMB-click" to open file by dialog'
            ]
        )

    def open_with_dialog_fnc(self):
        raise NotImplementedError()

    def set_ext_filter(self, ext_filter):
        self._ext_filter = ext_filter

        self._qt_input_widget._get_entry_widget_()._set_empty_sub_text_(
            self._ext_filter
        )

    def set_ext_includes(self, texts):
        self._ext_includes = texts

        self.set_ext_filter(
            'All File ({})'.format(' '.join(map(lambda x: '*{}'.format(x), texts)))
        )

        self._qt_input_widget._get_entry_widget_()._set_storage_ext_includes_(texts)

    def append(self, value):
        self._qt_input_widget._append_value_(
            value
        )

    def remove(self, value):
        self._qt_input_widget._remove_value_(
            value
        )

    def extend(self, values):
        self._qt_input_widget._extend_values_(
            values
        )

    def set(self, raw=None, **kwargs):
        self._qt_input_widget._set_values_(
            raw
        )

    def get(self):
        return self._qt_input_widget._get_values_()

    def do_clear(self):
        self._qt_input_widget._do_clear_()

    def set_history_key(self, key):
        self._history_key = key
        self.update_history()

    def _value_validation_fnc_(self, value):
        return True

    def update_history(self):
        if self._history_key is not None:
            values = self._qt_input_widget._get_values_()
            if values:
                value = values[-1]
                if value:
                    if self._value_validation_fnc_(value) is True:
                        _gui_core.GuiHistoryStage().append(
                            self._history_key,
                            value
                        )
            #
            histories = _gui_core.GuiHistoryStage().get_all(
                self._history_key
            )
            if histories:
                histories.reverse()
            #
            histories = [i for i in histories if self._value_validation_fnc_(i) is True]
            #
            self._qt_input_widget._set_choose_values_(
                histories
            )

    def pull_history(self):
        if self._history_key is not None:
            _ = _gui_core.GuiHistoryStage().get_latest(self._history_key)
            if _:
                self._qt_input_widget._append_value_(_)

    def set_history_button_visible(self, boolean):
        pass


#   many directories open
# noinspection PyUnusedLocal
class PrxInputForDirectoriesOpen(PrxInputForStorageArray):
    def __init__(self, *args, **kwargs):
        super(PrxInputForDirectoriesOpen, self).__init__(*args, **kwargs)
        self._open_button.set_name('open directory')
        self._open_button.set_icon_name('file/folder')
        self._open_button.set_tool_tip(
            [
                '"LMB-click" to open directory by dialog'
            ]
        )
        self._qt_input_widget._set_choose_popup_item_icon_file_path_(
            _gui_core.GuiIcon.get('file/folder')
        )
        self._qt_input_widget._set_entry_item_icon_file_path_(
            _gui_core.GuiIcon.get('file/folder')
        )
        self.set_history_key(['storage', 'directories-open'])

    def set_locked(self, boolean):
        self._qt_input_widget._set_entry_enable_(not boolean)
        self._qt_input_widget._set_input_entry_drop_enable_(not boolean)
        self._qt_input_widget._set_input_choose_enable_(not boolean)
        self._open_button.widget._set_action_enable_(not boolean)

    def set_history_button_visible(self, boolean):
        self._qt_input_widget._set_input_choose_visible_(boolean)

    def open_with_dialog_fnc(self):
        f = _qt_core.QtWidgets.QFileDialog()
        options = f.Options()
        # options |= f.DontUseNativeDialog
        s = f.getExistingDirectory(
            self.widget,
            'Open Directory',
            self.get()[-1] if self.get() else '',
        )
        if s:
            self.append(s)
            self.update_history()

    def _value_validation_fnc_(self, value):
        if value:
            return os.path.isdir(value)
        return False

    def set(self, *args, **kwargs):
        self._qt_input_widget._clear_all_values_()
        self._qt_input_widget._set_values_(args[0])


#   many files open
class PrxInputForFilesOpen(PrxInputForStorageArray):
    def __init__(self, *args, **kwargs):
        super(PrxInputForFilesOpen, self).__init__(*args, **kwargs)
        self._ext_filter = 'All File (*.*)'
        #
        self._open_button.set_name('open file')
        self._open_button.set_icon_name('file/file')
        self._open_button.set_tool_tip(
            [
                '"LMB-click" to open file by dialog'
            ]
        )
        self._qt_input_widget._set_choose_popup_item_icon_file_path_(
            _gui_core.GuiIcon.get('file/file')
        )
        self._qt_input_widget._set_entry_item_icon_file_path_(
            _gui_core.GuiIcon.get('file/file')
        )
        self._qt_input_widget._get_entry_widget_()._set_entry_use_as_file_(True)
        self._qt_input_widget._get_entry_widget_()._set_entry_use_as_storage_(True)
        self._qt_input_widget._get_entry_widget_()._set_entry_use_as_file_multiply_(True)

    def open_with_dialog_fnc(self):
        f = _qt_core.QtWidgets.QFileDialog()
        # options |= f.DontUseNativeDialog
        # noinspection PyArgumentList
        s = f.getOpenFileNames(
            self.widget,
            'Open Files',
            self.get()[-1] if self.get() else '',
            filter=self._ext_filter
        )
        if s:
            # s = files, filter
            values = s[0]
            if values:
                values = bsc_storage.StgFileTiles.merge_to(
                    values,
                    ['*.<udim>.####.*', '*.####.*']
                )
                self.extend(values)
                self.update_history()

    def _value_validation_fnc_(self, value):
        if value:
            if self._ext_includes:
                ext = os.path.splitext(value)[-1]
                if ext not in self._ext_includes:
                    return False
            return bsc_storage.StgFileTiles.get_is_exists(value)
        return False


#   many medias open
class PrxInputForMediasOpen(PrxInputForFilesOpen):
    def __init__(self, *args, **kwargs):
        super(PrxInputForMediasOpen, self).__init__(*args, **kwargs)
        self._create_button = _utility.PrxIconPressButton()
        self._qt_input_widget._add_input_button_(self._create_button.widget)
        self._create_button.connect_press_clicked_to(self._do_screenshot)
        self._create_button.set_name('create file')
        self._create_button.set_icon_name('camera')
        self._create_button.set_sub_icon_name('action/add')
        self._create_button.set_icon_frame_size(18, 18)
        self._create_button.set_tool_tip(
            [
                '"LMB-click" create file by "screenshot"'
            ]
        )

    @staticmethod
    def _generate_screenshot_file_path():
        d = bsc_core.BscSystem.get_home_directory()
        return six.u('{}/screenshot/untitled-{}.png').format(d, bsc_core.BscSystem.get_time_tag())

    def _do_screenshot_save(self, g):
        f = self._generate_screenshot_file_path()
        _utility.PrxScreenshotFrame.save_to(
            g, f
        )
        self.append(f)
        self.update_history()

    def _do_screenshot(self):
        active_window = _qt_core.QtUtil.get_qt_active_window()
        w = _utility.PrxScreenshotFrame()
        w.connect_started_to(active_window.hide)
        w.do_start()
        w.connect_accepted_to(self._do_screenshot_save)
        w.connect_finished_to(active_window.show)
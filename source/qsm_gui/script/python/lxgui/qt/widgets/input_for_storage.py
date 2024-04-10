# coding=utf-8
import os

import lxbasic.storage as bsc_storage
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts
# qt widgets
from . import base as gui_qt_wgt_base

from . import utility as gui_qt_wgt_utility

from . import bubble as gui_qt_wgt_bubble

from . import button as gui_qt_wgt_button

from . import entry as gui_qt_wgt_entry

from . import popup as gui_qt_wgt_popup


class QtInputAsStorage(
    gui_qt_wgt_entry.QtEntryFrame,
    gui_qt_abstracts.AbsQtInputBaseDef,
    # extra
    #   completion
    gui_qt_abstracts.AbsQtInputCompletionExtraDef,
    #   history
    gui_qt_abstracts.AbsQtInputHistoryExtraDef,
):
    class StorageScheme(object):
        FileOpen = 0x01
        FileSave = 0x02
        DirectoryOpen = 0x03
        DirectorySave = 0x04

        All = [
            FileOpen,
            FileSave,
            DirectoryOpen,
            DirectorySave
        ]

    QT_ENTRY_CLS = gui_qt_wgt_entry.QtEntryAsConstant

    QT_COMPLETION_POPUP_CLS = gui_qt_wgt_popup.QtPopupAsCompletion

    QT_HISTORY_POPUP_CLS = gui_qt_wgt_popup.QtPopupAsHistory

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_history_extend_(self):
        self._history_button.show()
        self._entry_widget._set_value_options_(
            self._get_history_values_()
        )
        if self._get_history_values_():
            self._history_button._set_action_enable_(True)
        else:
            self._history_button._set_action_enable_(False)

    def _pull_history_(self, value):
        self._set_value_(value)

    def __init__(self, *args, **kwargs):
        super(QtInputAsStorage, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(gui_core.GuiSize.InputHeight)

        self._storage_scheme = self.StorageScheme.FileOpen

        self._ext_filter = 'All File (*.*)'

        self._ext_includes = []

        self._init_input_base_def_(self)
        self._init_input_completion_extra_def_(self)
        self._init_input_history_extra_def_(self)

        self._build_input_entry_(self._value_type)

    def _set_ext_includes_(self, texts):
        self._ext_includes = texts

        self._set_ext_filter_(
            'All File ({})'.format(' '.join(map(lambda x: '*{}'.format(x), texts)))
        )

    def _get_ext_includes_(self):
        return self._ext_includes

    def _set_ext_filter_(self, text):
        self._ext_filter = text
        self._input_info_bubble._set_text_(self._ext_filter)
        self._input_info_bubble.setToolTip(
            gui_qt_core.GuiQtUtil.generate_tool_tip_css(
                'ext filter', self._ext_filter
            )
        )

    def _get_ext_filter_(self):
        return self._ext_filter

    def _set_storage_scheme_(self, scheme):
        self._storage_scheme = scheme
        if scheme == self.StorageScheme.FileOpen:
            self._input_button._set_icon_file_path_(gui_core.GuiIcon.get('file/file'))
            self._input_info_bubble.show()
            self._input_info_bubble._set_text_(self._ext_filter)
        elif scheme == self.StorageScheme.FileSave:
            self._input_button._set_icon_file_path_(gui_core.GuiIcon.get('file/file'))
            self._input_button._set_icon_sub_name_('action/save')
            self._input_info_bubble.show()
            self._input_info_bubble._set_text_(self._ext_filter)
        elif scheme == self.StorageScheme.DirectoryOpen:
            self._input_button._set_icon_file_path_(gui_core.GuiIcon.get('file/folder'))
        elif scheme == self.StorageScheme.DirectorySave:
            self._input_button._set_icon_file_path_(gui_core.GuiIcon.get('file/folder'))
            self._input_button._set_icon_sub_name_('action/save')
        else:
            raise RuntimeError()

    def _do_open_file_(self):
        dlg = QtWidgets.QFileDialog()
        options = dlg.Options()
        # options |= dlg.DontUseNativeDialog
        r = dlg.getOpenFileName(
            self,
            'Open File',
            self._get_value_() or '',
            filter=self._ext_filter,
            options=options,
        )
        if r:
            _ = r[0]
            if _:
                value = r[0]
                self._set_value_(value)
                self._push_history_(value)

    def _do_save_file_(self):
        dlg = QtWidgets.QFileDialog()
        options = dlg.Options()
        # options |= dlg.DontUseNativeDialog
        r = dlg.getSaveFileName(
            self,
            'Save File',
            self._get_value_() or '',
            filter=self._ext_filter,
            options=options,
        )
        if r:
            _ = r[0]
            if _:
                value = r[0]
                self._set_value_(value)
                self._push_history_(value)

    def _do_open_directory_(self):
        dlg = QtWidgets.QFileDialog()
        options = dlg.Options()
        # options |= dlg.DontUseNativeDialog
        r = dlg.getExistingDirectory(
            self,
            'Open Directory',
            self._get_value_() or '',
            options=options,
        )
        if r:
            value = r
            self._set_value_(
                value
            )
            self._push_history_(value)

    def _do_save_directory_(self):
        dlg = QtWidgets.QFileDialog()
        options = dlg.Options()
        # options |= dlg.DontUseNativeDialog
        r = dlg.getExistingDirectory(
            self,
            'Save Directory',
            self._get_value_() or '',
            options=options,
        )
        if r:
            value = r
            self._set_value_(
                value
            )
            self._push_history_(value)

    def _do_any_(self):
        if self._storage_scheme == self.StorageScheme.FileOpen:
            self._do_open_file_()
        elif self._storage_scheme == self.StorageScheme.FileSave:
            self._do_save_file_()
        elif self._storage_scheme == self.StorageScheme.DirectoryOpen:
            self._do_open_directory_()
        elif self._storage_scheme == self.StorageScheme.DirectorySave:
            self._do_save_directory_()
        else:
            raise RuntimeError()

    def _update_head_(self):
        p = self._get_value_()
        if p:
            if os.path.isdir(p):
                self._head._set_icon_(
                    gui_qt_core.GuiQtDcc.get_qt_folder_icon(use_system=True)
                )

            elif os.path.isfile(p):
                self._head._set_icon_(
                    gui_qt_core.GuiQtDcc.get_qt_file_icon(p)
                )
            else:
                self._head._set_icon_file_path_(
                    gui_core.GuiIcon.get('empty')
                )

    def _build_input_entry_(self, value_type):
        self._value_type = value_type
        #
        self._entry_frame_widget = self
        #
        main_layout = gui_qt_wgt_base.QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        entry_widget = gui_qt_wgt_utility.QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = gui_qt_wgt_base.QtHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(0)
        #
        self._head = gui_qt_wgt_button.QtIconPressButton()
        entry_layout.addWidget(self._head)
        self._head._set_icon_file_path_(gui_core.GuiIcon.get('empty'))
        # entry
        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_entry_frame_(self)
        self._entry_widget._set_value_type_(self._value_type)
        self._entry_widget._set_entry_enable_(True)
        self._entry_widget._set_entry_use_as_storage_(True)
        self._entry_widget._set_drop_enable_(True)
        self._entry_widget.entry_value_changed.connect(self._update_head_)
        #   connect tab key
        self._entry_widget.user_key_tab_pressed.connect(
            self.user_key_tab_pressed.emit
        )
        #
        self._input_info_bubble = gui_qt_wgt_bubble.QtInfoBubble()
        self._input_info_bubble.hide()
        entry_layout.addWidget(self._input_info_bubble)
        self._input_info_bubble._set_size_mode_(self._input_info_bubble.SizeMode.Fixed)
        self._input_info_bubble.setFixedWidth(64)
        #
        self._input_button_widget = gui_qt_wgt_utility.QtLineWidget()
        self._input_button_widget._set_line_styles_(
            [
                self._input_button_widget.Style.Null,
                self._input_button_widget.Style.Null,
                self._input_button_widget.Style.Solid,
                self._input_button_widget.Style.Null
            ]
        )
        entry_layout.addWidget(self._input_button_widget)
        self._input_button_layout = gui_qt_wgt_base.QtHBoxLayout(self._input_button_widget)
        self._input_button_layout.setContentsMargins(2, 0, 0, 0)
        self._input_button_layout.setSpacing(2)
        #
        self._input_button = gui_qt_wgt_button.QtIconPressButton()
        self._input_button_layout.addWidget(self._input_button)
        self._input_button._set_icon_file_path_(gui_core.GuiIcon.get('file/file'))
        self._input_button._set_icon_frame_draw_size_(18, 18)
        self._input_button.press_clicked.connect(self._do_any_)
        # completion
        self._build_input_completion_()
        self.user_input_completion_value_accepted.connect(self._set_value_)
        self.user_input_completion_value_accepted.connect(self._push_history_)
        self._set_input_completion_buffer_fnc_(
            self._choose_value_completion_gain_fnc_
        )
        self._get_completion_popup_widget_()._set_popup_use_as_storage_(True)
        # history
        self._history_button = gui_qt_wgt_button.QtIconPressButton()
        self._input_button_layout.addWidget(self._history_button)
        self._build_input_history_(self._history_button)

    def _choose_value_completion_gain_fnc_(self, value):
        if value:
            path = bsc_storage.StgPathMtd.clear_pathsep_to(value)
            p = path + '*'
            results = bsc_storage.StgPathMtd.glob_fnc(p)
            if self._storage_scheme in {self.StorageScheme.DirectoryOpen, self.StorageScheme.DirectorySave}:
                return [i for i in results if os.path.isdir(i)]
            return results
        return []

    def _set_entry_enable_(self, boolean):
        super(QtInputAsStorage, self)._set_entry_enable_(boolean)

        self._entry_widget._set_entry_enable_(boolean)
        self._update_background_color_by_locked_(boolean)
        self._input_button._set_action_enable_(boolean)
        #
        self._refresh_widget_all_()

    def _set_value_validation_fnc_(self, fnc):
        self._entry_widget._set_value_validation_fnc_(fnc)

    def _set_input_entry_use_as_storage_(self, boolean):
        self._entry_widget._set_entry_use_as_storage_(boolean)

    def _connect_input_user_entry_value_finished_to_(self, fnc):
        self._entry_widget.user_entry_finished.connect(fnc)

    def _connect_input_entry_value_changed_to_(self, fnc):
        self._entry_widget.entry_value_changed.connect(fnc)

    def _add_input_button_(self, widget):
        self._input_button_layout.addWidget(widget)

    def _create_input_button_(self, name_text, icon_name=None, sub_icon_name=None, tool_tip=None):
        button = gui_qt_wgt_button.QtIconPressButton()
        self._input_button_layout.addWidget(button)
        button._set_name_text_(name_text)
        if icon_name is not None:
            button._set_icon_file_path_(gui_core.GuiIcon.get(icon_name))
        if sub_icon_name is not None:
            button._set_icon_sub_file_path_(gui_core.GuiIcon.get(sub_icon_name))
        if tool_tip:
            button._set_tool_tip_(tool_tip)
        button._set_icon_frame_draw_size_(18, 18)
        return button

    def _clear_input_(self):
        self._restore_all_()
        self.user_input_value_cleared.emit()

    def _restore_all_(self):
        self._choose_values = []

        self._choose_popup_widget._restore_popup_()
        self._entry_widget._clear_input_()

# coding=utf-8
import six

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# gui
from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import abstracts as _qt_abstracts
# qt widgets
from .. import base as _wgt_base

from .. import utility as _wgt_utility

from .. import button as _wgt_button

from .. import entry_frame as _wgt_entry_frame

from ..entry import entry_for_content as _entry_for_content


# input as any content, etc. script, xml, doc
class QtInputForContent(
    _wgt_entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputBaseDef,
):
    def _pull_history_(self, *args, **kwargs):
        pass

    QT_ENTRY_CLS = _entry_for_content.QtEntryForContent

    entry_value_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtInputForContent, self).__init__(*args, **kwargs)
        #
        self._init_input_base_def_(self)
        #
        self._external_editor_ext = '.txt'
        #
        self._external_editor_is_enable = False
        self._external_editor_file_path = None
        #
        self._build_input_entry_(self._value_type)

        # self._frame_background_color = _qt_core.QtRgba.Dark

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type
        #
        main_layout = _wgt_base.QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        #
        entry_widget = _wgt_utility.QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = _wgt_base.QtHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(0)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        self._entry_widget._set_entry_frame_(self)
        # self._entry_widget.setReadOnly(False)
        entry_layout.addWidget(self._entry_widget)
        #
        self._input_button_widget = _wgt_utility.QtLineWidget()
        self._input_button_widget.hide()
        self._input_button_widget._set_line_styles_(
            [self._input_button_widget.Style.Null, self._input_button_widget.Style.Null,
             self._input_button_widget.Style.Solid,
             self._input_button_widget.Style.Null]
        )
        entry_layout.addWidget(self._input_button_widget)
        self._input_button_layout = _wgt_base.QtVBoxLayout(self._input_button_widget)
        self._input_button_layout._set_align_as_top_()
        self._input_button_layout.setContentsMargins(2, 0, 0, 0)
        self._input_button_layout.setSpacing(2)
        #
        self._open_in_external_editor_button = _wgt_button.QtIconToggleButton()
        self._input_button_layout.addWidget(self._open_in_external_editor_button)
        self._open_in_external_editor_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('application/sublime-text')
        )
        self._open_in_external_editor_button._set_name_text_('open in external editor')
        self._open_in_external_editor_button._set_tool_tip_('"LMB-click" to open in external editor')
        self._open_in_external_editor_button.check_toggled.connect(self._start_open_in_external_editor_fnc_)
        #
        self._entry_widget.focus_in.connect(
            self._update_from_external_editor_fnc_
        )
        #
        self._resize_handle.raise_()

    def _get_tmp_text_file_path_(self):
        return six.u('{}/editor/untitled-{}{}').format(
            bsc_core.BscSystem.get_home_directory(),
            bsc_core.BscSystem.get_time_tag(),
            self._external_editor_ext
        )

    def _set_external_editor_ext_(self, ext):
        self._external_editor_ext = ext

    def _update_from_external_editor_fnc_(self):
        if self._external_editor_is_enable is True:
            text = bsc_storage.StgFileOpt(self._external_editor_file_path).set_read()
            self._entry_widget._set_value_(text)

    def _start_open_in_external_editor_fnc_(self, boolean):
        if boolean is True:
            self._external_editor_is_enable = True
            self._external_editor_file_path = self._get_tmp_text_file_path_()
            text = self._entry_widget._get_value_()
            bsc_storage.StgFileOpt(self._external_editor_file_path).set_write(
                text
            )
            import lxbasic.extra.methods as bsc_etr_methods

            bsc_etr_methods.EtrBase.open_ide(self._external_editor_file_path)
        else:
            self._external_editor_is_enable = False
            if self._external_editor_file_path:
                text = bsc_storage.StgFileOpt(self._external_editor_file_path).set_read()
                self._entry_widget._set_value_(text)

    def _set_item_value_entry_enable_(self, boolean):
        self._entry_widget._set_entry_enable_(not boolean)
        if boolean is True:
            self._input_button_widget.show()
        else:
            self._input_button_widget.hide()

    def _set_entry_enable_(self, boolean):
        super(QtInputForContent, self)._set_entry_enable_(boolean)

        self._entry_widget.setReadOnly(not boolean)
        # fixme: not use?
        # self._frame_background_color = [
        #     _qt_core.QtRgba.Dark, _qt_core.QtRgba.Dim
        # ][boolean]
        self._update_background_color_by_locked_(boolean)
        self._refresh_widget_draw_()
        
    def _append_value_(self, text):
        self._entry_widget._append_value_(text)

    def _append_value_use_signal_(self, text):
        self._entry_widget._append_value_use_signal_(text)

    def _set_input_entry_drop_enable_(self, boolean):
        super(QtInputForContent, self)._set_input_entry_drop_enable_(boolean)
        self._frame_border_draw_style = QtCore.Qt.DashLine

    def _set_empty_text_(self, text):
        self._entry_widget._set_empty_text_(text)
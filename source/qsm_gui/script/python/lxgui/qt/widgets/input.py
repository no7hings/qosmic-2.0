# coding=utf-8
import six

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core

from .. import abstracts as gui_qt_abstracts
# qt widgets
from ..widgets import base as gui_qt_wgt_base

from ..widgets import utility as gui_qt_wgt_utility

from ..widgets import bubble as gui_qt_wgt_bubble

from ..widgets import button as gui_qt_wgt_button

from ..widgets import entry as gui_qt_wgt_entry

from ..widgets import entry_extend as gui_qt_wgt_entry_extend

from ..widgets import popup as gui_qt_wgt_popup


# input as any constant, etc. integer, float, string/text/name, ...
class QtInputAsConstant(
    gui_qt_wgt_entry.QtEntryFrame,
    gui_qt_abstracts.AbsQtInputBaseDef,
):
    QT_ENTRY_CLS = gui_qt_wgt_entry.QtEntryAsConstant

    entry_value_changed = qt_signal()

    def _pull_history_(self, value):
        self._entry_widget._set_value_(value)

    def __init__(self, *args, **kwargs):
        super(QtInputAsConstant, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(gui_core.GuiSize.InputHeight)

        self._init_input_base_def_(self)

        self._build_input_entry_(self._value_type)

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type
        #
        entry_layout = gui_qt_wgt_base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(4)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_value_type_(self._value_type)
        self._entry_widget._set_entry_frame_(self)

        self.input_value_change_accepted = self._entry_widget.entry_value_change_accepted

        self._entry_widget.entry_value_change_accepted.connect(self._push_history_)

    def _set_value_entry_validator_use_as_name_(self):
        self._entry_widget._set_validator_use_as_name_()

    def _set_entry_enable_(self, boolean):
        super(QtInputAsConstant, self)._set_entry_enable_(boolean)

        self._entry_widget.setReadOnly(not boolean)

        self._frame_background_color = [
            gui_qt_core.QtBackgroundColors.Basic, gui_qt_core.QtBackgroundColors.Dim
        ][boolean]
        self._refresh_widget_draw_()


# input as any constant entry and choose, etc. enumerate, file open/save, directory open/save, ...
class QtInputAsConstantWithChoose(
    gui_qt_wgt_entry.QtEntryFrame,
    gui_qt_abstracts.AbsQtInputBaseDef,
    # choose
    gui_qt_abstracts.AbsQtInputChooseExtraDef,
    # completion
    gui_qt_abstracts.AbsQtInputCompletionExtraDef,
):
    QT_ENTRY_CLS = gui_qt_wgt_entry.QtEntryAsConstant

    QT_POPUP_CHOOSE_CLS = gui_qt_wgt_popup.QtPopupAsChoose
    QT_COMPLETION_POPUP_CLS = gui_qt_wgt_popup.QtPopupAsCompletion

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_choose_index_(self):
        self._input_info_bubble.hide()
        if self._choose_index_show_enable is True:
            if self._entry_is_enable is True:
                values = self._get_choose_values_()
                if values:
                    self._input_info_bubble.show()
                    maximum = len(values)
                    value_cur = self._get_value_()
                    if value_cur in values:
                        index_cur = values.index(value_cur)+1
                        text = '{}/{}'.format(index_cur, maximum)
                    else:
                        text = str(maximum)
                    #
                    self._input_info_bubble._set_text_(text)

    def __init__(self, *args, **kwargs):
        super(QtInputAsConstantWithChoose, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(gui_core.GuiSize.InputHeight)

        self._init_input_base_def_(self)

        self._init_input_choose_extra_def_(self)
        self._init_input_completion_extra_def_(self)

        self._build_input_entry_(self._value_type)

        self.installEventFilter(self)

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type
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
        # entry
        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_entry_frame_(self)
        self._entry_widget._set_value_type_(self._value_type)
        self._entry_widget._set_entry_enable_(False)
        #   connect tab key
        self._entry_widget.user_key_tab_pressed.connect(
            self.user_key_tab_pressed.emit
        )
        #
        self._input_info_bubble = gui_qt_wgt_bubble.QtInfoBubble()
        self._input_info_bubble.hide()
        entry_layout.addWidget(self._input_info_bubble)
        #
        self._input_button_widget = gui_qt_wgt_utility.QtLineWidget()
        self._input_button_widget._set_line_styles_(
            [self._input_button_widget.Style.Null, self._input_button_widget.Style.Null, self._input_button_widget.Style.Solid,
             self._input_button_widget.Style.Null]
        )
        entry_layout.addWidget(self._input_button_widget)
        self._input_button_layout = gui_qt_wgt_base.QtHBoxLayout(self._input_button_widget)
        self._input_button_layout.setContentsMargins(2, 0, 0, 0)
        self._input_button_layout.setSpacing(2)
        #
        self._input_button = gui_qt_wgt_button.QtIconPressButton()
        self._input_button_layout.addWidget(self._input_button)
        self._input_button._set_icon_file_path_(gui_core.GuiIcon.get('down'))
        self._input_button._set_icon_frame_draw_size_(18, 18)
        self._input_button._set_name_text_('choose value')
        self._input_button._set_tool_tip_('"LMB-click" to choose value from popup view')
        self._input_button.press_clicked.connect(self._do_choose_popup_start_)
        # choose
        self._build_input_choose_()
        self.user_input_choose_value_accepted.connect(self._set_value_)
        self._entry_widget._set_choose_popup_widget_(self._get_choose_popup_widget_())
        # completion
        self._build_input_completion_()
        self.user_input_completion_value_accepted.connect(self._set_value_)
        #
        self._set_input_completion_buffer_fnc_(
            self._choose_value_completion_gain_fnc_
        )

        self._entry_widget.entry_value_changed.connect(self._refresh_choose_index_)

    def _set_entry_enable_(self, boolean):
        super(QtInputAsConstantWithChoose, self)._set_entry_enable_(boolean)

        self._entry_widget._set_entry_enable_(boolean)
        self._input_button.setHidden(not boolean)

        self._update_background_color_by_locked_(boolean)
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

    def _set_value_choose_button_icon_file_path_(self, file_path):
        self._input_button._set_icon_file_path_(file_path)

    def _set_value_choose_button_name_text_(self, text):
        self._input_button._set_name_text_(text)

    def _set_choose_button_state_icon_file_path_(self, file_path):
        self._input_button._set_icon_state_file_path_(file_path)

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

    def _set_choose_values_(self, values, *args, **kwargs):
        super(QtInputAsConstantWithChoose, self)._set_choose_values_(values, *args, **kwargs)
        self._refresh_choose_index_()
        self._get_entry_widget_()._set_value_options_(
            self._get_choose_values_()
        )

    def _extend_choose_values_current_(self, values):
        self._set_value_(values[-1])
        self._refresh_widget_all_()

    def _set_choose_value_by_index_(self, index):
        self._set_value_(
            self._get_choose_values_()[index]
        )

    def _set_choose_value_default_by_index_(self, index):
        self._set_value_default_(
            self._get_choose_value_at_(index)
        )

    def _set_choose_tag_filter_size_(self, w, h):
        pass

    def _clear_input_(self):
        self._restore_all_()
        self.user_input_value_cleared.emit()

    def _restore_all_(self):
        self._input_info_bubble.hide()
        self._choose_values = []

        self._choose_popup_widget._restore_popup_()
        self._entry_widget._clear_input_()

    # choose extra
    def _bridge_choose_get_popup_texts_(self):
        return self._get_choose_values_()

    def _bridge_choose_get_popup_texts_current_(self):
        return [self._get_value_()]


class QtInputAsCapsule(
    QtWidgets.QWidget,

    gui_qt_abstracts.AbsQtInputBaseDef,
):
    QT_ENTRY_CLS = gui_qt_wgt_entry.QtEntryAsCapsule

    def __init__(self, *args, **kwargs):
        super(QtInputAsCapsule, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(gui_core.GuiSize.InputHeight)

        self._init_input_base_def_(self)
        self._build_input_entry_(str)

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type
        #
        entry_layout = gui_qt_wgt_base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(*[1]*4)
        entry_layout.setSpacing(4)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)

        self.input_value_changed = self._entry_widget.value_changed

    def _set_value_options_(self, values):
        self._entry_widget._set_value_options_(values)

    def _set_value_by_index_(self, index):
        self._entry_widget._set_value_by_index_(index)

    def _set_value_type_(self, value_type):
        self._value_type = value_type
        if value_type == str:
            self._entry_widget._set_use_exclusive_(True)
        elif value_type == list:
            self._entry_widget._set_use_exclusive_(False)
        else:
            raise RuntimeError()

    def _set_entry_enable_(self, boolean):
        super(QtInputAsCapsule, self)._set_entry_enable_(boolean)
        self._entry_widget._set_entry_enable_(boolean)


class QtInputAsBubbleWithChoose(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtInputBaseDef,

    gui_qt_abstracts.AbsQtInputChooseExtraDef,
):
    QT_ENTRY_CLS = gui_qt_wgt_entry.QtEntryAsBubble

    QT_POPUP_CHOOSE_CLS = gui_qt_wgt_popup.QtPopupAsChoose

    def _pull_history_(self, value):
        if value in self._choose_values:
            self._entry_widget._set_value_(value)

    def __init__(self, *args, **kwargs):
        super(QtInputAsBubbleWithChoose, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(gui_core.GuiSize.InputHeight)

        self._init_input_base_def_(self)
        self._init_input_choose_extra_def_(self)

        self._build_input_entry_(str)

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type

        entry_layout = gui_qt_wgt_base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(*[1]*4)
        entry_layout.setSpacing(4)

        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)

        self._build_input_choose_()

        self._entry_widget.press_clicked.connect(self._do_choose_popup_start_)
        self.user_input_choose_value_accepted.connect(self._set_value_)
        self.input_value_changed = self._entry_widget.entry_value_changed
        self.input_value_change_accepted = self._entry_widget.entry_value_change_accepted

        self._choose_popup_widget._set_popup_style_(
            self._choose_popup_widget.PopupStyle.FromMouse
        )
        self._choose_popup_widget._set_popup_press_rect_(
            self._entry_widget._get_frame_rect_()
        )

        self._choose_popup_widget.user_popup_value_accepted.connect(self._push_history_)
        self.input_value_change_accepted.connect(self._push_history_)

        self.input_value_change_accepted = self._entry_widget.entry_value_change_accepted

    def _set_choose_values_(self, values, *args, **kwargs):
        super(QtInputAsBubbleWithChoose, self)._set_choose_values_(values, *args, **kwargs)
        self._entry_widget._set_value_options_(values, *args, **kwargs)

    def _bridge_choose_get_popup_texts_(self):
        return self._get_choose_values_()

    def _bridge_choose_get_popup_texts_current_(self):
        return [self._get_value_()]


# input as any content, etc. script, xml, doc
class QtInputAsContent(
    gui_qt_wgt_entry.QtEntryFrame,
    gui_qt_abstracts.AbsQtInputBaseDef,
):
    QT_ENTRY_CLS = gui_qt_wgt_entry.QtEntryAsContent

    entry_value_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtInputAsContent, self).__init__(*args, **kwargs)
        #
        self._init_input_base_def_(self)
        #
        self._external_editor_ext = '.txt'
        #
        self._external_editor_is_enable = False
        self._external_editor_file_path = None
        #
        self._build_input_entry_(self._value_type)

        # self._frame_background_color = gui_qt_core.QtBackgroundColors.Dark

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type
        #
        main_layout = gui_qt_wgt_base.QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        #
        entry_widget = gui_qt_wgt_utility.QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = gui_qt_wgt_base.QtHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(0)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        self._entry_widget._set_entry_frame_(self)
        # self._entry_widget.setReadOnly(False)
        entry_layout.addWidget(self._entry_widget)
        #
        self._input_button_widget = gui_qt_wgt_utility.QtLineWidget()
        self._input_button_widget.hide()
        self._input_button_widget._set_line_styles_(
            [self._input_button_widget.Style.Null, self._input_button_widget.Style.Null, self._input_button_widget.Style.Solid,
             self._input_button_widget.Style.Null]
        )
        entry_layout.addWidget(self._input_button_widget)
        self._input_button_layout = gui_qt_wgt_base.QtVBoxLayout(self._input_button_widget)
        self._input_button_layout._set_align_as_top_()
        self._input_button_layout.setContentsMargins(2, 0, 0, 0)
        self._input_button_layout.setSpacing(2)
        #
        self._open_in_external_editor_button = gui_qt_wgt_button.QtIconEnableButton()
        self._input_button_layout.addWidget(self._open_in_external_editor_button)
        self._open_in_external_editor_button._set_icon_file_path_(
            gui_core.GuiIcon.get('application/sublime-text')
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
            bsc_core.SysBaseMtd.get_home_directory(),
            bsc_core.TimeExtraMtd.generate_time_tag_36(),
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

    def _set_resize_enable_(self, boolean):
        self._resize_handle.setVisible(boolean)

    def _set_entry_enable_(self, boolean):
        super(QtInputAsContent, self)._set_entry_enable_(boolean)

        self._entry_widget.setReadOnly(not boolean)
        # self._frame_background_color = [
        #     gui_qt_core.QtBackgroundColors.Basic, gui_qt_core.QtBackgroundColors.Dim
        # ][boolean]
        # self._refresh_widget_draw_()

    def _set_input_entry_drop_enable_(self, boolean):
        super(QtInputAsContent, self)._set_input_entry_drop_enable_(boolean)
        self._frame_border_draw_style = QtCore.Qt.DashLine

    def _set_empty_text_(self, text):
        self._entry_widget._set_empty_text_(text)


# input as any list
class QtInputAsList(
    gui_qt_wgt_entry.QtEntryFrame,
    gui_qt_abstracts.AbsQtInputBaseDef,
    # extra
    #   choose
    gui_qt_abstracts.AbsQtInputChooseExtraDef,
):
    QT_ENTRY_CLS = gui_qt_wgt_entry.QtEntryAsList
    #
    QT_POPUP_CHOOSE_CLS = gui_qt_wgt_popup.QtPopupAsChoose
    #
    add_press_clicked = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtInputAsList, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._init_input_base_def_(self)
        self._init_input_choose_extra_def_(self)
        #
        self._build_input_entry_(str)
        self._set_choose_popup_item_multiply_enable_(True)

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type
        #
        main_layout = gui_qt_wgt_base.QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        #
        entry_widget = gui_qt_wgt_utility.QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = gui_qt_wgt_base.QtHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(0)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_entry_frame_(self)
        #
        self._input_button_widget = gui_qt_wgt_utility.QtLineWidget()
        self._input_button_widget._set_line_styles_(
            [self._input_button_widget.Style.Null, self._input_button_widget.Style.Null, self._input_button_widget.Style.Solid,
             self._input_button_widget.Style.Null]
        )
        entry_layout.addWidget(self._input_button_widget)
        self._input_button_layout = gui_qt_wgt_base.QtVBoxLayout(self._input_button_widget)
        self._input_button_layout._set_align_as_top_()
        self._input_button_layout.setContentsMargins(2, 0, 0, 0)
        self._input_button_layout.setSpacing(2)

        self._input_button = gui_qt_wgt_button.QtIconPressButton()
        self._input_button_layout.addWidget(self._input_button)
        self._input_button._set_icon_file_path_(gui_core.GuiIcon.get('file/file'))
        self._input_button._set_icon_state_name_('state/popup')
        self._input_button._set_icon_frame_draw_size_(18, 18)
        self._input_button._set_name_text_('choose value')
        self._input_button._set_tool_tip_('"LMB-click" to choose value from popup view')
        self._input_button.press_clicked.connect(self._do_choose_popup_start_)
        # choose
        self._build_input_choose_()
        self.user_input_choose_values_accepted.connect(self._extend_choose_values_current_)
        #
        self._resize_handle.raise_()

    def _set_entry_enable_(self, boolean):
        super(QtInputAsList, self)._set_entry_enable_(boolean)
        self._entry_widget._set_entry_enable_(boolean)
        self._update_background_color_by_locked_(boolean)
        self._refresh_widget_draw_()

    def _set_input_entry_drop_enable_(self, boolean):
        super(QtInputAsList, self)._set_input_entry_drop_enable_(boolean)
        self._frame_border_draw_style = QtCore.Qt.DashLine

    def _set_input_choose_enable_(self, boolean):
        self._input_button._set_action_enable_(boolean)

    def _set_input_choose_visible_(self, boolean):
        self._input_button._set_visible_(boolean)

    def _set_values_append_fnc_(self, fnc):
        pass

    def _append_value_(self, value):
        self._entry_widget._append_value_(value)

    def _extend_values_(self, values):
        self._entry_widget._extend_values_(values)

    def _set_values_(self, values):
        self._entry_widget._set_values_(values)

    def _get_values_(self):
        return self._entry_widget._get_values_()

    def _set_clear_(self):
        self._clear_all_values_()

    def _clear_all_values_(self):
        self._entry_widget._clear_all_values_()

    def _set_entry_item_icon_file_path_(self, file_path):
        self._entry_widget._set_item_icon_file_path_(file_path)

    def _add_input_button_(self, widget):
        self._input_button_layout.addWidget(widget)

    def _create_input_button_(self, name_text, icon_name=None, sub_icon_name=None):
        button = gui_qt_wgt_button.QtIconPressButton()
        self._input_button_layout.addWidget(button)
        button._set_name_text_(name_text)
        if icon_name is not None:
            button._set_icon_file_path_(gui_core.GuiIcon.get(icon_name))
        if sub_icon_name is not None:
            button._set_icon_sub_file_path_(gui_core.GuiIcon.get(sub_icon_name))
        button._set_icon_frame_draw_size_(18, 18)
        return button

    def _set_input_entry_use_as_storage_(self, boolean):
        self._entry_widget._set_entry_use_as_storage_(boolean)

    def _set_value_choose_button_icon_file_path_(self, file_path):
        self._input_button._set_icon_file_path_(file_path)

    def _set_value_choose_button_name_text_(self, text):
        self._input_button._set_name_text_(text)

    def _set_choose_button_state_icon_file_path_(self, file_path):
        self._input_button._set_icon_state_file_path_(file_path)

    # choose
    def _extend_choose_values_current_(self, values):
        self._extend_values_(values)

    def _set_empty_icon_name_(self, text):
        self._entry_widget._set_empty_icon_name_(text)

    def _set_empty_text_(self, text):
        self._entry_widget._set_empty_text_(text)

    # choose extra
    def _bridge_choose_get_popup_texts_(self):
        return self._get_choose_values_()

    def _bridge_choose_get_popup_texts_current_(self):
        return self._get_values_()


# input as any list with choose
class QtInputAsListWithChoose(
    gui_qt_wgt_entry.QtEntryFrame,
    gui_qt_abstracts.AbsQtInputBaseDef,
    # extra
    #   choose
    gui_qt_abstracts.AbsQtInputChooseExtraDef,
):
    QT_ENTRY_CLS = gui_qt_wgt_entry.QtEntryAsList
    QT_POPUP_CHOOSE_CLS = gui_qt_wgt_popup.QtPopupAsChoose
    #
    add_press_clicked = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtInputAsListWithChoose, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        #
        self._init_input_base_def_(self)
        self._init_input_choose_extra_def_(self)
        #
        self._build_input_entry_(str)
        self._set_choose_popup_item_multiply_enable_(True)

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type

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
        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_entry_frame_(self)
        #
        self._input_button_widget = gui_qt_wgt_utility.QtLineWidget()
        self._input_button_widget._set_line_styles_(
            [self._input_button_widget.Style.Null, self._input_button_widget.Style.Null, self._input_button_widget.Style.Solid,
             self._input_button_widget.Style.Null]
        )
        entry_layout.addWidget(self._input_button_widget)
        self._input_button_layout = gui_qt_wgt_base.QtVBoxLayout(self._input_button_widget)
        self._input_button_layout._set_align_as_top_()
        self._input_button_layout.setContentsMargins(2, 0, 0, 0)
        self._input_button_layout.setSpacing(2)

        self._input_button = gui_qt_wgt_button.QtIconPressButton()
        self._input_button_layout.addWidget(self._input_button)
        self._input_button._set_icon_file_path_(gui_core.GuiIcon.get('file/file'))
        self._input_button._set_icon_state_name_('state/popup')
        self._input_button._set_icon_frame_draw_size_(18, 18)
        self._input_button._set_name_text_('choose value')
        self._input_button._set_tool_tip_('"LMB-click" to choose value from popup view')
        self._input_button.press_clicked.connect(self._do_choose_popup_start_)
        # choose
        self._build_input_choose_()
        self.user_input_choose_values_accepted.connect(self._extend_choose_values_current_)
        #
        self._resize_handle.raise_()

    def _set_entry_enable_(self, boolean):
        super(QtInputAsListWithChoose, self)._set_entry_enable_(boolean)

        self._entry_widget._set_entry_enable_(boolean)
        self._update_background_color_by_locked_(boolean)
        self._refresh_widget_draw_()

    def _set_input_choose_enable_(self, boolean):
        self._input_button._set_action_enable_(boolean)

    def _set_input_choose_visible_(self, boolean):
        self._input_button._set_visible_(boolean)

    def _set_values_append_fnc_(self, fnc):
        pass

    def _append_value_(self, value):
        self._entry_widget._append_value_(value)

    def _extend_values_(self, values):
        self._entry_widget._extend_values_(values)

    def _set_values_(self, values):
        self._entry_widget._set_values_(values)

    def _get_values_(self):
        return self._entry_widget._get_values_()

    def _clear_all_values_(self):
        self._entry_widget._clear_all_values_()

    def _set_entry_item_icon_file_path_(self, file_path):
        self._entry_widget._set_item_icon_file_path_(file_path)

    def _add_input_button_(self, widget):
        self._input_button_layout.addWidget(widget)

    def _create_input_button_(self, name_text, icon_name=None, sub_icon_name=None):
        button = gui_qt_wgt_button.QtIconPressButton()
        self._input_button_layout.addWidget(button)
        button._set_name_text_(name_text)
        if icon_name is not None:
            button._set_icon_file_path_(gui_core.GuiIcon.get(icon_name))
        if sub_icon_name is not None:
            button._set_icon_sub_file_path_(gui_core.GuiIcon.get(sub_icon_name))
        button._set_icon_frame_draw_size_(18, 18)
        return button

    def _set_input_entry_use_as_storage_(self, boolean):
        self._entry_widget._set_entry_use_as_storage_(boolean)

    def _set_value_choose_button_icon_file_path_(self, file_path):
        self._input_button._set_icon_file_path_(file_path)

    def _set_value_choose_button_name_text_(self, text):
        self._input_button._set_name_text_(text)

    def _set_choose_button_state_icon_file_path_(self, file_path):
        self._input_button._set_icon_state_file_path_(file_path)

    def _extend_choose_values_current_(self, values):
        self._extend_values_(values)

    # choose extra
    def _bridge_choose_get_popup_texts_(self):
        return self._get_choose_values_()

    def _bridge_choose_get_popup_texts_current_(self):
        return self._get_values_()


# path
class QtInputAsPath(
    gui_qt_wgt_entry.QtEntryFrame,
    gui_qt_abstracts.AbsQtInputBaseDef,
    # extra
    #   choose
    gui_qt_abstracts.AbsQtInputChooseExtraDef,
    #   completion
    gui_qt_abstracts.AbsQtInputCompletionExtraDef,
    #   history
    gui_qt_abstracts.AbsQtInputHistoryExtraDef
):
    input_value_change_accepted = qt_signal(str)
    user_input_value_change_accepted = qt_signal(str)

    input_entry_key_enter_press = qt_signal()

    user_input_entry_finished = qt_signal()

    QT_ENTRY_EXTEND_CLS = gui_qt_wgt_entry_extend.QtEntryExtendAsPath

    QT_COMPLETION_POPUP_CLS = gui_qt_wgt_popup.QtPopupAsCompletion

    QT_POPUP_CHOOSE_CLS = gui_qt_wgt_popup.QtPopupAsChoose

    QT_HISTORY_POPUP_CLS = gui_qt_wgt_popup.QtPopupAsHistory

    def _pull_history_(self, value):
        self._set_value_(value)

    def _refresh_history_extend_(self):
        self._history_button.show()
        if self._get_history_values_():
            self._history_button._set_action_enable_(True)
        else:
            self._history_button._set_action_enable_(False)

    def __init__(self, *args, **kwargs):
        super(QtInputAsPath, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(gui_core.GuiSize.InputHeight)

        self._init_input_base_def_(self)
        # extra
        self._init_input_choose_extra_def_(self)
        self._init_input_completion_extra_def_(self)
        self._init_input_history_extra_def_(self)

        self.__buffer_fnc = lambda x: {}
        self.__buffer_cache = {}

        self._build_input_entry_()

        self._index_thread_batch = 0

    def _build_input_entry_(self):
        self._entry_frame_widget = self

        entry_layout = gui_qt_wgt_base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(4)

        self._entry_extend_widget = self.QT_ENTRY_EXTEND_CLS()
        entry_layout.addWidget(self._entry_extend_widget)
        self._entry_widget = self._entry_extend_widget._get_entry_widget_()
        self._entry_widget._set_entry_frame_(self)
        self._entry_extend_widget.next_index_accepted.connect(self._update_next_cbk_)
        self.user_input_entry_finished = self._entry_widget.user_entry_finished

        self._history_button = gui_qt_wgt_button.QtIconPressButton()
        entry_layout.addWidget(self._history_button)
        # choose
        self._build_input_choose_()
        self._entry_extend_widget.next_press_clicked.connect(self._do_choose_popup_start_)
        self.user_input_choose_value_accepted.connect(self._entry_extend_widget._enter_next_)
        self._entry_widget._set_choose_popup_widget_(self._get_choose_popup_widget_())
        self._entry_extend_widget.entry_value_changed.connect(
            self._choose_popup_widget._do_popup_close_
        )
        # completion
        self._build_input_completion_()
        self.user_input_completion_value_accepted.connect(self._entry_extend_widget._enter_next_)
        self._set_input_completion_buffer_fnc_(
            self._entry_extend_widget._get_matched_next_name_texts_
        )
        self._entry_extend_widget.entry_value_changed.connect(
            self._completion_popup_widget._do_popup_close_
        )
        # history
        self._build_input_history_(self._history_button)
        self._entry_extend_widget.entry_value_change_accepted.connect(self._push_history_)

        self.input_value_changed = self._entry_extend_widget.entry_value_changed
        self.input_value_change_accepted = self._entry_extend_widget.entry_value_change_accepted
        self.user_input_value_change_accepted = self._entry_extend_widget.user_entry_value_change_accepted

    def _set_buffer_fnc_(self, fnc):
        self.__buffer_fnc = fnc

    def _update_next_cbk_(self, path):
        def cache_fnc_():
            _key = path.to_string()
            if _key in self.__buffer_cache:
                return [self._index_thread_batch, self.__buffer_cache[_key]]

            _data = self.__buffer_fnc(path)
            self.__buffer_cache[_key] = _data
            return [self._index_thread_batch, _data]

        def build_fnc_(*args):
            _index_thread_batch_current, _dict = args[0]

            if _index_thread_batch_current != self._index_thread_batch:
                return

            if _dict:
                self._entry_extend_widget._set_next_name_texts_(
                    _dict.get('names') or []
                )
                self._set_choose_popup_item_image_url_dict_(
                    _dict.get('image_url_dict') or {}
                )
                self._set_choose_popup_item_keyword_filter_dict_(
                    _dict.get('keyword_filter_dict') or {}
                )
                self._set_choose_popup_item_tag_filter_dict_(
                    _dict.get('tag_filter_dict') or {}
                )

        def post_fnc_():
            self._entry_extend_widget._do_next_wait_end_()

        self._index_thread_batch += 1

        # thread only use when widget is show
        if self.isVisible() is True:
            self._entry_extend_widget._do_next_wait_start_()
            self._run_build_use_thread_(cache_fnc_, build_fnc_, post_fnc_)
        else:
            build_fnc_(cache_fnc_())
            post_fnc_()

    def _update_next_(self):
        self._entry_extend_widget._update_next_()

    def _set_value_(self, value):
        self._entry_extend_widget._set_path_text_(value)

    def _get_value_(self):
        return self._entry_extend_widget._get_path_text_()

    def _accept_element_(self, value):
        pass

    def _setup_(self):
        self._entry_extend_widget._update_next_()

    def _restore_buffer_cache_(self):
        self.__buffer_cache = {}

    def _get_buffer_cache_(self):
        return self.__buffer_cache

    # choose extra
    def _bridge_choose_get_popup_texts_(self):
        return self._entry_extend_widget._get_next_name_texts_()

    def _bridge_choose_get_popup_texts_current_(self):
        return [self._entry_widget._get_value_()]


# rgba entry and choose
class QtInputAsRgba(
    gui_qt_wgt_entry.QtEntryFrame,
    gui_qt_abstracts.AbsQtInputAsOtherBaseDef,
    # extra
    #   choose
    gui_qt_abstracts.AbsQtInputChooseExtraDef,

    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForHoverDef,
    gui_qt_abstracts.AbsQtActionForPressDef,

    gui_qt_abstracts.AbsQtValueDefaultExtraDef,
):
    QT_ENTRY_CLS = gui_qt_wgt_entry.QtEntryAsConstant

    QT_POPUP_CHOOSE_CLS = gui_qt_wgt_popup.QtPopupAsChooseForRgba

    def _refresh_widget_draw_geometry_(self):
        super(QtInputAsRgba, self)._refresh_widget_draw_geometry_()
        #
        x, y = 0, 0
        w = h = self.height()
        c_w, c_h = w, h
        v_w, v_h = self._value_draw_width, self._value_draw_height
        self._value_rect.setRect(
            x, y, c_w, c_h
        )
        self._value_draw_rect.setRect(
            x+(c_w-v_w)/2, y+(c_h-v_h)/2, v_w, v_h
        )

    def __init__(self, *args, **kwargs):
        super(QtInputAsRgba, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(gui_core.GuiSize.InputHeight)

        self._init_input_choose_extra_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

        self._init_input_as_other_base_def_(self)
        self._init_value_default_extra_def_(self)

        self._build_input_entry_()

    def _get_value_rect_(self):
        return self._value_rect

    def _build_input_entry_(self):
        self._entry_frame_widget = self

        entry_layout = gui_qt_wgt_base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(self._value_draw_width+2, 0, 0, 0)
        entry_layout.setSpacing(2)

        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_value_type_(str)
        self._entry_widget._set_entry_use_as_rgba_255_(True)
        self._entry_widget.user_entry_finished.connect(self._refresh_widget_draw_)

        self._build_input_choose_()

    def eventFilter(self, *args):
        super(QtInputAsRgba, self).eventFilter(*args)

        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._entry_is_enable is True:
                        if self._value_rect.contains(event.pos()):
                            self._set_action_flag_(self.ActionFlag.ChoosePress)

                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_is_match_(
                        self.ActionFlag.ChoosePress
                    ) is True:
                        self.press_clicked.emit()
                        self._do_choose_popup_start_()

                self._clear_all_action_flags_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
        return False

    def paintEvent(self, event):
        super(QtInputAsRgba, self).paintEvent(self)
        #
        painter = gui_qt_core.QtPainter(self)

        rgba = self._get_value_()
        offset = self._get_action_offset_()
        painter._draw_frame_by_rect_(
            self._value_draw_rect,
            border_color=gui_qt_core.QtBorderColors.Transparent,
            background_color=rgba,
            offset=offset
        )

    def _build_input_choose_(self):
        self._choose_popup_widget = self.QT_POPUP_CHOOSE_CLS(self)
        self._choose_popup_widget._set_entry_widget_(self._get_entry_widget_())
        self._choose_popup_widget._set_entry_frame_widget_(self._get_entry_frame_widget_())
        self._choose_popup_widget.hide()

    def _set_entry_enable_(self, boolean):
        super(QtInputAsRgba, self)._set_entry_enable_(boolean)

        self._entry_widget._set_entry_enable_(boolean)

        self._update_background_color_by_locked_(boolean)
        #
        self._refresh_widget_all_()

    def _set_value_(self, value):
        self._entry_widget._set_value_as_rgba_255_(value)

    def _get_value_(self):
        return self._entry_widget._get_value_as_rgba_255_()


# icon entry and choose
class QtInputAsIcon(
    gui_qt_wgt_entry.QtEntryFrame,
    gui_qt_abstracts.AbsQtInputAsOtherBaseDef,
    # extra
    #   choose
    gui_qt_abstracts.AbsQtInputChooseExtraDef,

    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForHoverDef,
    gui_qt_abstracts.AbsQtActionForPressDef,
):
    QT_ENTRY_CLS = gui_qt_wgt_entry.QtEntryAsConstant

    QT_POPUP_CHOOSE_CLS = gui_qt_wgt_popup.QtPopupAsChooseForIcon

    def _refresh_widget_draw_geometry_(self):
        super(QtInputAsIcon, self)._refresh_widget_draw_geometry_()

        x, y = 0, 0
        w = h = self.height()
        c_w, c_h = w, h
        v_w, v_h = self._value_draw_width, self._value_draw_height
        self._value_rect.setRect(
            x, y, c_w, c_h
        )
        self._value_draw_rect.setRect(
            x+(c_w-v_w)/2, y+(c_h-v_h)/2, v_w, v_h
        )

    def __init__(self, *args, **kwargs):
        super(QtInputAsIcon, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(gui_core.GuiSize.InputHeight)

        self._init_input_as_other_base_def_(self)
        self._init_input_choose_extra_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

        self._build_input_entry_()

    def eventFilter(self, *args):
        super(QtInputAsIcon, self).eventFilter(*args)

        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._entry_is_enable is True:
                        if self._value_rect.contains(event.pos()):
                            self._set_action_flag_(self.ActionFlag.ChoosePress)

                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._get_action_flag_is_match_(
                        self.ActionFlag.ChoosePress
                    ) is True:
                        self.press_clicked.emit()
                        self._do_choose_popup_start_()

                self._clear_all_action_flags_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
        return False

    def paintEvent(self, event):
        super(QtInputAsIcon, self).paintEvent(self)
        #
        painter = gui_qt_core.QtPainter(self)

        icon_name = self._get_value_()
        if icon_name == '':
            icon_name = 'state-disable'

        icon_file_path = gui_core.GuiIcon.get(icon_name)
        if icon_file_path:
            offset = self._get_action_offset_()

            painter._draw_icon_file_by_rect_(
                rect=self._value_draw_rect,
                file_path=icon_file_path,
                offset=offset
            )

    def _build_input_entry_(self):
        self._entry_frame_widget = self

        entry_layout = gui_qt_wgt_base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(self._value_draw_width+2, 0, 0, 0)
        entry_layout.setSpacing(2)

        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_value_type_(str)
        self._entry_widget.user_entry_finished.connect(self._refresh_widget_draw_)

        self._build_input_choose_()

    def _build_input_choose_(self):
        self._choose_popup_widget = self.QT_POPUP_CHOOSE_CLS(self)
        self._choose_popup_widget._set_entry_widget_(self._get_entry_widget_())
        self._choose_popup_widget._set_entry_frame_widget_(self._get_entry_frame_widget_())
        self._choose_popup_widget.hide()

        self._choose_popup_widget.user_popup_value_accepted.connect(
            self._do_choose_accept_
        )

    def _do_choose_accept_(self, text):
        self._set_value_(text)
        self._refresh_widget_draw_()

    def _set_entry_enable_(self, boolean):
        super(QtInputAsIcon, self)._set_entry_enable_(boolean)

        self._entry_widget._set_entry_enable_(boolean)

        self._update_background_color_by_locked_(boolean)
        #
        self._refresh_widget_all_()

    # choose extra
    def _bridge_choose_get_popup_texts_(self):
        return self._get_choose_values_()

    def _bridge_choose_get_popup_texts_current_(self):
        return [self._get_value_()]


# any tuple, etc. float2, float3, ...
class QtInputAsTuple(
    gui_qt_wgt_entry.QtEntryFrame,
    gui_qt_abstracts.AbsQtInputAsComponentsBaseDef,
):
    QT_ENTRY_CLS = gui_qt_wgt_entry.QtEntryAsConstant

    entry_value_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtInputAsTuple, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(gui_core.GuiSize.InputHeight)

        self._init_input_as_components_base_def_(self)
        # create entry layout first
        self._entry_layout = gui_qt_wgt_base.QtHBoxLayout(self)
        self._entry_layout.setContentsMargins(2, 2, 2, 2)
        self._entry_layout.setSpacing(8)
        self._build_input_entry_(2, self._value_type)

    def _build_input_entry_(self, value_size, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type
        #
        if self._value_entries:
            gui_qt_core.GuiQtLayout.clear_all_widgets(self._entry_layout)
        #
        self._value_entries = []
        #
        self._set_entry_count_(value_size)
        if value_size:
            for i in range(value_size):
                i_widget = gui_qt_wgt_entry.QtEntryAsConstant()
                i_widget._set_value_type_(self._value_type)
                self._entry_layout.addWidget(i_widget)
                self._value_entries.append(i_widget)

    def _set_entry_enable_(self, boolean):
        pass

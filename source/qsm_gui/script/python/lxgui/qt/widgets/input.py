# coding=utf-8
import six

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage
# gui
from ... import core as _gui_core
# qt
from ...qt.core.wrap import *

from ...qt import core as _qt_core

from ...qt import abstracts as _qt_abstracts
# qt widgets
from . import base as _base

from . import utility as _utility

from . import bubble as _bubble

from . import button as _button

from . import entry_frame as _entry_frame

from . import entry as _entry

from . import popup as _popup


# input as any constant, etc. integer, float, string/text/name, ...
class QtInputAsConstant(
    _entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputBaseDef,
):
    QT_ENTRY_CLS = _entry.QtEntryAsConstant

    entry_value_changed = qt_signal()

    def _pull_history_(self, value):
        self._entry_widget._set_value_(value)

    def __init__(self, *args, **kwargs):
        super(QtInputAsConstant, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(_gui_core.GuiSize.InputHeight)

        self._init_input_base_def_(self)

        self._build_input_entry_(self._value_type)

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type
        #
        entry_layout = _base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(4)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_value_type_(self._value_type)
        self._entry_widget._set_entry_frame_(self)

        self.input_value_accepted = self._entry_widget.entry_value_change_accepted

        self._entry_widget.entry_value_change_accepted.connect(self._push_history_)

    def _set_value_entry_validator_use_as_name_(self):
        self._entry_widget._set_validator_use_as_name_()

    def _set_entry_enable_(self, boolean):
        super(QtInputAsConstant, self)._set_entry_enable_(boolean)

        self._entry_widget.setReadOnly(not boolean)

        # self._frame_background_color = [
        #     _qt_core.QtBackgroundColors.Basic, _qt_core.QtBackgroundColors.Dim
        # ][boolean]
        self._update_background_color_by_locked_(boolean)
        self._refresh_widget_draw_()


# input as any constant entry and choose, etc. enumerate, file open/save, directory open/save, ...
class QtInputAsConstantWithChoose(
    _entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputBaseDef,
    # choose
    _qt_abstracts.AbsQtInputChooseExtraDef,
    # completion
    _qt_abstracts.AbsQtInputCompletionExtraDef,
):
    def _pull_history_(self, value):
        self._set_value_(value)

    QT_ENTRY_CLS = _entry.QtEntryAsConstant

    QT_POPUP_CHOOSE_CLS = _popup.QtPopupAsChoose
    QT_COMPLETION_POPUP_CLS = _popup.QtPopupAsCompletion

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
                        index_cur = values.index(value_cur) + 1
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
        self.setFixedHeight(_gui_core.GuiSize.InputHeight)

        self._init_input_base_def_(self)

        self._init_input_choose_extra_def_(self)
        self._init_input_completion_extra_def_(self)

        self._build_input_entry_(self._value_type)

        self.user_input_choose_value_accepted.connect(
            self._push_history_
        )

        self.installEventFilter(self)

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type
        #
        main_layout = _base.QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        entry_widget = _utility.QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = _base.QtHBoxLayout(entry_widget)
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
        self._input_info_bubble = _bubble.QtInfoBubble()
        self._input_info_bubble.hide()
        entry_layout.addWidget(self._input_info_bubble)
        #
        self._input_button_widget = _utility.QtLineWidget()
        self._input_button_widget._set_line_styles_(
            [self._input_button_widget.Style.Null, self._input_button_widget.Style.Null,
             self._input_button_widget.Style.Solid,
             self._input_button_widget.Style.Null]
        )
        entry_layout.addWidget(self._input_button_widget)
        self._input_button_layout = _base.QtHBoxLayout(self._input_button_widget)
        self._input_button_layout.setContentsMargins(2, 0, 0, 0)
        self._input_button_layout.setSpacing(2)
        #
        self._input_button = _button.QtIconPressButton()
        self._input_button_layout.addWidget(self._input_button)
        self._input_button._set_icon_file_path_(_gui_core.GuiIcon.get('down'))
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
        self._set_input_completion_buffer_fnc_(
            self._choose_value_completion_gain_fnc_
        )
        # connect completion to choose
        self._completion_popup_widget.user_popup_finished.connect(
            self.input_choose_changed.emit
        )
        self._completion_popup_widget.user_popup_finished.connect(
            self.user_input_choose_changed.emit
        )
        #
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
        button = _button.QtIconPressButton()
        self._input_button_layout.addWidget(button)
        button._set_name_text_(name_text)
        if icon_name is not None:
            button._set_icon_file_path_(_gui_core.GuiIcon.get(icon_name))
        if sub_icon_name is not None:
            button._set_icon_sub_file_path_(_gui_core.GuiIcon.get(sub_icon_name))
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


class QtInputAsBubbleWithChoose(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtInputBaseDef,

    _qt_abstracts.AbsQtInputChooseExtraDef,
):
    def _refresh_choose_index_(self):
        pass

    QT_ENTRY_CLS = _entry.QtEntryAsBubble

    QT_POPUP_CHOOSE_CLS = _popup.QtPopupAsChoose

    def _pull_history_(self, value):
        if value in self._choose_values:
            self._entry_widget._set_value_(value)

    def __init__(self, *args, **kwargs):
        super(QtInputAsBubbleWithChoose, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(_gui_core.GuiSize.InputHeight)

        self._init_input_base_def_(self)
        self._init_input_choose_extra_def_(self)

        self._build_input_entry_(str)

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type

        entry_layout = _base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(*[1] * 4)
        entry_layout.setSpacing(4)

        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)

        self._build_input_choose_()

        self._entry_widget.press_clicked.connect(self._do_choose_popup_start_)
        self.user_input_choose_value_accepted.connect(self._set_value_)
        self.input_value_changed = self._entry_widget.entry_value_changed
        self.input_value_accepted = self._entry_widget.entry_value_change_accepted

        self._choose_popup_widget._set_popup_style_(
            self._choose_popup_widget.PopupStyle.FromMouse
        )
        self._choose_popup_widget._set_popup_press_rect_(
            self._entry_widget._get_frame_rect_()
        )

        self._choose_popup_widget.user_popup_value_accepted.connect(self._push_history_)
        self.input_value_accepted.connect(self._push_history_)

        self.input_value_accepted = self._entry_widget.entry_value_change_accepted

    def _set_choose_values_(self, values, *args, **kwargs):
        super(QtInputAsBubbleWithChoose, self)._set_choose_values_(values, *args, **kwargs)
        self._entry_widget._set_value_options_(values, *args, **kwargs)

    def _bridge_choose_get_popup_texts_(self):
        return self._get_choose_values_()

    def _bridge_choose_get_popup_texts_current_(self):
        return [self._get_value_()]


# input as any content, etc. script, xml, doc
class QtInputAsContent(
    _entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputBaseDef,
):
    def _pull_history_(self, *args, **kwargs):
        pass

    QT_ENTRY_CLS = _entry.QtEntryAsContent

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

        # self._frame_background_color = _qt_core.QtBackgroundColors.Dark

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type
        #
        main_layout = _base.QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        #
        entry_widget = _utility.QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = _base.QtHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(0)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        self._entry_widget._set_entry_frame_(self)
        # self._entry_widget.setReadOnly(False)
        entry_layout.addWidget(self._entry_widget)
        #
        self._input_button_widget = _utility.QtLineWidget()
        self._input_button_widget.hide()
        self._input_button_widget._set_line_styles_(
            [self._input_button_widget.Style.Null, self._input_button_widget.Style.Null,
             self._input_button_widget.Style.Solid,
             self._input_button_widget.Style.Null]
        )
        entry_layout.addWidget(self._input_button_widget)
        self._input_button_layout = _base.QtVBoxLayout(self._input_button_widget)
        self._input_button_layout._set_align_as_top_()
        self._input_button_layout.setContentsMargins(2, 0, 0, 0)
        self._input_button_layout.setSpacing(2)
        #
        self._open_in_external_editor_button = _button.QtIconToggleButton()
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

    def _set_entry_enable_(self, boolean):
        super(QtInputAsContent, self)._set_entry_enable_(boolean)

        self._entry_widget.setReadOnly(not boolean)
        # fixme: not use?
        # self._frame_background_color = [
        #     _qt_core.QtBackgroundColors.Dark, _qt_core.QtBackgroundColors.Dim
        # ][boolean]
        self._update_background_color_by_locked_(boolean)
        self._refresh_widget_draw_()

    def _set_input_entry_drop_enable_(self, boolean):
        super(QtInputAsContent, self)._set_input_entry_drop_enable_(boolean)
        self._frame_border_draw_style = QtCore.Qt.DashLine

    def _set_empty_text_(self, text):
        self._entry_widget._set_empty_text_(text)


# input as any list
class QtInputAsList(
    _entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputBaseDef,
    # extra
    #   choose
    _qt_abstracts.AbsQtInputChooseExtraDef,
):
    def _refresh_choose_index_(self):
        pass

    def _pull_history_(self, *args, **kwargs):
        pass

    QT_ENTRY_CLS = _entry.QtEntryAsList
    #
    QT_POPUP_CHOOSE_CLS = _popup.QtPopupAsChoose
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
        main_layout = _base.QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        #
        entry_widget = _utility.QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = _base.QtHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(0)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_entry_frame_(self)
        #
        self._input_button_widget = _utility.QtLineWidget()
        self._input_button_widget._set_line_styles_(
            [self._input_button_widget.Style.Null, self._input_button_widget.Style.Null,
             self._input_button_widget.Style.Solid,
             self._input_button_widget.Style.Null]
        )
        entry_layout.addWidget(self._input_button_widget)
        self._input_button_layout = _base.QtVBoxLayout(self._input_button_widget)
        self._input_button_layout._set_align_as_top_()
        self._input_button_layout.setContentsMargins(2, 0, 0, 0)
        self._input_button_layout.setSpacing(2)

        self._input_button = _button.QtIconPressButton()
        self._input_button_layout.addWidget(self._input_button)
        self._input_button._set_icon_file_path_(_gui_core.GuiIcon.get('file/file'))
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

    def _do_clear_(self):
        self._clear_all_values_()

    def _clear_all_values_(self):
        self._entry_widget._clear_all_values_()

    def _set_entry_item_icon_file_path_(self, file_path):
        self._entry_widget._set_item_icon_file_path_(file_path)

    def _add_input_button_(self, widget):
        self._input_button_layout.addWidget(widget)

    def _create_input_button_(self, name_text, icon_name=None, sub_icon_name=None):
        button = _button.QtIconPressButton()
        self._input_button_layout.addWidget(button)
        button._set_name_text_(name_text)
        if icon_name is not None:
            button._set_icon_file_path_(_gui_core.GuiIcon.get(icon_name))
        if sub_icon_name is not None:
            button._set_icon_sub_file_path_(_gui_core.GuiIcon.get(sub_icon_name))
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
    _entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputBaseDef,
    # extra
    #   choose
    _qt_abstracts.AbsQtInputChooseExtraDef,
):
    def _refresh_choose_index_(self):
        pass

    def _pull_history_(self, *args, **kwargs):
        pass

    QT_ENTRY_CLS = _entry.QtEntryAsList
    QT_POPUP_CHOOSE_CLS = _popup.QtPopupAsChoose
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

        main_layout = _base.QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        entry_widget = _utility.QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = _base.QtHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(0)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_entry_frame_(self)
        #
        self._input_button_widget = _utility.QtLineWidget()
        self._input_button_widget._set_line_styles_(
            [self._input_button_widget.Style.Null, self._input_button_widget.Style.Null,
             self._input_button_widget.Style.Solid,
             self._input_button_widget.Style.Null]
        )
        entry_layout.addWidget(self._input_button_widget)
        self._input_button_layout = _base.QtVBoxLayout(self._input_button_widget)
        self._input_button_layout._set_align_as_top_()
        self._input_button_layout.setContentsMargins(2, 0, 0, 0)
        self._input_button_layout.setSpacing(2)

        self._input_button = _button.QtIconPressButton()
        self._input_button_layout.addWidget(self._input_button)
        self._input_button._set_icon_file_path_(_gui_core.GuiIcon.get('file/file'))
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
        button = _button.QtIconPressButton()
        self._input_button_layout.addWidget(button)
        button._set_name_text_(name_text)
        if icon_name is not None:
            button._set_icon_file_path_(_gui_core.GuiIcon.get(icon_name))
        if sub_icon_name is not None:
            button._set_icon_sub_file_path_(_gui_core.GuiIcon.get(sub_icon_name))
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


# rgba entry and choose
class QtInputAsRgba(
    _entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputAsOtherBaseDef,
    # extra
    #   choose
    _qt_abstracts.AbsQtInputChooseExtraDef,

    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,

    _qt_abstracts.AbsQtValueDefaultExtraDef,
):
    def _bridge_choose_get_popup_texts_(self):
        pass

    def _bridge_choose_get_popup_texts_current_(self):
        pass

    def _refresh_choose_index_(self):
        pass

    def _pull_history_(self, *args, **kwargs):
        pass

    QT_ENTRY_CLS = _entry.QtEntryAsConstant

    QT_POPUP_CHOOSE_CLS = _popup.QtPopupAsChooseForRgba

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
            x + (c_w - v_w) / 2, y + (c_h - v_h) / 2, v_w, v_h
        )

    def __init__(self, *args, **kwargs):
        super(QtInputAsRgba, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(_gui_core.GuiSize.InputHeight)

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

        entry_layout = _base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(self._value_draw_width + 2, 0, 0, 0)
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
                    if self._is_action_flag_match_(
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
        painter = _qt_core.QtPainter(self)

        rgba = self._get_value_()
        offset = self._get_action_offset_()
        painter._draw_frame_by_rect_(
            self._value_draw_rect,
            border_color=_qt_core.QtBorderColors.Transparent,
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
    _entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputAsOtherBaseDef,
    # extra
    #   choose
    _qt_abstracts.AbsQtInputChooseExtraDef,

    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,
):
    def _pull_history_(self, *args, **kwargs):
        pass

    def _refresh_choose_index_(self):
        pass

    QT_ENTRY_CLS = _entry.QtEntryAsConstant

    QT_POPUP_CHOOSE_CLS = _popup.QtPopupAsChooseForIcon

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
            x + (c_w - v_w) / 2, y + (c_h - v_h) / 2, v_w, v_h
        )

    def __init__(self, *args, **kwargs):
        super(QtInputAsIcon, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(_gui_core.GuiSize.InputHeight)

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
                    if self._is_action_flag_match_(
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
        painter = _qt_core.QtPainter(self)

        icon_name = self._get_value_()
        if icon_name == '':
            icon_name = 'state-disable'

        icon_file_path = _gui_core.GuiIcon.get(icon_name)
        if icon_file_path:
            offset = self._get_action_offset_()

            painter._draw_icon_file_by_rect_(
                rect=self._value_draw_rect,
                file_path=icon_file_path,
                offset=offset
            )

    def _build_input_entry_(self):
        self._entry_frame_widget = self

        entry_layout = _base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(self._value_draw_width + 2, 0, 0, 0)
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
    _entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputAsComponentsBaseDef,
):
    def _pull_history_(self, *args, **kwargs):
        pass

    QT_ENTRY_CLS = _entry.QtEntryAsConstant

    entry_value_changed = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtInputAsTuple, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(_gui_core.GuiSize.InputHeight)

        self._init_input_as_components_base_def_(self)
        # create entry layout first
        self._entry_layout = _base.QtHBoxLayout(self)
        self._entry_layout.setContentsMargins(2, 2, 2, 2)
        self._entry_layout.setSpacing(8)
        self._build_input_entry_(2, self._value_type)

    def _build_input_entry_(self, value_size, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type

        if self._value_entries:
            _qt_core.GuiQtLayout.clear_all_widgets(self._entry_layout)

        self._value_entries = []

        self._set_entry_count_(value_size)
        if value_size:
            for i in range(value_size):
                i_widget = _entry.QtEntryAsConstant()
                i_widget._set_value_type_(self._value_type)
                self._entry_layout.addWidget(i_widget)
                self._value_entries.append(i_widget)

    def _set_entry_enable_(self, boolean):
        for i in self._value_entries:
            i._set_entry_enable_(boolean)

        self._update_background_color_by_locked_(boolean)

        self._refresh_widget_all_()

    def _set_action_enable_(self, boolean):
        self._set_entry_enable_(boolean)

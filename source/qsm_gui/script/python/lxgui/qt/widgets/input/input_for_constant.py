# coding=utf-8
# gui
from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import abstracts as _qt_abstracts
# qt widgets
from .. import base as _wgt_base

from .. import utility as _wgt_utility

from .. import bubble as _wgt_bubble

from .. import button as _wgt_button

from .. import entry_frame as _wgt_entry_frame

from .. import popup as _wgt_popup

from ..entry import entry_for_constant as _entry_for_constant


# input as any constant, etc. integer, float, string/text/name, ...
class QtInputForConstant(
    _wgt_entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtNameBaseDef,
    _qt_abstracts.AbsQtInputBaseDef,
):
    QT_ENTRY_CLS = _entry_for_constant.QtEntryForConstant

    entry_value_changed = qt_signal()

    def _pull_history_(self, value):
        if value is not None:
            self._entry_widget._set_value_(value)

    def __init__(self, *args, **kwargs):
        super(QtInputForConstant, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(_gui_core.GuiSize.InputHeight)

        self._init_name_base_def_(self)
        self._init_input_base_def_(self)

        self._build_input_entry_(self._value_type)

    def _build_input_entry_(self, value_type):
        self._entry_frame_widget = self

        self._value_type = value_type
        #
        entry_layout = _wgt_base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(4)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_value_type_(self._value_type)
        self._entry_widget._set_entry_frame_(self)

        self.input_value_accepted = self._entry_widget.entry_value_accepted

        self._entry_widget.entry_value_accepted.connect(self._push_history_)

    def _set_value_entry_validator_use_as_name_(self):
        self._entry_widget._set_validator_use_as_name_()

    def _set_entry_enable_(self, boolean):
        super(QtInputForConstant, self)._set_entry_enable_(boolean)

        self._entry_widget.setReadOnly(not boolean)
        self._update_background_color_by_locked_(boolean)
        self._refresh_widget_draw_()

    def _set_use_as_password_(self):
        self._entry_widget._set_use_as_password_()


# input as any constant entry and choose, etc. enumerate, file open/save, directory open/save, ...
class QtInputForConstantChoose(
    _wgt_entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputBaseDef,
    # choose
    _qt_abstracts.AbsQtInputChooseExtraDef,
    # completion
    _qt_abstracts.AbsQtInputCompletionExtraDef,
):
    def _pull_history_(self, value):
        if value is not None:
            self._set_value_(value)

    QT_ENTRY_CLS = _entry_for_constant.QtEntryForConstant

    QT_POPUP_CHOOSE_CLS = _wgt_popup.QtPopupForChoose
    QT_COMPLETION_POPUP_CLS = _wgt_popup.QtPopupForCompletion

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
        super(QtInputForConstantChoose, self).__init__(*args, **kwargs)
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
        main_layout = _wgt_base.QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        entry_widget = _wgt_utility.QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = _wgt_base.QtHBoxLayout(entry_widget)
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
        self._input_info_bubble = _wgt_bubble.QtInfoBubble()
        self._input_info_bubble.hide()
        entry_layout.addWidget(self._input_info_bubble)
        #
        self._input_button_widget = _wgt_utility.QtLineWidget()
        self._input_button_widget._set_line_styles_(
            [self._input_button_widget.Style.Null, self._input_button_widget.Style.Null,
             self._input_button_widget.Style.Solid,
             self._input_button_widget.Style.Null]
        )
        entry_layout.addWidget(self._input_button_widget)
        self._input_button_layout = _wgt_base.QtHBoxLayout(self._input_button_widget)
        self._input_button_layout.setContentsMargins(2, 0, 0, 0)
        self._input_button_layout.setSpacing(2)
        #
        self._input_button = _wgt_button.QtIconPressButton()
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
        super(QtInputForConstantChoose, self)._set_entry_enable_(boolean)

        self._entry_widget._set_entry_enable_(boolean)
        self._input_button.setHidden(not boolean)

        self._update_background_color_by_locked_(boolean)

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
        button = _wgt_button.QtIconPressButton()
        self._input_button_layout.addWidget(button)
        button._set_name_text_(name_text)
        if icon_name is not None:
            button._set_icon_file_path_(_gui_core.GuiIcon.get(icon_name))
        if sub_icon_name is not None:
            button._set_sub_icon_file_path_(_gui_core.GuiIcon.get(sub_icon_name))
        if tool_tip:
            button._set_tool_tip_(tool_tip)
        button._set_icon_frame_draw_size_(18, 18)
        return button

    def _set_choose_values_(self, values, *args, **kwargs):
        super(QtInputForConstantChoose, self)._set_choose_values_(values, *args, **kwargs)

        self._refresh_choose_index_()

        self._get_entry_widget_()._set_value_options_(
            self._get_choose_values_()
        )

    def _set_value_options_(self, values, *args, **kwargs):
        self._set_choose_values_(values, *args, **kwargs)

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
# coding=utf-8
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

from .. import popup as _wgt_popup

from ..entry import entry_for_array as _entry_for_array


# input as any list
class QtInputForArray(
    _wgt_entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputBaseDef,
    # extra
    #   choose
    _qt_abstracts.AbsQtInputChooseExtraDef,
):
    def _refresh_choose_index_(self):
        pass

    def _pull_history_(self, *args, **kwargs):
        pass

    QT_ENTRY_CLS = _entry_for_array.QtEntryForArray
    #
    QT_POPUP_CHOOSE_CLS = _wgt_popup.QtPopupForChoose
    #
    add_press_clicked = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtInputForArray, self).__init__(*args, **kwargs)
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
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_entry_frame_(self)
        #
        self._input_button_widget = _wgt_utility.QtLineWidget()
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

        self._input_button = _wgt_button.QtIconPressButton()
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
        super(QtInputForArray, self)._set_entry_enable_(boolean)
        self._entry_widget._set_entry_enable_(boolean)
        self._update_background_color_by_locked_(boolean)
        self._refresh_widget_draw_()

    def _set_input_entry_drop_enable_(self, boolean):
        super(QtInputForArray, self)._set_input_entry_drop_enable_(boolean)
        self._frame_border_draw_style = QtCore.Qt.DashLine

    def _set_input_choose_enable_(self, boolean):
        self._input_button._set_action_enable_(boolean)

    def _set_input_choose_visible_(self, boolean):
        self._input_button._set_visible_(boolean)

    def _set_values_append_fnc_(self, fnc):
        pass

    def _append_value_(self, value):
        self._entry_widget._append_value_(value)

    def _remove_value_(self, value):
        self._entry_widget._remove_value_(value)

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
        button = _wgt_button.QtIconPressButton()
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
class QtInputForArrayChoose(
    _wgt_entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputBaseDef,
    # extra
    #   choose
    _qt_abstracts.AbsQtInputChooseExtraDef,
):
    def _refresh_choose_index_(self):
        pass

    def _pull_history_(self, *args, **kwargs):
        pass

    QT_ENTRY_CLS = _entry_for_array.QtEntryForArray
    QT_POPUP_CHOOSE_CLS = _wgt_popup.QtPopupForChoose
    #
    add_press_clicked = qt_signal()

    def __init__(self, *args, **kwargs):
        super(QtInputForArrayChoose, self).__init__(*args, **kwargs)
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

        main_layout = _wgt_base.QtVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        entry_widget = _wgt_utility.QtTranslucentWidget()
        main_layout.addWidget(entry_widget)
        #
        entry_layout = _wgt_base.QtHBoxLayout(entry_widget)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(0)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_entry_frame_(self)
        #
        self._input_button_widget = _wgt_utility.QtLineWidget()
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

        self._input_button = _wgt_button.QtIconPressButton()
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
        super(QtInputForArrayChoose, self)._set_entry_enable_(boolean)

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
        button = _wgt_button.QtIconPressButton()
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

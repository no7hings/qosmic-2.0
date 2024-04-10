# coding=utf-8
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from . import base as gui_qt_abs_base


# entry for value base
#   constant, etc. float, integer
class AbsQtInputBaseDef(
    gui_qt_abs_base.AbsQtValueBaseDef,
    gui_qt_abs_base.AbsQtValueDefaultExtraDef,
    gui_qt_abs_base.AbsQtValueValidationExtraDef,
    gui_qt_abs_base.AbsQtValueHistoryExtraDef,
):
    user_key_tab_pressed = qt_signal()
    #
    input_value_changed = qt_signal()
    input_value_cleared = qt_signal()
    # user
    #   change
    user_input_value_changed = qt_signal()
    #   finish
    user_input_value_finished = qt_signal()
    #   clear
    user_input_value_cleared = qt_signal()

    input_value_change_accepted = qt_signal(object)
    user_input_value_change_accepted = qt_signal(object)

    def _init_input_base_def_(self, widget):
        self._init_value_base_def_(widget)
        self._init_value_default_extra_def_(widget)
        self._init_value_validation_extra_def_(widget)
        self._init_value_history_base_def_(widget)

        self._widget = widget

        self._entry_is_enable = False

        self._value_type = str
        self._value_default = None
        self._entry_widget = None
        self._entry_frame_widget = None

    def _set_input_entry_focus_in_(self):
        self._get_entry_widget_().setFocus(QtCore.Qt.MouseFocusReason)

    def _get_input_entry_has_focus_(self):
        return self._get_entry_widget_().hasFocus()

    def _set_entry_enable_(self, boolean):
        self._entry_is_enable = boolean

    def _set_input_entry_drop_enable_(self, boolean):
        self._entry_widget._set_drop_enable_(boolean)

    def _set_value_validation_fnc_(self, fnc):
        pass

    def _set_input_entry_use_as_storage_(self, boolean):
        self._entry_widget._set_entry_use_as_storage_(boolean)

    def _set_input_entry_focus_enable_(self, boolean):
        self._entry_widget._set_entry_focus_enable_(boolean)

    def _get_entry_widget_(self):
        return self._entry_widget

    def _get_entry_frame_widget_(self):
        return self._entry_frame_widget

    def _build_input_entry_(self, *args, **kwargs):
        pass

    def _set_value_type_(self, value_type):
        self._value_type = value_type
        self._entry_widget._set_value_type_(value_type)

    def _set_value_validator_use_as_frames_(self):
        self._entry_widget._set_value_validator_use_as_frames_()

    def _set_value_validator_use_as_rgba_(self):
        self._entry_widget._set_value_validator_use_as_rgba_()

    def _get_value_type_(self):
        return self._value_type

    def _set_value_(self, value):
        self._entry_widget._set_value_(value)

    def _get_value_(self):
        return self._entry_widget._get_value_()

    def _connect_input_user_entry_value_finished_to_(self, fnc):
        self._entry_widget.user_entry_finished.connect(fnc)

    def _connect_input_entry_value_changed_to_(self, fnc):
        self._entry_widget.entry_value_changed.connect(fnc)

    def _set_item_value_entry_enable_(self, boolean):
        pass


#   tuple, etc. float2, float3, ...
class AbsQtInputAsComponentsBaseDef(
    gui_qt_abs_base.AbsQtValueBaseDef,
    gui_qt_abs_base.AbsQtValueDefaultExtraDef,
    gui_qt_abs_base.AbsQtValueValidationExtraDef,
    gui_qt_abs_base.AbsQtValueHistoryExtraDef,
):
    def _init_input_as_components_base_def_(self, widget):
        self._init_value_base_def_(widget)
        self._init_value_default_extra_def_(widget)
        self._init_value_validation_extra_def_(widget)
        self._init_value_history_base_def_(widget)

        self._widget = widget
        self._value_type = str
        #
        self._value_default = ()
        #
        self._value = []
        self._value_entries = []

    def _build_input_entry_(self, *args, **kwargs):
        raise NotImplementedError()

    def _set_value_type_(self, value_type):
        self._value_type = value_type
        for i_value_entry_widget in self._value_entries:
            i_value_entry_widget._set_value_type_(value_type)

    def _get_value_type_(self):
        return self._value_type

    def _set_value_size_(self, size):
        self._build_input_entry_(size, self._value_type)

    def _get_value_size_(self):
        return len(self._value_entries)

    def _set_value_(self, value):
        for i, i_value in enumerate(value):
            widget = self._value_entries[i]
            widget._set_value_(i_value)

    def _get_value_(self):
        value = []
        for i in self._value_entries:
            i_value = i._get_value_()
            value.append(
                i_value
            )
        return tuple(value)

    def _get_value_is_default_(self):
        return tuple(self._get_value_()) == tuple(self._get_value_default_())

    def _connect_input_entry_value_changed_to_(self, fnc):
        for i in self._value_entries:
            i.entry_value_changed.connect(fnc)


#   other, etc. rgba, icon, ...
class AbsQtInputAsOtherBaseDef(AbsQtInputBaseDef):
    def _init_input_as_other_base_def_(self, widget):
        self._init_input_base_def_(widget)

        self._value_rect = QtCore.QRect()
        self._value_draw_rect = QtCore.QRect()
        self._value_draw_width, self._value_draw_height = 16, 16

    def _get_value_rect_(self):
        return self._value_rect


# extra
#   choose
class AbsQtInputChooseExtraDef(
    gui_qt_abs_base.AbsQtChooseExtraDef
):
    QT_POPUP_CHOOSE_CLS = None

    def _get_entry_widget_(self):
        raise NotImplementedError()

    def _get_entry_frame_widget_(self):
        raise NotImplementedError()

    def _init_input_choose_extra_def_(self, widget):
        self._init_choose_extra_def_(widget)

        self._widget = widget

        self._choose_popup_widget = None

    def _build_input_choose_(self):
        self._choose_popup_widget = self.QT_POPUP_CHOOSE_CLS(self)
        self._choose_popup_widget.hide()

        self._choose_popup_widget._set_popup_auto_resize_enable_(True)
        self._choose_popup_widget._set_entry_widget_(self._get_entry_widget_())
        self._choose_popup_widget._set_entry_frame_widget_(self._get_entry_frame_widget_())

        self._choose_popup_widget.user_popup_finished.connect(
            self.input_choose_changed.emit
        )
        self._choose_popup_widget.user_popup_finished.connect(
            self.user_input_choose_changed.emit
        )
        self.user_input_choose_value_accepted = self._choose_popup_widget.user_popup_value_accepted
        self.user_input_choose_values_accepted = self._choose_popup_widget.user_popup_values_accepted

    def _do_choose_popup_start_(self):
        self._choose_popup_widget._do_popup_start_()

    def _do_choose_popup_close_(self):
        self._choose_popup_widget._do_popup_close_()

    def _set_choose_popup_auto_resize_enable_(self, boolean):
        self._choose_popup_widget._set_popup_auto_resize_enable_(boolean)

    def _get_choose_popup_widget_(self):
        return self._choose_popup_widget

    def _set_choose_popup_item_multiply_enable_(self, boolean):
        self._choose_popup_widget._set_popup_item_multiply_enable_(boolean)

    def _set_choose_popup_item_size_(self, w, h):
        self._choose_popup_widget._set_popup_item_size_(w, h)

    def _set_choose_popup_tag_filter_enable_(self, boolean):
        self._choose_popup_widget._set_popup_item_tag_filter_enable_(boolean)

    def _set_choose_popup_keyword_filter_enable_(self, boolean):
        self._choose_popup_widget._set_popup_item_keyword_filter_enable_(boolean)

    def _set_choose_popup_item_icon_file_path_for_(self, text, file_path):
        self._choose_popup_widget._set_popup_item_icon_file_path_for_(
            text, file_path
        )

    def _set_choose_popup_item_icon_file_path_(self, file_path):
        self._choose_popup_widget._set_popup_item_icon_file_path_(file_path)

    def _set_choose_popup_item_image_url_dict_(self, dict_):
        self._choose_popup_widget._set_popup_item_image_url_dict_(dict_)

    def _set_choose_popup_item_keyword_filter_dict_(self, dict_):
        self._choose_popup_widget._set_popup_item_keyword_filter_dict_(dict_)

    def _set_choose_popup_item_tag_filter_dict_(self, dict_):
        self._choose_popup_widget._set_popup_item_tag_filter_dict_(dict_)

    def _restore_choose_popup_(self):
        self._choose_popup_widget._restore_popup_()

    def _bridge_choose_get_popup_texts_(self):
        raise NotImplementedError()

    def _bridge_choose_get_popup_texts_current_(self):
        raise NotImplementedError()


#   completion
class AbsQtInputCompletionExtraDef(object):
    """
    for completion entry as a popup choose frame
    """
    QT_COMPLETION_POPUP_CLS = None
    #
    user_input_completion_finished = qt_signal()
    user_input_completion_value_accepted = qt_signal(str)

    def _get_entry_widget_(self):
        raise NotImplementedError()

    def _get_entry_frame_widget_(self):
        raise NotImplementedError()

    def _init_input_completion_extra_def_(self, widget):
        self._widget = widget

        self._completion_popup_widget = None
        self._input_completion_gain_fnc = None

    def _build_input_completion_(self):
        self._completion_popup_widget = self.QT_COMPLETION_POPUP_CLS(self)
        self._completion_popup_widget.hide()

        self._completion_popup_widget._set_entry_widget_(self._get_entry_widget_())
        self._completion_popup_widget._set_entry_frame_widget_(self._get_entry_frame_widget_())

        self._get_entry_widget_()._build_entry_for_completion_popup_(self._get_completion_popup_widget_())
        # emit
        self.user_input_completion_finished = self._completion_popup_widget.user_popup_finished
        self.user_input_completion_value_accepted = self._completion_popup_widget.user_popup_value_accepted

    def _get_completion_popup_widget_(self):
        return self._completion_popup_widget

    def _set_input_completion_buffer_fnc_(self, fnc):
        self._input_completion_gain_fnc = fnc

    def _generate_completion_texts_(self):
        if self._input_completion_gain_fnc is not None:
            keyword = self._get_entry_widget_()._get_value_()
            return self._input_completion_gain_fnc(keyword) or []
        return []


#   history
class AbsQtInputHistoryExtraDef(object):
    QT_HISTORY_POPUP_CLS = None

    def _get_entry_widget_(self):
        raise NotImplementedError()

    def _get_history_values_(self):
        raise NotImplementedError()

    def _pull_history_(self):
        raise NotImplementedError()

    def _init_input_history_extra_def_(self, widget):
        self._widget = widget

        self._history_popup_widget = None

    def _build_input_history_(self, history_button=None):
        self._history_popup_widget = self.QT_HISTORY_POPUP_CLS(self)
        self._history_popup_widget.hide()

        self._history_popup_widget._set_popup_name_text_('choose a record ...')
        self._history_popup_widget._set_entry_widget_(self._get_entry_widget_())
        self._history_popup_widget._set_entry_frame_widget_(self)

        if history_button is not None:
            history_button._set_icon_file_path_(gui_core.GuiIcon.get('history'))
            history_button._set_icon_state_name_('state/popup')
            history_button._set_icon_frame_draw_size_(18, 18)
            history_button.press_clicked.connect(self._get_history_popup_widget_()._do_popup_start_)
            history_button.hide()

        self._history_popup_widget.user_popup_value_accepted.connect(self._pull_history_)

    def _get_history_popup_widget_(self):
        return self._history_popup_widget

    def _bridge_history_get_popup_texts_(self):
        return self._get_history_values_()

    def _bridge_history_get_popup_texts_current_(self):
        return [self._get_entry_widget_()._get_value_()]

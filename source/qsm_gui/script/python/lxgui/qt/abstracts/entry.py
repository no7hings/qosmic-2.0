# coding=utf-8
# qt
from ..core.wrap import *

from . import base as gui_qt_abs_base


# entry base
class AbsQtEntryBaseDef(
    gui_qt_abs_base.AbsQtValueBaseDef,
    gui_qt_abs_base.AbsQtValueDefaultExtraDef,
    gui_qt_abs_base.AbsQtValueValidationExtraDef,
):
    entry_value_changed = qt_signal()
    entry_value_cleared = qt_signal()

    entry_value_change_accepted = qt_signal(object)

    entry_value_added = qt_signal()
    entry_value_removed = qt_signal()

    user_entry_value_changed = qt_signal()
    user_entry_value_cleared = qt_signal()

    user_entry_finished = qt_signal()

    def _init_entry_base_def_(self, widget):
        self._init_value_base_def_(widget)
        self._init_value_default_extra_def_(widget)
        self._init_value_validation_extra_def_(widget)

        self._widget = widget

        self._entry_is_enable = False

        self._entry_use_as_storage = False
        self._entry_use_as_file = False
        self._entry_use_as_file_multiply = False
        self._entry_use_as_rgba = False

        self._entry_focus_policy_mark = None

    def _set_entry_enable_(self, boolean):
        self._entry_is_enable = boolean

    def _set_entry_focus_enable_(self, boolean):
        pass

    def _set_entry_use_as_storage_(self, boolean):
        self._entry_use_as_storage = boolean

    def _set_entry_use_as_rgba_255_(self, boolean):
        self._entry_use_as_rgba = boolean

    def _set_entry_use_as_file_(self, boolean):
        self._entry_use_as_file = boolean

    def _set_entry_use_as_file_multiply_(self, boolean):
        self._entry_use_as_file_multiply = boolean

    def _set_focused_(self, boolean):
        if boolean is True:
            self._widget.setFocus(
                QtCore.Qt.MouseFocusReason
            )
        else:
            self._widget.setFocus(
                QtCore.Qt.NoFocusReason
            )


class AbsQtEntryAsArrayBaseDef(
    AbsQtEntryBaseDef,
    gui_qt_abs_base.AbsQtValueArrayBaseDef,
):
    def _init_entry_as_array_base_def_(self, widget):
        self._init_entry_base_def_(widget)
        self._init_value_array_base_def_(widget)

        self._widget = widget


# entry extra
class AbsQtEntryFrameExtraDef(object):
    def _init_entry_frame_extra_def_(self, widget):
        self._widget = widget

        self._entry_frame_widget = None

    def _set_entry_frame_(self, widget):
        self._entry_frame_widget = widget

    def _get_entry_frame_(self):
        if self._entry_frame_widget is not None:
            return self._entry_frame_widget
        return self._widget.parent()


class AbsQtEntryPopupExtra(object):
    key_up_pressed = qt_signal()
    key_down_pressed = qt_signal()
    key_left_pressed = qt_signal()
    key_right_pressed = qt_signal()
    key_down_and_alt_pressed = qt_signal()
    key_escape_pressed = qt_signal()

    def _init_entry_popup_extra_def_(self, widget):
        self._widget = widget

        self._choose_popup_widget = None
        self._completion_popup_widget = None

    def _set_choose_popup_widget_(self, widget):
        self._choose_popup_widget = widget

    def _get_choose_popup_widget_(self):
        return self._choose_popup_widget

    def _set_completion_popup_widget_(self, widget):
        self._completion_popup_widget = widget

    def _get_choose_popup_is_activated_(self):
        if self._choose_popup_widget is not None:
            return self._choose_popup_widget._get_popup_is_activated_()
        return False

    def _get_completion_popup_is_activated_(self):
        return self._completion_popup_widget._get_popup_is_activated_()

    def _build_entry_for_completion_popup_(self, popup_widget):
        raise NotImplementedError()

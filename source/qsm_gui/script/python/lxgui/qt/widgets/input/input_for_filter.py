# coding=utf-8
import copy
# gui
from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import abstracts as _qt_abstracts
# qt widgets
from .. import base as _wgt_base

from .. import utility as _wgt_utility

from .. import button as _wgt_button

from .. import resize as _wgt_resize

from .. import entry_frame as _wgt_entry_frame

from .. import popup as _wgt_popup

from .. import bubble as _wgt_bubble

from ..entry import entry_for_constant as _entry_for_constant


class QtInputForFilter(
    QtWidgets.QWidget,

    _qt_abstracts.AbsQtInputBaseDef,

    _qt_abstracts.AbsQtInputCompletionExtraDef,
    _qt_abstracts.AbsQtInputHistoryExtraDef,
):
    occurrence_previous_press_clicked = qt_signal()
    occurrence_next_press_clicked = qt_signal()

    occurrence_accepted = qt_signal(str)

    QT_ENTRY_CLS = _entry_for_constant.QtEntryForConstant

    QT_COMPLETION_POPUP_CLS = _wgt_popup.QtPopupForCompletion

    QT_HISTORY_POPUP_CLS = _wgt_popup.QtPopupForHistory

    def _refresh_widget_all_(self):
        self.update()

    def _refresh_widget_draw_(self):
        pass

    def _pull_history_fnc_(self, value):
        if value is not None:
            self._accept_element_(value)

    def _refresh_history_extend_(self):
        self._history_button.show()
        if self._get_history_values_():
            self._history_button._set_action_enable_(True)
        else:
            self._history_button._set_action_enable_(False)

    def __init__(self, *args, **kwargs):
        super(QtInputForFilter, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        lot = _wgt_base.QtHBoxLayout(self)
        lot.setContentsMargins(*[0]*4)
        lot.setSpacing(2)
        lot.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

        self._init_input_base_def_(self)

        self._init_input_completion_extra_def_(self)

        self._result_label = _wgt_utility.QtTextItem()
        # todo: fix result show bug
        # self._result_label.hide()
        lot.addWidget(self._result_label)
        #
        self._resize_handle = _wgt_resize.QtHResizeHandle()
        self._resize_handle._set_resize_icon_file_paths_(
            [
                _gui_core.GuiIcon.get('resize-handle-v'), _gui_core.GuiIcon.get('resize-handle-v')
            ]
        )
        self._resize_handle._resize_frame_draw_size = 10, 20
        self._resize_handle._resize_icon_draw_size = 8, 16
        self._resize_handle._set_resize_alignment_(self._resize_handle.ResizeAlignment.Left)
        lot.addWidget(self._resize_handle)
        self._resize_handle.setFixedWidth(8)
        #
        self._entry_frame_widget = _wgt_entry_frame.QtEntryFrame()
        self._entry_frame_widget.setFixedWidth(200)
        self._entry_frame_widget.setFixedHeight(24)
        self._resize_handle._set_resize_target_(self._entry_frame_widget)
        lot.addWidget(self._entry_frame_widget)
        #
        self._build_input_entry_(str)
        #
        self._match_case_button = _wgt_button.QtIconPressButton()
        self._match_case_button.hide()
        lot.addWidget(self._match_case_button)
        self._match_case_button.setFocusProxy(self._entry_widget)
        self._match_case_button.press_clicked.connect(self._do_match_case_swap_)
        self._match_case_icon_names = 'match_case_off', 'match_case_on'
        self._is_match_case = False
        #
        self._match_word_button = _wgt_button.QtIconPressButton()
        self._match_word_button.hide()
        lot.addWidget(self._match_word_button)
        self._match_word_button.setFocusProxy(self._entry_widget)
        self._match_word_button.press_clicked.connect(self._do_match_word_swap_)
        self._match_word_icon_names = 'match_word_off', 'match_word_on'
        self._is_match_word = False
        # occurrence
        self._occurrence_previous_button = _wgt_button.QtIconPressButton()
        lot.addWidget(self._occurrence_previous_button)
        self._occurrence_previous_button._set_name_text_('occurrence previous')
        self._occurrence_previous_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('occurrence-previous-disable')
        )
        self._occurrence_previous_button._set_tool_tip_text_('"LMB-click" to occurrence previous result')
        self._occurrence_previous_button.press_clicked.connect(
            self.occurrence_previous_press_clicked.emit
        )
        #
        self._occurrence_next_button = _wgt_button.QtIconPressButton()
        lot.addWidget(self._occurrence_next_button)
        self._occurrence_next_button._set_name_text_('occurrence next')
        self._occurrence_next_button._set_icon_file_path_(
            _gui_core.GuiIcon.get('occurrence-next-disable')
        )
        self._occurrence_next_button._set_tool_tip_text_('"LMB-click" to occurrence next result')
        self._occurrence_next_button.press_clicked.connect(
            self.occurrence_next_press_clicked.emit
        )
        #
        self._init_input_history_extra_def_(self)
        #
        self._filter_result_count = None
        self._filter_index_current = None
        #
        self._update_filter_()
        self._do_refresh_filter_tip_()

    def _build_input_entry_(self, value_type):
        self._value_type = value_type
        self._input_layout = _wgt_base.QtHBoxLayout(self._entry_frame_widget)
        self._input_layout.setContentsMargins(2, 0, 2, 0)
        self._input_layout.setSpacing(0)
        #
        self._header_button = _wgt_button.QtIconPressButton()
        self._header_button._set_icon_frame_draw_size_(18, 18)
        self._input_layout.addWidget(self._header_button)
        self._header_button._set_icon_file_path_(
            _gui_core.GuiIcon.get(
                'search'
            )
        )
        #
        self._text_bubbles = _wgt_bubble.QtTextBubbles()
        self._input_layout.addWidget(self._text_bubbles)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        self._input_layout.addWidget(self._entry_widget)
        #
        self._entry_widget.entry_value_changed.connect(self._do_input_change_)
        self._entry_widget.user_entry_value_changed.connect(self._do_user_input_change_)
        #
        self._entry_clear_button = _wgt_button.QtIconPressButton()
        self._input_layout.addWidget(self._entry_clear_button)
        self._entry_clear_button.hide()
        self._entry_clear_button._set_icon_file_path_(
            _gui_core.GuiIcon.get(
                'entry_clear'
            )
        )
        self._entry_clear_button._icon_draw_percent = .6
        self._entry_clear_button.press_clicked.connect(self._do_user_clear_entry_)
        #
        self._history_button = _wgt_button.QtIconPressButton()
        self._input_layout.addWidget(self._history_button)
        # completion
        self._build_input_completion_()
        self.user_input_completion_finished.connect(self.input_value_changed)
        self.user_input_completion_value_accepted.connect(self._accept_element_)
        self.user_input_completion_value_accepted.connect(self._push_history_fnc_)
        #
        self._build_input_history_(self._history_button)
        self._entry_widget.entry_value_accepted.connect(self._push_history_fnc_)
        self._entry_widget.entry_value_accepted.connect(self._text_bubbles._create_one_)
        #
        self._text_bubbles._set_entry_widget_(self._entry_widget)
        # noinspection PyUnresolvedReferences
        self._entry_widget.textEdited.connect(self._do_refresh_filter_tip_)
        self._entry_widget.user_entry_text_accepted.connect(self._text_bubbles._create_one_)
        self._entry_widget.user_entry_text_accepted.connect(self._push_history_fnc_)
        # backspace press
        self._entry_widget.key_backspace_extra_pressed.connect(self._text_bubbles._on_backspace_)
        #
        self._text_bubbles.bubbles_value_changed.connect(self._do_refresh_filter_tip_)
        self._text_bubbles.bubbles_value_changed.connect(self._do_input_change_)
        #
        self._entry_clear_button.press_clicked.connect(self._do_refresh_filter_tip_)

    def _do_refresh_filter_tip_(self):
        if self._entry_frame_widget._tip_text:
            if self._get_all_keywords_():
                self._entry_frame_widget._tip_draw_enable = False
            else:
                self._entry_frame_widget._tip_draw_enable = True

            self._entry_frame_widget._refresh_widget_draw_()

    def _get_all_keywords_(self):
        _ = copy.copy(self._text_bubbles._get_all_texts_())
        if self._entry_widget._get_value_():
            _.append(self._entry_widget._get_value_())
        return list(_)

    def _update_filter_(self):
        self._match_case_button._set_icon_file_path_(
            _gui_core.GuiIcon.get(self._match_case_icon_names[self._is_match_case])
        )
        #
        self._match_word_button._set_icon_file_path_(
            _gui_core.GuiIcon.get(self._match_word_icon_names[self._is_match_word])
        )

    def _do_match_case_swap_(self):
        self._is_match_case = not self._is_match_case
        self._update_filter_()

        self._do_input_change_()

    def _do_match_word_swap_(self):
        self._is_match_word = not self._is_match_word
        self._update_filter_()

        self._do_input_change_()

    def _clear_entry_(self):
        self._entry_widget._do_clear_()
        self._entry_widget.entry_value_cleared.emit()
        self._do_input_change_()

    def _do_user_clear_entry_(self):
        self._entry_widget._do_clear_()
        self._entry_widget.user_entry_value_cleared.emit()
        self._do_user_input_change_()

    def _set_occurrence_buttons_enable_(self, boolean):
        if boolean is True:
            self._occurrence_previous_button._set_icon_file_path_(
                _gui_core.GuiIcon.get('occurrence-previous')
            )
            self._occurrence_next_button._set_icon_file_path_(
                _gui_core.GuiIcon.get('occurrence-next')
            )
        else:
            self._occurrence_previous_button._set_icon_file_path_(
                _gui_core.GuiIcon.get('occurrence-previous-disable')
            )
            self._occurrence_next_button._set_icon_file_path_(
                _gui_core.GuiIcon.get('occurrence-next-disable')
            )

    def _set_occurrence_buttons_visible_(self, boolean):
        self._occurrence_previous_button.setVisible(boolean)
        self._occurrence_next_button.setVisible(boolean)

    def _set_filter_tip_(self, text):
        self._entry_frame_widget._set_tip_text_(text)
        self._do_refresh_filter_tip_()

    def _get_is_match_case_(self):
        return self._is_match_case

    def _get_is_match_word_(self):
        return self._is_match_word

    def _do_input_change_(self):
        # noinspection PyUnresolvedReferences
        self.input_value_changed.emit()
        self._refresh_entry_clear_button_visible_()

    def _do_user_input_change_(self):
        self.user_input_value_changed.emit()
        self._refresh_entry_clear_button_visible_()

    def _refresh_entry_clear_button_visible_(self):
        self._entry_clear_button.setVisible(
            not not self._entry_widget.text()
        )

    def _set_filter_result_count_(self, value):
        self._filter_result_count = value
        self._filter_index_current = None
        self._refresh_filter_result_()

    def _set_filter_result_index_current_(self, value):
        self._filter_index_current = value
        self._refresh_filter_result_()

    def _refresh_filter_result_(self):
        if self._filter_result_count is not None:
            if self._filter_index_current is not None:
                self._result_label._set_name_text_(
                    '{}/{}'.format(self._filter_index_current+1, self._filter_result_count)
                    )
            else:
                self._result_label._set_name_text_('1/{}'.format(self._filter_result_count))
        else:
            self._result_label._set_name_text_('')

    def _clear_filter_result_(self):
        self._filter_result_count = None
        self._filter_index_current = None
        self._refresh_filter_result_()

    def _restore_(self):
        self._entry_widget._do_clear_()

    def _set_entry_focus_(self, boolean):
        self._get_entry_widget_()._set_focused_(boolean)

    def _accept_element_(self, value):
        self._text_bubbles._create_one_(value)
        self.input_value_changed.emit()
        self.input_value_accepted.emit(value)

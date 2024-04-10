# coding=utf-8
import copy
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import abstracts as gui_qt_abstracts
# qt widgets
from . import base as gui_qt_wgt_base

from . import utility as gui_qt_wgt_utility

from . import button as gui_qt_wgt_button

from . import resize as gui_qt_wgt_resize

from . import entry as gui_qt_wgt_entry

from . import popup as gui_qt_wgt_popup

from . import bubble as gui_qt_wgt_bubble


class QtInputAsFilter(
    QtWidgets.QWidget,

    gui_qt_abstracts.AbsQtInputBaseDef,

    gui_qt_abstracts.AbsQtInputCompletionExtraDef,
    gui_qt_abstracts.AbsQtInputHistoryExtraDef,
):
    occurrence_previous_press_clicked = qt_signal()
    occurrence_next_press_clicked = qt_signal()

    occurrence_accepted = qt_signal(str)

    QT_ENTRY_CLS = gui_qt_wgt_entry.QtEntryAsConstant

    QT_COMPLETION_POPUP_CLS = gui_qt_wgt_popup.QtPopupAsCompletion

    QT_HISTORY_POPUP_CLS = gui_qt_wgt_popup.QtPopupAsHistory

    def _refresh_widget_all_(self):
        self.update()

    def _refresh_widget_draw_(self):
        pass

    def _pull_history_(self, value):
        self._accept_element_(value)

    def _refresh_history_extend_(self):
        self._history_button.show()
        if self._get_history_values_():
            self._history_button._set_action_enable_(True)
        else:
            self._history_button._set_action_enable_(False)

    def __init__(self, *args, **kwargs):
        super(QtInputAsFilter, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        qt_layout_0 = gui_qt_wgt_base.QtHBoxLayout(self)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(2)
        qt_layout_0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        #
        self._init_input_base_def_(self)
        #
        self._init_input_completion_extra_def_(self)
        #
        self._result_label = gui_qt_wgt_utility.QtTextItem()
        # todo: fix result show bug
        # self._result_label.hide()
        qt_layout_0.addWidget(self._result_label)
        #
        self._resize_handle = gui_qt_wgt_resize.QtHResizeHandle()
        self._resize_handle._set_resize_icon_file_paths_(
            [
                gui_core.GuiIcon.get('resize-handle-v'), gui_core.GuiIcon.get('resize-handle-v')
            ]
        )
        self._resize_handle._resize_frame_draw_size = 10, 20
        self._resize_handle._resize_icon_draw_size = 8, 16
        self._resize_handle._set_resize_alignment_(self._resize_handle.ResizeAlignment.Left)
        qt_layout_0.addWidget(self._resize_handle)
        self._resize_handle.setFixedWidth(8)
        #
        self._entry_frame_widget = gui_qt_wgt_entry.QtEntryFrame()
        self._entry_frame_widget.setFixedWidth(200)
        self._entry_frame_widget.setFixedHeight(24)
        self._resize_handle._set_resize_target_(self._entry_frame_widget)
        qt_layout_0.addWidget(self._entry_frame_widget)
        #
        self._build_input_entry_(str)
        #
        self._match_case_button = gui_qt_wgt_button.QtIconPressButton()
        self._match_case_button.hide()
        qt_layout_0.addWidget(self._match_case_button)
        self._match_case_button.setFocusProxy(self._entry_widget)
        self._match_case_button.press_clicked.connect(self._do_match_case_swap_)
        self._match_case_icon_names = 'match_case_off', 'match_case_on'
        self._is_match_case = False
        #
        self._match_word_button = gui_qt_wgt_button.QtIconPressButton()
        self._match_word_button.hide()
        qt_layout_0.addWidget(self._match_word_button)
        self._match_word_button.setFocusProxy(self._entry_widget)
        self._match_word_button.press_clicked.connect(self._do_match_word_swap_)
        self._match_word_icon_names = 'match_word_off', 'match_word_on'
        self._is_match_word = False
        # occurrence
        self._occurrence_previous_button = gui_qt_wgt_button.QtIconPressButton()
        qt_layout_0.addWidget(self._occurrence_previous_button)
        self._occurrence_previous_button._set_name_text_('occurrence previous')
        self._occurrence_previous_button._set_icon_file_path_(
            gui_core.GuiIcon.get('occurrence-previous-disable')
        )
        self._occurrence_previous_button._set_tool_tip_text_('"LMB-click" to occurrence previous result')
        self._occurrence_previous_button.press_clicked.connect(
            self.occurrence_previous_press_clicked.emit
        )
        #
        self._occurrence_next_button = gui_qt_wgt_button.QtIconPressButton()
        qt_layout_0.addWidget(self._occurrence_next_button)
        self._occurrence_next_button._set_name_text_('occurrence next')
        self._occurrence_next_button._set_icon_file_path_(
            gui_core.GuiIcon.get('occurrence-next-disable')
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
        self.__refresh_filter_()
        self._do_refresh_filter_tip_()

    def _build_input_entry_(self, value_type):
        self._value_type = value_type
        self._input_layout = gui_qt_wgt_base.QtHBoxLayout(self._entry_frame_widget)
        self._input_layout.setContentsMargins(2, 0, 2, 0)
        self._input_layout.setSpacing(0)
        #
        self._header_button = gui_qt_wgt_button.QtIconPressButton()
        self._header_button._set_icon_frame_draw_size_(18, 18)
        self._input_layout.addWidget(self._header_button)
        self._header_button._set_icon_file_path_(
            gui_core.GuiIcon.get(
                'search'
            )
        )
        #
        self.__text_bubbles = gui_qt_wgt_bubble.QtTextBubbles()
        self._input_layout.addWidget(self.__text_bubbles)
        #
        self._entry_widget = self.QT_ENTRY_CLS()
        self._input_layout.addWidget(self._entry_widget)
        #
        self._entry_widget.entry_value_changed.connect(self._do_input_change_)
        self._entry_widget.user_entry_value_changed.connect(self._do_user_input_change_)
        #
        self._entry_clear_button = gui_qt_wgt_button.QtIconPressButton()
        self._input_layout.addWidget(self._entry_clear_button)
        self._entry_clear_button.hide()
        self._entry_clear_button._set_icon_file_path_(
            gui_core.GuiIcon.get(
                'entry_clear'
            )
        )
        self._entry_clear_button._icon_draw_percent = .6
        self._entry_clear_button.press_clicked.connect(self._do_user_clear_entry_)
        #
        self._history_button = gui_qt_wgt_button.QtIconPressButton()
        self._input_layout.addWidget(self._history_button)
        # completion
        self._build_input_completion_()
        self.user_input_completion_finished.connect(self.input_value_changed)
        self.user_input_completion_value_accepted.connect(self._accept_element_)
        self.user_input_completion_value_accepted.connect(self._push_history_)
        #
        self._build_input_history_(self._history_button)
        self._entry_widget.entry_value_change_accepted.connect(self._push_history_)
        self._entry_widget.entry_value_change_accepted.connect(self.__text_bubbles._create_bubble_)
        #
        self.__text_bubbles._set_entry_widget_(self._entry_widget)
        self._entry_widget.textEdited.connect(self._do_refresh_filter_tip_)
        self._entry_widget.user_entry_text_accepted.connect(self.__text_bubbles._create_bubble_)
        self._entry_widget.user_entry_text_accepted.connect(self._push_history_)
        self._entry_widget.key_backspace_extra_pressed.connect(self.__text_bubbles._execute_bubble_backspace_)
        #
        self.__text_bubbles.bubbles_value_changed.connect(self._do_refresh_filter_tip_)
        self.__text_bubbles.bubbles_value_changed.connect(self._do_input_change_)
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
        _ = copy.copy(self.__text_bubbles._get_all_bubble_texts_())
        if self._entry_widget._get_value_():
            _.append(self._entry_widget._get_value_())
        return list(_)

    def __refresh_filter_(self):
        self._match_case_button._set_icon_file_path_(
            gui_core.GuiIcon.get(self._match_case_icon_names[self._is_match_case])
        )
        #
        self._match_word_button._set_icon_file_path_(
            gui_core.GuiIcon.get(self._match_word_icon_names[self._is_match_word])
        )

    def _do_match_case_swap_(self):
        self._is_match_case = not self._is_match_case
        self.__refresh_filter_()

        self._do_input_change_()

    def _do_match_word_swap_(self):
        self._is_match_word = not self._is_match_word
        self.__refresh_filter_()

        self._do_input_change_()

    def _clear_entry_(self):
        self._entry_widget._set_clear_()
        self._entry_widget.entry_value_cleared.emit()
        self._do_input_change_()

    def _do_user_clear_entry_(self):
        self._entry_widget._set_clear_()
        self._entry_widget.user_entry_value_cleared.emit()
        self._do_user_input_change_()

    def _set_occurrence_buttons_enable_(self, boolean):
        if boolean is True:
            self._occurrence_previous_button._set_icon_file_path_(
                gui_core.GuiIcon.get('occurrence-previous')
            )
            self._occurrence_next_button._set_icon_file_path_(
                gui_core.GuiIcon.get('occurrence-next')
            )
        else:
            self._occurrence_previous_button._set_icon_file_path_(
                gui_core.GuiIcon.get('occurrence-previous-disable')
            )
            self._occurrence_next_button._set_icon_file_path_(
                gui_core.GuiIcon.get('occurrence-next-disable')
            )

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
                    '{} / {}'.format(self._filter_index_current+1, self._filter_result_count)
                    )
            else:
                self._result_label._set_name_text_('1 / {}'.format(self._filter_result_count))
        else:
            self._result_label._set_name_text_('')

    def _set_result_clear_(self):
        self._filter_result_count = None
        self._filter_index_current = None
        self._refresh_filter_result_()

    def _restore_(self):
        self._entry_widget._set_clear_()

    def _set_entry_focus_(self, boolean):
        self._get_entry_widget_()._set_focused_(boolean)

    def _accept_element_(self, value):
        self.__text_bubbles._create_bubble_(value)
        self.input_value_changed.emit()
        self.input_value_change_accepted.emit(value)


class QtInputAsBubble(
    QtWidgets.QWidget,
):
    def __init__(self, *args, **kwargs):
        super(QtInputAsBubble, self).__init__(*args, **kwargs)

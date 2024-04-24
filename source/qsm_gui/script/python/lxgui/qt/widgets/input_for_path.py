# coding=utf-8
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import abstracts as gui_qt_abstracts
# qt widgets
from ..widgets import base as gui_qt_wgt_base

from ..widgets import button as gui_qt_wgt_button

from ..widgets import entry as gui_qt_wgt_entry

from ..widgets import entry_extend as gui_qt_wgt_entry_extend

from ..widgets import popup as gui_qt_wgt_popup


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
    def _refresh_choose_index_(self):
        pass

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

        self._buffer_fnc = lambda x: {}
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
        self._buffer_fnc = fnc

    def _update_next_cbk_(self, path):
        """
        buffer fnc always use thread
        """
        def cache_fnc_():
            _key = path.to_string()
            if _key in self.__buffer_cache:
                return [self._index_thread_batch, self.__buffer_cache[_key]]

            _data = self._buffer_fnc(path)
            self.__buffer_cache[_key] = _data
            return [self._index_thread_batch, _data]

        def build_fnc_(*args):
            _index_thread_batch_current, _dict = args[0]

            if _index_thread_batch_current != self._index_thread_batch:
                return

            if _dict:
                self._entry_extend_widget._set_next_name_texts_(
                    _dict.get('name_texts') or []
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
            else:
                self._entry_extend_widget._set_next_name_texts_(
                    []
                )
                self._set_choose_popup_item_image_url_dict_(
                    {}
                )
                self._set_choose_popup_item_keyword_filter_dict_(
                    {}
                )
                self._set_choose_popup_item_tag_filter_dict_(
                    {}
                )

        def post_fnc_():
            self._entry_extend_widget._do_next_wait_end_()

        self._index_thread_batch += 1

        # thread only use when widget is show
        # if self.isVisible() is True:
        #     self._entry_extend_widget._do_next_wait_start_()
        #     self._run_build_use_thread_(cache_fnc_, build_fnc_, post_fnc_)
        # else:
        #     build_fnc_(cache_fnc_())
        #     post_fnc_()
        # todo: always use thread
        self._entry_extend_widget._do_next_wait_start_()
        self._run_build_use_thread_(cache_fnc_, build_fnc_, post_fnc_)

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
# coding=utf-8
# gui
import time

import lxbasic.core as bsc_core

from .... import core as gui_core
# qt
from ...core.wrap import *

from ... import abstracts as gui_qt_abstracts
# qt widgets
from ..entry import cmp_entry_for_entity as _cmp_entry_for_path

from .. import base as _base

from .. import button as _button

from .. import entry_frame as _entry_frame

from .. import popup as _popup

from .. import entity as _entity_view


# path
class QtInputForEntity(
    _entry_frame.QtEntryFrame,
    gui_qt_abstracts.AbsQtInputBaseDef,
    # extra
    #   history
    gui_qt_abstracts.AbsQtInputHistoryExtraDef
):
    def _refresh_choose_index_(self):
        pass

    input_value_accepted = qt_signal(str)
    user_input_value_accepted = qt_signal(str)

    input_entry_key_enter_press = qt_signal()

    user_input_entry_finished = qt_signal()

    QT_CMP_ENTRY_CLS = _cmp_entry_for_path.QtCmpEntryForEntity

    QT_COMPLETION_POPUP_CLS = _popup.QtPopupForCompletion

    QT_HISTORY_POPUP_CLS = _popup.QtPopupForHistory

    def _pull_history_(self, value):
        self._set_value_(value)
        self.user_history_pull_accepted.emit(value)

    def _refresh_history_extend_(self):
        self._history_button.show()
        if self._get_history_values_():
            self._history_button._set_action_enable_(True)
        else:
            self._history_button._set_action_enable_(False)

    def __init__(self, *args, **kwargs):
        super(QtInputForEntity, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(gui_core.GuiSize.InputHeight)

        self._init_input_base_def_(self)
        # extra
        self._init_input_history_extra_def_(self)

        self._next_buffer_fnc = lambda x: {}
        self._next_buffer_cache = {}

        self._build_input_entry_()

        self._gui_thread_flag = 0

    def _build_input_entry_(self):
        self._entry_frame_widget = self

        entry_layout = _base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(2, 2, 2, 2)
        entry_layout.setSpacing(4)

        self._cmp_entry_widget = self.QT_CMP_ENTRY_CLS()
        entry_layout.addWidget(self._cmp_entry_widget)

        self._entry_widget = self._cmp_entry_widget._get_entry_widget_()
        self._entry_widget._set_entry_frame_(self)
        self._cmp_entry_widget.next_path_accepted.connect(self._on_next_path_accepted_)
        self.user_input_entry_finished = self._entry_widget.user_entry_finished

        self._history_button = _button.QtIconPressButton()
        entry_layout.addWidget(self._history_button)

        # history
        self._build_input_history_(self._history_button)
        self._cmp_entry_widget.entry_value_accepted.connect(self._push_history_)

        # choose popup
        self._choose_popup = _entity_view.QtEntityChooseStack(self)
        self._choose_popup._set_input_widget(self)
        self._choose_popup.hide()
        self._choose_popup.value_accepted.connect(self._accept_next_)

        self._cmp_entry_widget.next_press_clicked.connect(self._on_popup_choose)
        self._cmp_entry_widget.key_down_and_alt_pressed.connect(self._on_popup_choose)

        # completion popup
        self._completion_popup = _entity_view.QtEntityCompletionWidget(self)
        self._completion_popup._set_input_widget(self)
        self._completion_popup.hide()
        self._completion_popup.value_accepted.connect(self._accept_next_)

        self._entry_widget.entry_value_changed.connect(self._on_popup_completion)
        self._completion_popup.setFocusProxy(self._entry_widget)

        self._entry_widget.key_up_pressed.connect(self._completion_popup._on_occ_previous)
        self._entry_widget.key_down_pressed.connect(self._completion_popup._on_occ_next)
        self._entry_widget.key_enter_pressed.connect(self._completion_popup._on_accept)
        self._entry_widget.key_escape_pressed.connect(self._completion_popup._on_cancel)

        # other
        self.input_value_changed = self._cmp_entry_widget.entry_value_changed
        self.input_value_accepted = self._cmp_entry_widget.entry_value_accepted
        self.user_input_value_accepted = self._cmp_entry_widget.user_entry_value_accepted

    def _set_next_buffer_fnc_(self, fnc):
        self._next_buffer_fnc = fnc

    def _on_next_path_accepted_(self, path, post_fnc=None):
        """
        buffer fnc always use thread
        """
        def cache_fnc_():
            _time_start = time.time()
            _path_text = path.to_string()
            if _path_text in self._next_buffer_cache:
                _time_cost = time.time()-_time_start
                return [self._gui_thread_flag, _time_cost, self._next_buffer_cache[_path_text]]

            _data = self._next_buffer_fnc(path)
            self._next_buffer_cache[_path_text] = _data
            _time_cost = time.time()-_time_start
            return [self._gui_thread_flag, _time_cost, _data]

        def build_fnc_(*args):
            _index_thread_batch_current, _time_cost, _data = args[0]

            if _index_thread_batch_current != self._gui_thread_flag:
                return

            if _data:
                name_texts = _data.get('name_texts') or []
                # sort values
                name_texts = bsc_core.BscTexts.sort_by_number(name_texts)
                self._cmp_entry_widget._set_next_name_texts_(
                    name_texts
                )
                _type_text = _data.get('type_text')
                if _type_text:
                    self._cmp_entry_widget._set_entry_tip_(
                        '{} {} is found, cost {}s.'.format(
                            len(_data.get('name_texts') or []), _type_text, round(_time_cost, 2)
                        )
                    )
            else:
                self._cmp_entry_widget._set_next_name_texts_(
                    []
                )
                self._cmp_entry_widget._set_entry_tip_('')

        def post_fnc_():
            self._cmp_entry_widget._do_next_wait_end_()
            if post_fnc is not None:
                post_fnc()

        self._gui_thread_flag += 1

        self._cmp_entry_widget._set_entry_tip_('loading ...')
        # todo: always use thread
        self._cmp_entry_widget._do_next_wait_start_()
        self._run_build_extra_use_thread_(cache_fnc_, build_fnc_, post_fnc_)

    def _update_next_(self):
        self._cmp_entry_widget._update_next_()

    def _update_next_data_for_(self, path_text, post_fnc=None):
        if path_text in self._next_buffer_cache:
            self._next_buffer_cache.pop(path_text)

        self._on_next_path_accepted_(
            bsc_core.BscNodePathOpt(path_text), post_fnc
        )

    def _set_root_text_(self, text):
        self._cmp_entry_widget._set_root_text_(text)
        
    def _set_entry_tip_(self, text):
        self._cmp_entry_widget._set_entry_tip_(text)

    def _set_value_(self, value):
        self._cmp_entry_widget._set_path_text_(value)

    def _get_value_(self):
        return self._cmp_entry_widget._get_path_text_()

    def _setup_(self):
        self._cmp_entry_widget._update_next_()

    def _restore_next_cache_(self):
        self._next_buffer_cache = {}

    def _get_next_cache_(self):
        return self._next_buffer_cache.get(self._get_value_())

    def _accept_next_(self, text):
        self._cmp_entry_widget._enter_next_(text)

    def _on_popup_choose(self):
        data = self._get_next_cache_()
        if data:
            self._choose_popup._load_data(
                self._get_next_cache_()
            )
            self._choose_popup._popup()

    def _on_popup_completion(self):
        data = self._get_next_cache_()
        if data:
            keyword = self._entry_widget._get_value_()
            if keyword:
                if self._completion_popup._set_data(data, keyword):
                    self._completion_popup._popup()
                else:
                    self._completion_popup.hide()
            else:
                self._completion_popup.hide()
        else:
            self._completion_popup.hide()

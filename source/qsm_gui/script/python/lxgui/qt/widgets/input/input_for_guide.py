# coding=utf-8
import six

import fnmatch

import lxbasic.core as bsc_core
# gui
from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import core as _qt_core

from ....qt import abstracts as _qt_abstracts
# qt widgets
from .. import base as _wgt_base

from .. import button as _wgt_button

from .. import entry_frame as _wgt_entry_frame

from .. import popup as _wgt_popup

from ..entry import entry_for_constant as _entry_for_constant

from ..entry import etd_entry_for_guide as _etd_entry_for_guide


class QtInputForGuide(
    QtWidgets.QWidget,

    _qt_abstracts.AbsQtInputBaseDef,
    _qt_abstracts.AbsQtInputCompletionExtraDef,
):
    QT_ENTRY_CLS = _entry_for_constant.QtEntryForConstant
    QT_COMPLETION_POPUP_CLS = _wgt_popup.QtPopupForCompletion

    FILTER_COMPLETION_MAXIMUM = 50

    def _refresh_widget_draw_(self):
        self.update()

    def __init__(self, *args, **kwargs):
        super(QtInputForGuide, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self._init_input_base_def_(self)
        self._init_input_completion_extra_def_(self)

        self._guide_entry_mode = 0

        self._build_input_entry_(str)

    def _build_input_entry_(self, value_type):
        self._value_type = value_type

        qt_layout_0 = _wgt_base.QtHBoxLayout(self)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(0)
        qt_layout_0.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        self._entry_frame_widget = _wgt_entry_frame.QtEntryFrame()
        qt_layout_0.addWidget(self._entry_frame_widget)

        self._entry_frame_widget.setFixedHeight(24)

        self._input_layout = _wgt_base.QtHBoxLayout(self._entry_frame_widget)
        self._input_layout.setContentsMargins(2, 0, 2, 0)
        self._input_layout.setSpacing(2)

        self._guide_tree_button = _wgt_button.QtIconPressButton()
        self._input_layout.addWidget(self._guide_tree_button)
        self._guide_tree_button._set_icon_file_path_(_gui_core.GuiIcon.get('tree'))

        self._guide_entry = _etd_entry_for_guide.QtEtdEntryForGuide()
        self._input_layout.addWidget(self._guide_entry)

        self._guide_entry.entry_started.connect(
            self._guide_entry_started_cbk_
        )
        self._entry_widget = self.QT_ENTRY_CLS()
        self._entry_widget.hide()
        self._input_layout.addWidget(self._entry_widget)
        # self._entry_widget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self._entry_widget.key_escape_pressed.connect(self._guide_entry_finished_cbk_)
        self._entry_widget.focus_out.connect(self._set_guide_entry_finish_)
        self._entry_widget.setMinimumHeight(22)
        self._entry_widget.setMaximumHeight(22)
        self._entry_widget.setFont(_qt_core.QtFonts.Medium)
        #
        self._build_input_completion_()

        self._set_input_completion_buffer_fnc_(
            self._guide_value_completion_extra_gain_fnc_
        )
        self.user_input_completion_value_accepted.connect(self._guide_entry_cbk_)

    def _set_guide_entry_started_(self):
        self._guide_entry_mode = 1
        self._guide_entry.hide()
        self._entry_widget.show()

    def _guide_entry_started_cbk_(self):
        self._guide_entry_mode = 1
        self._guide_entry.hide()
        self._entry_widget.show()
        self._entry_widget._set_value_(self._guide_entry._get_guide_path_text_())
        self._entry_widget._set_focused_(True)
        self._entry_widget._set_all_selected_()

    def _set_guide_entry_finish_(self):
        self._guide_entry_mode = 0
        self._entry_widget.hide()
        self._guide_entry.show()

    def _guide_entry_finished_cbk_(self):
        self._set_guide_entry_finish_()
        self._guide_entry._set_focused_(True)

    # noinspection PyUnusedLocal
    def _guide_value_completion_extra_gain_fnc_(self, *args, **kwargs):
        keyword = args[0]
        if keyword:
            if isinstance(keyword, six.text_type):
                keyword = keyword.encode('utf-8')
            #
            path_texts = self._guide_entry._get_guide_valid_path_texts_()
            _ = fnmatch.filter(
                path_texts, '*{}*'.format(keyword)
            )
            return bsc_core.RawTextsMtd.sort_by_initial(_)[:self.FILTER_COMPLETION_MAXIMUM]
        return []

    def _guide_entry_cbk_(self, text):
        path_text_cur = text
        if path_text_cur:
            path_texts = self._guide_entry._get_guide_valid_path_texts_()
            if path_text_cur in path_texts:
                path_text_pre = self._guide_entry._get_guide_path_text_()
                if path_text_cur != path_text_pre:
                    self._guide_entry._set_guide_path_text_(path_text_cur)
                    # press
                    self._guide_entry.guide_text_press_accepted.emit(path_text_cur)
                    # any
                    self._guide_entry.guide_text_accepted.emit(path_text_cur)
                self._guide_entry_finished_cbk_()

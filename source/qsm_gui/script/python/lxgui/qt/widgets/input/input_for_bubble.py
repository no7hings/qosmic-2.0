# coding=utf-8
# gui
from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import abstracts as _qt_abstracts
# qt widgets
from .. import base as _wgt_base

from .. import popup as _wgt_popup

from ..entry import entry_for_bubble as _entry_for_bubble


class QtInputForBubbleChoose(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtInputBaseDef,

    _qt_abstracts.AbsQtInputChooseExtraDef,
):
    def _refresh_choose_index_(self):
        pass

    QT_ENTRY_CLS = _entry_for_bubble.QtEntryForTextBubble

    QT_POPUP_CHOOSE_CLS = _wgt_popup.QtPopupForChoose

    def _pull_history_(self, value):
        if value in self._choose_values:
            self._entry_widget._set_value_(value)

    def __init__(self, *args, **kwargs):
        super(QtInputForBubbleChoose, self).__init__(*args, **kwargs)
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

        entry_layout = _wgt_base.QtHBoxLayout(self)
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
        super(QtInputForBubbleChoose, self)._set_choose_values_(values, *args, **kwargs)
        self._entry_widget._set_value_options_(values, *args, **kwargs)

    def _bridge_choose_get_popup_texts_(self):
        return self._get_choose_values_()

    def _bridge_choose_get_popup_texts_current_(self):
        return [self._get_value_()]
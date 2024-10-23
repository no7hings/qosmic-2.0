# coding=utf-8
# gui
from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import core as _qt_core

from ....qt import abstracts as _qt_abstracts
# qt widgets
from .. import base as _wgt_base

from .. import entry_frame as _wgt_entry_frame

from .. import popup as _wgt_popup

from ..entry import entry_for_constant as _entry_for_constant


# rgba entry and choose
class QtInputForRgba(
    _wgt_entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputForOtherBaseDef,
    # extra
    #   choose
    _qt_abstracts.AbsQtInputChooseExtraDef,

    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,

    _qt_abstracts.AbsQtValueDefaultExtraDef,
):
    def _bridge_choose_get_popup_texts_(self):
        pass

    def _bridge_choose_get_popup_texts_current_(self):
        pass

    def _refresh_choose_index_(self):
        pass

    def _pull_history_(self, *args, **kwargs):
        pass

    QT_ENTRY_CLS = _entry_for_constant.QtEntryForConstant

    QT_POPUP_CHOOSE_CLS = _wgt_popup.QtPopupAsChooseForRgba

    def _refresh_widget_draw_geometry_(self):
        super(QtInputForRgba, self)._refresh_widget_draw_geometry_()
        #
        x, y = 0, 0
        w = h = self.height()
        c_w, c_h = w, h
        v_w, v_h = self._value_draw_width, self._value_draw_height
        self._value_rect.setRect(
            x, y, c_w, c_h
        )
        self._value_draw_rect.setRect(
            x + (c_w - v_w) / 2, y + (c_h - v_h) / 2, v_w, v_h
        )

    def __init__(self, *args, **kwargs):
        super(QtInputForRgba, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(_gui_core.GuiSize.InputHeight)

        self._init_input_choose_extra_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

        self._init_input_as_other_base_def_(self)
        self._init_value_default_extra_def_(self)

        self._build_input_entry_()

    def _get_value_rect_(self):
        return self._value_rect

    def _build_input_entry_(self):
        self._entry_frame_widget = self

        entry_layout = _wgt_base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(self._value_draw_width + 2, 0, 0, 0)
        entry_layout.setSpacing(2)

        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_value_type_(str)
        self._entry_widget._set_entry_use_as_rgba_255_(True)
        self._entry_widget.user_entry_finished.connect(self._refresh_widget_draw_)

        self._build_input_choose_()

    def eventFilter(self, *args):
        super(QtInputForRgba, self).eventFilter(*args)

        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._entry_is_enable is True:
                        if self._value_rect.contains(event.pos()):
                            self._set_action_flag_(self.ActionFlag.ChoosePress)

                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._is_action_flag_match_(
                            self.ActionFlag.ChoosePress
                    ) is True:
                        self.press_clicked.emit()
                        self._do_choose_popup_start_()

                self._clear_all_action_flags_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
        return False

    def paintEvent(self, event):
        super(QtInputForRgba, self).paintEvent(self)
        #
        painter = _qt_core.QtPainter(self)

        rgba = self._get_value_()
        offset = self._get_action_offset_()
        painter._draw_frame_by_rect_(
            self._value_draw_rect,
            border_color=_qt_core.QtRgba.Transparent,
            background_color=rgba,
            offset=offset
        )

    def _build_input_choose_(self):
        self._choose_popup_widget = self.QT_POPUP_CHOOSE_CLS(self)
        self._choose_popup_widget._set_entry_widget_(self._get_entry_widget_())
        self._choose_popup_widget._set_entry_frame_widget_(self._get_entry_frame_widget_())
        self._choose_popup_widget.hide()

    def _set_entry_enable_(self, boolean):
        super(QtInputForRgba, self)._set_entry_enable_(boolean)

        self._entry_widget._set_entry_enable_(boolean)

        self._update_background_color_by_locked_(boolean)
        #
        self._refresh_widget_all_()

    def _set_value_(self, value):
        self._entry_widget._set_value_as_rgba_255_(value)

    def _get_value_(self):
        return self._entry_widget._get_value_as_rgba_255_()


# icon entry and choose
class QtInputForIcon(
    _wgt_entry_frame.QtEntryFrame,
    _qt_abstracts.AbsQtInputForOtherBaseDef,
    # extra
    #   choose
    _qt_abstracts.AbsQtInputChooseExtraDef,

    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForHoverDef,
    _qt_abstracts.AbsQtActionForPressDef,
):
    def _pull_history_(self, *args, **kwargs):
        pass

    def _refresh_choose_index_(self):
        pass

    QT_ENTRY_CLS = _entry_for_constant.QtEntryForConstant

    QT_POPUP_CHOOSE_CLS = _wgt_popup.QtPopupAsChooseForIcon

    def _refresh_widget_draw_geometry_(self):
        super(QtInputForIcon, self)._refresh_widget_draw_geometry_()

        x, y = 0, 0
        w = h = self.height()
        c_w, c_h = w, h
        v_w, v_h = self._value_draw_width, self._value_draw_height
        self._value_rect.setRect(
            x, y, c_w, c_h
        )
        self._value_draw_rect.setRect(
            x + (c_w - v_w) / 2, y + (c_h - v_h) / 2, v_w, v_h
        )

    def __init__(self, *args, **kwargs):
        super(QtInputForIcon, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(_gui_core.GuiSize.InputHeight)

        self._init_input_as_other_base_def_(self)
        self._init_input_choose_extra_def_(self)

        self._init_action_base_def_(self)
        self._init_action_for_hover_def_(self)
        self._init_action_for_press_def_(self)

        self._build_input_entry_()

    def eventFilter(self, *args):
        super(QtInputForIcon, self).eventFilter(*args)

        widget, event = args
        if widget == self:
            self._execute_action_hover_by_filter_(event)
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._entry_is_enable is True:
                        if self._value_rect.contains(event.pos()):
                            self._set_action_flag_(self.ActionFlag.ChoosePress)

                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self._is_action_flag_match_(
                            self.ActionFlag.ChoosePress
                    ) is True:
                        self.press_clicked.emit()
                        self._do_choose_popup_start_()

                self._clear_all_action_flags_()
                self._refresh_widget_draw_()
            elif event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_draw_geometry_()
        return False

    def paintEvent(self, event):
        super(QtInputForIcon, self).paintEvent(self)
        #
        painter = _qt_core.QtPainter(self)

        icon_name = self._get_value_()
        if icon_name == '':
            icon_name = 'state-disable'

        icon_file_path = _gui_core.GuiIcon.get(icon_name)
        if icon_file_path:
            offset = self._get_action_offset_()

            painter._draw_icon_file_by_rect_(
                rect=self._value_draw_rect,
                file_path=icon_file_path,
                offset=offset
            )

    def _build_input_entry_(self):
        self._entry_frame_widget = self

        entry_layout = _wgt_base.QtHBoxLayout(self)
        entry_layout.setContentsMargins(self._value_draw_width + 2, 0, 0, 0)
        entry_layout.setSpacing(2)

        self._entry_widget = self.QT_ENTRY_CLS()
        entry_layout.addWidget(self._entry_widget)
        self._entry_widget._set_value_type_(str)
        self._entry_widget.user_entry_finished.connect(self._refresh_widget_draw_)

        self._build_input_choose_()

    def _build_input_choose_(self):
        self._choose_popup_widget = self.QT_POPUP_CHOOSE_CLS(self)
        self._choose_popup_widget._set_entry_widget_(self._get_entry_widget_())
        self._choose_popup_widget._set_entry_frame_widget_(self._get_entry_frame_widget_())
        self._choose_popup_widget.hide()

        self._choose_popup_widget.user_popup_value_accepted.connect(
            self._do_choose_accept_
        )

    def _do_choose_accept_(self, text):
        self._set_value_(text)
        self._refresh_widget_draw_()

    def _set_entry_enable_(self, boolean):
        super(QtInputForIcon, self)._set_entry_enable_(boolean)

        self._entry_widget._set_entry_enable_(boolean)

        self._update_background_color_by_locked_(boolean)
        #
        self._refresh_widget_all_()

    # choose extra
    def _bridge_choose_get_popup_texts_(self):
        return self._get_choose_values_()

    def _bridge_choose_get_popup_texts_current_(self):
        return [self._get_value_()]
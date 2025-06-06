# coding=utf-8
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core
# qt widgets
from . import utility as gui_qt_wgt_utility

from . import button as gui_qt_wgt_button


class AbsQtScrollBox(gui_qt_wgt_utility.QtLineWidget):
    QT_ORIENTATION = None

    def _refresh_widget_all_(self, fix_bug=False):
        self._refresh_widget_draw_geometry_(fix_bug=fix_bug)
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self, fix_bug=False):
        super(AbsQtScrollBox, self)._refresh_widget_draw_geometry_()

        if fix_bug is True:
            w, h = self.width(), self.height()
            self._viewport.resize(int(w/2), h)
            self._viewport.resize(w, h)
            self._viewport.hide()
            self._viewport.show()

        x, y = 0, 0
        w, h = self.width(), self.height()

        if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
            v_w = self._viewport.layout().minimumSize().width()

            abs_w = max(w, v_w)
            self._scroll_bar_model.set_w_or_h(w)
            self._scroll_bar_model.set_abs_w_or_h(abs_w)
            self._scroll_bar_model.update()
            if self._scroll_bar_model.is_valid():
                value_scroll = self._scroll_bar_model.get_value()

                btn_f_w, btn_f_h = 24, h-2
                btn_w, btn_h = 20, 20

                btn_w_1, btn_h_1 = btn_w/2, btn_h
                btn_f_r = btn_f_w
                c_x_1, c_y_1 = w-btn_f_r, y+1
                c_x_1 = max(c_x_1, btn_f_r)

                self._scroll_button_frame.show()
                self._scroll_button_frame.setGeometry(
                    int(c_x_1), int(c_y_1), int(btn_f_r), int(btn_f_h)
                )

                self._scroll_previous_button.show()
                self._scroll_previous_button.setGeometry(
                    int(c_x_1+(btn_f_w-btn_w)/2), int(y+(h-btn_h_1)/2), int(btn_w_1), int(btn_h_1)
                )
                if self._scroll_bar_model.get_is_minimum():
                    self._scroll_previous_button._set_icon_file_path_(self._icons_0[1])
                else:
                    self._scroll_previous_button._set_icon_file_path_(self._icons_0[0])

                self._scroll_next_button.show()
                self._scroll_next_button.setGeometry(
                    int(c_x_1+(btn_f_w-btn_w)/2+btn_w_1), int(y+(h-btn_h_1)/2), int(btn_w_1), int(btn_h_1)
                )
                if self._scroll_bar_model.get_is_maximum():
                    self._scroll_next_button._set_icon_file_path_(self._icons_1[1])
                    value_scroll += btn_f_w
                else:
                    self._scroll_next_button._set_icon_file_path_(self._icons_1[0])

                self._viewport.setGeometry(
                    int(x-value_scroll), int(y), int(abs_w), int(h)
                )
            else:
                self._scroll_button_frame.hide()
                self._scroll_previous_button.hide()
                self._scroll_next_button.hide()
                self._viewport.setGeometry(
                    int(x), int(y), int(abs_w), int(h)
                )

        elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
            v_h = self._viewport.layout().minimumSize().height()
            abs_h = max(h, v_h)
            self._scroll_bar_model.set_w_or_h(h)
            self._scroll_bar_model.set_abs_w_or_h(abs_h)
            self._scroll_bar_model.update()

            if self._scroll_bar_model.is_valid():
                value_scroll = self._scroll_bar_model.get_value()

                btn_f_w, btn_f_h = w-2, 24
                btn_w, btn_h = 20, 20

                btn_w_1, btn_h_1 = btn_w, btn_h/2
                btn_f_r = btn_f_h
                c_x_1, c_y_1 = x+1, h-btn_f_r
                c_y_1 = max(c_y_1, btn_f_r)

                self._scroll_button_frame.show()
                self._scroll_button_frame.setGeometry(
                    int(c_x_1), int(c_y_1), int(btn_f_r), int(btn_f_h)
                )

                self._scroll_previous_button.show()
                self._scroll_previous_button.setGeometry(
                    int(x+(w-btn_w)/2), int(c_y_1+(btn_f_h-btn_h_1)/2), int(btn_w_1), int(btn_h_1)
                )
                if self._scroll_bar_model.get_is_minimum():
                    self._scroll_previous_button._set_icon_file_path_(self._icons_0[1])
                else:
                    self._scroll_previous_button._set_icon_file_path_(self._icons_0[0])

                self._scroll_next_button.show()
                self._scroll_next_button.setGeometry(
                    int(x+(w-btn_w)/2), int(c_y_1+(btn_f_h-btn_h_1)/2+btn_h_1), int(btn_w_1), int(btn_h_1)
                )
                if self._scroll_bar_model.get_is_maximum():
                    self._scroll_next_button._set_icon_file_path_(self._icons_1[1])
                    value_scroll += btn_f_h
                else:
                    self._scroll_next_button._set_icon_file_path_(self._icons_1[0])

                self._viewport.setGeometry(
                    int(x), int(y-value_scroll), int(w), int(abs_h)
                )
            else:
                self._scroll_button_frame.hide()
                self._scroll_previous_button.hide()
                self._scroll_next_button.hide()

                self._viewport.setGeometry(
                    int(x), int(y), int(w), int(abs_h)
                )

    def __init__(self, *args, **kwargs):
        super(AbsQtScrollBox, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._viewport = QtWidgets.QWidget(self)
        self._viewport.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
            self.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
            )
            self._viewport.setSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
            )
            self._layout = QtWidgets.QHBoxLayout(self._viewport)
        elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
            self.setSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
            )
            self._viewport.setSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
            )
            self._layout = QtWidgets.QVBoxLayout(self._viewport)
        else:
            raise RuntimeError()

        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(2)

        self._scroll_bar_model = gui_qt_core.GuiQtModForScroll()
        self._scroll_bar_model.set_step(64)

        self._scroll_button_frame = gui_qt_wgt_utility.QtButtonFrame(self)
        self._scroll_button_frame.hide()

        self._scroll_previous_button = gui_qt_wgt_button.QtIconPressButton(self)
        self._scroll_previous_button.hide()
        self._scroll_previous_button._set_icon_geometry_mode_(
            gui_qt_wgt_button.QtIconPressButton.IconGeometryMode.Auto
        )

        self._scroll_next_button = gui_qt_wgt_button.QtIconPressButton(self)
        self._scroll_next_button.hide()
        self._scroll_next_button._set_icon_geometry_mode_(
            gui_qt_wgt_button.QtIconPressButton.IconGeometryMode.Auto
        )
        if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
            self._icons_0 = [
                gui_core.GuiIcon.get('window_base/scroll-left'),
                gui_core.GuiIcon.get('window_base/scroll-left-disable')
            ]
            self._icons_1 = [
                gui_core.GuiIcon.get('window_base/scroll-right'),
                gui_core.GuiIcon.get('window_base/scroll-right-disable')
            ]
            self._scroll_previous_button.setFixedSize(10, 20)
            self._scroll_next_button.setFixedSize(10, 20)
        elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
            self._icons_0 = [
                gui_core.GuiIcon.get('window_base/scroll-up'),
                gui_core.GuiIcon.get('window_base/scroll-up-disable')
            ]
            self._icons_1 = [
                gui_core.GuiIcon.get('window_base/scroll-down'),
                gui_core.GuiIcon.get('window_base/scroll-down-disable')
            ]
            self._scroll_previous_button.setFixedSize(20, 10)
            self._scroll_next_button.setFixedSize(20, 10)
        else:
            raise RuntimeError()
        self._scroll_previous_button._set_icon_file_path_(self._icons_0[0])
        self._scroll_next_button._set_icon_file_path_(self._icons_1[0])

        self._scroll_previous_button.press_clicked.connect(self._do_scroll_previous_)
        self._scroll_next_button.press_clicked.connect(self._do_scroll_next_)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
            elif event.type() == QtCore.QEvent.Wheel:
                self._do_wheel_(event)
        return False

    def _do_wheel_(self, event):
        if self._scroll_bar_model.is_valid():
            delta = event.angleDelta().y()
            if delta < 0:
                self._do_scroll_next_()
            else:
                self._do_scroll_previous_()

    def _get_viewport_(self):
        return self._viewport

    def _get_layout_(self):
        return self._layout

    def _set_layout_align_left_or_top_(self):
        if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
            self._layout.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
            self._layout.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        else:
            raise RuntimeError()

    def _do_scroll_previous_(self):
        if self._scroll_bar_model.step_to_previous() is True:
            self._refresh_widget_all_()

    def _do_scroll_next_(self):
        if self._scroll_bar_model.step_to_next() is True:
            self._refresh_widget_all_()

    def addWidget(self, *args, **kwargs):
        self._layout.addWidget(*args, **kwargs)

    def insertWidget(self, *args, **kwargs):
        self._layout.insertWidget(*args, **kwargs)


class QtHScrollBox(AbsQtScrollBox):
    QT_ORIENTATION = QtCore.Qt.Horizontal

    def __init__(self, *args, **kwargs):
        super(QtHScrollBox, self).__init__(*args, **kwargs)


class QtVScrollBox(AbsQtScrollBox):
    QT_ORIENTATION = QtCore.Qt.Vertical

    def __init__(self, *args, **kwargs):
        super(QtVScrollBox, self).__init__(*args, **kwargs)

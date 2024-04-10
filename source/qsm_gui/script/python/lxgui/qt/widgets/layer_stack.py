# coding=utf-8
# gui
from ... import core as gui_core
# qt
from ..core.wrap import *

from .. import core as gui_qt_core


class QtLayer(QtWidgets.QWidget):
    DELAY_TIME = 250
    DELAY_TIME_FPS = 25

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        _x_, _y_ = self.x(), self.y()
        if self.__swap_flag is True:
            index = min(self.__anim_index, self.__anim_index_maximum)
            d = sum([(0.5/(2**i))*1 for i in range(index)])
            c_w, c_h = self.__swap_width_mark, self.__swap_height_mark
            if self.__swap_mode == 'hide':
                c_h_d = c_h*d
                _c_h_ = c_h - c_h_d
                # self.setGeometry(x_, y_, w, c_h_)
                if self.__anim_index == self.__anim_index_maximum:
                    self.hide()
            elif self.__swap_mode == 'show':
                _c_h_d = c_h*d
                if self.__anim_index == self.__anim_index_maximum:
                    pass
        else:
            self._viewport.setGeometry(
                x, y, w, h
            )

    def __init__(self, *args, **kwargs):
        super(QtLayer, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )

        self.__anim_cycle_msec = 1000/self.DELAY_TIME_FPS
        self.__anim_timer = QtCore.QTimer(self)
        self.__anim_index_maximum = int(self.DELAY_TIME/self.__anim_cycle_msec)
        self.__anim_timer.timeout.connect(self.__do_swap_start)
        self.__anim_index = 0

        self.__swap_flag = False
        self.__swap_switch_direction = gui_core.GuiDirection.TopToBottom

        self.__swap_mode = 'hide'
        
        self.__swap_width_mark, self.__swap_height_mark = 0, 0
        self.__swap_width_maximum_mark, self.__swap_height_maximum_mark = 166667, 166667
        self.__swap_width_minimum_mark, self.__swap_height_minimum_mark = 0, 0

        self._viewport = QtWidgets.QWidget(self)
        self._layout = QtWidgets.QVBoxLayout(self._viewport)
        self._layout.setContentsMargins(*[0]*4)
        self._layout.setSpacing(0)

        self._viewport.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        elif widget == self._viewport:
            # auto update minimum size
            if event.type() == QtCore.QEvent.ChildPolished:
                self.setMinimumSize(self._layout.minimumSize())
            elif event.type() == QtCore.QEvent.Resize:
                self.setMinimumSize(self._layout.minimumSize())
        return False

    def _show_delay_(self):
        self.__do_swap_stop()
        if self.isVisible() is False:
            self._set_visible_delay_(True)

    def _hide_delay_(self):
        self.__do_swap_stop()
        if self.isVisible() is True:
            self._set_visible_delay_(False)

    def _set_visible_delay_(self, boolean):
        if boolean is True:
            self.__swap_mode = 'show'
            # self.setMaximumHeight(self.__swap_height_maximum_mark)
            self.show()
            self.__swap_flag = True
            self.__anim_timer.start(self.__anim_cycle_msec)
        else:
            self.__swap_mode = 'hide'
            w, h = self.width(), self.height()
            self.__swap_width_mark, self.__swap_height_mark = w, h
            self.__swap_width_maximum_mark, self.__swap_height_maximum_mark = self.maximumWidth(), self.maximumHeight()
            self.__swap_width_minimum_mark, self.__swap_height_minimum_mark = self.minimumWidth(), self.minimumHeight()
            self.__swap_flag = True
            self.__anim_timer.start(self.__anim_cycle_msec)

    def _add_widget_(self, widget):
        self._layout.addWidget(widget)

    def __do_swap_start(self):
        if self.__anim_index == self.__anim_index_maximum:
            self.__do_swap_stop()
        else:
            self.__anim_index += 1

            self._refresh_widget_all_()

    def __do_swap_stop(self):
        if self.__swap_flag is True:
            self.__swap_flag = False

            if self.__swap_mode == 'hide':
                self.hide()
            elif self.__swap_mode == 'show':
                self.setMaximumHeight(166667)

            self.__anim_index = 0
            self.__anim_timer.stop()

            self._refresh_widget_all_()


class QtLayerStack(QtWidgets.QWidget):
    current_changed = qt_signal()

    DELAY_TIME = 250
    DELAY_TIME_FPS = 25

    def __init__(self, *args, **kwargs):
        super(QtLayerStack, self).__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self.__widgets = []
        self.__count = 0

        self.__index_current = 0
        self.__index_pre = None
        self.__index_swap = None

        self.__anim_cycle_msec = 1000/self.DELAY_TIME_FPS
        self.__anim_timer = QtCore.QTimer(self)
        self.__anim_index_maximum = int(self.DELAY_TIME/self.__anim_cycle_msec)
        self.__anim_timer.timeout.connect(self.__do_swap_start)
        self.__anim_index = 0

        self.__swap_pixmap_0, self.__swap_pixmap_1 = None, None

        self.__swap_rect_0, self.__swap_rect_1 = QtCore.QRect(), QtCore.QRect()

        self.__swap_flag = False
        self.__swap_switch_direction = gui_core.GuiDirection.LeftToRight

        self.__swap_mode = 'switch'

        self.__anim_enable = True

    def _set_animation_enable_(self, boolean):
        self.__anim_enable = boolean

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self.update()

    def _refresh_widget_draw_geometry_(self):
        x, y = 0, 0
        w, h = self.width(), self.height()
        if self.__swap_flag is True and self.__anim_enable is True:
            index = min(self.__anim_index, self.__anim_index_maximum)
            d = sum([(0.5/(2**i))*1 for i in range(index)])
            if self.__swap_mode == 'switch':
                w_d = w*d
                if self.__swap_switch_direction == gui_core.GuiDirection.LeftToRight:
                    self.__swap_rect_0.setRect(
                        x-w_d, y, w, h
                    )
                    self.__swap_rect_1.setRect(
                        w-w_d, y, w, h
                    )
                elif self.__swap_switch_direction == gui_core.GuiDirection.RightToLeft:
                    self.__swap_rect_0.setRect(
                        x+w_d, y, w, h
                    )
                    self.__swap_rect_1.setRect(
                        x-w+w_d, y, w, h
                    )
            elif self.__swap_mode == 'delete':
                h_d = h*d
                self.__swap_rect_0.setRect(
                    x, y-h_d, w, h
                )
                self.__swap_rect_1.setRect(
                    x, h-h_d, w, h
                )
            elif self.__swap_mode == 'delete_latest':
                h_d = h*d
                self.__swap_rect_0.setRect(
                    x, y-h_d, w, h
                )
                self.__swap_rect_1.setRect(
                    x, y-h_d, w, h
                )
            elif self.__swap_mode == 'add':
                s = 20
                c_w, c_h = w-s, 10
                c_x, c_y = x+(w-c_w)/2, y+s
                w_d = c_w*d
                self.__swap_rect_0.setRect(
                    c_x, c_y, c_w, c_h
                )
                self.__swap_rect_1.setRect(
                    c_x, c_y, w_d, c_h
                )
            elif self.__swap_mode == 'new':
                s = 20
                c_w, c_h = w-s, 10
                c_x, c_y = x+(w-c_w)/2, y+s
                w_d = c_w*d
                self.__swap_rect_0.setRect(
                    c_x, c_y, c_w, c_h
                )
                self.__swap_rect_1.setRect(
                    c_x, c_y, w_d, c_h
                )
        else:
            for i_index, i_widget in enumerate(self.__widgets):
                i_widget.setGeometry(
                    x, y, w, h
                )
                if i_index == self.__index_current:
                    i_widget.show()
                else:
                    i_widget.hide()

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def paintEvent(self, event):
        if self.__swap_flag is True and self.__anim_enable is True:
            painter = gui_qt_core.QtPainter(self)
            if self.__swap_mode in {'add', 'new'}:
                painter._draw_alternating_colors_by_rect_(
                    rect=self.__swap_rect_0,
                    colors=((0, 0, 0, 63), (0, 0, 0, 0)),
                    running=True,
                    border_radius=5
                )
                painter._draw_frame_by_rect_(
                    rect=self.__swap_rect_1,
                    border_color=gui_qt_core.QtBorderColors.Button,
                    background_color=gui_core.GuiRgba.LightOrange,
                    border_radius=5,
                    border_width=2
                )
            else:
                painter.drawPixmap(
                    self.__swap_rect_0,
                    self.__swap_pixmap_0
                )
                painter.drawPixmap(
                    self.__swap_rect_1,
                    self.__swap_pixmap_1
                )

    # noinspection PyUnusedLocal
    def _add_widget_(self, widget, *args, **kwargs):
        widget.setParent(self)
        index = len(self.__widgets)
        self.__widgets.append(widget)
        if index == 0:
            self._refresh_widget_all_()
        elif index > 0:
            widget.hide()

        self.__count += 1
        #
        if 'switch_to' in kwargs:
            if kwargs['switch_to'] is True:
                index_pre = self.__index_current
                self.__index_current = index
                if index == 0:
                    self._swap_current_between_(index, index, 'new')
                else:
                    self._swap_current_between_(index_pre, index, 'add')

        return index

    def _switch_current_to_(self, index):
        if index < self.__count:
            self.__do_swap_stop()
            if index != self.__index_current:
                if self.__index_current is not None:
                    self.__index_pre = self.__index_current
                if self.__index_pre is not None:
                    # do swap
                    self.__index_current = index
                    self._swap_current_between_(self.__index_pre, self.__index_current, 'switch')
                else:
                    self.__index_current = index
                    self._refresh_widget_all_()

                self.current_changed.emit()

    def _set_current_index_(self, index):
        self.__index_current = index
        self._refresh_widget_all_()

    def _get_current_index_(self):
        return self.__index_current

    def _set_current_widget_(self, widget):
        if widget in self.__widgets:
            index = self.__widgets.index(widget)
            self._set_current_index_(index)

    def _switch_current_widget_to_(self, widget):
        if widget in self.__widgets:
            index = self.__widgets.index(widget)
            self._switch_current_to_(index)

    def _swap_current_between_(self, index_0, index_1, mode):
        if index_0 < index_1:
            self.__swap_switch_direction = gui_core.GuiDirection.LeftToRight
        else:
            self.__swap_switch_direction = gui_core.GuiDirection.RightToLeft

        self.__swap_mode = mode
        # x, y = 0, 0
        w, h = self.width(), self.height()
        wgt_0, wgt_1 = self.__widgets[index_0], self.__widgets[index_1]
        # wgt_0.setGeometry(x, y, w, h)
        self.__swap_pixmap_0, self.__swap_pixmap_1 = QtGui.QPixmap(w, h), QtGui.QPixmap(w, h)
        self.__swap_pixmap_0.fill(gui_qt_core.QtBackgroundColors.Basic)
        wgt_0.render(self.__swap_pixmap_0)
        self.__swap_pixmap_1.fill(gui_qt_core.QtBackgroundColors.Basic)
        # wgt_1.setGeometry(x, y, w, h)
        wgt_1.render(self.__swap_pixmap_1)
        self.__swap_flag = True

        # self._refresh_widget_all_()

        wgt_0.hide()
        self.__anim_timer.start(self.__anim_cycle_msec)

    def __do_swap_start(self):
        if self.__anim_index == self.__anim_index_maximum:
            self.__do_swap_stop()
        else:
            self.__anim_index += 1

            self._refresh_widget_all_()

    def __do_swap_stop(self):
        if self.__swap_flag is True:
            self.__swap_flag = False

            self.__anim_index = 0
            self.__anim_timer.stop()
            self.__swap_pixmap_0, self.__swap_pixmap_1 = None, None

            self._refresh_widget_all_()

    def _delete_widget_at_(self, index):
        if index < self.__count:
            widget = self.__widgets[index]
            # switch to next
            if index == 0:
                index_next = 0
            else:
                index_next = index-1

            if index == self.__index_current:
                if index == index_next == 0:
                    self._swap_current_between_(index, index_next, 'delete_latest')
                else:
                    self._swap_current_between_(index, index_next, 'delete')

            widget.close()
            widget.deleteLater()
            self.__widgets.pop(index)
            self.__count -= 1
            # update index maximum
            index_maximum = self.__count-1
            if self.__index_current > index_maximum:
                self.__index_current = index_maximum

    def _insert_widget_between_(self, index_0, index_1):
        widget_0 = self.__widgets[index_0]
        self.__widgets.pop(index_0)
        self.__widgets.insert(index_1, widget_0)

        self._set_current_index_(index_1)

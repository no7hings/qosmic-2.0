# coding=utf-8
# qt
import enum

from ...qt.core.wrap import *

from ...qt import core as _qt_core

from ...qt import abstracts as _qt_abstracts
# qt widgets
from . import base as _base

from . import utility as _utility

from . import head as _head

from . import drag as _drag

from . import scroll as _scroll


class AbsQtToolGroup(
    QtWidgets.QWidget,
    _qt_abstracts.AbsQtActionBaseDef,
    _qt_abstracts.AbsQtActionForDragDef,

    _qt_abstracts.AbsQtItemLayoutBaseDef,
):
    QT_HEAD_HEIGHT = 22

    QT_HEAD_CLS = None

    def __init__(self, *args, **kwargs):
        super(AbsQtToolGroup, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )

        self._init_action_base_def_(self)
        self._init_action_for_drag_def_(self)

        self._init_item_layout_base_def_(self)

        self.__base_layout = _base.QtVBoxLayout(self)
        self.__base_layout.setAlignment(QtCore.Qt.AlignTop)
        self.__base_layout.setContentsMargins(0, 0, 0, 0)
        self.__base_layout.setSpacing(2)

        self.__head = self.QT_HEAD_CLS()
        self.__base_layout.addWidget(self.__head)
        self.__head.setFixedHeight(self.QT_HEAD_HEIGHT)
        self.__head.expand_toggled.connect(self._set_expanded_)
        self.__head._set_tool_tip_text_('"LMB-click" expand tool group')

        self._view_widget = _utility.QtTranslucentWidget()
        self.__base_layout.addWidget(self._view_widget)
        self._view_layout = _base.QtVBoxLayout(self._view_widget)
        self._view_layout.setContentsMargins(2, 0, 0, 0)
        self._view_layout.setSpacing(2)

        self._refresh_expand_()

        self.installEventFilter(self)
        self.__head.installEventFilter(self)

        self._drag_press_point = QtCore.QPoint()
        self._drag_offset_move_x, self._drag_offset_move_y = 0, 0

        self.__drag_expand_mark = False

    def _refresh_widget_all_(self):
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        pass

    def eventFilter(self, *args):
        widget, event = args
        if widget == self.__head:
            if event.type() == QtCore.QEvent.MouseMove:
                if self._drag_is_enable is True:
                    if self.__head._is_action_flag_match_(self.ActionFlag.Press):
                        self._drag_press_point = self.__head._get_press_point_()
                        self.__head._set_action_flag_(self.ActionFlag.DragPress)
                    elif self.__head._is_action_flag_match_(self.ActionFlag.DragPress):
                        self._do_drag_press_(event)
                    elif self.__head._is_action_flag_match_(self.ActionFlag.DragMove):
                        self._do_drag_move_(event)
        return False

    def _do_drag_press_(self, event):
        p = event.pos()
        p_d = p-self._drag_press_point
        x, y = p_d.x(), p_d.y()
        # enable when mouse moved more than 10 pixel
        if abs(x) > 10 or abs(y) > 10:
            self.__head._set_action_flag_(self.ActionFlag.DragMove)
            self._set_action_flag_(self.ActionFlag.DragMove)
            event.accept()

    # noinspection PyUnusedLocal
    def _do_drag_move_(self, event):
        self.__drag = _drag.QtDrag(self.__head)

        item = self._get_layout_item_()
        if item:
            key = item.get_drag_and_drop_key()
            self._set_drag_data_(
                {'lynxi/drag-and-drop-key': key}
            )

            self.__drag.setMimeData(self._generate_drag_mime_data_())

            self.__drag._do_drag_move_(self._drag_press_point)

            self.__drag.released.connect(self._drag_release_cbk_)

            self._refresh_widget_draw_()

    def _drag_release_cbk_(self):
        self.__head._clear_all_action_flags_()
        self.__head._clear_hover_()
        l_i = self._get_layout_item_()
        if l_i is not None:
            l_i.get_layout_view()._drag_release_cbk_()

        self._clear_all_action_flags_()
        self._refresh_widget_all_()

    def _refresh_expand_(self):
        boolean = self._get_is_expanded_()
        self._view_widget.setVisible(
            boolean
        )
        if boolean is True:
            self.__head._set_tool_tip_text_('"LMB-click" collapse tool group')
        else:
            self.__head._set_tool_tip_text_('"LMB-click" expand tool group')

    def _add_widget_(self, widget):
        self._view_layout.addWidget(widget)

    def _prepend_widget_(self, widget):
        self._view_layout.insertWidget(0, widget)

    def _get_widgets_(self):
        list_ = []
        lot = self._view_layout
        c = lot.count()
        for i_idx in range(c):
            i_item = lot.itemAt(i_idx)
            if i_item is not None:
                i_widget = i_item.widget()
                list_.append(i_widget)
        return list_

    def _set_name_text_(self, text):
        self.__head._set_name_text_(text)

    def _get_name_text_(self):
        return self.__head._get_name_text_()

    def _set_tool_tip_text_(self, text):
        self.__head._set_tool_tip_text_(text)

    def _set_expanded_(self, boolean):
        self.__head._set_expanded_(boolean)
        self._refresh_expand_()

    def _get_is_expanded_(self):
        return self.__head._get_is_expanded_()

    def _get_layout_minimum_size_(self):
        return self.__base_layout.minimumSize()

    def _start_drag_mode_(self):
        if self._get_is_expanded_() is True:
            self._view_widget.hide()

    def _end_drag_mode_(self):
        if self._get_is_expanded_() is True:
            self._view_widget.show()


class QtHToolGroupStyleA(AbsQtToolGroup):
    QT_HEAD_CLS = _head.QtHeadStyleA

    def __init__(self, *args, **kwargs):
        super(QtHToolGroupStyleA, self).__init__(*args, **kwargs)


class QtHToolGroupStyleB(AbsQtToolGroup):
    QT_HEAD_CLS = _head.QtHeadStyleB

    def __init__(self, *args, **kwargs):
        super(QtHToolGroupStyleB, self).__init__(*args, **kwargs)


class QtHToolGroupStyleC(AbsQtToolGroup):
    QT_HEAD_CLS = _head.QtHeadStyleC

    def __init__(self, *args, **kwargs):
        super(QtHToolGroupStyleC, self).__init__(*args, **kwargs)


class AbsQtToolBox(QtWidgets.QWidget):
    class SizeMode(enum.IntEnum):
        Fixed = 0
        Expanding = 1

    QT_HEAD_CLS = None
    QT_ORIENTATION = None
    QT_HEAD_W, QT_HEAD_H = 12, 24

    def __init__(self, *args, **kwargs):
        super(AbsQtToolBox, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setSizePolicy(
        #     QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        # )
        self._build_widget_()

    def _build_widget_(self):
        if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
            lot = _base.QtHBoxLayout(self)
        elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
            lot = _base.QtVBoxLayout(self)
        else:
            raise RuntimeError()

        self.setMaximumSize(self.QT_HEAD_W, self.QT_HEAD_H)

        lot.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        lot.setContentsMargins(*[0]*4)
        lot.setSpacing(0)
        # header
        self._head = self.QT_HEAD_CLS()
        lot.addWidget(self._head)
        self._head.expand_toggled.connect(self._set_expanded_)
        self._head._set_tool_tip_text_('"LMB-click" to expand "on" / "off"')
        self._head.setFixedSize(self.QT_HEAD_W, self.QT_HEAD_H)

        self._body = QtWidgets.QWidget()
        lot.addWidget(self._body)
        if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
            self._layout = _base.QtHBoxLayout(self._body)
        elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
            self._layout = _base.QtVBoxLayout(self._body)
        else:
            raise RuntimeError()

        self._layout.setContentsMargins(*[0]*4)
        self._layout.setSpacing(2)
        # self._layout.setAlignment(QtCore.Qt.AlignLeft)

        self._refresh_expand_()
        self._set_size_mode_(0)

    def _refresh_expand_(self):
        self._body.setVisible(self._get_is_expanded_())
        self._head._refresh_expand_()

        self._refresh_widget_size_()

    def _refresh_widget_size_(self):
        if self._get_is_expanded_() is True:
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                self.setMaximumWidth(166667)
            else:
                self.setMaximumHeight(166667)
        else:
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                self.setMaximumWidth(self.QT_HEAD_W)
            else:
                self.setMaximumHeight(self.QT_HEAD_H)

    def _set_expanded_(self, boolean):
        self._head._set_expanded_(boolean)
        self._refresh_expand_()

    def _refresh_container_size_(self):
        pass

    def _get_is_expanded_(self):
        return self._head._get_is_expanded_()

    def _add_widget_(self, widget):
        if isinstance(widget, QtCore.QObject):
            self._layout.addWidget(widget)
        else:
            self._layout.addWidget(widget._qt_widget)

        self._refresh_widget_size_()

    def _set_name_text_(self, text):
        self._head._set_name_text_(text)
        
    def _set_visible_(self, boolean):
        self.setVisible(boolean)
    
    def _set_size_mode_(self, mode):
        # todo: fix size bug
        if mode == self.SizeMode.Fixed:
            self._body.setSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
            )
            # self.setSizePolicy(
            #     QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
            # )
        elif mode == self.SizeMode.Expanding:
            self._body.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
            )
            # self.setSizePolicy(
            #     QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
            # )


class QtHToolBox(AbsQtToolBox):
    QT_HEAD_CLS = _head.QtHExpandHead2
    QT_ORIENTATION = QtCore.Qt.Horizontal
    QT_HEAD_W, QT_HEAD_H = 12, 24

    def __init__(self, *args, **kwargs):
        super(QtHToolBox, self).__init__(*args, **kwargs)


class QtVToolBox(AbsQtToolBox):
    QT_HEAD_CLS = _head.QtVExpandHead2
    QT_ORIENTATION = QtCore.Qt.Vertical
    QT_HEAD_W, QT_HEAD_H = 24, 12

    def __init__(self, *args, **kwargs):
        super(QtVToolBox, self).__init__(*args, **kwargs)


class AbsQtToolBar(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(AbsQtToolBar, self).__init__(*args, **kwargs)
        qt_palette = _qt_core.GuiQtDcc.generate_qt_palette()
        self.setPalette(qt_palette)
        self.setAutoFillBackground(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )
        self._wgt_w, self._wgt_h = 28, 28
        self._wgt_w_min, self._wgt_h_min = 12, 12

        lot = _base.QtHBoxLayout(self)
        lot.setContentsMargins(0, 0, 0, 0)
        lot.setSpacing(2)
        # header
        self._head = _head.QtHHead()
        lot.addWidget(self._head)
        self._head.expand_toggled.connect(self._set_expanded_)
        self._head._set_tool_tip_text_('"LMB-click" to expand "on" / "off"')

        scb = _scroll.QtHScrollBox()
        lot.addWidget(scb)
        scb.setFixedHeight(self._wgt_h)

        self._body = scb
        self._layout = scb._get_layout_()

        self._refresh_expand_()

    def _refresh_expand_(self):
        if self._get_is_expanded_() is True:
            self._head.setMaximumSize(self._wgt_w_min, self._wgt_h)
            self._head.setMinimumSize(self._wgt_w_min, self._wgt_h)

            self.setFixedHeight(self._wgt_h)
        else:
            self._head.setMaximumSize(166667, self._wgt_h_min)
            self._head.setMinimumSize(self._wgt_w_min, self._wgt_h_min)

            self.setFixedHeight(self._wgt_h_min)

        self._body.setVisible(self._get_is_expanded_())
        self._head._refresh_expand_()

    def _set_expanded_(self, boolean):
        self._head._set_expanded_(boolean)
        self._refresh_expand_()

    def _get_is_expanded_(self):
        return self._head._get_is_expanded_()

    def _add_widget_(self, widget):
        if isinstance(widget, QtCore.QObject):
            self._layout.addWidget(widget)
        else:
            self._layout.addWidget(widget.widget)

    def _insert_widget_at_(self, index, widget):
        if isinstance(widget, QtCore.QObject):
            self._layout.insertWidget(index, widget)
        else:
            self._layout.insertWidget(index, widget.widget)
    
    def _create_tool_box_(self, name, expanded=True, visible=True, size_mode=0, insert_args=None):
        tool_box = QtHToolBox()
        if isinstance(insert_args, int):
            self._insert_widget_at_(insert_args, tool_box)
        else:
            self._add_widget_(tool_box)

        tool_box._set_name_text_(name)
        tool_box._set_expanded_(expanded)
        tool_box._set_visible_(visible)
        tool_box._set_size_mode_(size_mode)
        return tool_box

    def _set_width_(self, w):
        self._wgt_w = w
        self._refresh_expand_()

    def _set_height_(self, h):
        self._wgt_h = h
        self._refresh_expand_()

    def _get_layout_(self):
        return self._layout

    def _set_top_direction_(self):
        self._head._set_expand_direction_(self._head.ExpandDirection.TopToBottom)

    def _set_bottom_direction_(self):
        self._head._set_expand_direction_(self._head.ExpandDirection.BottomToTop)

    def _set_align_center_(self):
        self._layout.setAlignment(QtCore.Qt.AlignHCenter)

    def _set_align_left_(self):
        self._layout.setAlignment(QtCore.Qt.AlignLeft)

    def _set_align_right_(self):
        self._layout.setAlignment(QtCore.Qt.AlignRight)

    def _set_border_radius_(self, radius):
        self._head._set_frame_border_radius_(radius)


class QtHToolBar(AbsQtToolBar):
    def __init__(self, *args, **kwargs):
        super(QtHToolBar, self).__init__(*args, **kwargs)


# coding=utf-8
# qt
from ..core.wrap import *

from .. import abstracts as gui_qt_abstracts
# qt widgets
from . import base as gui_qt_wgt_base

from . import utility as gui_qt_wgt_utility

from . import head as gui_qt_wgt_head

from . import drag as gui_qt_wgt_drag


class AbsQtToolGroup(
    QtWidgets.QWidget,
    gui_qt_abstracts.AbsQtActionBaseDef,
    gui_qt_abstracts.AbsQtActionForDragDef,

    gui_qt_abstracts.AbsQtItemLayoutBaseDef,
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

        self.__base_layout = gui_qt_wgt_base.QtVBoxLayout(self)
        self.__base_layout.setAlignment(QtCore.Qt.AlignTop)
        self.__base_layout.setContentsMargins(0, 0, 0, 0)
        self.__base_layout.setSpacing(2)

        self.__head = self.QT_HEAD_CLS()
        self.__base_layout.addWidget(self.__head)
        self.__head.setFixedHeight(self.QT_HEAD_HEIGHT)
        self.__head.expand_toggled.connect(self._set_expanded_)
        self.__head._set_tool_tip_text_('"LMB-click" expand tool group')

        self.__view = gui_qt_wgt_utility.QtTranslucentWidget()
        self.__base_layout.addWidget(self.__view)
        self.__layout = gui_qt_wgt_base.QtVBoxLayout(self.__view)
        self.__layout.setContentsMargins(2, 0, 0, 0)
        self.__layout.setSpacing(2)

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
                    if self.__head._get_action_flag_is_match_(self.ActionFlag.Press):
                        self._drag_press_point = self.__head._get_press_point_()
                        self.__head._set_action_flag_(self.ActionFlag.DragPress)
                    elif self.__head._get_action_flag_is_match_(self.ActionFlag.DragPress):
                        self._do_drag_press_(event)
                    elif self.__head._get_action_flag_is_match_(self.ActionFlag.DragMove):
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
        self.__drag = gui_qt_wgt_drag.QtDrag(self.__head)

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
        self.__view.setVisible(
            boolean
        )
        if boolean is True:
            self.__head._set_tool_tip_text_('"LMB-click" collapse tool group')
        else:
            self.__head._set_tool_tip_text_('"LMB-click" expand tool group')

    def _add_widget_(self, widget):
        self.__layout.addWidget(widget)

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
            self.__view.hide()

    def _end_drag_mode_(self):
        if self._get_is_expanded_() is True:
            self.__view.show()


class QtHToolGroupStyleA(AbsQtToolGroup):
    QT_HEAD_CLS = gui_qt_wgt_head.QtHeadAsFrame

    def __init__(self, *args, **kwargs):
        super(QtHToolGroupStyleA, self).__init__(*args, **kwargs)


class QtHToolGroupStyleB(AbsQtToolGroup):
    QT_HEAD_CLS = gui_qt_wgt_head.QtHeadAsLine

    def __init__(self, *args, **kwargs):
        super(QtHToolGroupStyleB, self).__init__(*args, **kwargs)


class AbsQtToolBox(QtWidgets.QWidget):
    QT_HEAD_CLS = None
    QT_ORIENTATION = None
    QT_HEAD_W, QT_HEAD_H = 12, 24

    def __init__(self, *args, **kwargs):
        super(AbsQtToolBox, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self._build_widget_()

    def _build_widget_(self):
        if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
            layout = gui_qt_wgt_base.QtHBoxLayout(self)
        elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
            layout = gui_qt_wgt_base.QtVBoxLayout(self)
        else:
            raise RuntimeError()
        layout.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        layout.setContentsMargins(*[0]*4)
        layout.setSpacing(0)
        # header
        self._head = self.QT_HEAD_CLS()
        layout.addWidget(self._head)
        self._head.expand_toggled.connect(self._set_expanded_)
        self._head._set_tool_tip_text_('"LMB-click" to expand "on" / "off"')
        self._head.setFixedSize(self.QT_HEAD_W, self.QT_HEAD_H)
        #
        self._container = gui_qt_wgt_utility.QtTranslucentWidget()
        layout.addWidget(self._container)
        if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
            self._qt_layout = gui_qt_wgt_base.QtHBoxLayout(self._container)
        elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
            self._qt_layout = gui_qt_wgt_base.QtVBoxLayout(self._container)
        else:
            raise RuntimeError()
        self._qt_layout.setContentsMargins(*[0]*4)
        self._qt_layout.setSpacing(2)
        self._qt_layout.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        #
        self._refresh_expand_()

    def _refresh_expand_(self):
        self._container.setVisible(self._head._get_is_expanded_())
        self._head._refresh_expand_()
        self._refresh_widget_size_()

    def _refresh_widget_size_(self):
        if self._head._get_is_expanded_() is True:
            s = self._qt_layout.minimumSize()
            w, h = s.width(), s.height()
            if self.QT_ORIENTATION == QtCore.Qt.Horizontal:
                self.setFixedSize(self.QT_HEAD_W+w, self.QT_HEAD_H)
            elif self.QT_ORIENTATION == QtCore.Qt.Vertical:
                self.setFixedSize(self.QT_HEAD_W, self.QT_HEAD_H+h)
        else:
            self.setFixedSize(self.QT_HEAD_W, self.QT_HEAD_H)

    def _set_expanded_(self, boolean):
        self._head._set_expanded_(boolean)
        self._refresh_expand_()

    def _refresh_container_size_(self):
        pass

    def _get_is_expanded_(self):
        return self._head._get_is_expanded_()

    def _add_widget_(self, widget):
        if isinstance(widget, QtCore.QObject):
            self._qt_layout.addWidget(widget)
        else:
            self._qt_layout.addWidget(widget._qt_widget)
        #
        self._refresh_widget_size_()

    def _set_name_text_(self, text):
        self._head._set_name_text_(text)


class QtHToolBox(AbsQtToolBox):
    QT_HEAD_CLS = gui_qt_wgt_head.QtHExpandHead2
    QT_ORIENTATION = QtCore.Qt.Horizontal
    QT_HEAD_W, QT_HEAD_H = 12, 24

    def __init__(self, *args, **kwargs):
        super(QtHToolBox, self).__init__(*args, **kwargs)


class QtVToolBox(AbsQtToolBox):
    QT_HEAD_CLS = gui_qt_wgt_head.QtVExpandHead2
    QT_ORIENTATION = QtCore.Qt.Vertical
    QT_HEAD_W, QT_HEAD_H = 24, 12

    def __init__(self, *args, **kwargs):
        super(QtVToolBox, self).__init__(*args, **kwargs)

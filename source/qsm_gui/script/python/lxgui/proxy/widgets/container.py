# coding:utf-8
# qt
from ...qt import core as gui_qt_core
# qt widgets
from ...qt.widgets import base as gui_qt_wgt_base

from ...qt.widgets import utility as gui_qt_wgt_utility

from ...qt.widgets import head as gui_qt_wgt_head

from ...qt.widgets import scroll as gui_qt_wgt_scroll
# proxy abstracts
from .. import abstracts as gui_prx_abstracts


class AbsPrxToolGroup(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtLine
    QT_HEAD_CLS = None

    QT_HEAD_HEIGHT = 22

    def __init__(self, *args, **kwargs):
        super(AbsPrxToolGroup, self).__init__(*args, **kwargs)

    def _gui_build_(self):
        qt_layout_0 = gui_qt_wgt_base.QtVBoxLayout(self._qt_widget)
        qt_layout_0.setAlignment(gui_qt_core.QtCore.Qt.AlignTop)
        qt_layout_0.setContentsMargins(0, 0, 0, 0)
        qt_layout_0.setSpacing(2)
        # header
        self._qt_head = self.QT_HEAD_CLS()
        qt_layout_0.addWidget(self._qt_head)
        self._qt_head.setFixedHeight(self.QT_HEAD_HEIGHT)
        self._qt_head.expand_toggled.connect(self.set_expanded)
        self._qt_head._set_tool_tip_text_('"LMB-click" to expand "on" / "off"')
        self._qt_head.press_toggled.connect(self._qt_widget._set_pressed_)
        #
        qt_widget_1 = gui_qt_wgt_utility.QtTranslucentWidget()
        qt_layout_0.addWidget(qt_widget_1)
        qt_layout_1 = gui_qt_wgt_base.QtVBoxLayout(qt_widget_1)
        qt_layout_1.setContentsMargins(2, 0, 0, 0)
        qt_layout_1.setSpacing(2)
        #
        self._layout = qt_layout_1
        #
        self._qt_view = qt_widget_1
        #
        self._refresh_expand_()

    def _refresh_expand_(self):
        self._qt_view.setVisible(
            self.get_is_expanded()
        )

    def set_name(self, name):
        self._qt_head._set_name_text_(name)

    def set_icon_by_name(self, name):
        self._qt_head._set_icon_name_text_(name)

    def set_name_icon_enable(self, boolean):
        self._qt_head._set_icon_name_enable_(boolean)

    def set_expand_icon_file(self, icon_file_path_0, icon_file_path_1):
        self._qt_head._set_expand_icon_file_path_(
            icon_file_path_0, icon_file_path_1
        )

    def set_expand_icon_names(self, icon_name_0, icon_name_1):
        self._qt_head._set_expand_icon_names_(
            icon_name_0, icon_name_1
        )

    def set_expand_sub_icon_names(self, icon_name_0, icon_name_1):
        self._qt_head._set_expand_sub_icon_names_(
            icon_name_0, icon_name_1
        )

    def set_name_font_size(self, size):
        self._qt_head._set_name_font_size_(size)

    def set_expanded(self, boolean):
        self._qt_head._set_expanded_(boolean)
        self._refresh_expand_()

    def set_head_visible(self, boolean):
        self._qt_head.setHidden(not boolean)

    def get_is_expanded(self):
        return self._qt_head._get_is_expanded_()

    def add_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            qt_widget = widget
            self._layout.addWidget(widget)
        else:
            qt_widget = widget.widget
        #
        if qt_widget != self.widget:
            #
            self._layout.addWidget(qt_widget)

    def set_layout_alignment_to_top(self):
        self._layout.setAlignment(
            gui_qt_core.QtCore.Qt.AlignTop
        )

    def set_size_mode(self, mode):
        if mode == 0:
            self._qt_view.setSizePolicy(
                gui_qt_core.QtWidgets.QSizePolicy.Expanding,
                gui_qt_core.QtWidgets.QSizePolicy.Expanding
            )
        elif mode == 1:
            self._qt_view.setSizePolicy(
                gui_qt_core.QtWidgets.QSizePolicy.Expanding,
                gui_qt_core.QtWidgets.QSizePolicy.Minimum
            )

    def set_height_match_to_minimum(self):
        self._qt_view.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Minimum
        )

    def connect_expand_changed_to(self, fnc):
        self._qt_head.expand_clicked.connect(fnc)

    def set_clear(self):
        def rcs_fnc_(layout_):
            c = layout_.count()
            for i in range(c):
                i_item = self._layout.takeAt(0)
                if i_item is not None:
                    i_widget = i_item.widget()
                    if i_widget:
                        i_widget.deleteLater()
                    else:
                        _i_layout = i_item.layout()
                        if _i_layout:
                            rcs_fnc_(_i_layout)
                        else:
                            spacer = i_item.spacerItem()
                            if spacer:
                                spacer.deleteLater()

        #
        rcs_fnc_(self._layout)


class PrxHToolGroup(AbsPrxToolGroup):
    QT_HEAD_CLS = gui_qt_wgt_head.QtHeadAsFrame

    QT_HEAD_HEIGHT = 22

    def __init__(self, *args, **kwargs):
        super(PrxHToolGroup, self).__init__(*args, **kwargs)


class PrxHToolGroupNew(AbsPrxToolGroup):
    QT_HEAD_CLS = gui_qt_wgt_head.QtHeadAsLine

    QT_HEAD_HEIGHT = 20

    def __init__(self, *args, **kwargs):
        super(PrxHToolGroupNew, self).__init__(*args, **kwargs)


class PrxHToolBar(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtWidget

    def __init__(self, *args, **kwargs):
        super(PrxHToolBar, self).__init__(*args, **kwargs)
        #
        self.widget.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Minimum
        )

    def _gui_build_(self):
        self._wgt_w, self._wgt_h = 28, 28
        self._wgt_w_min, self._wgt_h_min = 12, 12
        #
        qt_layout_0 = gui_qt_wgt_base.QtHBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(2)
        # header
        self._qt_head = gui_qt_wgt_head.QtHExpandHead1()
        qt_layout_0.addWidget(self._qt_head)
        self._qt_head.expand_toggled.connect(self.set_expanded)
        self._qt_head._set_tool_tip_text_('"LMB-click" to expand "on" / "off"')
        #
        qt_widget_1 = gui_qt_wgt_scroll.QtHScrollBox()
        qt_layout_0.addWidget(qt_widget_1)
        # qt_layout_1.setAlignment(gui_qt_core.QtCore.Qt.AlignLeft)
        self._qt_view = qt_widget_1
        self._qt_layout_0 = qt_widget_1._get_layout_()
        #
        self._refresh_expand_()
        #
        self._qt_view.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Minimum
        )

    def _refresh_expand_(self):
        if self.get_is_expanded() is True:
            self._qt_head.setMaximumSize(self._wgt_w_min, self._wgt_h)
            self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h)
            #
            self.widget.setMaximumHeight(self._wgt_h)
            self.widget.setMinimumHeight(self._wgt_h)
        else:
            self._qt_head.setMaximumSize(166667, self._wgt_h_min)
            self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h_min)
            #
            self.widget.setMaximumHeight(self._wgt_h_min)
            self.widget.setMinimumHeight(self._wgt_h_min)
        #
        self._qt_view.setVisible(self.get_is_expanded())
        self._qt_head._refresh_expand_()

    def set_name(self, name):
        self._qt_head._set_name_text_(
            'tool bar for "{}"'.format(name)
        )

    def set_expanded(self, boolean):
        self._qt_head._set_expanded_(boolean)
        self._refresh_expand_()

    def swap_expanded(self):
        self.set_expanded(not self.get_is_expanded())

    def swap_visible(self):
        self.set_visible(not self.get_is_visible())

    def get_is_expanded(self):
        return self._qt_head._get_is_expanded_()

    def add_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._qt_layout_0.addWidget(widget)
        else:
            self._qt_layout_0.addWidget(widget.widget)

    def insert_widget_at(self, index, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._qt_layout_0.insertWidget(index, widget)
        else:
            self._qt_layout_0.insertWidget(index, widget.widget)

    def set_width(self, w):
        self._wgt_w = w
        self._refresh_expand_()

    def set_height(self, h):
        self._wgt_h = h
        self._refresh_expand_()

    def get_qt_layout(self):
        return self._qt_layout_0

    def set_top_direction(self):
        self._qt_head._set_expand_direction_(self._qt_head.ExpandDirection.TopToBottom)

    def set_bottom_direction(self):
        self._qt_head._set_expand_direction_(self._qt_head.ExpandDirection.BottomToTop)

    def set_alignment_center(self):
        self._qt_layout_0.setAlignment(gui_qt_core.QtCore.Qt.AlignHCenter)

    def set_left_alignment(self):
        self._qt_layout_0.setAlignment(gui_qt_core.QtCore.Qt.AlignLeft)

    def set_right_alignment(self):
        self._qt_layout_0.setAlignment(gui_qt_core.QtCore.Qt.AlignRight)

    def set_border_radius(self, radius):
        self._qt_head._set_frame_border_radius_(radius)


class PrxVToolBar(PrxHToolBar):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtWidget

    def __init__(self, *args, **kwargs):
        super(PrxVToolBar, self).__init__(*args, **kwargs)
        #
        self.widget.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Minimum,
            gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )

    def _gui_build_(self):
        self._wgt_w, self._wgt_h = 28, 28
        self._wgt_w_min, self._wgt_h_min = 12, 12
        #
        qt_layout_0 = gui_qt_wgt_base.QtHBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(2)
        qt_layout_0.setAlignment(gui_qt_core.QtCore.Qt.AlignLeft)
        # header
        self._qt_head = gui_qt_wgt_head.QtVExpandHead1()
        qt_layout_0.addWidget(self._qt_head)
        self._qt_head.expand_toggled.connect(self.set_expanded)
        self._qt_head._set_tool_tip_text_('"LMB-click" to expand "on" / "off"')
        #
        qt_widget_1 = gui_qt_wgt_utility.QtWidget()
        qt_layout_0.addWidget(qt_widget_1)
        qt_layout_1 = gui_qt_wgt_base.QtVBoxLayout(qt_widget_1)
        qt_layout_1.setContentsMargins(0, 0, 0, 0)
        qt_layout_1.setAlignment(gui_qt_core.QtCore.Qt.AlignLeft)
        self._qt_layout_0 = qt_layout_1
        #
        self._qt_view = qt_widget_1
        #
        self._refresh_expand_()
        #
        self._qt_view.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Minimum,
            gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )

    def _refresh_expand_(self):
        if self.get_is_expanded() is True:
            self._qt_head.setMaximumSize(self._wgt_w_min, 166667)
            self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h_min)
            #
            self.widget.setMaximumWidth(self._wgt_w)
            self.widget.setMinimumWidth(self._wgt_w)
        else:
            self._qt_head.setMaximumSize(self._wgt_w_min, 166667)
            self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h_min)
            #
            self.widget.setMaximumWidth(self._wgt_w_min)
            self.widget.setMinimumWidth(self._wgt_w_min)
        #
        self._qt_view.setVisible(self.get_is_expanded())
        self._qt_head._refresh_expand_()

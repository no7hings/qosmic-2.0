# coding:utf-8
# qt
from ...qt import core as gui_qt_core
# qt widgets
from ...qt.widgets import base as gui_qt_wgt_base

from ...qt.widgets import utility as gui_qt_wgt_utility

from ...qt.widgets import container as gui_qt_wgt_container

from ...qt.widgets import head as gui_qt_wgt_head
# proxy abstracts
from .. import abstracts as gui_prx_abstracts


class PrxHToolBox(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtWidget

    def __init__(self, *args, **kwargs):
        super(PrxHToolBox, self).__init__(*args, **kwargs)

    def _gui_build_fnc(self):
        self._wgt_w, self._wgt_h = 24, 24
        self._wgt_w_min, self._wgt_h_min = 12, 24
        #
        qt_layout_0 = gui_qt_wgt_base.QtHBoxLayout(self._qt_widget)
        qt_layout_0.setContentsMargins(*[0]*4)
        qt_layout_0.setSpacing(2)
        qt_layout_0.setAlignment(gui_qt_core.QtCore.Qt.AlignLeft)
        # header
        self._qt_head = gui_qt_wgt_head.QtHExpandHead2()
        qt_layout_0.addWidget(self._qt_head)
        self._qt_head.expand_toggled.connect(self.set_expanded)
        self._qt_head._set_tool_tip_text_('"LMB-click" to expand "on" / "off"')
        #
        qt_widget_1 = gui_qt_wgt_utility.QtTranslucentWidget()
        qt_layout_0.addWidget(qt_widget_1)
        qt_layout_1 = gui_qt_wgt_base.QtHBoxLayout(qt_widget_1)
        qt_layout_1.setContentsMargins(*[0]*4)
        qt_layout_1.setAlignment(gui_qt_core.QtCore.Qt.AlignLeft)
        #
        self._qt_view = qt_widget_1
        self._qt_layout_0 = qt_layout_1
        #
        self._refresh_expand_()
        #
        self.set_size_mode(0)

    def _refresh_expand_(self):
        self.widget.setMaximumSize(self._wgt_w_min, self._wgt_h_min)
        self._qt_head.setMaximumSize(self._wgt_w_min, self._wgt_h)
        self._qt_head.setMinimumSize(self._wgt_w_min, self._wgt_h)
        if self.get_is_expanded() is True:
            self.widget.setMaximumWidth(166667)
        else:
            self.widget.setMaximumWidth(self._wgt_w_min)
        #
        self._qt_view.setVisible(self.get_is_expanded())
        self._qt_head._refresh_expand_()

    def set_name(self, name):
        self._qt_head._set_name_text_(name)
        
    def get_name(self):
        return self._qt_head._get_name_text_()
    
    def set_path(self, path):
        self._qt_head._set_path_text_(path)
    
    def get_path(self):
        return self._qt_head._get_path_text_()

    def set_tool_tip(self, text):
        self._qt_head._set_tool_tip_(text)

    def set_expanded(self, boolean):
        self._qt_head._set_expanded_(boolean)
        self._refresh_expand_()

    def get_is_expanded(self):
        return self._qt_head._is_expanded_()

    def add_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._qt_layout_0.addWidget(widget)
        else:
            self._qt_layout_0.addWidget(widget._qt_widget)

    def set_height(self, h):
        self._wgt_h = h
        self._refresh_expand_()

    def get_qt_layout(self):
        return self._qt_layout_0

    def set_top_direction(self):
        self._qt_head._set_expand_direction_(self._qt_head.ExpandDirection.TopToBottom)

    def set_bottom_direction(self):
        self._qt_head._set_expand_direction_(self._qt_head.ExpandDirection.BottomToTop)

    def set_border_radius(self, radius):
        self._qt_head._set_frame_border_radius_(radius)

    def set_size_mode(self, mode):
        # todo: fix size bug
        if mode == 0:
            self._qt_view.setSizePolicy(
                gui_qt_core.QtWidgets.QSizePolicy.Fixed,
                gui_qt_core.QtWidgets.QSizePolicy.Fixed
            )
        elif mode == 1:
            self._qt_view.setSizePolicy(
                gui_qt_core.QtWidgets.QSizePolicy.Expanding,
                gui_qt_core.QtWidgets.QSizePolicy.Fixed
            )


class PrxHToolBoxNew(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_container.QtHToolBox

    def __init__(self, *args, **kwargs):
        super(PrxHToolBoxNew, self).__init__(*args, **kwargs)

    def set_expanded(self, boolean):
        self._qt_widget._set_expanded_(boolean)

    def add_widget(self, widget):
        self._qt_widget._add_widget_(widget)


class PrxVToolBoxNew(PrxHToolBoxNew):
    QT_WIDGET_CLS = gui_qt_wgt_container.QtVToolBox

    def __init__(self, *args, **kwargs):
        super(PrxVToolBoxNew, self).__init__(*args, **kwargs)
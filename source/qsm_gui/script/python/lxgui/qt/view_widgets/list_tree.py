# coding=utf-8
# qt
from ...qt.core.wrap import *

from ... import core as _gui_core

from ...qt import core as _qt_core
# qt widgets
from ..widgets import base as _wgt_base

from ..widgets import utility as _wgt_utility

from ..widgets import view_for_list as _wgt_view_for_list

from ..widgets import container as _wgt_container


class QtListGroupItem(_wgt_container.QtHToolGroupStyleC):
    def __init__(self, *args, **kwargs):
        super(QtListGroupItem, self).__init__(*args, **kwargs)

        self._view = None

    def _set_view_(self, view):
        self._view = view

    def _update_size_(self):
        h = self._view._compute_height_maximum_0_()
        self._view.setFixedHeight(h)


class QtListGroupView(QtWidgets.QWidget):
    def _refresh_widget_all_(self):
        self._refresh_widget_draw_geometry_()
        self._refresh_widget_draw_()

    def _refresh_widget_draw_(self):
        self.update()

    def _refresh_widget_draw_geometry_(self):
        for i in self._group_dict.values():
            i._update_size_()

    def __init__(self, *args, **kwargs):
        super(QtListGroupView, self).__init__(*args, **kwargs)

        self._group_dict = {}

        self._lot = _wgt_base.QtVBoxLayout(self)

        self._sca = _wgt_utility.QtVScrollArea()
        self._lot.addWidget(self._sca)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if not hasattr(event, 'type'):
                return False

            if event.type() == QtCore.QEvent.Resize:
                self._refresh_widget_all_()
        return False

    def _create_one_(self, path):
        grp = QtListGroupItem()
        self._sca._add_widget_(grp)
        grp._set_expanded_(True)
        grp._set_name_text_(path)
        wgt = _wgt_view_for_list.QtListWidget()
        grp._add_widget_(wgt)
        grp._set_view_(wgt)
        self._group_dict[path] = grp
        return wgt

# coding:utf-8
import collections

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.abstracts as prx_abstracts

from ...qt.widgets import base as _qt_wgt_base

from ...qt.widgets import utility as _qt_wgt_utility

from . import utility as _utility

from . import view_for_tree as _view_for_tree


class _GuiStorageOpt(
    prx_abstracts.AbsGuiPrxTreeViewAsStorageOpt
):
    NAMESPACE = 'storage'

    def __init__(self, parent, prx_tree_view):
        self._parent = parent
        self._prx_tree_view = prx_tree_view

        self._init_tree_view_as_storage_opt_(prx_tree_view, self.NAMESPACE)


class PrxViewForTask(prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = qt_widgets.QtTranslucentWidget

    def __init__(self, *args, **kwargs):
        super(PrxViewForTask, self).__init__(*args, **kwargs)

        self._qt_widget.setSizePolicy(
            gui_qt_core.QtWidgets.QSizePolicy.Expanding,
            gui_qt_core.QtWidgets.QSizePolicy.Expanding
        )
        self._qt_layout = _qt_wgt_base.QtVBoxLayout(self.widget)
        # self._qt_layout._set_align_top_()

        self._qt_title_label = _qt_wgt_utility.QtTextItem()
        self._qt_layout.addWidget(self._qt_title_label)
        self._qt_title_label._set_name_align_h_center_()
        self._qt_title_label.setFixedHeight(20)

        self._prx_tree_view = _view_for_tree.PrxTreeView()
        self._qt_layout.addWidget(self._prx_tree_view._qt_widget)
        self._prx_tree_view.create_header_view(
            [('name', 2), ('update', 1)],
            480
        )

        self._root = None

        self._gui_storage_opt = _GuiStorageOpt(self, self._prx_tree_view)

    def set_root(self, root):
        self._root = root
        self._gui_storage_opt.gui_add_all_use_thread(
            root
        )

    def set_title(self, name_text):
        self._qt_title_label._set_name_text_(name_text)

    def create_group(self, name_text):
        pass

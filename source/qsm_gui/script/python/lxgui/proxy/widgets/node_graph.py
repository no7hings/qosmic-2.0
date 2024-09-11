# coding:utf-8
# qt widgets
from ...qt.widgets import base as _qt_widget_base

from ...qt.widgets import entry_frame as _qt_wgt_entry_frame

from ...qt.graph_widgets import graph_for_node as _qt_grh_for_node

from ...qt.graph_widgets import graph_for_image as _qt_grh_for_image
# proxy abstracts
from ...proxy import abstracts as _proxy_abstracts
# proxy widgets
from . import utility as _utility

from . import container as _container


class PrxNGGraph(
    _proxy_abstracts.AbsPrxWidget
):
    QT_WIDGET_CLS = _qt_wgt_entry_frame.QtEntryFrame
    QT_VIEW_CLS = _qt_grh_for_node.QtNodeGraph

    def __init__(self, *args, **kwargs):
        super(PrxNGGraph, self).__init__(*args, **kwargs)
        self._qt_layout_0 = _qt_widget_base.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(2, 2, 2, 2)
        self._qt_layout_0.setSpacing(2)
        self._top_prx_tool_bar = _container.PrxHToolBar()
        self._qt_layout_0.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_border_radius(1)
        #
        self._prx_filer_bar_0 = _utility.PrxFilterBar()
        self._top_prx_tool_bar.add_widget(self._prx_filer_bar_0)
        # add custom menu
        self._qt_view = self.QT_VIEW_CLS()
        self._qt_layout_0.addWidget(self._qt_view)
        #
        self._prx_filter_bar = self._prx_filer_bar_0

    @property
    def view(self):
        return self._qt_view

    @property
    def filter_bar(self):
        return self._prx_filter_bar

    def set_node_add(self, *args, **kwargs):
        self._qt_view._create_node_(*args, **kwargs)

    def set_graph_universe(self, universe):
        self._qt_view._set_graph_universe_(universe)

    def set_node_show(self, obj_path=None):
        self._qt_view._set_ng_show_by_universe_(obj_path)


class PrxNGTree(
    _proxy_abstracts.AbsPrxWidget
):
    QT_WIDGET_CLS = _qt_wgt_entry_frame.QtEntryFrame
    QT_VIEW_CLS = _qt_grh_for_node._QtNGTree

    def __init__(self, *args, **kwargs):
        super(PrxNGTree, self).__init__(*args, **kwargs)
        self._qt_layout_0 = _qt_widget_base.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(4, 4, 4, 4)
        self._qt_layout_0.setSpacing(2)
        self._top_prx_tool_bar = _container.PrxHToolBar()
        self._qt_layout_0.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_border_radius(1)
        #
        self._prx_filer_bar_0 = _utility.PrxFilterBar()
        self._top_prx_tool_bar.add_widget(self._prx_filer_bar_0)
        # add custom menu
        self._qt_view = self.QT_VIEW_CLS()
        self._qt_layout_0.addWidget(self._qt_view)
        #
        self._prx_filter_bar = self._prx_filer_bar_0

        self._qt_view._set_view_header_(
            [('name', 4)], 320
        )

    def set_graph_universe(self, universe):
        self._qt_view._set_graph_universe_(universe)

    def expand_items_by_depth(self, depth):
        self._qt_view._expand_items_by_depth_(depth)


class PrxNGImageGraph(
    _proxy_abstracts.AbsPrxWidget
):
    QT_WIDGET_CLS = _qt_wgt_entry_frame.QtEntryFrame
    QT_VIEW_CLS = _qt_grh_for_image.QtImageGraph

    def __init__(self, *args, **kwargs):
        super(PrxNGImageGraph, self).__init__(*args, **kwargs)
        self._qt_layout_0 = _qt_widget_base.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(4, 4, 4, 4)
        self._qt_layout_0.setSpacing(2)
        self._top_prx_tool_bar = _container.PrxHToolBar()
        self._qt_layout_0.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_border_radius(1)
        #
        self._prx_filer_bar_0 = _utility.PrxFilterBar()
        self._top_prx_tool_bar.add_widget(self._prx_filer_bar_0)
        # add custom menu
        self._qt_view = self.QT_VIEW_CLS()
        self._qt_layout_0.addWidget(self._qt_view)
        #
        self._prx_filter_bar = self._prx_filer_bar_0

    @property
    def view(self):
        return self._qt_view

    @property
    def filter_bar(self):
        return self._prx_filter_bar

    def set_node_add(self, *args, **kwargs):
        self._qt_view._create_node_(*args, **kwargs)

    def restore_all(self):
        self._qt_view._set_restore_()

    def set_clear(self):
        self._qt_view._do_clear_()

    def set_graph_universe(self, universe):
        self._qt_view._set_graph_universe_(universe)

    def set_node_show(self, obj_path=None):
        self._qt_view._set_ng_show_by_universe_(obj_path)

    def set_graph_save_to(self, file_path):
        self._qt_view._save_ng_graph_image_to_(file_path)

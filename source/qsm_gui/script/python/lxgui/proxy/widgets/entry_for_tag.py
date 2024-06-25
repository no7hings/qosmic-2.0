# coding:utf-8
# qt widgets
from ...qt.widgets import base as _qt_widget_base

from ...qt.widgets import entry_frame as _qt_widget_entry_frame

from ...qt.widgets import entry_for_tag as _view_for_tag_filter
# proxy abstracts
from .. import abstracts as _prx_abstracts

from . import container as _container

from . import utility as _utility


class PrxTagInput(
    _prx_abstracts.AbsPrxWidget,
):
    QT_WIDGET_CLS = _qt_widget_entry_frame.QtEntryFrame
    QT_VIEW_CLS = _view_for_tag_filter.QtEntryRootForTag

    def _add_fnc(self):
        pass

    # def _gui_add_main_tools(self):
    #     for i in [
    #         ('create', 'file/add-file', '', self._add_fnc)
    #     ]:
    #         i_key, i_icon_name, i_tool_tip, i_fnc = i
    #         i_tool = _utility.PrxIconPressButton()
    #         self._main_prx_tool_box.add_widget(i_tool)
    #         i_tool.set_name(i_key)
    #         i_tool.set_icon_name(i_icon_name)
    #         i_tool.set_tool_tip(i_tool_tip)
    #         i_tool.connect_press_clicked_to(i_fnc)

    def __init__(self, *args, **kwargs):
        super(PrxTagInput, self).__init__(*args, **kwargs)
        self._qt_layout_0 = _qt_widget_base.QtVBoxLayout(self._qt_widget)
        self._qt_layout_0.setContentsMargins(4, 4, 4, 4)
        self._qt_layout_0.setSpacing(2)

        self._top_prx_tool_bar = _container.PrxHToolBar()
        self._top_prx_tool_bar.set_name('top')
        self._top_prx_tool_bar.set_align_left()
        self._qt_layout_0.addWidget(self._top_prx_tool_bar.widget)
        self._top_prx_tool_bar.set_border_radius(1)

        # self._main_prx_tool_box = self._top_prx_tool_bar.create_tool_box(
        #     'main'
        # )
        # self._gui_add_main_tools()
        #
        self._qt_view = self.QT_VIEW_CLS()
        self._qt_view.setMinimumHeight(42)
        self._qt_view.setMaximumHeight(166667)
        self._qt_view.gui_proxy = self
        self._qt_layout_0.addWidget(self._qt_view)
    
    def create_group(self, path, *args, **kwargs):
        return self._qt_view._create_group_(path, *args, **kwargs)
        
    def create_node(self, path, *args, **kwargs):
        return self._qt_view._create_node_(path, *args, **kwargs)

    def check_exists(self, path):
        return self._qt_view._check_exists_(path)

    def get_one(self, path):
        return self._qt_view._get_one_(path)

    def set_node_checked(self, path, boolean):
        _ = self.get_one(path)
        if _:
            _._apply_check_state_(boolean)
    
    def expand_exclusive_for_node(self, path):
        self._qt_view._expand_exclusive_for_node_(path)
    
    def expand_all_groups(self):
        self._qt_view._expand_all_groups_()

    def expand_for_group(self, path):
        self._qt_view._expand_for_group_(path)
    
    def clear_all_checked(self):
        self._qt_view._clear_all_checked_()

    def get_top_tool_bar(self):
        return self._top_prx_tool_bar

    def connect_check_paths_change_accepted_to(self, fnc):
        self._qt_view.check_paths_change_accepted.connect(fnc)
    
    def connect_check_paths_changed_to(self, fnc):
        self._qt_view.check_paths_changed.connect(fnc)

    def apply_intersection_paths(self, path_set):
        self._qt_view._apply_intersection_paths_(path_set)
    
    def get_all_checked_node_paths(self):
        return self._qt_view._get_all_checked_node_paths_()

    def set_force_hidden_flag_for_group(self, path, boolean):
        self._qt_view._set_force_hidden_flag_for_group_(path, boolean)

    def restore(self):
        self._qt_view._restore_()

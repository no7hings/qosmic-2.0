# coding:utf-8
# qt
from ...qt import core as gui_qt_core
# qt widgets
from ...qt.widgets import split as gui_qt_wgt_split

from ...qt.widgets import view_for_layout as gui_qt_wgt_view_for_layout

from ...qt.widgets import view_for_tab as gui_qt_wgt_view_for_tab
# proxy abstracts
from .. import abstracts as gui_prx_abstracts


class PrxHSplitter(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_split.QtHSplitter

    def __init__(self, *args, **kwargs):
        super(PrxHSplitter, self).__init__(*args, **kwargs)

    def add_widget(self, widget):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            qt_widget = widget
        else:
            qt_widget = widget.widget
        #
        self.widget._add_widget_(qt_widget)

    def set_stretches(self, values):
        self._qt_widget._set_stretch_factors_(values)

    def set_fixed_size_at(self, index, value):
        self._qt_widget._set_fixed_size_at_(index, value)

    def set_widget_hide_at(self, index):
        self._qt_widget._set_widget_hide_at_(index)

    def set_contract_left_or_top_at(self, index, size=None):
        self._qt_widget._set_contract_left_or_top_at_(index, size)

    def set_contract_right_or_bottom_at(self, index, size=None):
        self._qt_widget._set_contract_right_or_bottom_at_(index, size)

    def get_is_contracted_at(self, index):
        return self._qt_widget._get_is_contracted_at_(index)

    def set_swap_enable(self, boolean):
        self.widget._swap_enable = boolean

    def get_handle_at(self, index):
        return self._qt_widget._get_handle_at_(index)

    def set_window(self, widget):
        self._qt_widget._set_window_(widget)

    def set_width(self, value):
        self._qt_widget.setFixedWidth(value)

    def install_full_size_shortcut(self):
        self._qt_widget._install_full_size_shortcut_()


class PrxVSplitter(PrxHSplitter):
    QT_WIDGET_CLS = gui_qt_wgt_split.QtVSplitter

    def __init__(self, *args, **kwargs):
        super(PrxVSplitter, self).__init__(*args, **kwargs)


class PrxTabView(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_view_for_tab.QtTabView

    def __init__(self, *args, **kwargs):
        super(PrxTabView, self).__init__(*args, **kwargs)

    def add_widget(self, widget, *args, **kwargs):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            qt_widget = widget
        else:
            qt_widget = widget.widget
        #
        self._qt_widget._add_widget_(qt_widget, *args, **kwargs)

    def get_current_name(self):
        return self._qt_widget._get_current_name_text_()

    def get_current_key(self):
        return self._qt_widget._get_current_key_text_()

    def get_all_page_names(self):
        return self._qt_widget._get_all_page_name_texts_()

    def get_all_page_keys(self):
        return self._qt_widget._get_all_page_key_texts_()

    def set_current_changed_connect_to(self, fnc):
        self._qt_widget.current_changed.connect(fnc)

    def set_current_by_name(self, name):
        self._qt_widget._set_item_current_by_name_text_(name)

    def set_current_by_key(self, key):
        self._qt_widget._set_item_current_by_key_text_(key)

    def set_add_enable(self, boolean):
        self._qt_widget._set_tab_add_enable_(boolean)

    def set_add_menu_data_gain_fnc(self, fnc):
        self._qt_widget._set_tab_add_menu_gain_fnc_(fnc)

    def set_menu_enable(self, boolean):
        self._qt_widget._set_tab_menu_enable_(boolean)

    def set_menu_data_generate_fnc(self, fnc):
        self._qt_widget._set_tab_menu_data_generate_fnc_(fnc)

    def connect_delete_accepted_to(self, fnc):
        self._qt_widget.tab_delete_accepted.connect(fnc)

    def set_drag_enable(self, boolean):
        self._qt_widget._set_drag_enable_(boolean)


class PrxToolGridLayoutWidget(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_view_for_layout.QtToolGridLayoutWidget

    def __init__(self, *args, **kwargs):
        super(PrxToolGridLayoutWidget, self).__init__(*args, **kwargs)

    def set_path(self, path):
        self._qt_widget._set_path_text_(path)

    def add_widget(self, widget, *args, **kwargs):
        if isinstance(widget, gui_qt_core.QtCore.QObject):
            self._qt_widget._add_widget_(widget, *args, **kwargs)
        else:
            self._qt_widget._add_widget_(widget.widget, *args, **kwargs)

    def set_item_size(self, w, h):
        self._qt_widget._set_item_size_(w, h)

    def refresh_widget(self):
        self._qt_widget._refresh_widget_all_()

    def set_menu_data(self, data):
        self._qt_widget._set_menu_data_(data)

    def set_drop_enable(self, boolean):
        self._qt_widget._set_drop_enable_(boolean)

    def set_drag_and_drop_scheme(self, text):
        self._qt_widget._set_drag_and_drop_scheme_(text)

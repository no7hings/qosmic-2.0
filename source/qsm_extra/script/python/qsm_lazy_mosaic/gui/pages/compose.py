# coding:utf-8
import copy

import functools

import six

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.resource as bsc_resource

import lxbasic.pinyin as bsc_pinyin

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.qt.view_widgets as gui_qt_view_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.proxy.graphs as gui_prx_graphs

import lxgui.qt.graph_widgets as gui_qt_graphs


class _GuiBaseOpt(object):
    def __init__(self, window, unit, session):
        self._window = window
        self._unit = unit
        self._session = session

        self._gui_thread_flag = 0

    def gui_update_thread_flag(self):
        self._gui_thread_flag += 1


class _GuiPackageOpt(_GuiBaseOpt):
    def __init__(self, *args, **kwargs):
        super(_GuiPackageOpt, self).__init__(*args, **kwargs)

        self._task_unit_path = None
        self._task_unit_path_tmp = None

        self._qt_tree_widget = gui_qt_view_widgets.QtTreeWidget()
        self._unit._prx_h_splitter.add_widget(self._qt_tree_widget)
        self._qt_tree_widget._set_item_sort_enable_(True)
        self._qt_tree_widget._view_model.set_item_expand_record_enable(True)
        self._qt_tree_widget._view_model.set_menu_name_dict(self._window._configure.get('build.menu_names'))

        self._qt_tree_widget.refresh.connect(self.gui_load_all_packages)

    def gui_load_all_packages(self):
        import rez.resolved_context as r_c


class _GuiLaunchOpt(_GuiBaseOpt):
    def __init__(self, *args, **kwargs):
        super(_GuiLaunchOpt, self).__init__(*args, **kwargs)

        self._task_unit_path = None
        self._task_unit_path_tmp = None

        self._qt_tree_widget = gui_qt_view_widgets.QtTreeWidget()
        self._unit._prx_h_splitter.add_widget(self._qt_tree_widget)
        self._qt_tree_widget._set_item_sort_enable_(True)
        self._qt_tree_widget._view_model.set_item_expand_record_enable(True)
        self._qt_tree_widget._view_model.set_menu_name_dict(self._window._configure.get('build.menu_names'))


class AbsPrxPageForCompose(gui_prx_widgets.PrxBasePage):
    QT_WIDGET_CLS = gui_qt_widgets.QtTranslucentWidget

    GUI_KEY = 'compose'

    def __init__(self, *args, **kwargs):
        super(AbsPrxPageForCompose, self).__init__(*args, **kwargs)

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        prx_v_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_v_sca.widget)

        self._prx_h_splitter = gui_prx_widgets.PrxHSplitter()
        prx_v_sca.add_widget(self._prx_h_splitter)

        self._gui_package_opt = _GuiPackageOpt(self._window, self, self._session)

        self._gui_launch_opt = _GuiLaunchOpt(self._window, self, self._session)

        self._prx_h_splitter.set_fixed_size_at(0, 320)

    def do_gui_refresh_all(self, force=False):
        self._gui_package_opt.gui_load_all_packages()

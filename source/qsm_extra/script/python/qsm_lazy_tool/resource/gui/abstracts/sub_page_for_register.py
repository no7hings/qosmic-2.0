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

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_lazy.screw.core as qsm_lzy_scr_core


class AbsPrxSubPageForResourceMotionRegister(gui_prx_widgets.PrxBaseSubPage):
    PAGE_KEY = None

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(AbsPrxSubPageForResourceMotionRegister, self).__init__(window, session, sub_window, *args, **kwargs)
        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_sca.widget)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self._sub_window.choice_name(
                self._sub_window._configure.get('build.{}.options'.format(self.PAGE_KEY))
            )
        )
        prx_sca.add_widget(self._prx_options_node)

        self._prx_options_node.build_by_data(
            self._sub_window._configure.get('build.{}.options.parameters'.format(self.PAGE_KEY)),
        )

        self._prx_tool_group = gui_prx_widgets.PrxHToolGroup()
        prx_sca.add_widget(self._prx_tool_group)
        self._prx_tool_group.set_expanded(True)
        self._prx_tool_group.set_name(
            gui_core.GuiUtil.choice_name(
                self._sub_window._language, self._sub_window._configure.get('build.{}.filter'.format(self.PAGE_KEY))
            )
        )
        qt_widget_0 = gui_qt_widgets.QtTranslucentWidget()
        self._prx_tool_group.add_widget(qt_widget_0)
        h_qt_lot_0 = gui_qt_widgets.QtHBoxLayout(qt_widget_0)

        self._type_prx_tag_view = gui_prx_widgets.PrxTagView()
        h_qt_lot_0.addWidget(
            self._type_prx_tag_view.widget
        )

        self._tag_prx_tag_view = gui_prx_widgets.PrxTagView()
        h_qt_lot_0.addWidget(
            self._tag_prx_tag_view.widget
        )

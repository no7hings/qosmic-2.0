# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxSubpageForNewSplicing(gui_prx_widgets.PrxBaseSubpage):

    def _on_apply(self):
        pass

    def _on_close(self):
        self._subwindow.close_window()

    def _on_apply_and_close(self):
        self._on_apply()
        self._on_close()

    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(AbsPrxSubpageForNewSplicing, self).__init__(window, session, subwindow, *args, **kwargs)

        self._configure = self.generate_local_configure()

        self.gui_page_setup_fnc()

    def get_gui_name(self):
        return self.choice_gui_name(
            self._configure.get('build')
        )

    def get_gui_tool_tip(self):
        return self.choice_gui_tool_tip(
            self._configure.get('build')
        )

    def gui_page_setup_fnc(self):
        prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_sca.widget)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self.choice_gui_name(
                self._configure.get('build.options')
            )
        )
        prx_sca.add_widget(self._prx_options_node)

        self._prx_options_node.build_by_data(
            self._configure.get('build.options.parameters'),
        )

        bottom_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(bottom_tool_bar.widget)
        bottom_tool_bar.set_expanded(True)

        self._apply_button = gui_qt_widgets.QtPressButton()
        bottom_tool_bar.add_widget(self._apply_button)
        self._apply_button._set_name_text_(
            self.choice_gui_name(
                self._configure.get('build.buttons.apply')
            )
        )
        self._apply_button.press_clicked.connect(self._on_apply)

        self._apply_and_close_button = gui_qt_widgets.QtPressButton()
        bottom_tool_bar.add_widget(self._apply_and_close_button)
        self._apply_and_close_button._set_name_text_(
            self._subwindow.choice_gui_name(
                self._configure.get('build.buttons.apply_and_close')
            )
        )
        self._apply_and_close_button.press_clicked.connect(self._on_apply_and_close)

        self._close_button = gui_qt_widgets.QtPressButton()
        bottom_tool_bar.add_widget(self._close_button)
        self._close_button._set_name_text_(
            self._subwindow.choice_gui_name(
                self._configure.get('build.buttons.close')
            )
        )
        self._close_button.press_clicked.connect(self._on_close)

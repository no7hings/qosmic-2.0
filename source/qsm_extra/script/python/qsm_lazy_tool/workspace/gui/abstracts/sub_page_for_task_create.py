# coding:utf-8
import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxSubPageForTaskCreate(gui_prx_widgets.PrxBaseSubPage):
    GUI_KEY = None

    RESOURCE_BRANCH = None

    STEP = None

    TASK = None

    def _on_apply(self):
        pass

    def _on_close(self):
        self._sub_window.close_window()

    def _on_apply_and_close(self):
        self._on_apply()
        self._on_close()

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(AbsPrxSubPageForTaskCreate, self).__init__(window, session, sub_window, *args, **kwargs)

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_sca.widget)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self._sub_window.choice_name(
                self._sub_window._configure.get('build.{}.options'.format(self.GUI_KEY))
            )
        )
        prx_sca.add_widget(self._prx_options_node)

        self._prx_options_node.build_by_data(
            self._sub_window._configure.get('build.{}.options.parameters'.format(self.GUI_KEY)),
        )

        bottom_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(bottom_tool_bar.widget)
        bottom_tool_bar.set_expanded(True)

        self._apply_button = gui_qt_widgets.QtPressButton()
        bottom_tool_bar.add_widget(self._apply_button)
        self._apply_button._set_name_text_(
            self._sub_window.choice_name(
                self._sub_window._configure.get('build.main.buttons.apply')
            )
        )
        self._apply_button.press_clicked.connect(self._on_apply)

        self._apply_and_close_button = gui_qt_widgets.QtPressButton()
        bottom_tool_bar.add_widget(self._apply_and_close_button)
        self._apply_and_close_button._set_name_text_(
            self._sub_window.choice_name(
                self._sub_window._configure.get('build.main.buttons.apply_and_close')
            )
        )
        self._apply_and_close_button.press_clicked.connect(self._on_apply_and_close)

        self._close_button = gui_qt_widgets.QtPressButton()
        bottom_tool_bar.add_widget(self._close_button)
        self._close_button._set_name_text_(
            self._sub_window.choice_name(
                self._sub_window._configure.get('build.main.buttons.close')
            )
        )
        self._close_button.press_clicked.connect(self._on_close)

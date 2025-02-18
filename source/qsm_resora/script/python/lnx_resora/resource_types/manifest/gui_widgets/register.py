# coding:utf-8
import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_screw.scripts as lnx_scr_scripts

from ....gui import abstracts as _abstracts


class PrxSubpageForManifestRegister(_abstracts.AbsPrxSubpageForManifestRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForManifestRegister, self).__init__(window, session, subwindow, *args, **kwargs)

    def _on_apply(self):
        node = self._prx_options_node
        resource_type = node.get('resource_type')
        gui_name = node.get('gui_name')
        gui_name_chs = node.get('gui_name_chs')
        image = node.get('image')

        lnx_scr_scripts.ManifestStageOpt().new_page(
            resource_type, gui_name, gui_name_chs, image
        )

        self._subwindow.popup_message(
            self._subwindow.choice_gui_message(
                self._configure.get('build.messages.register_successful')
            )
        )

        self._window.do_gui_refresh_all()

    def _on_close(self):
        self._subwindow.close_window()

    def _on_apply_and_close(self):
        self._on_apply()
        self._on_close()

    def gui_page_setup_fnc(self):
        prx_sca = gui_prx_widgets.PrxVScrollArea()
        self._qt_layout.addWidget(prx_sca.widget)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self._subwindow.choice_gui_name(
                self._configure.get('build.options')
            )
        )
        prx_sca.add_widget(self._prx_options_node)

        self._prx_options_node.build_by_data(
            self._configure.get('build.options.parameters'),
        )

        values, option_names, option_names_chs = lnx_scr_scripts.ManifestStageOpt.get_resource_type_gui_args()

        p = self._prx_options_node.get_port('resource_type')
        if self._window._language == 'chs':
            p.set_options(values, option_names_chs)
        else:
            p.set_options(values, option_names)

        p.set_history_key('tool-panels.lazy-resource.manifest-register.resource_type')
        p.pull_history_latest()

        bottom_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(bottom_tool_bar.widget)
        bottom_tool_bar.set_expanded(True)

        self._apply_button = gui_qt_widgets.QtPressButton()
        bottom_tool_bar.add_widget(self._apply_button)
        self._apply_button._set_name_text_(
            self._subwindow.choice_gui_name(
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

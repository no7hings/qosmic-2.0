# coding:utf-8
import lxbasic.scan as bsc_scan

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

from lnx_resora.gui import abstracts as lnx_rsr_abstracts

from .. import scripts as _scripts


class PrxSubpageForRegister(lnx_rsr_abstracts.AbsPrxSubpageForRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForRegister, self).__init__(window, session, subwindow, *args, **kwargs)

    def _on_apply(self):
        prx_node = self._prx_options_node

        directory_path = prx_node.get('directory')
        with_preview = prx_node.get('preview.enable')
        preview_pattern = prx_node.get('preview.pattern')
        with_file_reference = prx_node.get('file_reference.enable')
        file_reference_pattern = prx_node.get('file_reference.pattern')

        directory_kwargs = dict(
            directory=directory_path
        )

        formats = [str(x).strip() for x in prx_node.get('formats').split(',')]
        file_pattern = prx_node.get('file_pattern')

        file_paths = []

        for i_format in formats:
            i_directory_kwargs = dict(directory_kwargs)
            i_directory_kwargs['format'] = i_format

            i_file_regex = file_pattern.format(
                **i_directory_kwargs
            )

            i_file_paths = bsc_scan.ScanGlob.glob_files(i_file_regex)

            if i_file_paths:
                file_paths.extend(i_file_paths)

        if file_paths:
            result = self._window.exec_message_dialog(
                u'\n'.join(file_paths),
                title='Upload Files',
                size=(480, 480),
                status='warning',
            )
            if result:
                _scripts.MayaSceneRegisterBatch(
                    self._scr_stage.key, file_paths,
                    with_preview=with_preview, preview_pattern=preview_pattern,
                    with_file_reference=with_file_reference, file_reference_pattern=file_reference_pattern,
                ).execute()
        else:
            self._window.exec_message_dialog(
                'File is not found.',
                title='Upload Files',
                size=(480, 480),
                status='warning',
            )

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
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

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_lazy.screw.core as qsm_lzy_scr_core


class _AbsRegister(object):
    def _init_register_(self):
        self._scr_stage = None

    def set_scr_stage_key(self, scr_stage_key):
        self._scr_stage = qsm_lzy_scr_core.Stage(scr_stage_key)

        self._load_type_and_tags()

    def _load_type_and_tags(self):
        pass


class AbsPrxSubPageForMotionRegister(
    gui_prx_widgets.PrxBaseSubPage,
    _AbsRegister
):
    PAGE_KEY = 'motion'

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(AbsPrxSubPageForMotionRegister, self).__init__(window, session, sub_window, *args, **kwargs)
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

        self._type_qt_tag_widget = gui_qt_view_widgets.QtTagWidget()
        h_qt_lot_0.addWidget(
            self._type_qt_tag_widget
        )

        self._tag_qt_tag_widget = gui_qt_view_widgets.QtTagWidget()
        h_qt_lot_0.addWidget(
            self._tag_qt_tag_widget
        )


class _AbsPrxPageForAnyRegister(
    gui_prx_widgets.PrxBaseSubPage,
    _AbsRegister
):

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(_AbsPrxPageForAnyRegister, self).__init__(window, session, sub_window, *args, **kwargs)
        self._init_register_()
        self.gui_page_setup_fnc()

    def _on_apply(self):
        pass

    def _on_close(self):
        self._sub_window.close_window()

    def _on_apply_and_close(self):
        self._on_apply()
        self._on_close()

    def _load_type_and_tags(self):
        self._load_all_types()
        self._load_all_tags()

    def _load_all_types(self):
        entities = self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Type,
            filters=[
                ('kind', 'is not', 'unavailable')
            ]
        )
        entity_paths = [x.path for x in entities]
        leaf_paths = bsc_core.BscPath.to_leaf_paths(entity_paths)

        for i in entities:
            if i.path in leaf_paths:
                i_gui_name = i.gui_name
                if self._sub_window._language == 'chs':
                    i_gui_name = i.gui_name_chs

                i_flag, i_node = self._type_qt_tag_widget._view_model.create_item(i.path)

                i_node._item_model.set_name(i_gui_name)
                i_node._set_tool_tip_(i.to_description(self._sub_window._language))
            else:
                i_gui_name = i.gui_name
                if self._sub_window._language == 'chs':
                    i_gui_name = i.gui_name_chs

                i_flag, i_group = self._type_qt_tag_widget._view_model.create_item_as_group(i.path)

                i_group._set_expanded_(True)

                i_group._item_model.set_name(i_gui_name)
                i_group._set_tool_tip_(i.to_description(self._sub_window._language))

    def _load_all_tags(self):
        entities = self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Tag,
            filters=[
                ('kind', 'is not', 'unavailable')
            ]
        )
        entity_paths = [x.path for x in entities]
        leaf_paths = bsc_core.BscPath.to_leaf_paths(entity_paths)

        for i in entities:
            if i.path in leaf_paths:
                i_gui_name = i.gui_name
                if self._sub_window._language == 'chs':
                    i_gui_name = i.gui_name_chs

                i_flag, i_node = self._tag_qt_tag_widget._view_model.create_item(i.path)

                i_node._item_model.set_name(i_gui_name)
                i_node._set_tool_tip_(i.to_description(self._sub_window._language))
            # add as group
            else:
                i_gui_name = i.gui_name
                if self._sub_window._language == 'chs':
                    i_gui_name = i.gui_name_chs

                i_flag, i_group = self._tag_qt_tag_widget._view_model.create_item_as_group(i.path)

                i_group._set_expanded_(True)
                i_group._item_model.set_name(i_gui_name)
                i_group._set_tool_tip_(i.to_description(self._sub_window._language))

    def _on_list_all_files(self):
        directory_path = self._prx_options_node.get('directory')
        if directory_path:
            directory_opt = bsc_storage.StgDirectoryOpt(directory_path)
            formats = self._prx_options_node.get('formats')
            ext_includes = ['.{}'.format(str(x).strip()) for x in formats.split(',')]
            if self._prx_options_node.get('recursion_down_enable') is True:
                file_paths = directory_opt.get_all_file_paths(ext_includes=ext_includes)
            else:
                file_paths = directory_opt.get_file_paths(ext_includes=ext_includes)

            p = self._prx_options_node.get_port('files')
            for i_file_path in file_paths:
                p.append(i_file_path)

    def gui_get_scr_type_paths(self):
        return self._type_qt_tag_widget._view_model.get_all_checked_node_paths()

    def gui_get_scr_tag_paths(self):
        return self._tag_qt_tag_widget._view_model.get_all_checked_node_paths()

    def clear_type_and_tag_checked(self):
        self._type_qt_tag_widget._view_model.uncheck_all_items()
        self._tag_qt_tag_widget._view_model.uncheck_all_items()

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

        self._type_qt_tag_widget = gui_qt_view_widgets.QtTagWidget()
        h_qt_lot_0.addWidget(
            self._type_qt_tag_widget
        )
        self._type_qt_tag_widget._hide_all_tool_bar_()

        self._tag_qt_tag_widget = gui_qt_view_widgets.QtTagWidget()
        h_qt_lot_0.addWidget(
            self._tag_qt_tag_widget
        )
        self._tag_qt_tag_widget._hide_all_tool_bar_()

        bottom_tool_bar = gui_prx_widgets.PrxHToolBar()
        self._qt_layout.addWidget(bottom_tool_bar.widget)
        bottom_tool_bar.set_expanded(True)

        self._apply_and_close_button = gui_qt_widgets.QtPressButton()
        bottom_tool_bar.add_widget(self._apply_and_close_button)
        self._apply_and_close_button._set_name_text_(
            self._sub_window.choice_name(
                self._sub_window._configure.get('build.main.buttons.apply_and_close')
            )
        )
        self._apply_and_close_button.press_clicked.connect(self._on_apply_and_close)

        self._apply_button = gui_qt_widgets.QtPressButton()
        bottom_tool_bar.add_widget(self._apply_button)
        self._apply_button._set_name_text_(
            self._sub_window.choice_name(
                self._sub_window._configure.get('build.main.buttons.apply')
            )
        )
        self._apply_button.press_clicked.connect(self._on_apply)

        self._close_button = gui_qt_widgets.QtPressButton()
        bottom_tool_bar.add_widget(self._close_button)
        self._close_button._set_name_text_(
            self._sub_window.choice_name(
                self._sub_window._configure.get('build.main.buttons.close')
            )
        )
        self._close_button.press_clicked.connect(self._on_close)

        self._prx_options_node.set(
            'list_all_files', self._on_list_all_files
        )


class AbsPrxSubPageForVideoRegister(_AbsPrxPageForAnyRegister):
    PAGE_KEY = 'video'

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(AbsPrxSubPageForVideoRegister, self).__init__(window, session, sub_window, *args, **kwargs)

    def _on_apply(self):
        file_paths = self._prx_options_node.get('files')

        scr_type_paths = self.gui_get_scr_type_paths()
        scr_tag_paths = self.gui_get_scr_tag_paths()

        if file_paths:
            import qsm_lazy.resource.scripts as qsm_lzy_rsc_scripts

            qsm_lzy_rsc_scripts.VideoBatchRegister(
                self._scr_stage.key, file_paths
            ).execute(
                scr_type_paths, scr_tag_paths
            )

            self._sub_window.popup_message(
                self._sub_window.choice_message(
                    self._sub_window._configure.get('build.main.messages.register_successful')
                )
            )

        self._prx_options_node.get_port('files').do_clear()

        self.clear_type_and_tag_checked()


class AbsPrxSubPageForAudioRegister(_AbsPrxPageForAnyRegister):
    PAGE_KEY = 'audio'

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(AbsPrxSubPageForAudioRegister, self).__init__(window, session, sub_window, *args, **kwargs)

    def _on_apply(self):
        file_paths = self._prx_options_node.get('files')

        scr_type_paths = self.gui_get_scr_type_paths()
        scr_tag_paths = self.gui_get_scr_tag_paths()

        if file_paths:
            import qsm_lazy.resource.scripts as qsm_lzy_rsc_scripts

            qsm_lzy_rsc_scripts.AudioBatchRegister(
                self._scr_stage.key, file_paths
            ).execute(scr_type_paths, scr_tag_paths)

            self._sub_window.popup_message(
                self._sub_window.choice_message(
                    self._sub_window._configure.get('build.main.messages.register_successful')
                )
            )

        self._prx_options_node.get_port('files').do_clear()

        self.clear_type_and_tag_checked()

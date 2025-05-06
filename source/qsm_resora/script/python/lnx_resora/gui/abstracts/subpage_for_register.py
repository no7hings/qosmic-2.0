# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.qt.view_widgets as gui_qt_vew_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_screw.core as lnx_scr_core

from ... import core as _rsr_core


class _AbsRegister(object):
    @classmethod
    def _get_scr_type_or_tag_paths_addition(cls, qt_tag_widget):
        list_ = []
        for i_qt_item in qt_tag_widget._view_model.get_all_nodes():
            if i_qt_item._is_checked_() is True:
                list_.append(i_qt_item._item_model.get_path())
        return list_

    def _init_base(self):
        self._scr_stage = None

        self._post_fnc = None

    def set_scr_stage_key(self, scr_stage_name):
        self._scr_stage = lnx_scr_core.Stage(scr_stage_name)

        self._load_type_and_tags()
        self._update_history_options()

    def _load_type_and_tags(self):
        pass

    def _update_history_options(self):
        pass

    def set_post_fnc(self, fnc):
        self._post_fnc = fnc


class AbsGuiResourceRegisterMain(
    gui_prx_widgets.PrxBaseSubpage,
    _AbsRegister
):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(AbsGuiResourceRegisterMain, self).__init__(window, session, subwindow, *args, **kwargs)

        self._configure = self.generate_local_configure()

        self.gui_page_setup_fnc()


class AbsPrxSubpageForMotionRegister(
    gui_prx_widgets.PrxBaseSubpage,
    _AbsRegister
):
    GUI_KEY = 'motion'

    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(AbsPrxSubpageForMotionRegister, self).__init__(window, session, subwindow, *args, **kwargs)

        self._configure = self.generate_local_configure()

        self.gui_page_setup_fnc()

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

        self._prx_tool_group = gui_prx_widgets.PrxHToolGroupA()
        prx_sca.add_widget(self._prx_tool_group)
        self._prx_tool_group.set_expanded(True)
        self._prx_tool_group.set_name(
            gui_core.GuiUtil.choice_gui_name(
                self._subwindow._language, self._configure.get('build.filter')
            )
        )
        qt_widget_0 = gui_qt_widgets.QtTranslucentWidget()
        self._prx_tool_group.add_widget(qt_widget_0)
        h_qt_lot_0 = gui_qt_widgets.QtHBoxLayout(qt_widget_0)

        self._type_qt_tag_widget = gui_qt_vew_widgets.QtTagWidget()
        h_qt_lot_0.addWidget(
            self._type_qt_tag_widget
        )

        self._tag_qt_tag_widget = gui_qt_vew_widgets.QtTagWidget()
        h_qt_lot_0.addWidget(
            self._tag_qt_tag_widget
        )


class AbsPrxPageForMediaRegister(
    gui_prx_widgets.PrxBaseSubpage,
    _AbsRegister
):

    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(AbsPrxPageForMediaRegister, self).__init__(window, session, subwindow, *args, **kwargs)
        self._init_base()

        self._configure = self.generate_local_configure()

        self.gui_page_setup_fnc()

    def _on_apply(self):
        pass

    def _on_close(self):
        self._subwindow.close_window()

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
        leaf_paths = bsc_core.BscNodePath.to_leaf_paths(entity_paths)

        for i_scr_entity in entities:
            if i_scr_entity.path in leaf_paths:
                i_gui_name = i_scr_entity.gui_name
                if self._subwindow._language == 'chs':
                    i_gui_name = i_scr_entity.gui_name_chs

                if i_scr_entity.category == 'group':
                    i_flag, i_group = self._type_qt_tag_widget._view_model.create_group_item(i_scr_entity.path)

                    i_group._set_expanded_(True)

                    i_group._item_model.set_name(i_gui_name)
                    i_group._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))
                else:
                    i_flag, i_node = self._type_qt_tag_widget._view_model.create_item(i_scr_entity.path)

                    i_node._item_model.set_name(i_gui_name)
                    i_node._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))
            else:
                i_gui_name = i_scr_entity.gui_name
                if self._subwindow._language == 'chs':
                    i_gui_name = i_scr_entity.gui_name_chs

                i_flag, i_group = self._type_qt_tag_widget._view_model.create_group_item(i_scr_entity.path)

                i_group._set_expanded_(True)

                i_group._item_model.set_name(i_gui_name)
                i_group._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))

    def _load_all_tags(self):
        entities = self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Tag,
            filters=[
                ('kind', 'is not', 'unavailable'),
                ('trash', 'is', False),
            ]
        )
        entity_paths = [x.path for x in entities]
        leaf_paths = bsc_core.BscNodePath.to_leaf_paths(entity_paths)

        for i_scr_entity in entities:
            if i_scr_entity.path in leaf_paths:
                i_gui_name = i_scr_entity.gui_name
                if self._subwindow._language == 'chs':
                    i_gui_name = i_scr_entity.gui_name_chs
                if i_scr_entity.category == 'group':
                    i_flag, i_group = self._tag_qt_tag_widget._view_model.create_group_item(i_scr_entity.path)

                    i_group._set_expanded_(True)
                    i_group._item_model.set_name(i_gui_name)
                    i_group._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))
                else:
                    i_flag, i_node = self._tag_qt_tag_widget._view_model.create_item(i_scr_entity.path)

                    i_node._item_model.set_name(i_gui_name)
                    i_node._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))
            # add as group
            else:
                i_gui_name = i_scr_entity.gui_name
                if self._subwindow._language == 'chs':
                    i_gui_name = i_scr_entity.gui_name_chs

                i_flag, i_group = self._tag_qt_tag_widget._view_model.create_group_item(i_scr_entity.path)

                i_group._set_expanded_(True)
                i_group._item_model.set_name(i_gui_name)
                i_group._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))

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
            self._subwindow.choice_gui_name(
                self._configure.get('build.options')
            )
        )
        prx_sca.add_widget(self._prx_options_node)

        self._prx_options_node.build_by_data(
            self._configure.get('build.options.parameters'),
        )

        self._prx_tool_group = gui_prx_widgets.PrxHToolGroupA()
        prx_sca.add_widget(self._prx_tool_group)
        self._prx_tool_group.set_expanded(True)
        self._prx_tool_group.set_name(
            gui_core.GuiUtil.choice_gui_name(
                self._subwindow._language, self._configure.get('build.filter')
            )
        )
        qt_widget_0 = gui_qt_widgets.QtTranslucentWidget()
        self._prx_tool_group.add_widget(qt_widget_0)
        h_qt_lot_0 = gui_qt_widgets.QtHBoxLayout(qt_widget_0)

        self._type_qt_tag_widget = gui_qt_vew_widgets.QtTagWidget()
        h_qt_lot_0.addWidget(
            self._type_qt_tag_widget
        )
        self._type_qt_tag_widget._hide_all_tool_bar_()

        self._tag_qt_tag_widget = gui_qt_vew_widgets.QtTagWidget()
        h_qt_lot_0.addWidget(
            self._tag_qt_tag_widget
        )
        self._tag_qt_tag_widget._hide_all_tool_bar_()

        bottom_tool_bar = gui_prx_widgets.PrxHToolbar()
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

        self._prx_options_node.set(
            'list_all_files', self._on_list_all_files
        )


class AbsPrxSubpageForVideoRegister(AbsPrxPageForMediaRegister):
    GUI_KEY = 'video'

    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(AbsPrxSubpageForVideoRegister, self).__init__(window, session, subwindow, *args, **kwargs)

    def _update_history_options(self):
        for i in [
            'directory',
            'collect_source',
            'recursion_down_enable',
        ]:
            i_p = self._prx_options_node.get_port(i)
            if i_p:
                i_p.set_history_group(['resora', self._scr_stage.key])
                i_p.pull_history()


class AbsPrxSubpageForAudioRegister(AbsPrxPageForMediaRegister):
    GUI_KEY = 'audio'

    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(AbsPrxSubpageForAudioRegister, self).__init__(window, session, subwindow, *args, **kwargs)


class AbsPrxPageForAnyRegister(
    gui_prx_widgets.PrxBaseSubpage,
    _AbsRegister
):

    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(AbsPrxPageForAnyRegister, self).__init__(window, session, subwindow, *args, **kwargs)
        self._init_base()

        self._configure = self.generate_local_configure()

        self.gui_page_setup_fnc()

    def _on_apply(self):
        pass

    def _on_close(self):
        self._subwindow.close_window()

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
                ('kind', 'is not', 'unavailable'),
                ('trash', 'is', False),
            ]
        )
        entity_paths = [x.path for x in entities]
        leaf_paths = bsc_core.BscNodePath.to_leaf_paths(entity_paths)

        for i_scr_entity in entities:
            if i_scr_entity.path in leaf_paths:
                i_gui_name = i_scr_entity.gui_name
                if self._subwindow._language == 'chs':
                    i_gui_name = i_scr_entity.gui_name_chs

                if i_scr_entity.category == 'group':
                    i_flag, i_group = self._type_qt_tag_widget._view_model.create_group_item(i_scr_entity.path)

                    i_group._set_expanded_(True)

                    i_group._item_model.set_name(i_gui_name)
                    i_group._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))
                else:
                    i_flag, i_node = self._type_qt_tag_widget._view_model.create_item(i_scr_entity.path)

                    i_node._item_model.set_name(i_gui_name)
                    i_node._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))
            else:
                i_gui_name = i_scr_entity.gui_name
                if self._subwindow._language == 'chs':
                    i_gui_name = i_scr_entity.gui_name_chs

                i_flag, i_group = self._type_qt_tag_widget._view_model.create_group_item(i_scr_entity.path)

                i_group._set_expanded_(True)

                i_group._item_model.set_name(i_gui_name)
                i_group._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))

    def _load_all_tags(self):
        entities = self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Tag,
            filters=[
                ('kind', 'is not', 'unavailable')
            ]
        )
        entity_paths = [x.path for x in entities]
        leaf_paths = bsc_core.BscNodePath.to_leaf_paths(entity_paths)

        for i_scr_entity in entities:
            if i_scr_entity.path in leaf_paths:
                i_gui_name = i_scr_entity.gui_name
                if self._subwindow._language == 'chs':
                    i_gui_name = i_scr_entity.gui_name_chs
                if i_scr_entity.category == 'group':
                    i_flag, i_group = self._tag_qt_tag_widget._view_model.create_group_item(i_scr_entity.path)

                    i_group._set_expanded_(True)
                    i_group._item_model.set_name(i_gui_name)
                    i_group._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))
                else:
                    i_flag, i_node = self._tag_qt_tag_widget._view_model.create_item(i_scr_entity.path)

                    i_node._item_model.set_name(i_gui_name)
                    i_node._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))
            # add as group
            else:
                i_gui_name = i_scr_entity.gui_name
                if self._subwindow._language == 'chs':
                    i_gui_name = i_scr_entity.gui_name_chs

                i_flag, i_group = self._tag_qt_tag_widget._view_model.create_group_item(i_scr_entity.path)

                i_group._set_expanded_(True)
                i_group._item_model.set_name(i_gui_name)
                i_group._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))

    def _update_history_options(self):
        for i in [
            'directory',
            'file.pattern'
        ]:
            i_p = self._prx_options_node.get_port(i)
            if i_p:
                i_p.set_history_group(['resora', self._scr_stage.key])
                i_p.pull_history()

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
            self._subwindow.choice_gui_name(
                self._configure.get('build.options')
            )
        )
        prx_sca.add_widget(self._prx_options_node)

        self._prx_options_node.build_by_data(
            self._configure.get('build.options.parameters'),
        )

        self._prx_tool_group = gui_prx_widgets.PrxHToolGroupA()
        prx_sca.add_widget(self._prx_tool_group)
        self._prx_tool_group.set_expanded(True)
        self._prx_tool_group.set_name(
            gui_core.GuiUtil.choice_gui_name(
                self._subwindow._language, self._configure.get('build.filter')
            )
        )
        qt_widget_0 = gui_qt_widgets.QtTranslucentWidget()
        self._prx_tool_group.add_widget(qt_widget_0)
        h_qt_lot_0 = gui_qt_widgets.QtHBoxLayout(qt_widget_0)

        self._type_qt_tag_widget = gui_qt_vew_widgets.QtTagWidget()
        h_qt_lot_0.addWidget(
            self._type_qt_tag_widget
        )
        self._type_qt_tag_widget._hide_all_tool_bar_()

        self._tag_qt_tag_widget = gui_qt_vew_widgets.QtTagWidget()
        h_qt_lot_0.addWidget(
            self._tag_qt_tag_widget
        )
        self._tag_qt_tag_widget._hide_all_tool_bar_()

        bottom_tool_bar = gui_prx_widgets.PrxHToolbar()
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


class AbsPrxPageForAnySceneRegister(AbsPrxPageForAnyRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(AbsPrxPageForAnySceneRegister, self).__init__(window, session, subwindow, *args, **kwargs)

    def _on_apply(self):
        prx_node = self._prx_options_node

        directory_path = prx_node.get('directory')
        file_pattern = prx_node.get('file.pattern')
        file_formats = prx_node.get('file.formats')
        with_preview = prx_node.get('preview.enable')
        preview_pattern = prx_node.get('preview.pattern')
        preview_formats = prx_node.get('preview.formats')
        with_file_reference = prx_node.get('file_reference.enable')
        file_reference_pattern = prx_node.get('file_reference.pattern')

        scr_type_paths = self.gui_get_scr_type_paths()
        scr_tag_paths = self.gui_get_scr_tag_paths()

        _rsr_core.AnySceneRegisterBatch.register_fnc(
            self._scr_stage.key, directory_path,
            file_pattern=file_pattern, file_formats=file_formats,
            with_preview=with_preview, preview_pattern=preview_pattern, preview_formats=preview_formats,
            with_file_reference=with_file_reference, file_reference_pattern=file_reference_pattern,
            scr_type_paths=scr_type_paths, scr_tag_paths=scr_tag_paths
        )

        if self._post_fnc is not None:
            scr_type_paths_addition = self._get_scr_type_or_tag_paths_addition(self._type_qt_tag_widget)
            scr_tag_paths_addition = self._get_scr_type_or_tag_paths_addition(self._tag_qt_tag_widget)
            if scr_type_paths_addition or scr_tag_paths_addition:
                self._post_fnc(scr_type_paths_addition, scr_tag_paths_addition)

        self._subwindow.popup_message(
            self._subwindow.choice_gui_message(
                self._configure.get('build.messages.register_successful')
            )
        )


class AbsPrxSubpageForAssetRegister(
    gui_prx_widgets.PrxBaseSubpage,
    _AbsRegister
):
    GUI_KEY = 'asset'

    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(AbsPrxSubpageForAssetRegister, self).__init__(window, session, subwindow, *args, **kwargs)

        self._init_base()

        self._configure = self.generate_local_configure()

        self.gui_page_setup_fnc()

    def gui_page_setup_fnc(self):
        pass


class AbsPrxPageForQuixelRegister(
    gui_prx_widgets.PrxBaseSubpage,
    _AbsRegister
):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(AbsPrxPageForQuixelRegister, self).__init__(window, session, subwindow, *args, **kwargs)

        self._init_base()

        self._configure = self.generate_local_configure()

        self.gui_page_setup_fnc()

    def _on_close(self):
        self._subwindow.close_window()

    def _on_apply_and_close(self):
        self._on_apply()
        self._on_close()

    def _on_apply(self):
        pass

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

        bottom_tool_bar = gui_prx_widgets.PrxHToolbar()
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

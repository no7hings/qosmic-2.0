# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.widgets as gui_qt_widgets

import lxgui.qt.view_widgets as gui_qt_vew_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lnx_screw.core as lnx_scr_core


class _AbsAssign(object):

    @classmethod
    def _get_scr_type_or_tag_paths_addition(cls, qt_tag_widget):
        list_ = []
        for i_qt_item in qt_tag_widget._view_model.get_all_nodes():
            if i_qt_item._is_checked_() is True:
                list_.append(i_qt_item._item_model.get_path())
        return list_

    @classmethod
    def _get_scr_type_or_tag_paths_deletion(cls, qt_tag_widget):
        list_ = []
        for i_qt_item in qt_tag_widget._view_model.get_all_nodes():
            # check is usable
            if i_qt_item._item_model.get_number_flag() is True:
                if i_qt_item._is_checked_() is False:
                    list_.append(i_qt_item._item_model.get_path())
        return list_

    def _init_base(self):
        self._scr_stage = None

        self._scr_nodes = []

        self._post_fnc = None

    def set_scr_stage_key(self, scr_stage_name):
        self._scr_stage = lnx_scr_core.Stage(scr_stage_name)

        self._load_type_or_tags()

    def _load_type_or_tags(self):
        raise NotImplementedError()

    def set_scr_node_paths(self, paths):
        self._scr_nodes = list(filter(None, [self._scr_stage.get_node(x) for x in paths]))
        self._update_type_or_tags()

    def set_scr_nodes(self, scr_nodes):
        self._scr_nodes = scr_nodes
        self._update_type_or_tags()

    def _update_type_or_tags(self):
        raise NotImplementedError()

    def set_post_fnc(self, fnc):
        self._post_fnc = fnc


class AbsPrxSubpageForAnyAssign(
    gui_prx_widgets.PrxBaseSubpage,
    _AbsAssign
):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(AbsPrxSubpageForAnyAssign, self).__init__(window, session, subwindow, *args, **kwargs)

        self._configure = self.generate_local_configure()

        self._init_base()

        self.gui_page_setup_fnc()

    def _on_apply(self):
        pass

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

        self._prx_tool_group = gui_prx_widgets.PrxHToolGroup()
        prx_sca.add_widget(self._prx_tool_group)
        self._prx_tool_group.set_expanded(True)
        self._prx_tool_group.set_name(
            gui_core.GuiUtil.choice_gui_name(
                self._subwindow._language, self._configure.get('build.filter'.format(self.GUI_KEY))
            )
        )
        self._qt_tag_widget = gui_qt_vew_widgets.QtTagWidget()
        self._prx_tool_group.add_widget(
            self._qt_tag_widget
        )
        self._qt_tag_widget._hide_all_tool_bar_()

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


class AbsPrxSubpageForTypeAssign(AbsPrxSubpageForAnyAssign):
    GUI_KEY = 'type'

    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(AbsPrxSubpageForTypeAssign, self).__init__(window, session, subwindow, *args, **kwargs)

    def _on_apply(self):
        if not self._scr_nodes:
            return

        includes = self._prx_options_node.get('includes')

        scr_entity_path_set = set()
        if 'addition' in includes:
            scr_entity_paths_addition = self._get_scr_type_or_tag_paths_addition(self._qt_tag_widget)
            if scr_entity_paths_addition:
                scr_entity_path_set.update(set(scr_entity_paths_addition))
                with self._subwindow.gui_progressing(maximum=len(self._scr_nodes)) as g_p:
                    for i_scr_node in self._scr_nodes:
                        for j_scr_entity_path in scr_entity_paths_addition:
                            self._scr_stage.create_node_type_assign(i_scr_node.path, j_scr_entity_path)

                        g_p.do_update()

        if 'deletion' in includes:
            scr_entity_paths_deletion = self._get_scr_type_or_tag_paths_deletion(self._qt_tag_widget)
            if scr_entity_paths_deletion:
                scr_entity_path_set.update(set(scr_entity_paths_deletion))
                with self._subwindow.gui_progressing(maximum=len(self._scr_nodes)) as g_p:
                    for i_scr_node in self._scr_nodes:
                        for j_scr_entity_path in scr_entity_paths_deletion:
                            self._scr_stage.remove_node_type_assign(i_scr_node.path, j_scr_entity_path)

                        g_p.do_update()

        self._update_type_or_tags()
        if self._post_fnc:
            self._post_fnc(scr_entity_path_set)

    def _load_type_or_tags(self):
        self._load_all_types()

    def _load_all_types(self):
        entities = self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Type,
            filters=[
                # ignore unavailable kind, this kind do not support for user action.
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
                    i_flag, i_group = self._qt_tag_widget._view_model.create_group_item(i_scr_entity.path)

                    i_group._set_expanded_(True)
                    i_group._item_model.set_name(i_gui_name)
                    i_group._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))
                else:
                    i_flag, i_node = self._qt_tag_widget._view_model.create_item(i_scr_entity.path)

                    i_node._item_model.set_name(i_gui_name)
                    i_node._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))
            # add as group
            else:
                i_gui_name = i_scr_entity.gui_name
                if self._subwindow._language == 'chs':
                    i_gui_name = i_scr_entity.gui_name_chs

                i_flag, i_group = self._qt_tag_widget._view_model.create_group_item(i_scr_entity.path)

                i_group._set_expanded_(True)
                i_group._item_model.set_name(i_gui_name)
                i_group._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))

    def _update_type_or_tags(self):
        self._update_all_types()

    def _update_all_types(self):
        dict_ = {}
        for i_scr_node in self._scr_nodes:
            i_scr_tags = self._scr_stage.find_node_assign_types(i_scr_node.path)
            for j_scr_tag in i_scr_tags:
                dict_.setdefault(
                    j_scr_tag.path, set()
                ).add(i_scr_node.path)

        for i_qt_item in self._qt_tag_widget._view_model.get_all_nodes():
            i_path = i_qt_item._item_model.get_path()
            if i_path in dict_:
                i_qt_item._set_assign_path_set_(dict_[i_path])
                i_qt_item._update_assign_path_set_to_ancestors()
                i_qt_item._update_check_state_(True)
            else:
                i_qt_item._set_assign_path_set_(set())


class AbsPrxSubpageForTagAssign(AbsPrxSubpageForAnyAssign):
    GUI_KEY = 'tag'

    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(AbsPrxSubpageForTagAssign, self).__init__(window, session, subwindow, *args, **kwargs)

    def _on_apply(self):
        if not self._scr_nodes:
            return

        includes = self._prx_options_node.get('includes')

        scr_entity_path_set = set()
        if 'addition' in includes:
            scr_entity_paths_addition = self._get_scr_type_or_tag_paths_addition(self._qt_tag_widget)
            if scr_entity_paths_addition:
                scr_entity_path_set.update(set(scr_entity_paths_addition))
                with self._subwindow.gui_progressing(maximum=len(self._scr_nodes)) as g_p:
                    for i_scr_node in self._scr_nodes:
                        for j_scr_entity_path in scr_entity_paths_addition:
                            self._scr_stage.create_node_tag_assign(i_scr_node.path, j_scr_entity_path)

                        g_p.do_update()

        if 'deletion' in includes:
            scr_entity_paths_deletion = self._get_scr_type_or_tag_paths_deletion(self._qt_tag_widget)
            if scr_entity_paths_deletion:
                scr_entity_path_set.update(set(scr_entity_paths_deletion))
                with self._subwindow.gui_progressing(maximum=len(self._scr_nodes)) as g_p:
                    for i_scr_node in self._scr_nodes:
                        for j_scr_entity_path in scr_entity_paths_deletion:
                            self._scr_stage.remove_node_tag_assign(i_scr_node.path, j_scr_entity_path)

                        g_p.do_update()

        self._update_type_or_tags()
        if self._post_fnc:
            self._post_fnc(scr_entity_path_set)

    def _load_type_or_tags(self):
        self._load_all_tags()

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
                    i_flag, i_group = self._qt_tag_widget._view_model.create_group_item(i_scr_entity.path)

                    i_group._set_expanded_(True)
                    i_group._item_model.set_name(i_gui_name)
                    i_group._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))
                else:
                    i_flag, i_node = self._qt_tag_widget._view_model.create_item(i_scr_entity.path)

                    i_node._item_model.set_name(i_gui_name)
                    i_node._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))
            # add as group
            else:
                i_gui_name = i_scr_entity.gui_name
                if self._subwindow._language == 'chs':
                    i_gui_name = i_scr_entity.gui_name_chs

                i_flag, i_group = self._qt_tag_widget._view_model.create_group_item(i_scr_entity.path)

                i_group._set_expanded_(True)
                i_group._item_model.set_name(i_gui_name)
                i_group._set_tool_tip_(i_scr_entity.to_description(self._subwindow._language))

    def _update_type_or_tags(self):
        self._update_all_tags()

    def _update_all_tags(self):
        dict_ = {}
        for i_scr_node in self._scr_nodes:
            i_scr_tags = self._scr_stage.find_node_assign_tags(i_scr_node.path)
            for j_scr_tag in i_scr_tags:
                dict_.setdefault(
                    j_scr_tag.path, set()
                ).add(i_scr_node.path)

        for i_qt_item in self._qt_tag_widget._view_model.get_all_nodes():
            i_path = i_qt_item._item_model.get_path()
            if i_path in dict_:
                i_qt_item._set_assign_path_set_(dict_[i_path])
                i_qt_item._update_assign_path_set_to_ancestors()
                i_qt_item._update_check_state_(True)
            else:
                i_qt_item._set_assign_path_set_(set())

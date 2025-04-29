# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.proxy.abstracts as gui_prx_abstracts

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core


class PrxUnitBaseOpt(object):
    GUI_NAMESPACE = 'rig'

    def __init__(self, window, page, session):
        self._window = window
        self._page = page
        self._session = session


class PrxTreeviewUnitForAssetTagFilterOpt(
    PrxUnitBaseOpt,
    gui_prx_abstracts.AbsGuiTreeViewAsTagOpt,
):
    GROUP_SCHEME = gui_prx_abstracts.AbsGuiTreeViewAsTagOpt.GroupScheme.Hide

    def __init__(self, window, page, session, prx_tree_view):
        super(PrxTreeviewUnitForAssetTagFilterOpt, self).__init__(window, page, session)
        self._init_tree_view_as_tag_opt_(prx_tree_view, self.GUI_NAMESPACE)

        self._gui_thread_flag = 0


class PrxTreeviewUnitForAssetOpt(
    PrxUnitBaseOpt,
    gui_prx_abstracts.AbsGuiPrxCacheDef,
):
    ROOT_NAME = 'Tags'

    NAMESPACE = 'tag'
    
    NAMESPACE_FOR_COMPONENT = 'component'

    TAG_KEYS_INCLUDE = [
        'project',
        'role',
        'asset',
    ]

    RESOURCES_QUERY_CLS = None

    CHECK_BOX_FLAG = False
    CHECK_DEFAULT = True

    TOOL_INCLUDES = [
        'isolate-select',
        'reference',
    ]

    def _gui_build_reference_tools(self):
        for i in [
            (
                'remove-resource',
                'tool/maya/remove-reference',
                '"LMB-click" to remove selected rigs',
                self.do_dcc_remove_asset_references
            ),
            (
                'duplicate-resource',
                'tool/maya/duplicate-reference',
                '"LMB-click" to duplicate selected rigs',
                self.do_dcc_duplicate_asset_references
            ),
            (
                'reload-resource',
                'tool/maya/reload-reference',
                '"LMB-click" to reload selected rigs',
                self.do_dcc_reload_asset_references
            ),
            (
                'unload-resource',
                'tool/maya/unload-reference',
                '"LMB-click" to unload selected rigs',
                self.do_dcc_unload_asset_references
            ),
            (
                'replace-resource',
                'tool/maya/replace-reference',
                '"LMB-click" to unload replace rigs',
                self.do_dcc_replace_asset_references
            ),
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = gui_prx_widgets.PrxIconPressButton()
            self._prx_asset_prx_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_press_clicked_to(i_fnc)
            self._tool_dict[i_key] = i_tool

    def _gui_asset_menu_data_generate_fnc(self):
        if gui_core.GuiUtil.language_is_chs():
            return [
                [
                    '引用', 'file/folder',
                    [
                        ('复制', 'tool/maya/duplicate-reference', self.do_dcc_duplicate_asset_references),
                        ('加载/重载', 'tool/maya/reload-reference', self.do_dcc_reload_asset_references),
                        ('卸载', 'tool/maya/unload-reference', self.do_dcc_unload_asset_references),
                        ('替换', 'tool/maya/replace-reference', self.do_dcc_replace_asset_references),
                    ]
                ],
            ]
        else:
            return [
                [
                    'Reference', 'file/folder',
                    [
                        ('Duplicate', 'tool/maya/duplicate-reference', self.do_dcc_duplicate_asset_references),
                        ('Load/Reload', 'tool/maya/reload-reference', self.do_dcc_reload_asset_references),
                        ('Unload', 'tool/maya/unload-reference', self.do_dcc_unload_asset_references),
                        ('Replace', 'tool/maya/replace-reference', self.do_dcc_replace_asset_references),
                    ]
                ],
            ]
    
    # reference
    def do_dcc_remove_asset_references(self):

        result = self._window.exec_message_dialog(
            self._window.choice_gui_message(
                self._window._configure.get('build.messages.remove_reference')
            ),
            status='warning'
        )
        # w = gui_core.GuiDialog.create(
        #     label=self._session.gui_name,
        #     sub_label='remove-resource',
        #     content='do you want remove selected rigs?\n, press "Ok" to continue',
        #     status=gui_core.GuiDialog.ValidationStatus.Warning,
        #     parent=self._window.widget
        # )

        # result = w.get_result()
        if result is True:
            _ = self._prx_tree_view.get_selected_items()
            for i in _:
                i_resource = i.get_gui_dcc_obj(self.NAMESPACE)
                i_reference_opt = i_resource.reference_opt
                i_reference_opt.do_remove()

            self._page.do_gui_refresh_all()

    def do_dcc_duplicate_asset_references(self):
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_resource = i.get_gui_dcc_obj(self.NAMESPACE)
            i_reference_opt = i_resource.reference_opt
            i_reference_opt.do_duplicate()

        self._page.do_gui_refresh_all()

    def do_dcc_reload_asset_references(self):
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_resource = i.get_gui_dcc_obj(self.NAMESPACE)
            i_reference_opt = i_resource.reference_opt
            i_reference_opt.do_reload()

        self._page.do_gui_refresh_all(force=True)

    def do_dcc_unload_asset_references(self):
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_resource = i.get_gui_dcc_obj(self.NAMESPACE)
            i_reference_opt = i_resource.reference_opt
            i_reference_opt.do_unload()

        self._page.do_gui_refresh_all(force=True)

    def do_dcc_replace_asset_references(self):
        file_path = gui_core.GuiStorageDialog.open_file(
            ext_filter='All File (*.ma *.mb)',
            parent=self._window._qt_widget
        )
        if file_path:
            _ = self._prx_tree_view.get_selected_items()
            for i in _:
                i_resource = i.get_gui_dcc_obj(self.NAMESPACE)
                i_reference_opt = i_resource.reference_opt
                i_reference_opt.do_replace(file_path)

        self._page.do_gui_refresh_all(force=True)

    # isolate select
    def _gui_build_isolate_select_tools(self):
        for i in [
            (
                'isolate-select-resource',
                'tool/isolate-select',
                '"LMB-click" to turn "on" or "off" isolate select mode',
                self.do_dcc_isolate_select_resources
            )
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = gui_prx_widgets.PrxIconToggleButton()
            self._prx_isolate_select_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_check_toggled_to(i_fnc)
            self._tool_dict[i_key] = i_tool

        for i in [
            (
                'isolate-select-add-resource',
                'tool/isolate-select-add',
                '"LMB-click" to add rigs to isolate select',
                self.do_dcc_isolate_select_add_resources
            ),
            (
                'isolate-select-remove-resource',
                'tool/isolate-select-remove',
                '"LMB-click" to remove rigs to isolate select',
                self.do_dcc_isolate_select_remove_resources
            )
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = gui_prx_widgets.PrxIconPressButton()
            self._prx_isolate_select_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_press_clicked_to(i_fnc)
            self._tool_dict[i_key] = i_tool

    def do_dcc_isolate_select_resources(self, boolean):
        panel_current = qsm_mya_core.ViewPanels.get_current_name()
        isolate_select_opt = qsm_mya_core.ViewPanelIsolateSelectOpt(panel_current)
        isolate_select_opt.set_enable(boolean)
        if boolean is True:
            _ = self._prx_tree_view.get_selected_items()
            for i in _:
                i_resource = i.get_gui_dcc_obj(self.NAMESPACE)
                i_roots = i_resource.get_all_for_isolate_select()
                isolate_select_opt.add_nodes(i_roots)

    def do_dcc_isolate_select_add_resources(self):
        panel_current = qsm_mya_core.ViewPanels.get_current_name()
        isolate_select_opt = qsm_mya_core.ViewPanelIsolateSelectOpt(panel_current)
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_resource = i.get_gui_dcc_obj(self.NAMESPACE)
            i_roots = i_resource.get_all_for_isolate_select()
            isolate_select_opt.add_nodes(i_roots)

    def do_dcc_isolate_select_remove_resources(self):
        panel_current = qsm_mya_core.ViewPanels.get_current_name()
        isolate_select_opt = qsm_mya_core.ViewPanelIsolateSelectOpt(panel_current)
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_resource = i.get_gui_dcc_obj(self.NAMESPACE)
            i_roots = i_resource.get_all_for_isolate_select()
            isolate_select_opt.remove_nodes(i_roots)

    def do_gui_refresh_tools(self):
        panel_current = qsm_mya_core.ViewPanels.get_current_name()
        if self._window.window_is_active():
            isolate_tool = self._tool_dict['isolate-select-resource']
            isolate_select_opt = qsm_mya_core.ViewPanelIsolateSelectOpt(panel_current)
            is_checked = isolate_tool.get_is_checked()
            is_enable = isolate_select_opt.is_enable()
            if is_checked != is_enable:
                isolate_tool.set_checked(is_enable)

    # selection
    def do_dcc_refresh_resources_selection(self):
        if self._prx_tree_view.has_focus() is True:
            resources = self.gui_get_selected_resources()
            components = self.gui_get_selected_components()
            paths = []
            if resources:
                scheme = self._page.gui_get_selection_scheme()
                [paths.extend(x.find_nodes_by_scheme(scheme)) for x in resources]
            if components:
                [paths.append(x.get_path()) for x in components]

            if paths:
                cmds.select([x for x in paths if x])
            else:
                cmds.select(clear=1)

    def do_gui_refresh_by_dcc_selection(self):
        if self._prx_tree_view.has_focus() is False:
            namespaces = qsm_mya_core.Namespaces.extract_from_selection()
            if namespaces:
                paths = ['/{}'.format(i) for i in namespaces]
            else:
                paths = []

            self.do_gui_selected(paths)

    def __init__(self, window, page, session, prx_tree_view):
        super(PrxTreeviewUnitForAssetOpt, self).__init__(window, page, session)
        self._init_cache_def_(prx_tree_view)
        self._prx_tree_view = prx_tree_view
        self._prx_tree_view.create_header_view(
            [('name', 2), ('description', 1)],
            self._window.get_definition_window_size()[0]-48
        )
        self._prx_tree_view.connect_item_select_changed_to(
            self.do_dcc_refresh_resources_selection
        )
        self._prx_tree_view.get_top_tool_bar().set_expanded(True)

        self._tool_dict = {}
        if 'reference' in self.TOOL_INCLUDES:
            self._prx_asset_prx_tool_box = self._prx_tree_view.add_top_tool_box(
                'reference', insert_args=1
            )
            self._gui_build_reference_tools()

        if 'isolate-select' in self.TOOL_INCLUDES:
            self._prx_isolate_select_tool_box = self._prx_tree_view.add_top_tool_box(
                'isolate-select', insert_args=1
            )
            self._gui_build_isolate_select_tools()

        self._item_dict = self._prx_tree_view._item_dict

        self._assets_query = self.RESOURCES_QUERY_CLS()

    def restore(self):
        self._push_cache()
        self._prx_tree_view.do_clear()

    def gui_check_exists(self, path):
        return self._item_dict.get(path) is not None

    def gui_get_one(self, path):
        return self._item_dict[path]

    def gui_register(self, path, prx_item):
        self._item_dict[path] = prx_item

    def gui_add_root(self):
        path = '/'
        if self.gui_check_exists(path) is False:
            prx_item = self._prx_tree_view.create_item(
                self.ROOT_NAME,
                icon=gui_core.GuiIcon.get('database/all'),
            )

            self.gui_register(path, prx_item)

            prx_item.set_expanded(True)
            if self.CHECK_BOX_FLAG is True:
                prx_item.set_checked(self.CHECK_DEFAULT)
            return True, prx_item
        return False, self.gui_get_one(path)

    def gui_add_group(self, path_opt):
        def build_fnc_():
            prx_item.set_name(
                path_opt.get_name()
            )
            prx_item.set_icon_by_file(
                gui_core.GuiIcon.get('database/group')
            )
            prx_item.set_tool_tip(
                (
                    'path: {}\n'
                ).format(path_opt.get_path())
            )

        path = path_opt.path
        if self.gui_check_exists(path) is False:
            create_kwargs = dict(
                name='loading ...',
                filter_key=path,
            )
            parent = path_opt.get_parent()
            if parent is not None:
                prx_item_parent = self.gui_get_one(parent.path)
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_tree_view.create_item(
                    **create_kwargs
                )

            self.gui_register(path, prx_item)

            prx_item.set_expanded(True)
            if self.CHECK_BOX_FLAG is True:
                prx_item.set_checked(self.CHECK_DEFAULT)

            prx_item.set_show_build_fnc(build_fnc_)
            return True, prx_item
        return False, self.gui_get_one(path)

    def gui_add_resource(self, resource):
        def build_fnc_():
            prx_item.set_name(
                path_opt.get_name()
            )
            _reference_node = resource.reference_opt
            _semantic_tag_filter_data = {}
            _tag_group_key = '/status'
            if _reference_node.is_loaded():
                prx_item.set_icon_by_file(
                    gui_core.GuiIcon.get('node/maya/reference')
                )
                _semantic_tag_filter_data.setdefault(
                    _tag_group_key, set()
                ).add('/status/loaded')
                self._page._gui_asset_tag_filter_prx_unit.gui_register_tag_by_path(
                    '/status/loaded', path, auto_create_ancestors=True
                )
            else:
                prx_item.set_icon_by_file(
                    gui_core.GuiIcon.get('node/maya/reference-unloaded')
                )
                _semantic_tag_filter_data.setdefault(
                    _tag_group_key, set()
                ).add('/status/unloaded')
                self._page._gui_asset_tag_filter_prx_unit.gui_register_tag_by_path(
                    '/status/unloaded', path, auto_create_ancestors=True
                )

            if isinstance(resource, qsm_mya_hdl_anm_core.AdvRigAsset):
                if resource.is_skin_proxy_exists():
                    prx_item.set_status(
                        prx_item.ValidationStatus.Active
                    )
                    if resource.is_skin_proxy_enable():
                        if self._window._language == 'chs':
                            prx_item.set_name('简模代理（启用）', 1)
                        else:
                            prx_item.set_name('Skin Proxy (Enable)', 1)
                    else:
                        if self._window._language == 'chs':
                            prx_item.set_name('简模代理（禁用）', 1)
                        else:
                            prx_item.set_name('Skin Proxy (Disable)', 1)
                elif resource.is_dynamic_gpu_exists():
                    prx_item.set_status(
                        prx_item.ValidationStatus.New
                    )
                    if resource.is_dynamic_gpu_enable():
                        if self._window._language == 'chs':
                            prx_item.set_name('动态GPU（启用）', 1)
                        else:
                            prx_item.set_name('Dynamic GPU (Enable)', 1)
                    else:
                        if self._window._language == 'chs':
                            prx_item.set_name('动态GPU（禁用）', 1)
                        else:
                            prx_item.set_name('Dynamic GPU (Disable)', 1)
                elif resource.is_cfx_cloth_exists():
                    prx_item.set_status(
                        prx_item.ValidationStatus.Locked
                    )
                    if self._window._language == 'chs':
                        prx_item.set_name('CFX布料', 1)
                    else:
                        prx_item.set_name('CFX Cloth', 1)
                else:
                    prx_item.set_status(
                        prx_item.ValidationStatus.Normal
                    )
                    prx_item.set_name('Rig', 1)

            prx_item.get_item()._update_item_semantic_tag_filter_keys_tgt_(_semantic_tag_filter_data)
            prx_item.set_tool_tip(
                '\n'.join(['{}: {}'.format(_k, _v) for _k, _v in resource.variants.items()])
            )

            tag = self.gui_add_resource_components(resource)
            if tag is not None:
                prx_item.set_icon_name(
                    'node/maya/reference-cfx'
                )
                prx_item.set_name('Rig for {}'.format(tag), 1)

            prx_item.set_menu_data(self._gui_asset_menu_data_generate_fnc())

        path = resource.path
        if self.gui_check_exists(path) is False:
            path_opt = resource.path_opt
            create_kwargs = dict(
                name='loading ...',
                filter_key=path,
            )
            parent = path_opt.get_parent()
            if parent is not None:
                prx_item_parent = self.gui_get_one(parent.path)
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_tree_view.create_item(
                    **create_kwargs
                )

            # prx_item.set_checked(True)
            self.gui_register(path, prx_item)
            variants = resource.variants
            semantic_tag_filter_data = {}
            for i in self.TAG_KEYS_INCLUDE:
                if i in variants:
                    i_v = variants[i]
                    i_tag_group = '/{}'.format(i)
                    i_tag_path = '/{}/{}'.format(i, i_v)

                    semantic_tag_filter_data.setdefault(
                        i_tag_group, set()
                    ).add(i_tag_path)
                    self._page._gui_asset_tag_filter_prx_unit.gui_register_tag_by_path(
                        i_tag_path, path, auto_create_ancestors=True
                    )

            prx_item.get_item()._update_item_semantic_tag_filter_keys_tgt_(semantic_tag_filter_data)
            prx_item.set_gui_dcc_obj(
                resource, namespace=self.NAMESPACE
            )

            if self.CHECK_BOX_FLAG is True:
                prx_item.set_checked(self.CHECK_DEFAULT)

            prx_item.set_show_build_fnc(build_fnc_)
            return True, prx_item
        return False, self.gui_get_one(path)

    def gui_add_resource_components(self, resource):
        return None
    
    def gui_add_resource_component(self, path, dcc_path):
        def build_fnc_():
            prx_item.set_name(
                path_opt.get_name()
            )
            _node_type = node_opt.get_type_name()
            prx_item.set_icon(
                gui_qt_core.QtMaya.generate_qt_icon_by_name(_node_type)
            )
            prx_item.set_name(
                _node_type, 1
            )

        if self.gui_check_exists(path) is False:
            path_opt = bsc_core.BscNodePathOpt(path)
            create_kwargs = dict(
                name='loading ...',
                filter_key=path,
            )

            parent = path_opt.get_parent()
            if parent is not None:
                prx_item_parent = self.gui_get_one(parent.path)
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
                # fixme: bug for child has non filter data, so copy from parent temporary.
                prx_item.get_item()._set_item_semantic_tag_filter_keys_tgt_(
                    prx_item_parent.get_item()._get_item_semantic_tag_filter_keys_tgt_()
                )
            else:
                prx_item = self._prx_tree_view.create_item(
                    **create_kwargs
                )
            self.gui_register(path, prx_item)

            node_opt = qsm_mya_core.EtrNodeOpt(dcc_path)
            prx_item.set_gui_dcc_obj(
                node_opt, namespace=self.NAMESPACE_FOR_COMPONENT
            )

            if self.CHECK_BOX_FLAG is True:
                prx_item.set_checked(self.CHECK_DEFAULT)

            prx_item.set_show_build_fnc(build_fnc_)
            return True, prx_item
        return False, self.gui_get_one(path)

    def gui_add_one(self, resource):
        ancestors = resource.path_opt.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i_path_opt in ancestors:
                if self.gui_check_exists(i_path_opt.path) is False:
                    i_is_create, i_prx_item = self.gui_add_group(i_path_opt)
                    if i_is_create is True:
                        i_prx_item.set_expanded(True)
        #
        self.gui_add_resource(resource)

    def gui_add_all(self):
        self.gui_add_root()
        resources = self._assets_query.get_all()
        for i_resource in resources:
            self.gui_add_one(i_resource)

        self._pull_cache()

    def get_current_obj(self):
        _ = self._prx_tree_view.get_selected_items()
        if _:
            return _[-1].get_gui_dcc_obj(self.NAMESPACE)

    def gui_get_selected_resources(self):
        list_ = []
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_resource = i.get_gui_dcc_obj(self.NAMESPACE)
            if i_resource is not None:
                list_.append(i_resource)
        return list_
    
    def gui_get_checked_resources(self):
        list_ = []
        _ = self._prx_tree_view.get_all_checked_items()
        for i in _:
            i_resource = i.get_gui_dcc_obj(self.NAMESPACE)
            if i_resource is not None:
                list_.append(i_resource)
        return list_

    def gui_get_selected_components(self):
        list_ = []
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_component = i.get_gui_dcc_obj(self.NAMESPACE_FOR_COMPONENT)
            if i_component is not None:
                list_.append(i_component)
        return list_

    def gui_get_items_selected(self, paths):
        return [self.gui_get_one(i) for i in paths if self.gui_check_exists(i)]

    def do_gui_selected(self, paths):
        if paths:
            prx_items = self.gui_get_items_selected(paths)
            self._prx_tree_view.select_items(prx_items)
        else:
            self._prx_tree_view.clear_selection()

    def get_resources_query(self):
        return self._assets_query

    def do_gui_select_all_resources(self):
        list_ = []
        for k, v in self._item_dict.items():
            i_resource = v.get_gui_dcc_obj(self.NAMESPACE)
            if i_resource is not None:
                list_.append(v)

        self._prx_tree_view.select_items(list_)

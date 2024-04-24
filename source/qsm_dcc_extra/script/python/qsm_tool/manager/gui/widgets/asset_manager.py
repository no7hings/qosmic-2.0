# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets

import lxgui.proxy.abstracts as gui_prx_abstracts

import qsm_general.scan as qsm_gnl_scan

import qsm_maya.core as qsm_mya_core

import qsm_maya.asset.core as qsm_mya_ast_core

import qsm_maya.rig.core as qsm_mya_rig_core

import qsm_maya.rig.scripts as qsm_mya_rig_scripts

import qsm_maya.motion as qsm_mya_motion

import qsm_gui.proxy.widgets as qsm_prx_widgets


class _GuiProcessOpt(object):
    def __init__(self, window):
        self._window = window

        self._ts = []

    def execute(self, button, cmds):
        def finished_fnc_(index, status, results):
            button.set_finished_at(index, status)

        def status_changed_fnc_(index, status):
            button.set_status_at(index, status)

        def run_fnc_():
            self._ts = []

            for _i_index, _i_cmd in enumerate(cmds):
                bsc_core.TrdCommandPool.set_wait()
                #
                _i_t = bsc_core.TrdCommandPool.generate(_i_cmd, _i_index)
                self._ts.append(_i_t)
                _i_t.status_changed.connect_to(status_changed_fnc_)
                _i_t.finished.connect_to(finished_fnc_)
                _i_t.start()

        def quit_fnc_():
            button.set_stopped()

            for _i in self._ts:
                _i.do_kill()

            q_t.do_quit()

        contents = []
        if cmds:
            button.set_stopped(False)

            c = len(cmds)

            button.set_status(bsc_core.TrdCommandPool.Status.Started)
            button.initialization(c, bsc_core.TrdCommandPool.Status.Started)

            q_t = gui_qt_core.QtMethodThread(self._window.widget)
            q_t.append_method(
                run_fnc_
            )
            q_t.start()
            self._window.connect_window_close_to(quit_fnc_)
        else:
            button.restore_all()


class _GuiBaseOpt(object):
    DCC_NAMESPACE = 'resolver'

    def __init__(self, window, session):
        self._window = window
        self._session = session


class _GuiRigTagOpt(
    _GuiBaseOpt,
    gui_prx_abstracts.AbsGuiTreeViewAsTagOpt
):
    GROUP_SCHEME = gui_prx_abstracts.AbsGuiTreeViewAsTagOpt.GroupScheme.Hide

    def __init__(self, window, session, prx_tree_view):
        super(_GuiRigTagOpt, self).__init__(window, session)
        self._init_tree_view_as_tag_opt_(prx_tree_view, self.DCC_NAMESPACE)

        self._index_thread_batch = 0

    def gui_add_all_groups(self, rsv_project):
        self.gui_add_root()
        branch = self._window._rsv_filter_opt.get('branch')
        all_steps = rsv_project.get_all_steps(branch=branch)
        for i_step in all_steps:
            i_path = '/{}'.format(i_step)
            self.gui_add_group_by_path(i_path)

    def gui_add_all_groups_use_thread(self, rsv_project):
        def cache_fnc_():
            branch = self._window._rsv_filter_opt.get('branch')
            return [
                self._index_thread_batch,
                rsv_project.get_all_steps(branch=branch)
            ]

        def build_fnc_(*args):
            _index_thread_batch_current, _all_steps = args[0]
            for _i_step in _all_steps:
                _i_path = '/{}'.format(_i_step)
                self.gui_add_group_by_path(_i_path)

        def post_fnc_():
            pass

        self.gui_add_root()

        self._index_thread_batch += 1

        t = gui_qt_core.QtBuildThread(self._window.widget)
        t.set_cache_fnc(cache_fnc_)
        t.cache_value_accepted.connect(build_fnc_)
        t.run_finished.connect(post_fnc_)
        #
        t.start()


class _GuiRigOpt(
    _GuiBaseOpt
):
    ROOT_NAME = 'All'

    NAMESPACE = 'rig'

    TAG_KEYS_INCLUDE = [
        'project',
        'role',
        'asset',
    ]

    def _gui_build_reference_tools(self):
        for i in [
            (
                    'remove-rig',
                    'tool/maya/remove-reference',
                    '"LMB-click" to remove selected rigs',
                    self.do_dcc_remove_rigs
            ),
            (
                    'duplicate-rig',
                    'tool/maya/duplicate-reference',
                    '"LMB-click" to duplicate selected rigs',
                    self.do_dcc_duplicate_rigs
            ),
            (
                    'reload-rig',
                    'tool/maya/reload-reference',
                    '"LMB-click" to reload selected rigs',
                    self.do_dcc_reload_rigs
            ),
            (
                    'unload-rig',
                    'tool/maya/unload-reference',
                    '"LMB-click" to unload selected rigs',
                    self.do_dcc_unload_rigs
            ),
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = prx_widgets.PrxIconPressButton()
            self._prx_reference_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_press_clicked_to(i_fnc)
            self._tool_dict[i_key] = i_tool

    def _gui_build_isolate_select_tools(self):
        for i in [
            (
                    'isolate-select-rig',
                    'tool/isolate-select',
                    '"LMB-click" to turn "on" or "off" isolate select mode',
                    self.do_dcc_isolate_select_rigs
            )
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = prx_widgets.PrxToggleButton()
            self._prx_isolate_select_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_check_toggled_to(i_fnc)
            self._tool_dict[i_key] = i_tool

        for i in [
            (
                    'isolate-select-add-rig',
                    'tool/isolate-select-add',
                    '"LMB-click" to add rigs to isolate select',
                    self.do_dcc_isolate_select_add_rigs
            ),
            (
                    'isolate-select-remove-rig',
                    'tool/isolate-select-remove',
                    '"LMB-click" to remove rigs to isolate select',
                    self.do_dcc_isolate_select_remove_rigs
            )
        ]:
            i_key, i_icon_name, i_tool_tip, i_fnc = i
            i_tool = prx_widgets.PrxIconPressButton()
            self._prx_isolate_select_tool_box.add_widget(i_tool)
            i_tool.set_name(i_key)
            i_tool.set_icon_name(i_icon_name)
            i_tool.set_tool_tip(i_tool_tip)
            i_tool.connect_press_clicked_to(i_fnc)
            self._tool_dict[i_key] = i_tool

    # reference
    def do_dcc_remove_rigs(self):
        w = gui_core.GuiDialog.create(
            label=self._session.gui_name,
            sub_label='remove-rig',
            content='do you want remove selected rigs?\n, press "Yes" to continue',
            status=gui_core.GuiDialog.ValidationStatus.Warning,
            parent=self._window.widget
        )

        result = w.get_result()
        if result is True:
            _ = self._prx_tree_view.get_selected_items()
            for i in _:
                i_rig = i.get_gui_dcc_obj(self.NAMESPACE)
                i_reference_opt = i_rig.reference_opt
                i_reference_opt.do_remove()

            self._window.do_gui_refresh_all()

    def do_dcc_duplicate_rigs(self):
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_rig = i.get_gui_dcc_obj(self.NAMESPACE)
            i_reference_opt = i_rig.reference_opt
            i_reference_opt.do_duplicate()

        self._window.do_gui_refresh_all()

    def do_dcc_reload_rigs(self):
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_rig = i.get_gui_dcc_obj(self.NAMESPACE)
            i_reference_opt = i_rig.reference_opt
            i_reference_opt.do_reload()

        self._window.do_gui_refresh_all()

    def do_dcc_unload_rigs(self):
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_rig = i.get_gui_dcc_obj(self.NAMESPACE)
            i_reference_opt = i_rig.reference_opt
            i_reference_opt.do_unload()

        self._window.do_gui_refresh_all()

    # isolate select
    def do_dcc_isolate_select_rigs(self, boolean):
        panel_current = qsm_mya_core.ViewPanels.get_current_name()
        isolate_select_opt = qsm_mya_core.ViewPanelIsolateSelectOpt(panel_current)
        isolate_select_opt.set_enable(boolean)
        if boolean is True:
            _ = self._prx_tree_view.get_selected_items()
            for i in _:
                i_rig = i.get_gui_dcc_obj(self.NAMESPACE)
                i_reference_opt = i_rig.reference_opt
                i_root = i_reference_opt.get_root()
                isolate_select_opt.add_node(i_root)

    def do_dcc_isolate_select_add_rigs(self):
        panel_current = qsm_mya_core.ViewPanels.get_current_name()
        isolate_select_opt = qsm_mya_core.ViewPanelIsolateSelectOpt(panel_current)
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_rig = i.get_gui_dcc_obj(self.NAMESPACE)
            i_reference_opt = i_rig.reference_opt
            i_root = i_reference_opt.get_root()
            isolate_select_opt.add_node(i_root)

    def do_dcc_isolate_select_remove_rigs(self):
        panel_current = qsm_mya_core.ViewPanels.get_current_name()
        isolate_select_opt = qsm_mya_core.ViewPanelIsolateSelectOpt(panel_current)
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_rig = i.get_gui_dcc_obj(self.NAMESPACE)
            i_reference_opt = i_rig.reference_opt
            i_root = i_reference_opt.get_root()
            isolate_select_opt.remove_node(i_root)

    #
    def do_gui_refresh_tools(self):
        panel_current = qsm_mya_core.ViewPanels.get_current_name()
        isolate_select_opt = qsm_mya_core.ViewPanelIsolateSelectOpt(panel_current)
        self._tool_dict['isolate-select-rig'].set_checked(isolate_select_opt.is_enable())

    #
    def do_dcc_remove_skin_proxy(self):
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_rig = i.get_gui_dcc_obj(self.NAMESPACE)
            qsm_mya_rig_scripts.AdvSkinProxyGenerate(
                i_rig.namespace
            ).do_remove()

    def do_dcc_remove_dynamic_gpu(self):
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_rig = i.get_gui_dcc_obj(self.NAMESPACE)
            qsm_mya_rig_scripts.DynamicGpuCacheGenerate(
                i_rig.namespace
            ).do_remove()

    # selection
    def do_dcc_select_rigs(self):
        if self._prx_tree_view.has_focus() is True:
            rigs = self.get_selected_rigs()
            paths = []
            if rigs:
                scheme = self._window._rig_utility_options_node.get('selection_scheme')
                paths = [i.get_location_for_selection(scheme) for i in rigs]

            if paths:
                cmds.select([i for i in paths if i])
            else:
                cmds.select(clear=1)

    def do_gui_select_rigs(self):
        if self._prx_tree_view.has_focus() is False:
            namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
            if namespaces:
                paths = ['/{}'.format(i) for i in namespaces]
            else:
                paths = []

            self.do_gui_selected(paths)

    def __init__(self, window, session, prx_tree_view):
        super(_GuiRigOpt, self).__init__(window, session)
        self._prx_tree_view = prx_tree_view
        self._prx_tree_view.set_header_view_create(
            [('name', 2), ('description', 2)],
            self._window.get_definition_window_size()[0] * (2.0 / 3.0) - 48
        )
        self._prx_tree_view.connect_item_select_changed_to(
            self.do_dcc_select_rigs
        )
        self._prx_tree_view.get_top_tool_bar().set_expanded(True)
        self._prx_reference_tool_box = self._prx_tree_view.create_top_tool_box(
            'reference', insert_args=1
        )
        self._prx_isolate_select_tool_box = self._prx_tree_view.create_top_tool_box(
            'isolate-select', insert_args=1
        )
        self._tool_dict = {}
        self._gui_build_reference_tools()
        self._gui_build_isolate_select_tools()

        self._item_dict = self._prx_tree_view._item_dict

        self._adv_rig_query = qsm_mya_rig_core.AdvRigQuery()

    def restore(self):
        self._prx_tree_view.set_clear()
        self._adv_rig_query = qsm_mya_rig_core.AdvRigQuery()

    def gui_is_exists(self, path):
        return self._item_dict.get(path) is not None

    def gui_get(self, path):
        return self._item_dict[path]

    def gui_register(self, path, prx_item):
        self._item_dict[path] = prx_item

    def gui_add_root(self):
        path = '/'
        if self.gui_is_exists(path) is False:
            prx_item = self._prx_tree_view.create_item(
                self.ROOT_NAME,
                icon=gui_core.GuiIcon.get('database/all'),
            )

            self.gui_register(path, prx_item)

            prx_item.set_expanded(True)
            # prx_item.set_checked(True)
            return True, prx_item
        return False, self.gui_get(path)

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
        if self.gui_is_exists(path) is False:
            create_kwargs = dict(
                name='loading ...',
                filter_key=path,
            )
            parent = path_opt.get_parent()
            if parent is not None:
                prx_item_parent = self.gui_get(parent.path)
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_tree_view.create_item(
                    **create_kwargs
                )
            #
            # prx_item.set_checked(True)
            self.gui_register(path, prx_item)
            prx_item.set_show_build_fnc(build_fnc_)
            return True, prx_item
        return False, self.gui_get(path)

    def gui_add_rig(self, rig):
        def build_fnc_():
            prx_item.set_name(
                path_opt.get_name()
            )
            _reference_node = rig.reference_opt
            _semantic_tag_filter_data = {}
            _tag_group_key = '/status'
            if _reference_node.is_loaded():
                prx_item.set_icon_by_file(
                    gui_core.GuiIcon.get('node/maya/reference')
                )
                _semantic_tag_filter_data.setdefault(
                    _tag_group_key, set()
                ).add('/status/loaded')
                self._window._gui_rig_tag_opt.gui_register_tag_by_path(
                    '/status/loaded', path, auto_create_ancestors=True
                )
            else:
                prx_item.set_icon_by_file(
                    gui_core.GuiIcon.get('node/maya/reference-unloaded')
                )
                _semantic_tag_filter_data.setdefault(
                    _tag_group_key, set()
                ).add('/status/unloaded')
                self._window._gui_rig_tag_opt.gui_register_tag_by_path(
                    '/status/unloaded', path, auto_create_ancestors=True
                )

            prx_item.get_item()._update_item_semantic_tag_filter_keys_tgt_(_semantic_tag_filter_data)
            prx_item.set_tool_tip(
                '\n'.join(['{}: {}'.format(_k, _v) for _k, _v in rig.variants.items()])
            )

        path = rig.path
        if self.gui_is_exists(path) is False:
            path_opt = rig.path_opt
            create_kwargs = dict(
                name='loading ...',
                filter_key=path,
            )
            parent = path_opt.get_parent()
            if parent is not None:
                prx_item_parent = self.gui_get(parent.path)
                prx_item = prx_item_parent.add_child(
                    **create_kwargs
                )
            else:
                prx_item = self._prx_tree_view.create_item(
                    **create_kwargs
                )

            # prx_item.set_checked(True)
            self.gui_register(path, prx_item)
            variants = rig.variants
            semantic_tag_filter_data = {}
            for i in self.TAG_KEYS_INCLUDE:
                if i in variants:
                    i_v = variants[i]
                    i_tag_group = '/{}'.format(i)
                    i_tag_path = '/{}/{}'.format(i, i_v)
                    semantic_tag_filter_data.setdefault(
                        i_tag_group, set()
                    ).add(i_tag_path)
                    self._window._gui_rig_tag_opt.gui_register_tag_by_path(
                        i_tag_path, path, auto_create_ancestors=True
                    )

            prx_item.get_item()._update_item_semantic_tag_filter_keys_tgt_(semantic_tag_filter_data)
            prx_item.set_gui_dcc_obj(
                rig, namespace=self.NAMESPACE
            )
            prx_item.set_show_build_fnc(build_fnc_)
            return True, prx_item
        return False, self.gui_get(path)

    def gui_add_one(self, rig):
        ancestors = rig.path_opt.get_ancestors()
        if ancestors:
            ancestors.reverse()
            for i_path_opt in ancestors:
                if self.gui_is_exists(i_path_opt.path) is False:
                    i_is_create, i_prx_item = self.gui_add_group(i_path_opt)
                    if i_is_create is True:
                        i_prx_item.set_expanded(True)
        #
        self.gui_add_rig(rig)

    def gui_add_all(self):
        self.gui_add_root()
        rigs = self._adv_rig_query.get_all()
        for i_rig in rigs:
            self.gui_add_one(i_rig)

    def get_current_obj(self):
        _ = self._prx_tree_view.get_selected_items()
        if _:
            return _[-1].get_gui_dcc_obj(self.NAMESPACE)

    def get_selected_rigs(self):
        list_ = []
        _ = self._prx_tree_view.get_selected_items()
        for i in _:
            i_rig = i.get_gui_dcc_obj(self.NAMESPACE)
            if i_rig is not None:
                list_.append(i_rig)
        return list_

    def gui_get_items_selected(self, paths):
        return [self.gui_get(i) for i in paths if self.gui_is_exists(i)]

    def do_gui_selected(self, paths):
        if paths:
            prx_items = self.gui_get_items_selected(paths)
            self._prx_tree_view.select_items(prx_items)
        else:
            self._prx_tree_view.clear_selection()
    
    def get_adv_rig_query(self):
        return self._adv_rig_query


class _GuiRigReferenceOpt(
    _GuiBaseOpt
):
    def __init__(self, window, session, prx_input_for_asset):
        super(_GuiRigReferenceOpt, self).__init__(window, session)
        self._scan_root = qsm_gnl_scan.Root.generate()
        self._prx_input_for_asset = prx_input_for_asset

        self._count_input = qt_widgets.QtInputAsConstant()
        self._prx_input_for_asset.add_widget(self._count_input)
        self._count_input._set_value_type_(int)
        self._count_input.setMaximumWidth(64)
        self._count_input.setMinimumWidth(64)
        self._count_input._set_value_(1)

        self._reference_button = qt_widgets.QtPressButton()
        self._prx_input_for_asset.add_widget(self._reference_button)
        self._reference_button._set_name_text_(
            gui_core.GuiUtil.choice_label(
                self._window._language, self._session.configure.get('build.buttons.reference')
            )
        )
        self._reference_button.setMaximumWidth(64)
        self._reference_button.setMinimumWidth(64)
        self._reference_button.press_clicked.connect(self.do_dcc_reference_rig)
        self._reference_button._set_action_enable_(False)

        self._prx_input_for_asset.connect_input_change_accepted_to(self.do_gui_refresh_rig)

        self._rig_file_path = None

        self.do_gui_refresh_rig(self._prx_input_for_asset.get_path())

    def do_dcc_reference_rig(self):
        if self._rig_file_path is not None:
            file_opt = bsc_storage.StgFileOpt(self._rig_file_path)
            count = self._count_input._get_value_()
            for i in range(count):
                qsm_mya_core.Scene.reference_file(
                    self._rig_file_path,
                    namespace=file_opt.name_base
                )
            self._window.do_gui_refresh_all()

    def do_gui_refresh_rig(self, path):
        self._rig_file_path = None
        self._reference_button._set_action_enable_(False)
        entity = self._prx_input_for_asset.get_entity(path)
        if entity is not None:
            if entity.type == 'Asset':
                task = entity.task(self._scan_root.EntityTasks.Rig)
                if task is not None:
                    result = task.find_result(
                        self._scan_root.ResultPatterns.RigFile
                    )
                    if result is not None:
                        self._rig_file_path = result
                        self._reference_button._set_action_enable_(True)


class _GuiRigMotionOpt(
    _GuiBaseOpt
):
    def __init__(self, window, session, prx_options_node):
        super(_GuiRigMotionOpt, self).__init__(window, session)

        self._prx_options_node = prx_options_node
        self._prx_options_node.get_port(
            'animation_transfer.transfer'
        ).set(
            self.do_dcc_transfer_animation
        )

    def do_dcc_transfer_animation(self):
        namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
        namespace_src, namespace_dst = None, None
        if namespaces:
            self._dynamic_gpu_load_args_array = []

            adv_rig_query = self._window._gui_rig_opt.get_adv_rig_query()
            valid_namespaces = adv_rig_query.to_valid_namespaces(namespaces)
            if len(valid_namespaces) >= 2:
                namespace_src = valid_namespaces[-2]
                namespace_dst = valid_namespaces[-1]

        if namespace_src is not None and namespace_dst is not None:
            w = gui_core.GuiDialog.create(
                label=self._session.gui_name,
                sub_label='transfer-animation',
                content='do you want transfer animation from "{}" to "{}"?,\n press "Yes" to continue'.format(
                    namespace_src, namespace_dst
                ),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                parent=self._window.widget
            )

            result = w.get_result()
            if result is True:
                force = self._prx_options_node.get('animation_transfer.force')
                frame_offset = self._prx_options_node.get('animation_transfer.frame_offset')
                qsm_mya_motion.AdvMotionOpt(namespace_src).transfer_animations_to(
                    namespace_dst, frame_offset=frame_offset, force=force
                )


class PnlAssetManager(prx_widgets.PrxSessionWindow):
    RIG_SELECTION_SCRIPT_JOB_NAME = 'asset_manager_rig_selection'

    def do_gui_refresh_by_rig_tag_checking(self):
        filter_data_src = self._gui_rig_tag_opt.generate_semantic_tag_filter_data_src()
        qt_view = self._rig_prx_tree_view._qt_view
        qt_view._set_view_semantic_tag_filter_data_src_(filter_data_src)
        qt_view._set_view_keyword_filter_data_src_(
            self._rig_prx_tree_view.filter_bar.get_keywords()
        )
        qt_view._refresh_view_items_visible_by_any_filter_()
        qt_view._refresh_viewport_showable_auto_()

    def do_gui_refresh_by_camera_changing(self):
        cameras = qsm_mya_core.Cameras.get_all()
        active_camera = qsm_mya_core.Cameras.get_active_camera()
        self._rig_camera_port.set(
            cameras
        )
        self._rig_camera_port.set(
            active_camera
        )

    def do_dcc_refresh_by_fps_changing(self):
        pass

    def do_gui_refresh_by_fps_changing(self):
        fps = qsm_mya_core.Scene.get_fps()
        self._rig_fps_port.set(fps)

    def do_gui_refresh_by_frame_scheme_changing(self):
        frame_scheme = self.get_rig_frame_scheme()
        if frame_scheme == 'frame_range':
            self._rig_frame_range_port.set_locked(False)
        else:
            self._rig_frame_range_port.set_locked(True)
            self.do_gui_refresh_by_dcc_frame_changing()

    def do_gui_refresh_by_dcc_frame_changing(self):
        frame_scheme = self.get_rig_frame_scheme()
        if frame_scheme == 'render_settings':
            frame_range = qsm_mya_core.Scene.get_render_frame_range()
            self._rig_frame_range_port.set(frame_range)
        elif frame_scheme == 'time_slider':
            frame_range = qsm_mya_core.Scene.get_frame_range()
            self._rig_frame_range_port.set(frame_range)

    def do_gui_refresh_by_window_active_changing(self):
        self._gui_rig_opt.do_gui_refresh_tools()

    def get_rig_frame_scheme(self):
        return self._rig_utility_options_node.get('scene.frame_scheme')

    def __init__(self, session, *args, **kwargs):
        super(PnlAssetManager, self).__init__(session, *args, **kwargs)

    def _register_rig_selection_script_job(self):
        self._rig_selection_script_job = qsm_mya_core.ScriptJob(
            self.RIG_SELECTION_SCRIPT_JOB_NAME
        )
        self._rig_selection_script_job.register(
            self._gui_rig_opt.do_gui_select_rigs,
            self._rig_selection_script_job.EventTypes.SelectionChanged
        )
        self._rig_selection_script_job.register(
            self.do_gui_refresh_by_dcc_frame_changing,
            self._rig_selection_script_job.EventTypes.FrameRangeChanged
        )
        self._rig_selection_script_job.register(
            self.do_gui_refresh_all,
            self._rig_selection_script_job.EventTypes.SceneOpened
        )

    def _destroy_rig_selection_script_job(self):
        self._rig_selection_script_job.destroy()

    def set_all_setup(self):
        self._skin_proxy_load_args_array = []
        self._dynamic_gpu_load_args_array = []

        self.set_main_style_mode(1)
        self._tab_view = prx_widgets.PrxTabView()
        self.add_widget(self._tab_view)

        s_a_0 = prx_widgets.PrxVScrollArea()
        self._tab_view.add_widget(
            s_a_0,
            name=gui_core.GuiUtil.choice_label(
                self._language, self._session.configure.get('build.tabs.rig')
            ),
            icon_name_text='rig',
        )

        # rig reference
        self._prx_rig_input_for_asset = qsm_prx_widgets.PrxInputForAsset()
        s_a_0.add_widget(self._prx_rig_input_for_asset)

        h_s_0 = prx_widgets.PrxHSplitter()
        s_a_0.add_widget(h_s_0)

        self._rig_tag_tree_view = prx_widgets.PrxTreeView()
        h_s_0.add_widget(self._rig_tag_tree_view)
        self._rig_tag_tree_view.set_header_view_create(
            [('name', 2)],
            self.get_definition_window_size()[0]
        )
        self.connect_refresh_action_for(
            self.do_gui_refresh_all
        )

        self._rig_prx_tree_view = prx_widgets.PrxTreeView()
        h_s_0.add_widget(self._rig_prx_tree_view)
        h_s_0.set_fixed_size_at(0, 240)
        # h_s_0.set_contract_left_or_top_at(0)

        self._gui_rig_tag_opt = _GuiRigTagOpt(self, self._session, self._rig_tag_tree_view)
        self._gui_rig_opt = _GuiRigOpt(self, self._session, self._rig_prx_tree_view)

        self._rig_tag_tree_view.connect_item_check_changed_to(
            self.do_gui_refresh_by_rig_tag_checking
        )

        self._prx_rig_tab_group = prx_widgets.PrxHTabGroup()
        s_a_0.add_widget(self._prx_rig_tab_group)

        self._gui_rig_reference_opt = _GuiRigReferenceOpt(
            self, self._session, self._prx_rig_input_for_asset
        )
        # rig utility
        self._rig_utility_options_node = prx_widgets.PrxNode(
            gui_core.GuiUtil.choice_label(
                self._language, self._session.configure.get('build.options.rig_utility')
            )
        )
        self._prx_rig_tab_group.add_widget(
            self._rig_utility_options_node,
            name=gui_core.GuiUtil.choice_label(
                self._language, self._session.configure.get('build.tag-groups.utility')
            )
        )
        self._rig_utility_options_node.create_ports_by_data(
            self._session.configure.get('build.options.rig_utility.parameters'),
        )

        self._load_skin_proxy_button = self._rig_utility_options_node.get_port('skin_proxy.load_skin_proxy')
        self._load_skin_proxy_button.set(self.do_dcc_load_skin_proxies_by_selection)
        self._load_skin_proxy_button.connect_finished_to(self.load_skin_proxies)

        self._rig_utility_options_node.set('skin_proxy.remove_skin_proxy', self._gui_rig_opt.do_dcc_remove_skin_proxy)

        self._load_dynamic_gpu_button = self._rig_utility_options_node.get_port('dynamic_gpu.load_dynamic_gpu')
        self._load_dynamic_gpu_button.set(self.do_dcc_load_dynamic_gpus_bt_selection)
        self._load_dynamic_gpu_button.connect_finished_to(self.load_dynamic_gpus)

        self._rig_utility_options_node.set('dynamic_gpu.remove_dynamic_gpu', self._gui_rig_opt.do_dcc_remove_dynamic_gpu)

        self._rig_utility_options_node.get_port('selection_scheme').connect_input_changed_to(
            self._gui_rig_opt.do_dcc_select_rigs
        )
        self._rig_utility_options_node.get_port('scene.frame_scheme').connect_input_changed_to(
            self.do_gui_refresh_by_frame_scheme_changing
        )
        self._rig_camera_port = self._rig_utility_options_node.get_port('scene.camera')
        self._rig_fps_port = self._rig_utility_options_node.get_port('scene.fps')
        self._rig_frame_range_port = self._rig_utility_options_node.get_port('scene.frame_range')
        # rig motion
        self._rig_motion_options_node = prx_widgets.PrxNode(
            gui_core.GuiUtil.choice_label(
                self._language, self._session.configure.get('build.options.rig_extend')
            )
        )
        self._prx_rig_tab_group.add_widget(
            self._rig_motion_options_node,
            name=gui_core.GuiUtil.choice_label(
                self._language, self._session.configure.get('build.tag-groups.extend')
            )
        )
        self._rig_motion_options_node.create_ports_by_data(
            self._session.configure.get('build.options.rig_extend.parameters'),
        )

        self._rig_motion_opt = _GuiRigMotionOpt(self, self._session, self._rig_motion_options_node)

        self.do_gui_refresh_all()

        self.do_gui_refresh_by_camera_changing()
        self.do_gui_refresh_by_fps_changing()
        self.do_gui_refresh_by_dcc_frame_changing()
        self._gui_rig_opt.do_gui_select_rigs()

        self._register_rig_selection_script_job()

        self.connect_window_activate_changed_to(self.do_gui_refresh_by_window_active_changing)
        self.connect_window_close_to(self._destroy_rig_selection_script_job)

    def do_gui_refresh_all(self):
        self._gui_rig_tag_opt.restore()
        self._gui_rig_tag_opt.gui_add_root()

        self._gui_rig_opt.restore()
        self._gui_rig_opt.gui_add_all()

    def load_skin_proxies(self):
        if self._skin_proxy_load_args_array:
            with self.gui_progressing(maximum=len(self._skin_proxy_load_args_array), label='load skin proxies') as g_p:
                for i_namespace, i_cache_file in self._skin_proxy_load_args_array:
                    g_p.do_update()
                    qsm_mya_rig_scripts.AdvSkinProxyGenerate(i_namespace).load_cache(
                        i_cache_file
                    )

    def do_dcc_load_skin_proxies_by_selection(self):
        if self._load_skin_proxy_button.get_is_started() is False:
            namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
            if namespaces:
                self._skin_proxy_load_args_array = []
                create_cmds = []

                adv_rig_query = self._gui_rig_opt.get_adv_rig_query()
                valid_namespaces = adv_rig_query.to_valid_namespaces(namespaces)
                if valid_namespaces:
                    with self.gui_progressing(maximum=len(valid_namespaces), label='processing skin proxies') as g_p:
                        for i_namespace in valid_namespaces:
                            g_p.do_update()
                            i_generate = qsm_mya_rig_scripts.AdvSkinProxyGenerate(i_namespace)
                            if i_generate.is_exists() is False:
                                i_cmd, i_cache_file = qsm_mya_rig_scripts.AdvSkinProxyGenerate(
                                    i_namespace).generate_args()
                                if i_cmd is not None:
                                    create_cmds.append(i_cmd)

                                self._skin_proxy_load_args_array.append((i_namespace, i_cache_file))

                if create_cmds:
                    mtd = _GuiProcessOpt(self)
                    mtd.execute(self._load_skin_proxy_button, create_cmds)
                else:
                    self.load_skin_proxies()

    def load_dynamic_gpus(self):
        if self._dynamic_gpu_load_args_array:
            with self.gui_progressing(maximum=len(self._skin_proxy_load_args_array), label='load dynamic gpus') as g_p:
                for i_namespace, i_cache_file, i_start_frame, i_end_frame in self._dynamic_gpu_load_args_array:
                    g_p.do_update()
                    qsm_mya_rig_scripts.DynamicGpuCacheGenerate(i_namespace).load_cache(
                        i_cache_file
                    )

    def do_dcc_load_dynamic_gpus_bt_selection(self):
        if self._load_dynamic_gpu_button.get_is_started() is False:
            namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
            if namespaces:
                self._dynamic_gpu_load_args_array = []
                create_cmds = []

                adv_rig_query = self._gui_rig_opt.get_adv_rig_query()
                valid_namespaces = adv_rig_query.to_valid_namespaces(namespaces)
                if valid_namespaces:
                    start_frame, end_frame = self._rig_utility_options_node.get('scene.frame_range')
                    with self.gui_progressing(maximum=len(valid_namespaces), label='processing dynamic gpus') as g_p:
                        for i_namespace in valid_namespaces:
                            g_p.do_update()

                            i_generate = qsm_mya_rig_scripts.DynamicGpuCacheGenerate(i_namespace)
                            if i_generate.is_exists() is False:
                                i_directory_path = qsm_mya_ast_core.AssetCache.get_dynamic_gpu_directory(
                                    user_name=bsc_core.SysBaseMtd.get_user_name()
                                )
                                i_cmd, i_file_path, i_cache_file, i_start_frame, i_end_frame = \
                                    i_generate.generate_args(i_directory_path, start_frame, end_frame)
                                i_generate.export_source(i_file_path)

                                create_cmds.append(i_cmd)

                                self._dynamic_gpu_load_args_array.append(
                                    (i_namespace, i_cache_file, i_start_frame, i_end_frame))

                if create_cmds:
                    mtd = _GuiProcessOpt(self)
                    mtd.execute(self._load_dynamic_gpu_button, create_cmds)
                else:
                    self.load_dynamic_gpus()

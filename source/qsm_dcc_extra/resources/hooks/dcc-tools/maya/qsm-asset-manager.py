# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets

import lxgui.proxy.scripts as gui_prx_scripts

import lxgui.proxy.abstracts as gui_prx_abstracts

import qsm_maya.general.core as qsm_mya_gnl_core

import qsm_maya.asset.core as qsm_mya_ast_core

import qsm_maya.rig.core as qsm_mya_rig_core

import qsm_maya.rig.scripts as qsm_mya_rig_scripts

import qsm_maya.assembly.scripts as qsm_mya_asb_scripts

import qsm_gui.proxy.widgets as qsm_prx_widgets


class CreateMtd(object):
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
            #
            for _i_index, _i_cmd in enumerate(cmds):
                bsc_core.TrdCommandPool.set_wait()
                #
                _i_t = bsc_core.TrdCommandPool.set_start(_i_cmd, _i_index)
                self._ts.append(_i_t)
                _i_t.status_changed.connect_to(status_changed_fnc_)
                _i_t.finished.connect_to(finished_fnc_)

        def quit_fnc_():
            button.set_stopped()

            for _i in self._ts:
                _i.do_kill()
            #
            q_t.do_quit()

        contents = []
        if cmds:
            button.set_stopped(False)

            c = len(cmds)

            button.set_status(bsc_core.TrdCommandPool.Status.Started)
            button.set_initialization(c, bsc_core.TrdCommandPool.Status.Started)

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

    def __init__(self, window, session, prx_tree_view):
        super(_GuiRigOpt, self).__init__(window, session)
        self._prx_tree_view = prx_tree_view

        self._item_dict = self._prx_tree_view._item_dict

        self._rigs_query = qsm_mya_rig_core.RigsQuery()

    def restore(self):
        self._prx_tree_view.set_clear()

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
            prx_item.set_checked(True)
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
            prx_item.set_checked(True)
            self.gui_register(path, prx_item)
            prx_item.set_show_build_fnc(build_fnc_)
            return True, prx_item
        return False, self.gui_get(path)

    def gui_add_rig(self, rig):
        def build_fnc_():
            prx_item.set_name(
                path_opt.get_name()
            )
            prx_item.set_icon_by_file(
                gui_core.GuiIcon.get('database/object')
            )
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

            prx_item.set_checked(True)
            self.gui_register(path, prx_item)
            variants = rig.variants
            semantic_tag_filter_data = {}
            for k, v in variants.items():
                i_tag_group = '/{}'.format(k)
                i_tag_path = '/{}/{}'.format(k, v)
                semantic_tag_filter_data.setdefault(
                    i_tag_group, set()
                ).add(i_tag_path)
                self._window._gui_rig_tag_opt.gui_register_tag_by_path(i_tag_path, path, auto_create_ancestors=True)

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

        for i_rig in self._rigs_query.get_all():
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
    
    def gui_do_selected(self, paths):
        if paths:
            prx_items = self.gui_get_items_selected(paths)
            self._prx_tree_view.select_items(prx_items)
        else:
            self._prx_tree_view.clear_selection()
    

class PnlAssetManager(prx_widgets.PrxSessionWindow):

    RIG_SELECTION_SCRIPT_JOB_NAME = 'asset_manager_rig_selection'

    def dcc_do_selection_by_rig_selection(self):
        if self._rig_prx_tree_view.has_focus():
            rigs = self._gui_rig_opt.get_selected_rigs()
            paths = []
            if rigs:
                scheme = self._rig_options_node.get('selection_scheme')
                paths = [i.get_location_for_selection(scheme) for i in rigs]

            if paths:
                cmds.select([i for i in paths if i])
            else:
                cmds.select(clear=1)

    def gui_do_refresh_by_rig_tag_checking(self):
        filter_data_src = self._gui_rig_tag_opt.generate_semantic_tag_filter_data_src()
        qt_view = self._rig_prx_tree_view._qt_view
        qt_view._set_view_semantic_tag_filter_data_src_(filter_data_src)
        qt_view._set_view_keyword_filter_data_src_(
            self._rig_prx_tree_view.filter_bar.get_keywords()
        )
        qt_view._refresh_view_items_visible_by_any_filter_()
        qt_view._refresh_viewport_showable_auto_()

    def gui_do_refresh_by_dcc_selection(self):
        namespaces = qsm_mya_gnl_core.Namespaces.get_roots_by_selection()
        if namespaces:
            paths = ['/{}'.format(i) for i in namespaces]
        else:
            paths = []

        self._gui_rig_opt.gui_do_selected(paths)

    def gui_do_refresh_by_frame_scheme_changing(self):
        frame_scheme = self.get_frame_scheme()
        if frame_scheme == 'frame_range':
            self._rig_frame_range_port.set_locked(False)
        else:
            self._rig_frame_range_port.set_locked(True)

    def gui_do_refresh_by_dcc_frame_changing(self):
        frame_scheme = self.get_frame_scheme()
        if frame_scheme != 'frame_range':
            frame_range = qsm_mya_gnl_core.Scene.get_frame_range()
            self._rig_frame_range_port.set(frame_range)

    def get_frame_scheme(self):
        return self._rig_options_node.get('dynamic_gpu.frame_scheme')

    def __init__(self, session, *args, **kwargs):
        super(PnlAssetManager, self).__init__(session, *args, **kwargs)

    def _register_rig_selection_script_job(self):
        self._rig_selection_script_job = qsm_mya_gnl_core.ScriptJob(
            self.RIG_SELECTION_SCRIPT_JOB_NAME
        )
        self._rig_selection_script_job.register(
            self.gui_do_refresh_by_dcc_selection,
            self._rig_selection_script_job.EventTypes.SelectionChanged
        )
        self._rig_selection_script_job.register(
            self.gui_do_refresh_by_dcc_frame_changing,
            self._rig_selection_script_job.EventTypes.FrameRangeChanged
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
            name='rig',
            icon_name_text='rig',
        )

        self._prx_asset_input = qsm_prx_widgets.PrxInputForAsset()
        s_a_0.add_widget(self._prx_asset_input)

        h_s_0 = prx_widgets.PrxHSplitter()
        s_a_0.add_widget(h_s_0)

        self._rig_tag_tree_view = prx_widgets.PrxTreeView()
        h_s_0.add_widget(self._rig_tag_tree_view)
        self._rig_tag_tree_view.set_header_view_create(
            [('name', 2)],
            self.get_definition_window_size()[0]
        )

        self._rig_prx_tree_view = prx_widgets.PrxTreeView()
        h_s_0.add_widget(self._rig_prx_tree_view)
        self._rig_prx_tree_view.set_header_view_create(
            [('name', 2), ('status', 2)],
            self.get_definition_window_size()[0]*(2.0/3.0)-48
        )
        h_s_0.set_fixed_size_at(0, 240)
        # h_s_0.set_contract_left_or_top_at(0)
        self._rig_prx_tree_view.connect_item_select_changed_to(
            self.dcc_do_selection_by_rig_selection
        )

        self._gui_rig_tag_opt = _GuiRigTagOpt(self, self._session, self._rig_tag_tree_view)
        self._gui_rig_opt = _GuiRigOpt(self, self._session, self._rig_prx_tree_view)

        self._rig_tag_tree_view.connect_item_check_changed_to(
            self.gui_do_refresh_by_rig_tag_checking
        )
        #
        self._rig_options_node = prx_widgets.PrxNode('options')
        s_a_0.add_widget(self._rig_options_node)
        self._rig_options_node.create_ports_by_data(
            self._session.configure.get('build.node.rig_options'),
        )

        self._load_skin_proxy_button = self._rig_options_node.get_port('skin_proxy.load_skin_proxy')
        self._load_skin_proxy_button.set(self.load_skin_proxies_by_selection)
        self._load_skin_proxy_button.set_finished_connect_to(self.load_skin_proxies)

        self._load_dynamic_gpu_button = self._rig_options_node.get_port('dynamic_gpu.load_dynamic_gpu')
        self._load_dynamic_gpu_button.set(self.load_dynamic_gpus_bt_selection)
        self._load_dynamic_gpu_button.set_finished_connect_to(self.load_dynamic_gpus)

        self._rig_options_node.get_port('selection_scheme').connect_input_changed_to(
            self.dcc_do_selection_by_rig_selection
        )
        self._rig_options_node.get_port('dynamic_gpu.frame_scheme').connect_input_changed_to(
            self.gui_do_refresh_by_frame_scheme_changing
        )
        self._rig_frame_range_port = self._rig_options_node.get_port('dynamic_gpu.frame_range')

        self.gui_refresh_all()

        self._register_rig_selection_script_job()
        self.gui_do_refresh_by_dcc_frame_changing()
        self.gui_do_refresh_by_dcc_selection()

        self.connect_window_close_to(self._destroy_rig_selection_script_job)

    def gui_refresh_all(self):
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

    def load_skin_proxies_by_selection(self):
        namespaces = qsm_mya_gnl_core.Namespaces.get_roots_by_selection()
        if namespaces:
            self._skin_proxy_load_args_array = []
            create_cmds = []
            namespace_query = qsm_mya_ast_core.NamespaceQuery()
            valid_namespaces = namespace_query.to_valid_namespaces(namespaces)
            if valid_namespaces:
                for i_namespace in valid_namespaces:
                    i_cmd, i_cache_file = qsm_mya_rig_scripts.AdvSkinProxyGenerate(i_namespace).generate_args()
                    if i_cmd is not None:
                        create_cmds.append(i_cmd)

                    self._skin_proxy_load_args_array.append((i_namespace, i_cache_file))

            if create_cmds:
                mtd = CreateMtd(self)
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

    def load_dynamic_gpus_bt_selection(self):
        namespaces = qsm_mya_gnl_core.Namespaces.get_roots_by_selection()
        if namespaces:
            self._dynamic_gpu_load_args_array = []
            create_cmds = []
            namespace_query = qsm_mya_ast_core.NamespaceQuery()
            valid_namespaces = namespace_query.to_valid_namespaces(namespaces)
            if valid_namespaces:
                with self.gui_progressing(maximum=len(valid_namespaces), label='processing dynamic gpus') as g_p:
                    for i_namespace in valid_namespaces:
                        i_directory_path = qsm_mya_ast_core.AssetCache.get_dynamic_gpu_directory(
                            user_name=bsc_core.SysBaseMtd.get_user_name()
                        )
                        i_cmd, i_file_path, i_cache_file, i_start_frame, i_end_frame = \
                            qsm_mya_rig_scripts.DynamicGpuCacheGenerate(i_namespace).generate_args(i_directory_path)

                        qsm_mya_rig_scripts.DynamicGpuCacheGenerate(i_namespace).export_source(i_file_path)

                        create_cmds.append(i_cmd)

                        self._dynamic_gpu_load_args_array.append((i_namespace, i_cache_file, i_start_frame, i_end_frame))

            if create_cmds:
                mtd = CreateMtd(self)
                mtd.execute(self._load_dynamic_gpu_button, create_cmds)
            else:
                self.load_dynamic_gpus()


def main(session):
    w = PnlAssetManager(session)

    w.set_window_show()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

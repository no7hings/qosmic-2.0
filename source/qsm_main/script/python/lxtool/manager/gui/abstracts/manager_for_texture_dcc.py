# coding:utf-8
import time

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.dcc.objects as bsc_dcc_objects

import lxgui.proxy.widgets as prx_widgets

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.proxy.scripts as gui_prx_scripts


# noinspection PyUnusedLocal
class AbsPnlManagerForAssetTextureDcc(prx_widgets.PrxSessionWindow):
    DCC_NAMESPACE = None
    DCC_SELECTION_CLS = None

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlManagerForAssetTextureDcc, self).__init__(session, *args, **kwargs)

    def restore_variants(self):
        self._create_data = []

    def post_setup_fnc(self):
        pass

    def set_all_setup(self):
        self.set_main_style_mode(1)
        self._tab_view = prx_widgets.PrxTabView()
        self.add_widget(self._tab_view)

        s_a_0 = prx_widgets.PrxVScrollArea()
        self._tab_view.add_widget(
            s_a_0,
            name='dcc',
            icon_name_text='dcc',
        )

        e_p_0 = prx_widgets.PrxHToolGroup()
        s_a_0.add_widget(e_p_0)
        h_s_0 = prx_widgets.PrxHSplitter()
        e_p_0.add_widget(h_s_0)
        e_p_0.set_name('textures')
        e_p_0.set_expanded(True)
        #
        self._prx_tree_view_for_filter = prx_widgets.PrxTreeView()
        self._prx_tree_view_for_filter.set_selection_use_single()
        self._prx_tree_view_for_filter.set_header_view_create(
            [('name', 3)],
            self.get_definition_window_size()[0]*(2.0/6.0)-32
        )
        h_s_0.add_widget(self._prx_tree_view_for_filter)
        #
        self._tree_view = prx_widgets.PrxTreeView()
        h_s_0.add_widget(self._tree_view)
        self._tree_view.set_header_view_create(
            [('name', 4), ('color-space', 2), ('description', 2)],
            self.get_definition_window_size()[0]*(3.0/4.0)-32
        )
        h_s_0.set_fixed_size_at(0, 240)
        h_s_0.set_contract_left_or_top_at(0)
        #
        self._texture_add_opt = gui_prx_scripts.GuiPrxScpForStorageTreeAdd(
            prx_tree_view=self._tree_view,
            prx_tree_item_cls=prx_widgets.PrxStgObjTreeItem,
        )
        self._dcc_add_opt = gui_prx_scripts.GuiPrxScpForTreeAdd(
            prx_tree_view=self._tree_view,
            prx_tree_item_cls=prx_widgets.PrxDccObjTreeItem,
            dcc_namespace=self.DCC_NAMESPACE
        )
        #
        self._tree_view_selection_opt = gui_prx_scripts.GuiPrxScpForTreeSelection(
            prx_tree_view=self._tree_view,
            dcc_selection_cls=self.DCC_SELECTION_CLS,
            dcc_namespace=self.DCC_NAMESPACE
        )
        self._tree_view.connect_item_select_changed_to(
            self._tree_view_selection_opt.set_select
        )

        self._gui_tag_filter_opt = gui_prx_scripts.GuiPrxScpForTreeTagFilter(
            prx_tree_view_src=self._prx_tree_view_for_filter,
            prx_tree_view_tgt=self._tree_view,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )
        self.connect_refresh_action_for(self.refresh_gui_fnc)
        #
        self._options_prx_node = prx_widgets.PrxNode('options')
        s_a_0.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )

        self._options_prx_node.set(
            'target.create_target', self._set_target_create_execute_
        )

        self._options_prx_node.set(
            'target.repath_to_source', self._set_repath_to_src_
        )
        self._options_prx_node.set(
            'target.repath_to_target', self._set_repath_to_tgt_
        )

        self._options_prx_node.set(
            'extra.search', self.execute_search_with_dialog
        )

        self._options_prx_node.set(
            'extra.collection', self.execute_collection_with_dialog
        )

        self._set_collapse_update_(
            collapse_dict={
                'options': self._options_prx_node,
            }
        )

        self._refresh_button = prx_widgets.PrxPressItem()
        self.add_button(self._refresh_button)
        self._refresh_button.set_name('refresh')
        self._refresh_button.connect_press_clicked_to(self.refresh_gui_fnc)

        self.post_setup_fnc()

        self.set_refresh_all()

    def set_refresh_all(self):
        self.refresh_gui_fnc()

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = None

    def _set_dcc_objs_update_(self):
        self._dcc_objs = []

    def refresh_gui_fnc(self):
        self._set_dcc_texture_references_update_()
        self._set_dcc_objs_update_()
        method_args = [
            (self._set_gui_textures_refresh_, ()),
            (self._set_gui_textures_validator_, ())
        ]
        with bsc_log.LogProcessContext.create(maximum=len(method_args), label='gui processing') as g_p:
            for i_fnc, i_args in method_args:
                g_p.do_update()
                i_fnc(*i_args)

    def _set_gui_textures_refresh_(self):
        self._texture_add_opt.restore_all()
        self._gui_tag_filter_opt.restore_all()

        if self._dcc_objs:
            with bsc_log.LogProcessContext.create(maximum=len(self._dcc_objs), label='gui texture showing') as g_p:
                for i_dcc_obj in self._dcc_objs:
                    g_p.do_update()

                    i_files = i_dcc_obj.get_stg_files()
                    if i_files:
                        j_keys = []
                        for j_file in i_files:
                            j_is_create, j_file_prx_item = self._texture_add_opt.gui_add_as(
                                j_file,
                                mode='list',
                                use_show_thread=True
                            )
                            if j_is_create is True:
                                j_file_prx_item.connect_press_db_clicked_to(
                                    self._show_image_detail
                                )
                            # create relevant node as a child, node may be more than one
                            if j_file_prx_item is not None:
                                i_dcc_obj_prx_item = self._dcc_add_opt._set_prx_item_add_2_(
                                    i_dcc_obj,
                                    j_file_prx_item
                                )
                                i_dcc_obj.set_obj_gui(i_dcc_obj_prx_item)
                                j_keys.append('format.{}'.format(j_file.type_name))

    def _set_gui_textures_validator_(self):
        textures = self._texture_add_opt.get_files()
        c = len(textures)

        repath_src_port = self._options_prx_node.get_port('target.repath_to_source')
        repath_src_statuses = [gui_core.GuiDialog.ValidationStatus.Normal]*c

        repath_tgt_port = self._options_prx_node.get_port('target.repath_to_target')
        repath_tgt_statuses = [gui_core.GuiDialog.ValidationStatus.Normal]*c

        if self._options_prx_node.get('validation_enable') is True:
            ext_tgt = self._options_prx_node.get('target.extension')
            with bsc_log.LogProcessContext.create(maximum=len(textures), label='gui texture validating') as g_p:
                for i_index, i_texture_any in enumerate(textures):
                    g_p.do_update()

                    i_texture_prx_item = i_texture_any.get_obj_gui()
                    #
                    i_descriptions = []

                    i_directory_args_dpt = bsc_dcc_objects.StgTexture.get_directory_args_dpt_as_default_fnc(
                        i_texture_any, ext_tgt
                        )
                    if i_directory_args_dpt:
                        i_texture_src, i_texture_tgt = i_texture_any.get_args_as_ext_tgt_by_directory_args(
                            ext_tgt, i_directory_args_dpt
                            )
                        if i_texture_src.ext == ext_tgt:
                            i_descriptions.append(
                                u'source is non-exists'
                            )
                            repath_src_statuses[i_index] = i_texture_prx_item.ValidationStatus.Lost
                        else:
                            if i_texture_src.get_is_exists() is True:
                                if i_texture_src.get_is_writable() is True:
                                    if i_texture_any == i_texture_src:
                                        repath_src_statuses[i_index] = i_texture_prx_item.ValidationStatus.Correct
                                else:
                                    repath_src_statuses[i_index] = i_texture_prx_item.ValidationStatus.Locked
                            else:
                                i_descriptions.append(
                                    u'source is non-exists'
                                )
                                repath_src_statuses[i_index] = i_texture_prx_item.ValidationStatus.Lost
                        #
                        if i_texture_tgt.get_is_exists() is True:
                            if i_texture_tgt.get_is_writable() is True:
                                if i_texture_any == i_texture_tgt:
                                    repath_tgt_statuses[i_index] = i_texture_prx_item.ValidationStatus.Correct
                            else:
                                repath_tgt_statuses[i_index] = i_texture_prx_item.ValidationStatus.Locked
                        else:
                            i_descriptions.append(
                                u'target is non-exists'
                            )
                            repath_tgt_statuses[i_index] = i_texture_prx_item.ValidationStatus.Lost
                        #
                        if i_texture_src.get_is_exists() is True and i_texture_tgt.get_is_exists() is True:
                            if i_texture_src.get_timestamp_is_same_to(i_texture_tgt) is False:
                                i_descriptions.append(
                                    u'target is changed'
                                )
                                repath_tgt_statuses[i_index] = i_texture_prx_item.ValidationStatus.Warning

                    i_texture_prx_item.set_name(
                        u', '.join(i_descriptions), 2
                    )

                    i_color_space = i_texture_src.get_best_color_space()
                    i_texture_prx_item.set_name(i_color_space, 1)

                    i_dcc_obj_prx_items = i_texture_prx_item.get_children()
                    for j_dcc_obj_prx_item in i_dcc_obj_prx_items:
                        j_dcc_obj = j_dcc_obj_prx_item.get_gui_dcc_obj(
                            namespace=self.DCC_NAMESPACE
                        )
                        j_color_space = j_dcc_obj.get_color_space()
                        j_dcc_obj_prx_item.set_name(j_color_space, 1)
                        if i_descriptions:
                            self._gui_tag_filter_opt.register(
                                j_dcc_obj_prx_item, [bsc_core.SPathMtd.set_quote_to(i) for i in i_descriptions]
                            )
                        else:
                            self._gui_tag_filter_opt.register(
                                j_dcc_obj_prx_item, [bsc_core.SPathMtd.set_quote_to(i) for i in ['N/a']]
                            )

        repath_src_port.set_statuses(
            repath_src_statuses
        )
        repath_tgt_port.set_statuses(
            repath_tgt_statuses
        )

    def _set_target_create_data_update_(self, ext_tgt, force_enable):
        contents = []
        #
        self._create_data = []
        textures = self._texture_add_opt.get_checked_files()
        if textures:
            with bsc_log.LogProcessContext.create(maximum=len(textures), label='gain texture create-data') as g_p:
                for i_texture_any in self._texture_add_opt.get_checked_files():
                    g_p.do_update()
                    # ignore is locked
                    if i_texture_any.get_is_readable() is False:
                        continue
                    #
                    i_directory_args_dpt = bsc_dcc_objects.StgTexture.get_directory_args_dpt_as_default_fnc(
                        i_texture_any, ext_tgt
                        )
                    if i_directory_args_dpt:
                        i_texture_src, i_texture_tgt = i_texture_any.get_args_as_ext_tgt_by_directory_args(
                            ext_tgt, i_directory_args_dpt
                            )
                        if i_texture_src is not None:
                            i_texture_src_units = i_texture_src.get_exists_units()
                            i_output_directory_path = i_texture_tgt.directory.path
                            for j_texture_src_unit in i_texture_src_units:
                                if force_enable is True:
                                    self._create_data.append(
                                        (j_texture_src_unit.path, i_output_directory_path)
                                    )
                                else:
                                    if j_texture_src_unit._get_unit_is_exists_as_tgt_ext_by_src_(
                                            j_texture_src_unit.path,
                                            ext_tgt=ext_tgt,
                                            search_directory_path=i_output_directory_path,
                                    ) is False:
                                        self._create_data.append(
                                            (j_texture_src_unit.path, i_output_directory_path)
                                        )
        else:
            contents.append(
                u'check one or more node and retry'
            )

        if contents:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False

    def _set_target_create_by_data_(self, button, post_fnc=None):
        def finished_fnc_(index, status, results):
            button.set_finished_at(index, status)
            print '\n'.join(results)

        def status_update_at_fnc_(index, status):
            button.set_status_at(index, status)

        def run_fnc_():
            for i_index, (i_file_path, i_output_directory_path) in enumerate(self._create_data):
                bsc_storage.StgPathMtd.create_directory(
                    i_output_directory_path
                )

                i_cmd = bsc_dcc_objects.StgTexture._get_unit_tx_create_cmd_by_src_force_(
                    i_file_path,
                    search_directory_path=i_output_directory_path,
                )
                if button.get_is_stopped():
                    break
                #
                if i_cmd:
                    bsc_core.TrdCommandPool.set_wait()
                    i_t = bsc_core.TrdCommandPool.set_start(i_cmd, i_index)
                    i_t.status_changed.connect_to(status_update_at_fnc_)
                    i_t.finished.connect_to(finished_fnc_)
                else:
                    status_update_at_fnc_(
                        i_index, button.Status.Completed
                    )
                    finished_fnc_(
                        i_index, button.Status.Completed
                    )

        def quit_fnc_():
            button.set_stopped()
            #
            time.sleep(1)
            #
            t.quit()
            t.wait()
            t.deleteLater()

        contents = []
        if self._create_data:
            button.set_stopped(False)

            c = len(self._create_data)

            button.set_status(button.Status.Started)
            button.set_initialization(c, button.Status.Started)

            t = gui_qt_core.QtMethodThread(self.widget)
            t.append_method(
                run_fnc_
            )
            t.start()
            if post_fnc is not None:
                t.run_finished.connect(
                    post_fnc
                )

            self.connect_window_close_to(quit_fnc_)
        else:
            button.restore_all()

            contents = [
                'non-texture(s) to create, you can click refresh and try again or turn on "create force enable"'
            ]

        if contents:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False
        else:
            return True

    def _set_target_create_execute_(self):
        force_enable = self._options_prx_node.get('target.create_force_enable')
        ext_tgt = self._options_prx_node.get('target.extension')
        button = self._options_prx_node.get_port('target.create_target')
        method_args = [
            (self._set_target_create_data_update_, (ext_tgt, force_enable)),
            (self._set_target_create_by_data_, (button, self.refresh_gui_fnc))
        ]
        with bsc_log.LogProcessContext.create(maximum=len(method_args), label='create texture by data') as g_p:
            for i_fnc, i_args in method_args:
                g_p.do_update()
                #
                i_result = i_fnc(*i_args)
                if i_result is False:
                    break

    def _set_repath_to_src_(self):
        contents = []
        ext_tgt = self._options_prx_node.get('target.extension')
        #
        textures = self._texture_add_opt.get_checked_files()
        if textures:
            with bsc_log.LogProcessContext.create(maximum=len(textures), label='repath texture to source') as g_p:
                for i_texture_any in self._texture_add_opt.get_checked_files():
                    g_p.do_update()

                    i_texture_prx_item = i_texture_any.get_obj_gui()

                    i_directory_args_dpt = bsc_dcc_objects.StgTexture.get_directory_args_dpt_as_default_fnc(
                        i_texture_any, ext_tgt
                        )
                    if i_directory_args_dpt:
                        i_texture_src, i_texture_tgt = i_texture_any.get_args_as_ext_tgt_by_directory_args(
                            ext_tgt, i_directory_args_dpt
                            )
                        if i_texture_src is not None:
                            if i_texture_src.get_is_exists() is True:
                                i_dcc_obj_prx_items = i_texture_prx_item.get_children()
                                i_port_path = i_texture_any.get_relevant_dcc_port_path()
                                for j_dcc_obj_prx_item in i_dcc_obj_prx_items:
                                    if j_dcc_obj_prx_item.get_is_checked() is True:
                                        j_dcc_obj = j_dcc_obj_prx_item.get_gui_dcc_obj(
                                            namespace=self.DCC_NAMESPACE
                                        )
                                        #
                                        self._dcc_texture_references.repath_fnc(
                                            j_dcc_obj, i_port_path, i_texture_src.path
                                        )
                #
                self.refresh_gui_fnc()
                return True
        else:
            contents.append(
                u'check one or more node and retry'
            )

        if contents:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False

    def _set_repath_to_tgt_(self):
        contents = []
        #
        ext_tgt = self._options_prx_node.get('target.extension')
        #
        textures = self._texture_add_opt.get_checked_files()
        if textures:
            with bsc_log.LogProcessContext.create(maximum=len(textures), label='repath texture to target') as g_p:
                for i_texture_any in self._texture_add_opt.get_checked_files():
                    g_p.do_update()

                    i_texture_prx_item = i_texture_any.get_obj_gui()

                    i_directory_args_dpt = bsc_dcc_objects.StgTexture.get_directory_args_dpt_as_default_fnc(
                        i_texture_any, ext_tgt
                        )
                    if i_directory_args_dpt:
                        i_texture_src, i_texture_tgt = i_texture_any.get_args_as_ext_tgt_by_directory_args(
                            ext_tgt, i_directory_args_dpt
                            )
                        if i_texture_tgt.get_is_exists() is True:
                            i_dcc_obj_prx_items = i_texture_prx_item.get_children()
                            i_port_path = i_texture_any.get_relevant_dcc_port_path()
                            for j_dcc_obj_prx_item in i_dcc_obj_prx_items:
                                if j_dcc_obj_prx_item.get_is_checked() is True:
                                    j_dcc_obj = j_dcc_obj_prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
                                    #
                                    self._dcc_texture_references.repath_fnc(
                                        j_dcc_obj, i_port_path, i_texture_tgt.path
                                    )
                #
                self.refresh_gui_fnc()
                return True
        else:
            contents.append(
                u'check one or more node and retry'
            )

        if contents:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False

    def execute_search_process(
        self, window, textures, directory, below_enable, ignore_exists, ignore_name_case, ignore_ext_case,
        ignore_ext
    ):
        if directory:
            search_opt = bsc_storage.StgFileSearchOpt(
                ignore_name_case=ignore_ext_case,
                ignore_ext_case=ignore_name_case,
                ignore_ext=ignore_ext
            )
            search_opt.append_search_directory(directory, below_enable)
            with window.gui_progressing(maximum=len(textures)) as p:
                for i_texture_any in self._texture_add_opt.get_checked_files():
                    p.do_update()
                    #
                    if ignore_exists is True:
                        if i_texture_any.get_is_exists() is True:
                            continue

                    if i_texture_any.directory.path == directory:
                        continue

                    i_texture_prx_item = i_texture_any.get_obj_gui()
                    i_result = search_opt.get_result(i_texture_any.path)
                    if i_result:
                        i_dcc_obj_prx_items = i_texture_prx_item.get_children()
                        i_port_path = i_texture_any.get_relevant_dcc_port_path()
                        for j_dcc_obj_prx_item in i_dcc_obj_prx_items:
                            if j_dcc_obj_prx_item.get_is_checked() is True:
                                j_dcc_obj = j_dcc_obj_prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)

                                self._dcc_texture_references.repath_fnc(
                                    j_dcc_obj, i_port_path, i_result
                                )

            self.refresh_gui_fnc()

    def execute_search_with_dialog(self):
        contents = []
        textures = self._texture_add_opt.get_checked_files()
        if textures:
            def yes_fnc_():
                self.execute_search_process(w, textures, **w.get_options_as_kwargs())

            w = gui_core.GuiDialog.create(
                self._session.gui_name,
                sub_label='Search',
                content=u'choose or entry a directory, press "Confirm" to continue',
                status=gui_core.GuiDialog.ValidationStatus.Active,
                #
                options_configure=self._session.configure.get('build.node.extra_search'),
                #
                yes_label='Confirm',
                #
                yes_method=yes_fnc_,
                #
                no_visible=False,
                show=False,
                #
                window_size=(480, 480),
                #
                parent=self.widget,
            )
            w.set_window_show()
        else:
            contents.append(
                u'check one or more node and retry'
            )
        if contents:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False

    def execute_collection_process(
        self, window, textures, directory, scheme, mode, copy_or_link_enable, replace_enable, repath_enable,
        target_extension
    ):
        if directory:
            with window.gui_progressing(maximum=len(textures)) as p:
                for i_texture_any in self._texture_add_opt.get_checked_files():
                    p.do_update()
                    #
                    if i_texture_any.directory.path == directory:
                        continue

                    if i_texture_any.get_is_readable() is False:
                        continue

                    i_texture_prx_item = i_texture_any.get_obj_gui()

                    i_directory_args_dpt = bsc_dcc_objects.StgTexture.get_directory_args_dpt_fnc(
                        i_texture_any, target_extension
                    )

                    if scheme == 'default':
                        i_directory_args_dst = bsc_dcc_objects.StgTexture.get_directory_args_dst_as_default_fnc(
                            i_texture_any, target_extension, directory
                        )
                    elif scheme == 'separate':
                        i_directory_args_dst = bsc_dcc_objects.StgTexture.get_directory_args_dst_as_separate_fnc(
                            i_texture_any, target_extension, directory
                        )
                    else:
                        raise TypeError()

                    if i_directory_args_dpt and i_directory_args_dst:
                        i_texture_src, i_texture_tgt = i_texture_any.get_args_as_ext_tgt_by_directory_args(
                            target_extension, i_directory_args_dpt
                        )
                        i_directory_src_dst, i_directory_tgt_dst = i_directory_args_dst

                        if copy_or_link_enable is True:
                            if mode == 'copy':
                                [j.copy_to_directory(i_directory_src_dst, replace=replace_enable) for j in
                                 i_texture_src.get_exists_units()]
                                [j.copy_to_directory(i_directory_tgt_dst, replace=replace_enable) for j in
                                 i_texture_tgt.get_exists_units()]
                            elif mode == 'link':
                                [j.set_link_to_directory(i_directory_src_dst, replace=replace_enable) for j in
                                 i_texture_src.get_exists_units()]
                                [j.set_link_to_directory(i_directory_tgt_dst, replace=replace_enable) for j in
                                 i_texture_tgt.get_exists_units()]
                        #
                        if repath_enable is True:
                            i_dcc_obj_prx_items = i_texture_prx_item.get_children()
                            i_port_path = i_texture_any.get_relevant_dcc_port_path()
                            for j_dcc_obj_prx_item in i_dcc_obj_prx_items:
                                if j_dcc_obj_prx_item.get_is_checked() is True:
                                    j_dcc_obj = j_dcc_obj_prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
                                    #
                                    if i_texture_any == i_texture_src:
                                        i_texture_any_dst = i_texture_src.get_target_file(
                                            i_directory_src_dst
                                        )
                                    else:
                                        i_texture_any_dst = i_texture_tgt.get_target_file(
                                            i_directory_tgt_dst
                                        )
                                    #
                                    if i_texture_any_dst.get_is_exists() is True:
                                        self._dcc_texture_references.repath_fnc(
                                            j_dcc_obj, i_port_path, i_texture_any_dst.path
                                        )
            #
            self.refresh_gui_fnc()
            return True

    def execute_collection_with_dialog(self):
        contents = []
        textures = self._texture_add_opt.get_checked_files()
        if textures:
            def yes_fnc_():
                self.execute_collection_process(w, textures, **w.get_options_as_kwargs())

            #
            w = gui_core.GuiDialog.create(
                self._session.gui_name,
                sub_label='Collection',
                content=u'choose or entry a directory, press "Confirm" to continue',
                status=gui_core.GuiDialog.ValidationStatus.Active,
                #
                options_configure=self._session.configure.get('build.node.extra_collection'),
                #
                yes_label='Confirm',
                #
                yes_method=yes_fnc_,
                #
                no_visible=False,
                show=False,
                #
                window_size=(480, 480),
                #
                parent=self.widget,
            )
            w.set_window_show()
        else:
            contents.append(
                u'check one or more node and retry'
            )
        if contents:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            return False

    def _show_image_detail(self, item, column):
        texture = self._texture_add_opt.get_file(item)
        w = gui_core.GuiDialog.create(
            self._session.gui_name,
            window_size=(512, 512),
            #
            yes_visible=False, no_visible=False,
            tip_visible=False,
            show=False,
            #
            parent=self.widget
        )

        v = prx_widgets.PrxImageView()
        w.add_customize_widget(v)

        v.set_textures([texture])

        w.set_window_show()

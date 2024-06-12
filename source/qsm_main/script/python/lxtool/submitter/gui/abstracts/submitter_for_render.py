# coding:utf-8
import lxbasic.content as bsc_content

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.shotgun as bsc_shotgun

import lxgeneral.dcc.objects as gnl_dcc_objects

import lxuniverse.objects as unr_objects

import lxresolver.core as rsv_core

import lxsession.commands as ssn_commands

import lxshotgun.rsv.scripts as stg_rsv_scripts

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.core as gui_prx_core

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.proxy.scripts as gui_prx_scripts


class AbsRenderSubmitterDef(object):
    OPTION_HOOK_KEY = None

    def _set_render_submitter_def_init_(self, hook_option):
        if hook_option is not None:
            self._hook_option_opt = bsc_core.ArgDictStringOpt(hook_option)
            self._file_path = self._hook_option_opt.get('file')
            self._hook_option_opt.set(
                'option_hook_key', self.OPTION_HOOK_KEY
            )

            self._option_hook_configure = ssn_commands.get_option_hook_configure(
                self._hook_option_opt.to_string()
            )

            self._hook_gui_configure = self._option_hook_configure.get_as_content('option.gui')
            self._hook_build_configure = self._option_hook_configure.get_as_content('build')

            raw = bsc_core.EnvBaseMtd.get('REZ_BETA')
            if raw:
                self._rez_beta = True
            else:
                self._rez_beta = False

            self._stg_connector = bsc_shotgun.StgConnector()
        else:
            self._file_path = None
        #
        self._rsv_scene_properties = None
        self._rsv_task = None
        self._rsv_entity = None
        self._stg_entity_query = None
        self._render_movie_file_rsv_unit = None
        self._start_frame, self._end_frame = 0, 0
        #
        self._variable_keys = []


class AbsPnlSubmitterForRenderBase(
    gui_prx_widgets.PrxBaseWindow,
    AbsRenderSubmitterDef,
):
    ITEM_ICON_FRAME_SIZE = 26, 26
    ITEM_ICON_SIZE = 24, 24

    def __init__(self, hook_option=None, *args, **kwargs):
        super(AbsPnlSubmitterForRenderBase, self).__init__(*args, **kwargs)
        self._qt_thread_enable = bsc_core.EnvBaseMtd.get_qt_thread_enable()
        #
        if hook_option is not None:
            self._set_render_submitter_def_init_(hook_option)
            if self._rez_beta:
                self.set_window_title(
                    '[BETA] {}'.format(self._hook_gui_configure.get('name'))
                )
            else:
                self.set_window_title(
                    self._hook_gui_configure.get('name')
                )
            #
            self.set_window_icon_name_text(
                self._hook_gui_configure.get('name')
            )
            self.set_definition_window_size(
                self._hook_gui_configure.get('size')
            )
        else:
            self._file_path = None
        #
        self._set_panel_build_()
        # self.get_log_bar().set_expanded(True)
        #
        self.start_window_loading(
            self._set_tool_panel_setup_
        )

    def _set_panel_build_(self):
        self._set_viewer_groups_build_()

    def _set_viewer_groups_build_(self):
        h_splitter_0 = gui_prx_widgets.PrxHSplitter()
        self.add_widget(h_splitter_0)
        #
        v_splitter_0 = gui_prx_widgets.PrxVSplitter()
        h_splitter_0.add_widget(v_splitter_0)
        qt_scroll_area_0 = qt_widgets.QtVScrollArea()
        v_splitter_0.add_widget(qt_scroll_area_0)
        qt_layout_0 = qt_scroll_area_0._layout
        #
        self._schemes_prx_node = gui_prx_widgets.PrxOptionsNode('schemes')
        qt_layout_0.addWidget(self._schemes_prx_node.widget)
        #
        self._options_prx_node = gui_prx_widgets.PrxOptionsNode('options')
        qt_layout_0.addWidget(self._options_prx_node.widget)
        #
        prx_expanded_group_0 = gui_prx_widgets.PrxHToolGroup()
        v_splitter_0.add_widget(prx_expanded_group_0)
        prx_expanded_group_0.set_name('combinations')
        prx_expanded_group_0.set_expanded(True)
        #
        self._filter_tree_viewer_0 = gui_prx_widgets.PrxTreeView()
        prx_expanded_group_0.add_widget(self._filter_tree_viewer_0)
        v_splitter_0.set_stretches([2, 1])
        #
        prx_expanded_group_1 = gui_prx_widgets.PrxHToolGroup()
        h_splitter_0.add_widget(prx_expanded_group_1)
        prx_expanded_group_1.set_expanded(True)
        prx_expanded_group_1.set_name('renderers')
        self._rsv_renderer_list_view = gui_prx_widgets.PrxListView()
        prx_expanded_group_1.add_widget(self._rsv_renderer_list_view)

        qt_scroll_area_1 = qt_widgets.QtVScrollArea()
        qt_layout_1 = qt_scroll_area_1._layout
        h_splitter_0.add_widget(qt_scroll_area_1)
        #
        self._usd_prx_node = gui_prx_widgets.PrxOptionsNode('usd')
        qt_layout_1.addWidget(self._usd_prx_node.widget)
        #
        self._variables_prx_node = gui_prx_widgets.PrxOptionsNode('variables')
        qt_layout_1.addWidget(self._variables_prx_node.widget)
        #
        self._settings_prx_node = gui_prx_widgets.PrxOptionsNode('settings')
        qt_layout_1.addWidget(self._settings_prx_node.widget)
        #
        h_splitter_0.set_stretches([1, 2, 1])
        #
        self._set_obj_viewer_build_()

    def _set_obj_viewer_build_(self):
        self._filter_tree_viewer_0.create_header_view(
            [('name', 3), ('count', 1)],
            self.get_definition_window_size()[0]*(1.0/5.0)-24
        )
        self._filter_tree_viewer_0.set_selection_use_single()

        self._prx_dcc_obj_tree_view_tag_filter_opt = gui_prx_scripts.GuiPrxScpForTreeTagFilter(
            prx_tree_view_src=self._filter_tree_viewer_0,
            prx_tree_view_tgt=self._rsv_renderer_list_view,
            prx_tree_item_cls=gui_prx_widgets.PrxObjTreeItem
        )

        self._rsv_renderer_list_view.set_item_frame_size_basic(
            *self._hook_gui_configure.get('item_frame_size')
        )
        self._rsv_renderer_list_view.set_item_name_frame_draw_enable(True)
        self._rsv_renderer_list_view.set_item_image_frame_draw_enable(True)
        #
        self._rsv_renderer_list_view.set_item_icon_frame_size(*self.ITEM_ICON_FRAME_SIZE)
        self._rsv_renderer_list_view.set_item_icon_size(*self.ITEM_ICON_SIZE)

    def _set_tool_panel_setup_(self):
        self._set_prx_node_build_()
        self.set_all_refresh()

    def _set_prx_node_build_(self):
        self._schemes_prx_node.create_ports_by_data(
            self._hook_build_configure.get('node.schemes')
        )
        #
        self._options_prx_node.create_ports_by_data(
            self._hook_build_configure.get('node.options')
        )
        # usd
        self._usd_prx_node.create_ports_by_data(
            self._hook_build_configure.get('node.usd')
        )

        self._variables_prx_node.create_ports_by_data(
            self._hook_build_configure.get('node.variables')
        )

        self._settings_prx_node.create_ports_by_data(
            self._hook_build_configure.get('node.settings')
        )

        self._set_prx_node_effect_()

    def _set_prx_node_effect_(self):
        raise NotImplementedError()

    def set_all_refresh(self):
        raise NotImplementedError()

    def get_file_is_changed(self):
        file_path_src = self._file_path
        file_path_tgt = None
        return True


class AbsPnlRenderSubmitterForAsset(AbsPnlSubmitterForRenderBase):
    def __init__(self, hook_option=None, *args, **kwargs):
        super(AbsPnlRenderSubmitterForAsset, self).__init__(hook_option, *args, **kwargs)

    def set_all_refresh(self):
        if self._file_path:
            self._file_path = bsc_storage.StgPathMapper.map_to_current(self._file_path)
            self._resolver = rsv_core.RsvBase.generate_root()
            self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(self._file_path)
            if self._rsv_scene_properties:
                self._variable_variants_dic = self._hook_build_configure.get(
                    'variables.character'
                )
                self._variable_keys = self._hook_build_configure.get_key_names_at(
                    'variables.character'
                )
                #
                self._rsv_task = self._resolver.get_rsv_task(
                    **self._rsv_scene_properties.value
                )
                self._rsv_project = self._rsv_task.get_rsv_project()
                self._rsv_entity = self._rsv_task.get_rsv_resource()
                self._render_movie_file_rsv_unit = self._rsv_task.get_rsv_unit(
                    keyword='{branch}-temporary-katana-render-video-mov-file'
                )
                self._render_info_file_rsv_unit = self._rsv_task.get_rsv_unit(
                    keyword='{branch}-temporary-render-info-yaml-file'
                )
                self._camera_rsv_task = self._rsv_entity.get_rsv_task(
                    step='cam', task='camera'
                )
                if self._camera_rsv_task is not None:
                    self._camera_work_maya_scene_src_file_rsv_unit = self._camera_rsv_task.get_rsv_unit(
                        keyword='{branch}-source-maya-scene-src-file'
                    )
                    self._camera_abc_file_rsv_unit = self._camera_rsv_task.get_rsv_unit(
                        keyword='{branch}-camera-main-abc-file'
                    )
                    self._check_rsv_units = [
                        # self._rsv_task.get_rsv_unit(
                        #     keyword='{branch}-component-usd-file'
                        # ),
                        # self._rsv_task.get_rsv_unit(
                        #     keyword='{branch}-temporary-component-usd-file'
                        # ),
                        self._camera_work_maya_scene_src_file_rsv_unit,
                        self._camera_abc_file_rsv_unit
                    ]
                    #
                    self.set_current_refresh()
                    #
                    self.set_settings_refresh()
                    self.set_combinations_refresh()
                    self.set_variables_refresh()
                else:
                    gui_core.GuiDialog.create(
                        self._hook_gui_configure.get('name'),
                        content='file="{}" camera task is non-exists, please call for TD get more help'.format(
                            self._file_path
                            ),
                        status=gui_core.GuiDialog.ValidationStatus.Error,
                        #
                        ok_label='Close', ok_method=self.do_close_window_later,
                        #
                        no_visible=False, cancel_visible=False,
                        use_exec=False,
                        #
                        parent=self._qt_widget
                    )

    def set_scheme_save(self):
        filter_dict = self._prx_dcc_obj_tree_view_tag_filter_opt.get_filter_dict()
        # print filter_dict
        bsc_content.Content(value=filter_dict).print_as_yaml_style()

    # options
    def set_options_refresh(self):
        import lxusd.rsv.objects as usd_rsv_objects

        self._options_prx_node.set(
            'task', self._rsv_task.path
        )
        branch = self._rsv_task.get('branch')
        step = self._rsv_task.get('step')
        if step in ['mod']:
            self._schemes_prx_node.set(
                'variables', 'model'
            )
            self._schemes_prx_node.set(
                'settings', 'asset'
            )
            key = 'model'
            cache_workspace = 'output'
        elif step in ['srf']:
            self._schemes_prx_node.set(
                'variables', 'surface'
            )
            self._schemes_prx_node.set(
                'settings', 'asset'
            )
            key = 'surface'
            cache_workspace = 'output'
        elif step in ['grm']:
            self._schemes_prx_node.set(
                'variables', 'groom'
            )
            self._schemes_prx_node.set(
                'settings', 'asset'
            )
            key = 'groom'
            cache_workspace = 'output'
        elif step in ['rig']:
            self._schemes_prx_node.set(
                'variables', 'rig'
            )
            self._schemes_prx_node.set(
                'settings', 'asset'
            )
            key = 'rig'
            cache_workspace = 'output'
        else:
            gui_core.GuiDialog.create(
                self._hook_gui_configure.get('name'),
                content='step="{}" is not available, please call for TD get more help'.format(step),
                status=gui_core.GuiDialog.ValidationStatus.Error,
                #
                ok_label='Close', ok_method=self.set_window_close,
                #
                no_visible=False, cancel_visible=False,
                use_exec=False
            )
            return False
        #
        application = self._rsv_scene_properties.get('application')
        self._work_keyword = '{}-work-{}-scene-src-file'.format(
            branch, application
        )
        self._output_keyword = '{}-output-{}-scene-src-file'.format(
            branch, application
        )
        #
        choice_scheme = 'asset-{}-{}-{}'.format(
            key, application, cache_workspace
        )
        self._options_prx_node.set('choice_scheme', choice_scheme)

        self._work_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=self._work_keyword)
        self._output_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=self._output_keyword)
        self._rsv_entity_set_usd_creator = usd_rsv_objects.RsvUsdAssetSetCreator(self._rsv_entity)
        #
        self._set_options_add_rsv_versions_()

        self._set_options_add_rsv_shots_()

    def _set_options_add_rsv_versions_(self):
        def post_fnc_():
            pass

        def cache_fnc_():
            return self._work_scene_file_rsv_unit.get_rsv_versions(trim=(-10, None))

        def build_fnc_(rsv_versions_):
            self._options_prx_node.set('version', rsv_versions_)

        if self._qt_thread_enable is True:
            t = gui_qt_core.QtBuildThread(self.widget)
            t.set_cache_fnc(
                cache_fnc_
            )
            t.cache_value_accepted.connect(build_fnc_)
            t.run_finished.connect(post_fnc_)
            #
            t.start()
        else:
            build_fnc_(cache_fnc_())
            post_fnc_()

    def _set_options_add_rsv_shots_(self):
        def post_fnc_():
            pass

        def cache_fnc_():
            return self._rsv_entity_set_usd_creator.get_rsv_asset_shots()

        def build_fnc_(rsv_shots_):
            self._options_prx_node.set('shot', rsv_shots_)

        if self._qt_thread_enable is True:
            t = gui_qt_core.QtBuildThread(self.widget)
            t.set_cache_fnc(
                cache_fnc_
            )
            t.cache_value_accepted.connect(build_fnc_)
            t.run_finished.connect(post_fnc_)
            #
            t.start()
        else:
            build_fnc_(cache_fnc_())
            post_fnc_()

    def set_current_refresh(self):
        methods = [
            self.set_options_refresh,
            self.set_renderers_refresh,
            self.set_usd_refresh,
        ]
        with bsc_log.LogProcessContext.create(maximum=len(methods), label='execute refresh method') as g_p:
            for i in methods:
                g_p.do_update()
                result = i()
                if result is False:
                    break
        #
        self.set_settings_load_from_scheme()

    def _set_prx_node_effect_(self):
        # self._schemes_prx_node.set(
        #     'save', self.set_scheme_save
        # )
        self._schemes_prx_node.connect_input_changed_to(
            'variables', self.set_combinations_load_from_scheme
        )
        self._schemes_prx_node.connect_input_changed_to(
            'settings', self.set_settings_load_from_scheme
        )

        self._options_prx_node.get_port(
            'shot'
        ).connect_input_changed_to(
            self.set_usd_refresh
        )

        self._options_prx_node.get_port(
            'shot'
        ).connect_input_changed_to(
            self.set_settings_refresh
        )

        self._options_prx_node.set(
            'refresh', self.set_current_refresh
        )

        self._settings_prx_node.set(
            'submit', self.set_submit
        )

        self._settings_prx_node.set(
            'td.publish_camera', self.set_camera_publish
        )

        collapse_dict = {
            'usd': self._usd_prx_node,
            'variables': self._variables_prx_node,
            'settings': self._settings_prx_node,
        }

        for i_k, i_v in collapse_dict.items():
            i_c = self._hook_build_configure.get(
                'node_collapse.{}'.format(i_k)
            ) or []
            if i_c:
                for i in i_c:
                    i_v.get_port(
                        i.replace('/', '.')
                    ).set_expanded(False)

    def _set_gui_rsv_task_unit_show_deferred_(self, prx_item_widget, variants):
        hook_options = []
        pixmaps = []
        #
        show_info_dict = variants
        variable_name = '.'.join(variants.values())
        # print variable_name
        movie_file_path = self._render_movie_file_rsv_unit.get_result(
            version='latest',
            variants_extend=variants
        )
        if movie_file_path:
            rsv_properties = self._render_movie_file_rsv_unit.generate_properties_by_result(
                movie_file_path
            )
            version = rsv_properties.get('version')
            show_info_dict['version'] = version
            show_info_dict['update'] = bsc_core.TimePrettifyMtd.to_prettify_by_timestamp(
                bsc_storage.StgFileOpt(
                    movie_file_path
                ).get_modify_timestamp(),
                language=1
            )
            render_info_file_path = self._render_info_file_rsv_unit.get_result(
                version=version
            )
            if render_info_file_path:
                render_info = bsc_storage.StgFileOpt(render_info_file_path).set_read()
                show_info_dict['user'] = render_info['user']
                # show_info_dict['submit_time'] = bsc_core.TimePrettifyMtd.to_prettify_by_time_tag(
                #     render_info['time_tag'],
                #     language=1
                # )
                if variants['camera'] == 'shot':
                    show_info_dict['shot'] = render_info['shot']
            #
            image_file_path, image_sub_process_cmds = bsc_storage.VdoFileOpt(movie_file_path).generate_thumbnail_create_args()
            prx_item_widget.set_image(image_file_path)
            prx_item_widget.set_movie_enable(True)
            #
            session, execute_fnc = ssn_commands.get_option_hook_args(
                bsc_core.ArgDictStringOpt(
                    dict(
                        option_hook_key='actions/movie-open',
                        file=movie_file_path,
                        gui_group_name='movie',
                        gui_name='open movie'
                    )
                ).to_string()
            )
            #
            prx_item_widget.connect_press_dbl_clicked_to(
                execute_fnc
            )
            #
            hook_options.extend(
                [
                    bsc_core.ArgDictStringOpt(
                        dict(
                            option_hook_key='actions/movie-open',
                            file=movie_file_path,
                            gui_group_name='movie',
                        )
                    ).to_string(),
                    bsc_core.ArgDictStringOpt(
                        dict(
                            option_hook_key='actions/file-directory-open',
                            file=movie_file_path,
                            gui_group_name='directory',
                            gui_name='open movie directory'
                        )
                    ).to_string(),
                    bsc_core.ArgDictStringOpt(
                        dict(
                            option_hook_key='actions/movie-upload',
                            file=movie_file_path,
                            gui_group_name='upload',
                        )
                    ).to_string(),
                ]
            )
            if image_sub_process_cmds is not None:
                prx_item_widget.set_image_show_args(image_file_path, image_sub_process_cmds)
        else:
            prx_item_widget.set_image(
                gui_core.GuiIcon.get('image_loading_failed')
            )
        #
        for i_rsv_unit in self._check_rsv_units:
            i_file_path = i_rsv_unit.get_result(version='latest')
            if i_file_path:
                i_rsv_properties = i_rsv_unit.generate_properties_by_result(i_file_path)
                i_rsv_unit_file = gnl_dcc_objects.StgFile(i_file_path)
                i_pixmap = gui_qt_core.GuiQtPixmap.get_by_file_ext_with_tag(
                    i_rsv_unit_file.ext,
                    tag=i_rsv_properties.get('workspace'),
                    frame_size=self.ITEM_ICON_SIZE
                )
                pixmaps.append(i_pixmap)

                hook_options.append(
                    bsc_core.ArgDictStringOpt(
                        dict(
                            option_hook_key='actions/file-directory-open',
                            file=i_file_path,
                            gui_parent='/Open Folder',
                            gui_group_name='usd',
                            gui_name='{}'.format(i_rsv_unit.get('keyword'))
                        )
                    ).to_string()
                )
        #
        menu_content = ssn_commands.get_menu_content_by_hook_options(hook_options)
        prx_item_widget.set_menu_content(menu_content)

        prx_item_widget.set_name_dict(show_info_dict)
        prx_item_widget.set_icons_by_pixmap(pixmaps)
        r, g, b = bsc_core.RawTextOpt(variable_name).to_rgb()
        prx_item_widget.set_name_frame_background_color((r, g, b, 127))

        prx_item_widget.set_tool_tip(
            '\n'.join(['{} : {}'.format(k, v) for k, v in show_info_dict.items()])
        )

    def _set_usd_load_asset_variant_(self, rsv_asset):
        def post_fnc_():
            pass

        def cache_fnc_():
            return [
                self._rsv_entity_set_usd_creator._get_asset_usd_set_dress_variant_cache(rsv_asset)
            ]

        def build_fnc_(data_):
            if data_:
                for k, v in data_[0].items():
                    i_port_path = v['port_path']
                    i_variant_names = v['variant_names']
                    i_current_variant_name = v['variant_name']
                    self._usd_prx_node.set(
                        i_port_path, i_variant_names
                    )
                    self._usd_prx_node.set(
                        i_port_path, i_current_variant_name
                    )
                    self._usd_prx_node.set_default(
                        i_port_path, i_current_variant_name
                    )

        if self._qt_thread_enable is True:
            t = gui_qt_core.QtBuildThread(self.widget)
            t.set_cache_fnc(
                cache_fnc_
            )
            t.cache_value_accepted.connect(build_fnc_)
            t.run_finished.connect(post_fnc_)
            #
            t.start()
        else:
            build_fnc_(cache_fnc_())
            post_fnc_()

    def _set_usd_load_shot_variant_(self, rsv_asset, rsv_shot):
        def post_fnc_():
            pass

        def cache_fnc_():
            return [
                self._rsv_entity_set_usd_creator._get_shot_asset_cache(
                    rsv_asset, rsv_shot
                )
            ]

        def build_fnc_(data_):
            self._usd_prx_node.set('variants.shot_asset', data_[0].keys())

        if self._qt_thread_enable is True:
            t = gui_qt_core.QtBuildThread(self.widget)
            t.set_cache_fnc(
                cache_fnc_
            )
            t.cache_value_accepted.connect(build_fnc_)
            t.run_finished.connect(post_fnc_)
            #
            t.start()
        else:
            build_fnc_(cache_fnc_())
            post_fnc_()

    # renderers
    def set_renderers_refresh(self):
        self._rsv_renderer_list_view.set_clear()
        self._prx_dcc_obj_tree_view_tag_filter_opt.restore_all()
        #
        self._set_renderers_add_rsv_units_()

    # combinations
    def set_combinations_refresh(self):
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh(expand_depth=1)
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def set_combinations_load_from_scheme(self):
        scheme = self._schemes_prx_node.get('variables')
        filter_dict = self._hook_build_configure.get(
            'scheme.variables.{}'.format(scheme)
        )
        if filter_dict:
            self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_by_dict(
                filter_dict
            )

    # usds
    def set_usd_refresh(self):
        if self._rsv_entity is not None:
            self._set_usd_load_asset_variant_(self._rsv_entity)
            #
            rsv_shot = self._options_prx_node.get(
                'shot'
            )
            if rsv_shot is not None:
                self._set_usd_load_shot_variant_(self._rsv_entity, rsv_shot)

    def _set_renderers_add_rsv_units_(self):
        def post_fnc_():
            self.set_combinations_refresh()
            self.set_combinations_load_from_scheme()

        def cache_fnc_():
            return [
                bsc_core.RawVariablesMtd.get_all_combinations(
                    self._variable_variants_dic
                )
            ]

        def build_fnc_(data_):
            for i_seq, i_variants in enumerate(data_[0]):
                self._set_gui_add_rsv_unit_(i_variants)

        if self._qt_thread_enable is True:
            t = gui_qt_core.QtBuildThread(self.widget)
            t.set_cache_fnc(
                cache_fnc_
            )
            t.cache_value_accepted.connect(build_fnc_)
            t.run_finished.connect(post_fnc_)
            #
            t.start()
        else:
            build_fnc_(cache_fnc_())
            post_fnc_()

    def _set_gui_add_rsv_unit_(self, variants):
        def cache_fnc_():
            return []

        def build_fnc_(data):
            self._set_gui_rsv_task_unit_show_deferred_(
                rsv_unit_prx_item, variants
            )

        #
        rsv_unit_prx_item = self._rsv_renderer_list_view.create_item_widget()
        keys = []
        for j_key in self._variable_keys:
            keys.append(
                '{}.{}'.format(j_key, variants[j_key])
            )
        #
        self._prx_dcc_obj_tree_view_tag_filter_opt.register(
            rsv_unit_prx_item, keys
        )

        rsv_unit_prx_item.set_show_fnc(
            cache_fnc_, build_fnc_
        )
        return rsv_unit_prx_item

    def set_settings_refresh(self):
        rsv_task = self._rsv_task
        if rsv_task is not None:
            rsv_shot = self._options_prx_node.get(
                'shot'
            )
            if rsv_shot is not None:
                stg_shot_query = self._stg_connector.get_stg_resource_query(
                    **rsv_shot.properties.value
                )
                if stg_shot_query:
                    frame_range = (
                        stg_shot_query.get('sg_cut_in'), stg_shot_query.get('sg_cut_out')
                    )
                    frames = '{}-{}'.format(*frame_range)
                    self._settings_prx_node.set(
                        'render.shot.frames', frames
                    )
                    self._settings_prx_node.set_default(
                        'render.shot.frames', frames
                    )

        if bsc_core.EnvExtraMtd.get_is_td_enable() is True:
            self._settings_prx_node.set_default(
                'td.test_scheme', 'td_enable'
            )
            self._settings_prx_node.set(
                'td.test_scheme', 'td_enable'
            )

    def set_variables_refresh(self):
        light_rig_rsv_assets = stg_rsv_scripts.RsvStgProjectOpt(
            self._rsv_project
        ).get_standard_light_rig_rsv_assets()
        if light_rig_rsv_assets:
            names = [i.name for i in light_rig_rsv_assets]
            for seq, i in enumerate(['all', 'add_1', 'add_2']):
                self._variables_prx_node.set(
                    'light_pass.{}'.format(i), names
                )
                self._variables_prx_node.set(
                    'light_pass.{}'.format(i), names[seq]
                )
        else:
            gui_core.GuiDialog.create(
                self._hook_gui_configure.get('name'),
                content='light-rig(s) is not found, please call for TD get more help',
                status=gui_core.GuiDialog.ValidationStatus.Error,
                #
                ok_label='Close', ok_method=self.set_window_close,
                #
                no_visible=False, cancel_visible=False,
            )

    def set_settings_load_from_scheme(self):
        scheme = self._schemes_prx_node.get('settings')

        dic = self._hook_build_configure.get(
            'scheme.settings.{}'.format(scheme)
        )
        self._settings_prx_node.set_reset()
        if dic:
            for k, v in dic.items():
                if isinstance(v, dict):
                    if 'expression' in v:
                        value = None
                        e = 'value{}'.format(v['expression'])
                        exec e
                        self._settings_prx_node.set(
                            k.replace('/', '.'), value
                        )
                else:
                    self._settings_prx_node.set(
                        k.replace('/', '.'), v
                    )

    def _get_usd_dict_(self):
        c = bsc_content.Content(value={})
        c.set('usd_reverse_face_vertex_enable', self._usd_prx_node.get('debuggers.reverse_face_vertex_enable'))
        return c.get_value()

    def _get_settings_dict_(self):
        dic = {}
        #
        asset_frames = self._settings_prx_node.get('render.asset.frames')
        #
        dic['cache_asset_frames'] = asset_frames
        dic['render_asset_frames'] = asset_frames
        dic['render_asset_frame_step'] = int(self._settings_prx_node.get('render.asset.frame_step'))
        #
        shot_frames = self._settings_prx_node.get('render.shot.frames')
        #
        dic['cache_shot_frames'] = shot_frames
        dic['render_shot_frames'] = shot_frames
        dic['render_shot_frame_step'] = int(self._settings_prx_node.get('render.shot.frame_step'))
        #
        dic['render_override_enable'] = self._settings_prx_node.get('render.override_enable')
        dic['render_override_percent'] = self._settings_prx_node.get('render.override.percent')
        #
        dic['render_arnold_aov_enable'] = self._settings_prx_node.get('render.arnold.aov_enable')
        #
        dic['render_arnold_override_enable'] = self._settings_prx_node.get('render.arnold_override_enable')
        dic['render_arnold_override_aa_sample'] = self._settings_prx_node.get('render.arnold_override.aa_sample')
        #
        dic['light_pass_all'] = self._settings_prx_node.get('light_pass.all')
        dic['light_pass_add_1'] = self._settings_prx_node.get('light_pass.add_1')
        dic['light_pass_add_2'] = self._settings_prx_node.get('light_pass.add_2')
        #
        dic['deadline_priority'] = int(self._settings_prx_node.get('deadline.priority'))
        return dic

    def _get_combinations_dict_(self):
        def update_fnc(key_):
            _ks = c.get_keys('/{}/*'.format(key_))
            _key = key_mapper[key_]
            for _i_k in _ks:
                if c.get(_i_k) is True:
                    _name = bsc_core.PthNodeOpt(_i_k).get_name()
                    dic.setdefault(_key, []).append(_name)

        #
        key_mapper = {
            'camera': 'cameras',
            'layer': 'layers',
            'light_pass': 'light_passes',
            'look_pass': 'look_passes',
            'quality': 'qualities'
        }
        #
        dic = {}
        filter_dic = self._prx_dcc_obj_tree_view_tag_filter_opt.get_filter_dict()
        c = bsc_content.Content(value=filter_dic)
        for i in self._variable_keys:
            update_fnc(i)
        return dic

    def _get_variables_dict_(self):
        dic = {}
        dic['light_pass_all'] = self._variables_prx_node.get('light_pass.all')
        dic['light_pass_add_1'] = self._variables_prx_node.get('light_pass.add_1')
        dic['light_pass_add_2'] = self._variables_prx_node.get('light_pass.add_2')
        return dic

    @classmethod
    def _get_frames_(cls, frame_range, frame_step):
        pass

    def _get_hook_option_dic_(self):
        dic = {}
        rsv_task = self._rsv_task
        if rsv_task is not None:
            dic['file'] = self._file_path
            #
            rsv_shot = self._options_prx_node.get(
                'shot'
            )
            if rsv_shot:
                dic['shot'] = rsv_shot.name
            #
            dic['shot_asset'] = self._usd_prx_node.get('variants.shot_asset')
            #
            dic['choice_scheme'] = self._options_prx_node.get('choice_scheme')
            #
            dic.update(self._get_usd_dict_())
            #
            dic.update(self._get_settings_dict_())
            #
            dic.update(self._get_combinations_dict_())

            dic.update(self._get_variables_dict_())
            #
            td_test_scheme = self._settings_prx_node.get(
                'td.test_scheme'
            )
            if td_test_scheme == 'auto':
                dic['rez_beta'] = self._rez_beta
            elif td_test_scheme == 'td_enable':
                dic['td_enable'] = True
            elif td_test_scheme == 'rez_beta':
                dic['rez_beta'] = True
        return dic

    def get_file_is_changed(self):
        # file_path_src = self._file_path
        # file_path_tgt = self._output_scene_file_rsv_unit.get_result('latest')
        # return not bsc_storage.StgFileOpt(file_path_src).get_timestamp_is_same_to(file_path_tgt)
        return True

    @gui_prx_core.GuiProxyModifier.window_proxy_waiting
    def set_camera_publish(self):
        camera_work_maya_scene_scr_file_path = self._camera_work_maya_scene_src_file_rsv_unit.get_result(
            version='latest'
        )
        if camera_work_maya_scene_scr_file_path:
            hook_option_opt = bsc_core.ArgDictStringOpt(
                option=dict(
                    option_hook_key='rsv-task-batchers/asset/maya/camera-export',
                    #
                    file=camera_work_maya_scene_scr_file_path,
                    user=bsc_core.BscSystem.get_user_name(),
                    #
                    # td_enable=True,
                    rez_beta=True,
                )
            )
            #
            ssn_commands.execute_option_hook_by_deadline(
                option=hook_option_opt.to_string()
            )
            #
            gui_core.GuiDialog.create(
                self._hook_gui_configure.get('name'),
                content='{} publish job is send to deadline, more information you see in deadline monitor'.format(
                    camera_work_maya_scene_scr_file_path
                    ),
                status=gui_core.GuiDialog.ValidationStatus.Correct,
                #
                ok_label='Close',
                #
                no_visible=False, cancel_visible=False,
                use_exec=False
            )

    @gui_prx_core.GuiProxyModifier.window_proxy_waiting
    def set_submit(self):
        if self._camera_abc_file_rsv_unit.get_result(
                version='latest'
        ):
            hook_option_dic = self._get_hook_option_dic_()
            if hook_option_dic:
                if self.get_file_is_changed() is True:
                    hook_option_dic['user'] = bsc_core.BscSystem.get_user_name()
                    hook_option_dic['option_hook_key'] = 'rsv-task-batchers/asset/gen-cmb-render-submit'
                    option_opt = bsc_core.ArgDictStringOpt(hook_option_dic)
                    #
                    ssn_commands.execute_option_hook_by_deadline(
                        option=option_opt.to_string()
                    )
                    gui_core.GuiDialog.create(
                        self._hook_gui_configure.get('name'),
                        content='{} render job is send to deadline, more information you see in deadline monitor'.format(
                            self._file_path
                            ),
                        status=gui_core.GuiDialog.ValidationStatus.Correct,
                        #
                        ok_label='Close',
                        #
                        no_visible=False, cancel_visible=False,
                        use_exec=False
                    )
                else:
                    gui_core.GuiDialog.create(
                        self._hook_gui_configure.get('name'),
                        content='file="{}" is already submitted or scene changed is not be save'.format(
                            self._file_path
                            ),
                        status=gui_core.GuiDialog.ValidationStatus.Error,
                        #
                        ok_label='Close',
                        #
                        no_visible=False, cancel_visible=False,
                        use_exec=False
                    )
        else:
            gui_core.GuiDialog.create(
                self._hook_gui_configure.get('name'),
                content='file="{}" camera cache(abc) is non-exists, please call for TD get more help'.format(
                    self._file_path
                    ),
                status=gui_core.GuiDialog.ValidationStatus.Error,
                #
                ok_label='Close',
                #
                no_visible=False, cancel_visible=False,
                use_exec=False
            )


class AbsPnlRenderSubmitterForShot(AbsPnlSubmitterForRenderBase):
    def __init__(self, hook_option=None, *args, **kwargs):
        super(AbsPnlRenderSubmitterForShot, self).__init__(hook_option, *args, **kwargs)

    def _set_prx_node_effect_(self):
        # self._schemes_prx_node.set(
        #     'save', self.set_scheme_save
        # )
        self._schemes_prx_node.connect_input_changed_to(
            'variables', self.set_combinations_load_from_scheme
        )

        self._schemes_prx_node.connect_input_changed_to(
            'settings', self.set_settings_load_from_scheme
        )

        self._options_prx_node.set(
            'refresh', self.set_current_refresh
        )

        self._settings_prx_node.get_port('td').set_expanded(
            False
        )

        self._settings_prx_node.set(
            'submit', self.set_submit
        )

        collapse_dict = {
            'usd': self._usd_prx_node,
            'variables': self._variables_prx_node,
            'settings': self._settings_prx_node,
        }

        for i_k, i_v in collapse_dict.items():
            i_c = self._hook_build_configure.get(
                'node_collapse.{}'.format(i_k)
            ) or []
            if i_c:
                for i in i_c:
                    i_v.get_port(
                        i.replace('/', '.')
                    ).set_expanded(False)

    def _set_gui_rsv_task_unit_show_deferred_(self, prx_item_widget, variants):
        hook_options = []
        pixmaps = []
        #
        variable_name = '.'.join(variants.values())
        # print variable_name

        movie_file_path = self._render_movie_file_rsv_unit.get_result(
            version='latest',
            variants_extend=variants
        )
        if movie_file_path:
            rsv_properties = self._render_movie_file_rsv_unit.generate_properties_by_result(
                movie_file_path
            )
            version = rsv_properties.get('version')
            variants['version'] = version
            variants['update'] = bsc_core.TimePrettifyMtd.to_prettify_by_timestamp(
                bsc_storage.StgFileOpt(
                    movie_file_path
                ).get_modify_timestamp(),
                language=1
            )
            #
            image_file_path, image_sub_process_cmds = bsc_storage.VdoFileOpt(movie_file_path).generate_thumbnail_create_args()
            prx_item_widget.set_image(image_file_path)
            prx_item_widget.set_movie_enable(True)
            #
            session, execute_fnc = ssn_commands.get_option_hook_args(
                bsc_core.ArgDictStringOpt(
                    dict(
                        option_hook_key='actions/movie-open',
                        file=movie_file_path,
                        gui_group_name='movie',
                        gui_name='open movie'
                    )
                ).to_string()
            )
            #
            prx_item_widget.connect_press_dbl_clicked_to(
                execute_fnc
            )
            #
            hook_options.extend(
                [
                    bsc_core.ArgDictStringOpt(
                        dict(
                            option_hook_key='actions/movie-open',
                            file=movie_file_path,
                            gui_group_name='movie',
                            gui_name='open movie'
                        )
                    ).to_string(),
                    bsc_core.ArgDictStringOpt(
                        dict(
                            option_hook_key='actions/file-directory-open',
                            file=movie_file_path,
                            gui_group_name='movie',
                            gui_name='open movie directory'
                        )
                    ).to_string()
                ]
            )
            if image_sub_process_cmds is not None:
                prx_item_widget.set_image_show_args(image_file_path, image_sub_process_cmds)
        else:
            prx_item_widget.set_image(
                gui_core.GuiIcon.get('image_loading_failed')
            )

        for i_rsv_unit in self._check_rsv_units:
            i_file_path = i_rsv_unit.get_result(version='latest')
            if i_file_path:
                i_rsv_properties = i_rsv_unit.generate_properties_by_result(i_file_path)
                i_rsv_unit_file = gnl_dcc_objects.StgFile(i_file_path)
                i_pixmap = gui_qt_core.GuiQtPixmap.get_by_file_ext_with_tag(
                    i_rsv_unit_file.ext,
                    tag=i_rsv_properties.get('workspace'),
                    frame_size=self.ITEM_ICON_SIZE
                )
                pixmaps.append(i_pixmap)

                hook_options.append(
                    bsc_core.ArgDictStringOpt(
                        dict(
                            option_hook_key='actions/file-directory-open',
                            file=i_file_path,
                            gui_parent='Extend',
                            gui_group_name='usd',
                            gui_name='open "{}" directory'.format(i_rsv_unit.get('keyword'))
                        )
                    ).to_string()
                )

        menu_content = ssn_commands.get_menu_content_by_hook_options(hook_options)
        prx_item_widget.set_menu_content(menu_content)

        prx_item_widget.set_name_dict(variants)
        prx_item_widget.set_icons_by_pixmap(pixmaps)
        r, g, b = bsc_core.RawTextOpt(variable_name).to_rgb()
        prx_item_widget.set_name_frame_background_color((r, g, b, 127))

        prx_item_widget.set_tool_tip(
            '\n'.join(['{} = {}'.format(k, v) for k, v in variants.items()])
        )

        prx_item_widget.refresh_widget_force()

    def set_all_refresh(self):
        if self._file_path:
            self._file_path = bsc_storage.StgPathMapper.map_to_current(self._file_path)
            self._resolver = rsv_core.RsvBase.generate_root()
            self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(self._file_path)
            if self._rsv_scene_properties:
                self._rsv_task = self._resolver.get_rsv_task(
                    **self._rsv_scene_properties.value
                )
                self._rsv_entity = self._rsv_task.get_rsv_resource()
                self._render_movie_file_rsv_unit = self._rsv_task.get_rsv_unit(
                    keyword='{branch}-temporary-katana-render-video-mov-file'
                )
                self._component_usd_file_unit = self._rsv_task.get_rsv_unit(
                    keyword='{branch}-component-usd-file'
                )
                self._output_component_usd_file_unit = self._rsv_task.get_rsv_unit(
                    keyword='{branch}-temporary-component-usd-file'
                )
                self._check_rsv_units = [
                    self._component_usd_file_unit,
                    self._output_component_usd_file_unit
                ]
                #
                self._stg_entity_query = self._stg_connector.get_stg_resource_query(
                    **self._rsv_entity.properties.value
                )
                if self._stg_entity_query:
                    self._start_frame, self._end_frame = (
                        self._stg_entity_query.get('sg_cut_in'), self._stg_entity_query.get('sg_cut_out')
                    )
                #
                self.set_current_refresh()

                self.set_settings_refresh()

    def set_current_refresh(self):
        methods = [
            self.set_options_refresh,
            self.set_usd_refresh,
            self.set_renderers_refresh,
            self.set_combinations_refresh,
        ]
        with bsc_log.LogProcessContext.create(maximum=len(methods), label='execute refresh method') as g_p:
            for i in methods:
                g_p.do_update()
                result = i()
                if result is False:
                    break
        #
        self.set_combinations_load_from_scheme()
        self.set_settings_load_from_scheme()

    # combinations
    def set_combinations_refresh(self):
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_src_items_refresh(expand_depth=1)
        self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter()
        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def set_combinations_load_from_scheme(self):
        scheme = self._schemes_prx_node.get('variables')
        dic = self._hook_build_configure.get(
            'scheme.variables.{}'.format(scheme)
        )
        if dic:
            self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_by_dict(
                dic
            )

    def get_frames(self):
        if self._start_frame != self._end_frame:
            return '{}-{}'.format(self._start_frame, self._end_frame)
        return self._start_frame

    def get_single_frame(self):
        return self._start_frame

    # options
    @gui_prx_core.GuiProxyModifier.window_proxy_waiting
    def set_options_refresh(self):
        import lxusd.rsv.objects as usd_rsv_objects

        #
        self._options_prx_node.set(
            'task', self._rsv_task.path
        )
        branch = self._rsv_task.get('branch')
        step = self._rsv_task.get('step')
        if step in ['rlo', 'ani', 'flo']:
            self._schemes_prx_node.set(
                'variables', 'animation'
            )
            self._schemes_prx_node.set(
                'settings', 'animation-default'
            )
            key = 'animation'
            cache_workspace = 'output'
        elif step in ['cfx']:
            self._schemes_prx_node.set(
                'variables', 'character_effect'
            )
            self._schemes_prx_node.set(
                'settings', 'character_effect-default'
            )
            key = 'character_effect'
            cache_workspace = 'custom'
        elif step in ['efx']:
            self._schemes_prx_node.set(
                'variables', 'effect'
            )
            self._schemes_prx_node.set(
                'settings', 'effect-default'
            )
            key = 'effect'
            cache_workspace = 'custom'
        else:
            raise RuntimeError()
        #
        application = self._rsv_scene_properties.get('application')
        self._work_keyword = '{}-work-{}-scene-src-file'.format(
            branch, application
        )
        self._output_keyword = '{}-output-{}-scene-src-file'.format(
            branch, application
        )
        choice_scheme = 'shot-{}-{}-{}'.format(
            key, application, cache_workspace
        )
        self._options_prx_node.set('choice_scheme', choice_scheme)

        self._work_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=self._work_keyword)
        self._output_scene_file_rsv_unit = self._rsv_task.get_rsv_unit(keyword=self._output_keyword)
        #
        self._set_options_add_rsv_versions_()

        self._rsv_entity_set_usd_creator = usd_rsv_objects.RsvUsdShotSetCreator(self._rsv_entity)

    def _set_options_add_rsv_versions_(self):
        def post_fnc_():
            pass

        def cache_fnc_():
            return self._work_scene_file_rsv_unit.get_rsv_versions()

        def build_fnc_(rsv_versions_):
            self._options_prx_node.set('version', rsv_versions_)

        if self._qt_thread_enable is True:
            t = gui_qt_core.QtBuildThread(self.widget)
            t.set_cache_fnc(
                cache_fnc_
            )
            t.cache_value_accepted.connect(build_fnc_)
            t.run_finished.connect(post_fnc_)
            #
            t.start()
        else:
            build_fnc_(cache_fnc_())
            post_fnc_()

    def set_usd_refresh(self):
        if bsc_core.BscSystem.get_is_linux():
            output_component_usd_file_path = self._output_component_usd_file_unit.get_result('latest')
            if output_component_usd_file_path:
                paths = self._rsv_entity_set_usd_creator.get_effect_component_paths(output_component_usd_file_path)
                u = unr_objects.ObjUniverse()
                o_t = u.generate_obj_type('usd', 'effect')
                for i_path in paths:
                    o_t.create_obj(i_path)
                #
                self._usd_prx_node.set(
                    'components.effect', u.get_obj_type('effect').get_objs()
                )

    def set_settings_refresh(self):
        if self._stg_entity_query is not None:
            self._start_frame, self._end_frame = (
                self._stg_entity_query.get('sg_cut_in'), self._stg_entity_query.get('sg_cut_out')
            )
            frames = '{}-{}'.format(self._start_frame, self._end_frame)
            self._settings_prx_node.set(
                'render.frames', frames
            )
            self._settings_prx_node.set_default(
                'render.frames', frames
            )

        if bsc_core.EnvExtraMtd.get_is_td_enable() is True:
            self._settings_prx_node.set(
                'td.test_scheme', 'td_enable'
            )

    def set_settings_load_from_scheme(self):
        scheme = self._schemes_prx_node.get('settings')

        dic = self._hook_build_configure.get(
            'scheme.settings.{}'.format(scheme)
        )
        self._settings_prx_node.set_reset()
        if dic:
            for k, v in dic.items():
                if isinstance(v, dict):
                    if 'expression' in v:
                        value = None
                        e = 'value{}'.format(v['expression'])
                        exec e
                        self._settings_prx_node.set(
                            k.replace('/', '.'), value
                        )
                else:
                    self._settings_prx_node.set(
                        k.replace('/', '.'), v
                    )

    @gui_prx_core.GuiProxyModifier.window_proxy_waiting
    def set_renderers_refresh(self):
        def set_thread_create_fnc_(prx_item_, variants_):
            prx_item_.set_show_build_fnc(
                lambda *args, **kwargs: self._set_gui_rsv_task_unit_show_deferred_(
                    prx_item_, variants_
                )
            )

        #
        self._rsv_renderer_list_view.set_clear()
        self._prx_dcc_obj_tree_view_tag_filter_opt.restore_all()
        #
        self._variable_variants_dic = self._hook_build_configure.get('variables.character')
        self._variable_keys = self._hook_build_configure.get_key_names_at(
            'variables.character'
        )
        combinations = bsc_core.RawVariablesMtd.get_all_combinations(
            self._variable_variants_dic
        )
        for i_seq, i_variants in enumerate(combinations):
            # print i_seq, i_variants
            i_prx_item = self._rsv_renderer_list_view.create_item_widget()
            set_thread_create_fnc_(i_prx_item, i_variants)
            for j_key in self._variable_keys:
                self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                    '{}.{}'.format(j_key, i_variants[j_key]), i_prx_item
                )

        # self._prx_dcc_obj_tree_view_tag_filter_opt.set_filter_statistic()

    def set_scheme_save(self):
        pass

    def _get_usd_dict_(self):
        c = bsc_content.Content(value={})
        c.set('usd_effect_components', [i.name for i in self._usd_prx_node.get('components.effect')])
        return c.get_value()

    def _get_settings_dict_(self):
        c = bsc_content.Content(value={})
        #
        c.set('render_look', self._settings_prx_node.get('render.look'))
        frames = self._settings_prx_node.get('render.frames')
        c.set('render_frames', frames)
        c.set('render_frame_step', int(self._settings_prx_node.get('render.frame_step')))
        c.set('render_motion_enable', int(self._settings_prx_node.get('render.motion_enable')))
        c.set('render_instance_enable', int(self._settings_prx_node.get('render.instance_enable')))
        c.set('render_bokeh_enable', int(self._settings_prx_node.get('render.bokeh_enable')))
        c.set('render_background_enable', int(self._settings_prx_node.get('render.background_enable')))
        c.set('render_chunk', self._settings_prx_node.get('render.chunk'))
        c.set('render_arnold_aa_sample', self._settings_prx_node.get('render.arnold.aa_sample'))

        c.set('cache_workspace', self._settings_prx_node.get('cache.workspace'))
        c.set('cache_cfx_scheme', self._settings_prx_node.get('cache.xiaov'))

        c.set('user_upload_shotgun_enable', int(self._settings_prx_node.get('user.upload_shotgun_enable')))
        c.set('user_tech_review_enable', int(self._settings_prx_node.get('user.tech_review_enable')))
        c.set('user_description', self._settings_prx_node.get('user.description'))

        c.set('cache_frames', frames)

        return c.value

    def _get_hook_option_dic_(self):
        dic = {}
        rsv_task = self._rsv_task
        if rsv_task is not None:
            dic['file'] = self._file_path
            #
            rsv_shot = self._options_prx_node.get(
                'shot'
            )
            if rsv_shot:
                dic['shot'] = rsv_shot.name
            #
            dic['choice_scheme'] = self._options_prx_node.get('choice_scheme')
            #
            dic.update(self._get_settings_dict_())
            dic.update(self._get_usd_dict_())

            td_test_scheme = self._settings_prx_node.get(
                'td.test_scheme'
            )
            if td_test_scheme == 'auto':
                dic['rez_beta'] = self._rez_beta
            elif td_test_scheme == 'td_enable':
                dic['td_enable'] = True
            elif td_test_scheme == 'rez_beta':
                dic['rez_beta'] = True
        return dic

    def get_file_is_changed(self):
        file_path_src = self._file_path
        file_path_tgt = self._output_scene_file_rsv_unit.get_result('latest')
        # return not bsc_storage.StgFileOpt(file_path_src).get_timestamp_is_same_to(file_path_tgt)
        return True

    @gui_prx_core.GuiProxyModifier.window_proxy_waiting
    def set_submit(self):
        hook_option_dic = self._get_hook_option_dic_()
        if hook_option_dic:
            if self.get_file_is_changed() is True:
                hook_option_dic['user'] = bsc_core.BscSystem.get_user_name()
                hook_option_dic['option_hook_key'] = 'rsv-task-batchers/shot/tmp-render-submit'
                #
                option_opt = bsc_core.ArgDictStringOpt(hook_option_dic)
                #
                ssn_commands.execute_option_hook_by_deadline(
                    option=option_opt.to_string()
                )
                #
                gui_core.GuiDialog.create(
                    self._hook_gui_configure.get('name'),
                    content='{} is submit completed'.format(self._file_path),
                    status=gui_core.GuiDialog.ValidationStatus.Correct,
                    #
                    ok_label='Close',
                    #
                    no_visible=False, cancel_visible=False,
                    use_exec=False
                )
            else:
                gui_core.GuiDialog.create(
                    self._hook_gui_configure.get('name'),
                    content='file="{}" is already submitted or scene changed is not be save'.format(self._file_path),
                    status=gui_core.GuiDialog.ValidationStatus.Error,
                    #
                    ok_label='Close',
                    #
                    no_visible=False, cancel_visible=False,
                    use_exec=False
                )

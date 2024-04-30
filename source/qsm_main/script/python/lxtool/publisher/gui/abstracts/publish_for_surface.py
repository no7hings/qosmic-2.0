# coding:utf-8
import collections

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.proxy.widgets as prx_widgets

import lxgeneral.dcc.objects as gnl_dcc_objects

import lxgui.proxy.scripts as gui_prx_scripts

import lxresolver.core as rsv_core

import lxsession.commands as ssn_commands

import lxgui.core as gui_core

import lxtool.publisher.core as pbs_core

import lxsession.core as ssn_core


class _PublishOptForSurface(object):
    def __init__(self, window, session, scene_file_path, validation_info_file, rsv_task, rsv_scene_properties, options):
        self._window = window
        self._session = session
        self._scene_file_path = scene_file_path
        self._validation_info_file = validation_info_file
        self._rsv_task = rsv_task
        self._rsv_scene_properties = rsv_scene_properties
        self._options = options

    def collection_review_fnc(self):
        self._review_mov_file_path = None
        #
        file_paths = self._options['review']
        if file_paths:
            movie_file_path = pbs_core.VideoComp.comp_movie(
                file_paths
            )
            self._review_mov_file_path = movie_file_path

    def farm_process_fnc(self):
        version_type = self._options['version_type']
        scene_file_path = self._scene_file_path

        user = bsc_core.SysBaseMtd.get_user_name()

        extra_data = dict(
            user=user,
            #
            version_type=self._options['version_type'],
            version_status='pub',
            #
            notice=self._options['notice'],
            description=self._options['description'],
        )

        extra_key = ssn_core.SsnHookFileMtd.set_extra_data_save(extra_data)

        application = self._rsv_scene_properties.get('application')
        if application == 'katana':
            choice_scheme = 'asset-katana-publish'
        elif application == 'maya':
            choice_scheme = 'asset-maya-publish'
        else:
            raise RuntimeError()

        option_opt = bsc_core.ArgDictStringOpt(
            option=dict(
                option_hook_key='rsv-task-batchers/asset/gen-surface-export',
                #
                file=scene_file_path,
                #
                extra_key=extra_key,
                #
                choice_scheme=choice_scheme,
                #
                version_type=version_type,
                movie_file=self._review_mov_file_path,
                #
                validation_info_file=self._validation_info_file,
                #
                with_workspace_texture_lock=self._options['process.settings.with_workspace_texture_lock'],
                #
                user=user,
                #
                td_enable=self._session.get_is_td_enable(),
                rez_beta=self._session.get_is_beta_enable(),
                #
                localhost_enable=self._options['process.deadline.scheme'] == 'localhost'
            )
        )

        if bsc_core.SysApplicationMtd.get_is_katana():
            import lxkatana.core as ktn_core
            option_opt.set('katana_version', ktn_core.KtnUtil.get_katana_version())

        ssn_commands.execute_option_hook_by_deadline(
            option=option_opt.to_string()
        )

    @bsc_core.MdfBaseMtd.run_with_exception_catch
    def execute(self):
        fncs = [
            self.collection_review_fnc,
            #
            self.farm_process_fnc,
        ]
        with self._window.gui_progressing(maximum=len(fncs), label='execute publish process') as g_p:
            for i_fnc in fncs:
                g_p.do_update()
                i_fnc()
        #
        self._window.show_message(
            'publish process is complected',
            self._window.ValidationStatus.Correct
        )


class AbsValidatorOpt(object):
    DCC_NAMESPACE = None
    DCC_NODE_CLS = None
    DCC_COMPONENT_CLS = None
    DCC_SELECTION_CLS = None
    DCC_PATHSEP = None

    def __init__(self, filter_tree_view, result_tree_view):
        self._prx_tree_view_for_filter = filter_tree_view
        self._result_tree_view = result_tree_view
        self._item_dict = self._result_tree_view._item_dict

        self._result_tree_view.connect_item_select_changed_to(
            self.set_select
        )

        self._filter_opt = gui_prx_scripts.GuiPrxScpForTreeTagFilter(
            prx_tree_view_src=self._prx_tree_view_for_filter,
            prx_tree_view_tgt=self._result_tree_view,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )

    def set_select(self):
        gui_prx_scripts.GuiPrxScpForTreeSelection.select_fnc(
            prx_tree_view=self._result_tree_view,
            dcc_selection_cls=self.DCC_SELECTION_CLS,
            dcc_namespace=self.DCC_NAMESPACE
        )

    def set_results_at(self, rsv_scene_properties, results):
        file_path = rsv_scene_properties.get('extra.file')
        check_results = results['check_results']
        scene_prx_item = self._get_scene_(file_path)
        scene_prx_item.clear_children()
        self._filter_opt.restore_all()
        scene_prx_item._child_dict = {}
        if not check_results:
            scene_prx_item.set_status(
                gui_core.GuiDialog.ValidationStatus.Correct
            )
            return True
        #
        self._set_sub_check_results_build_at_(
            scene_prx_item, rsv_scene_properties, check_results
        )
        #
        self._result_tree_view.expand_items_by_depth(1)

    def _set_sub_check_results_build_at_(self, scene_prx_item, rsv_scene_properties, results):
        with bsc_log.LogProcessContext.create(maximum=len(results), label='gui-add for check result') as g_p:
            for i_result in results:
                g_p.do_update()
                #
                i_type = i_result['type']
                i_dcc_path = i_result['node']
                i_group_name = i_result['group']
                i_status = i_result['status']
                if i_status == 'warning':
                    i_validation_status = gui_core.GuiDialog.ValidationStatus.Warning
                elif i_status == 'error':
                    i_validation_status = gui_core.GuiDialog.ValidationStatus.Error
                else:
                    raise RuntimeError()

                i_description = i_result['description']
                #
                self._set_status_update_(scene_prx_item, i_status, i_validation_status)
                #
                i_group_prx_item = self._get_group_(scene_prx_item, i_group_name)
                self._set_status_update_(i_group_prx_item, i_status, i_validation_status)
                i_node_prx_item = self._get_node_(
                    scene_prx_item,
                    rsv_scene_properties,
                    i_group_prx_item,
                    i_dcc_path,
                    i_description,
                    i_validation_status
                )

                i_filter_key = '.'.join(
                    [
                        bsc_core.SPathMtd.set_quote_to(i_group_name),
                        bsc_core.SPathMtd.set_quote_to(i_description)
                    ]
                )

                self._filter_opt.register(
                    i_node_prx_item, [i_filter_key]
                )
                if i_type == 'file':
                    j_elements = i_result['elements']
                    for j_file_path in j_elements:
                        j_file_prx_item = self._get_file_(
                            scene_prx_item, i_node_prx_item,
                            j_file_path, i_description, i_validation_status
                        )
                        self._filter_opt.register(
                            j_file_prx_item, [i_filter_key]
                        )
                elif i_type == 'directory':
                    j_elements = i_result['elements']
                    for j_directory_path in j_elements:
                        j_file_prx_item = self._get_directory_(
                            scene_prx_item, i_node_prx_item,
                            j_directory_path, i_description, i_validation_status
                        )
                        self._filter_opt.register(
                            j_file_prx_item, [i_filter_key]
                        )
                elif i_type == 'component':
                    j_elements = i_result['elements']
                    for j_dcc_path in j_elements:
                        j_comp_prx_item = self._get_component_(
                            scene_prx_item, i_node_prx_item,
                            j_dcc_path, i_description, i_validation_status
                        )
                        self._filter_opt.register(
                            j_comp_prx_item, [i_filter_key]
                        )

    def _set_status_update_(self, prx_item, status, validation_status):
        name = prx_item._validation_name
        result = prx_item._validation_result
        #
        pre_validation_status = prx_item.get_status()
        if validation_status > pre_validation_status:
            prx_item.set_status(validation_status)

        if status in result:
            count = result[status]
        else:
            count = 0
            result[status] = 0

        count += 1

        result[status] = count
        #
        d = ' '.join(['[ {} x {} ]'.format(k, v) for k, v in result.items() if v])
        #
        prx_item.set_name(
            '{} {}'.format(name, d)
        )

    def _get_scene_(self, file_path):
        if file_path in self._item_dict:
            return self._item_dict[file_path]
        #
        stg_file = gnl_dcc_objects.StgFile(file_path)
        name = stg_file.get_path_prettify_()
        prx_item = self._result_tree_view.create_item(
            name=name,
            icon=stg_file.icon,
            tool_tip=file_path,
        )
        prx_item.set_expanded(True)
        prx_item.set_checked(False)

        prx_item._validation_name = name
        prx_item._validation_result = collections.OrderedDict(
            [
                ('error', 0),
                ('warning', 0)
            ]
        )

        prx_item._child_dict = {}
        self._item_dict[file_path] = prx_item
        return prx_item

    def _get_group_(self, scene_prx_item, group_name):
        if group_name in scene_prx_item._child_dict:
            prx_item = scene_prx_item._child_dict[group_name]
            return prx_item

        prx_item = scene_prx_item.add_child(
            name=group_name,
            icon=gui_core.GuiIcon.get('application/python'),
        )
        prx_item.set_checked(False)
        #
        prx_item._validation_name = group_name
        prx_item._validation_result = collections.OrderedDict(
            [
                ('error', 0),
                ('warning', 0)
            ]
        )
        #
        scene_prx_item._child_dict[group_name] = prx_item
        return prx_item

    def _get_node_(self, scene_prx_item, rsv_scene_properties, group_prx_item, dcc_path, description, status):
        dcc_path_dag_opt = bsc_core.PthNodeOpt(dcc_path)
        pathsep = dcc_path_dag_opt.get_pathsep()
        pathsep_src = rsv_scene_properties.get('dcc.pathsep')
        if pathsep == pathsep_src:
            if pathsep != self.DCC_PATHSEP:
                dcc_path = dcc_path_dag_opt.translate_to(self.DCC_PATHSEP).to_string()
        #
        dcc_obj = self.DCC_NODE_CLS(dcc_path)
        prx_item = group_prx_item.add_child(
            name=[dcc_obj.name, description],
            icon=dcc_obj.icon,
            tool_tip=dcc_obj.path,
        )
        prx_item.set_checked(False)
        prx_item.set_status(status)
        prx_item.set_gui_dcc_obj(
            dcc_obj, self.DCC_NAMESPACE
        )
        return prx_item

    def _get_component_(self, scene_prx_item, node_prx_item, dcc_path, description, status):
        dcc_path_dag_opt = bsc_core.PthNodeOpt(dcc_path)
        pathsep = dcc_path_dag_opt.get_pathsep()
        if pathsep != self.DCC_PATHSEP:
            dcc_path = dcc_path_dag_opt.translate_to(self.DCC_PATHSEP).to_string()
        #
        dcc_obj = self.DCC_COMPONENT_CLS(dcc_path)
        prx_item = node_prx_item.add_child(
            name=[dcc_obj.name, description],
            icon=dcc_obj.icon,
            tool_tip=dcc_obj.path,
        )
        prx_item.set_checked(False)
        prx_item.set_status(status)
        prx_item.set_gui_dcc_obj(
            dcc_obj, self.DCC_NAMESPACE
        )
        return prx_item

    def _get_file_(self, scene_prx_item, node_prx_item, file_path, description, status):
        stg_file = gnl_dcc_objects.StgFile(file_path)
        prx_item = node_prx_item.add_child(
            name=[stg_file.get_path_prettify_(maximum=32), description],
            icon=stg_file.icon,
            menu=stg_file.get_gui_menu_raw(),
            tool_tip=stg_file.path
        )
        prx_item.set_status(status)
        prx_item.set_checked(False)
        return prx_item

    def _get_directory_(self, scene_prx_item, node_prx_item, directory_path, description, status):
        stg_directory = gnl_dcc_objects.StgDirectory(directory_path)
        prx_item = node_prx_item.add_child(
            name=[stg_directory.get_path_prettify_(maximum=32), description],
            icon=stg_directory.icon,
            menu=stg_directory.get_gui_menu_raw(),
            tool_tip=stg_directory.path
        )
        prx_item.set_status(status)
        prx_item.set_checked(False)
        return prx_item


class AbsPnlPublisherForSurface(prx_widgets.PrxSessionWindow):
    DCC_VALIDATOR_OPT_CLS = None

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlPublisherForSurface, self).__init__(session, *args, **kwargs)

    def restore_variants(self):
        self._scene_file_path = None
        self._rsv_scene_properties = None
        self._rsv_task = None
        self._notice_user_names = []

    def gui_setup_window(self):
        self._check_key_map = {
            'validation.ignore_shotgun_check': 'with_shotgun_check',
            #
            'validation.ignore_scene_check': 'with_scene_check',
            #
            'validation.ignore_geometry_check': 'with_geometry_check',
            'validation.ignore_geometry_topology_check': 'with_geometry_topology_check',
            #
            'validation.ignore_look_check': 'with_look_check',
            #
            'validation.ignore_texture_check': 'with_texture_check',
            'validation.ignore_texture_workspace_check': 'with_texture_workspace_check',
        }
        self.set_main_style_mode(1)
        self._tab_view = prx_widgets.PrxTabView()
        self.add_widget(self._tab_view)

        sa_0 = prx_widgets.PrxVScrollArea()
        self._tab_view.add_widget(
            sa_0,
            name='Validation',
            icon_name_text='Validation',
        )

        sa_1 = prx_widgets.PrxVScrollArea()
        self._tab_view.add_widget(
            sa_1,
            name='Configure',
            icon_name_text='Configure',
        )

        ep_0 = prx_widgets.PrxHToolGroup()
        sa_0.add_widget(ep_0)
        ep_0.set_expanded(True)
        ep_0.set_name('check results')

        h_s_0 = prx_widgets.PrxHSplitter()
        ep_0.add_widget(h_s_0)

        self._prx_tree_view_for_filter = prx_widgets.PrxTreeView()
        h_s_0.add_widget(self._prx_tree_view_for_filter)
        self._prx_tree_view_for_filter.create_header_view(
            [('name', 3)],
            self.get_definition_window_size()[0]*(1.0/3.0)-32
        )
        #
        self._result_tree_view = prx_widgets.PrxTreeView()
        h_s_0.add_widget(self._result_tree_view)
        self._result_tree_view.create_header_view(
            [('name', 4), ('description', 2)],
            self.get_definition_window_size()[0]*(2.0/3.0)-32
        )
        h_s_0.set_fixed_size_at(0, 240)
        h_s_0.swap_contract_left_or_top_at(0)

        self._tree_view_opt = self.DCC_VALIDATOR_OPT_CLS(
            self._prx_tree_view_for_filter, self._result_tree_view
        )

        self._cfg_options_prx_node = prx_widgets.PrxNode('options')
        sa_1.add_widget(self._cfg_options_prx_node)
        self._cfg_options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.validation_options'),
        )

        self._cfg_options_prx_node.set(
            'resolver.load', self.set_refresh_all
        )

        self._set_collapse_update_(
            collapse_dict={
                'options': self._cfg_options_prx_node,
            }
        )

        self._validation_button = prx_widgets.PrxPressButton()
        self._validation_button.set_name('validation')
        self.add_button(
            self._validation_button
        )
        self._validation_button.connect_press_clicked_to(self.execute_validation)

        self._next_button = prx_widgets.PrxPressButton()
        self._next_button.set_name('next')
        self.add_button(
            self._next_button
        )
        self._next_button.connect_press_clicked_to(self.execute_show_next)

        self._validation_checker = None
        self._validation_check_options = {}
        self._validation_info_file = None

        self._next_button.set_enable(
            False
        )
        self._cfg_options_prx_node.get_port(
            'publish.ignore_validation_error'
        ).connect_input_changed_to(
            self.refresh_next_enable_fnc
        )

        self.set_help_content(
            self._session.configure.get('option.gui.content'),
        )

        self._cfg_options_prx_node.set(
            'validation.ignore_all', self._set_validation_ignore_all_
        )
        self._cfg_options_prx_node.set(
            'validation.ignore_clear', self._set_validation_ignore_clear_
        )
        # publish
        layer_widget = self.create_layer_widget('publish', 'Publish')
        sa_2 = prx_widgets.PrxVScrollArea()
        layer_widget.add_widget(sa_2)
        self._publish_options_prx_node = prx_widgets.PrxNode('options')
        sa_2.add_widget(self._publish_options_prx_node)
        self._publish_options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.publish_options')
        )

        self._publish_tip = prx_widgets.PrxTextBrowser()
        sa_2.add_widget(self._publish_tip)
        self._publish_tip.set_content(
            self._session.configure.get('build.node.publish_content')
        )
        self._publish_tip.set_font_size(12)

        tool_bar = prx_widgets.PrxHToolBar()
        layer_widget.add_widget(tool_bar)
        tool_bar.set_expanded(True)

        self._publish_button = prx_widgets.PrxPressButton()
        tool_bar.add_widget(self._publish_button)
        self._publish_button.set_name('publish')
        self._publish_button.connect_press_clicked_to(
            self.execute_publish
        )

        self.set_refresh_all()

    def _get_publish_is_enable_(self):
        if self._cfg_options_prx_node.get('publish.ignore_validation_error') is True:
            return True
        if self._validation_checker is not None:
            return self._validation_checker.get_is_passed()
        return False

    def _get_validation_info_file_path_(self):
        if self._rsv_scene_properties:
            file_opt = bsc_storage.StgFileOpt(
                self._scene_file_path
            )
            return bsc_storage.StgTmpInfoMtd.get_file_path(
                file_opt.get_path(), 'validation'
            )

    def _get_validation_info_texts_(self):
        list_ = []
        if self._cfg_options_prx_node.get('publish.ignore_validation_error') is True:
            list_.append(
                'validation check ignore: on'
            )
        if self._validation_checker is not None:
            list_.append(
                'validation check run: on'
            )
            list_.append(self._validation_checker.get_info())
            return list_
        return ['validation check run: off']

    def refresh_validation_enable_fnc(self):
        pass

    def refresh_next_enable_fnc(self):
        self._validation_info_file = self._get_validation_info_file_path_()
        if self._validation_info_file is not None:
            info = '\n'.join(map(bsc_core.auto_string, self._get_validation_info_texts_()))
            bsc_storage.StgFileOpt(
                self._validation_info_file
            ).set_write(
                info
            )
            self._next_button.set_enable(
                self._get_publish_is_enable_()
            )

    def set_refresh_all(self):
        contents = []
        application = bsc_core.SysBaseMtd.get_application()
        #
        if bsc_core.SysApplicationMtd.get_is_dcc():
            self._scene_file_path = self._get_dcc_scene_file_path_()
            self._cfg_options_prx_node.set(
                'resolver.scene_file', self._scene_file_path
            )
            self._cfg_options_prx_node.get_port(
                'resolver.scene_file'
            ).set_locked(True)
        else:
            self._scene_file_path = self._cfg_options_prx_node.get(
                'resolver.scene_file'
            )
        #
        r = rsv_core.RsvBase.generate_root()
        #
        self._result_tree_view.set_clear()
        if self._scene_file_path:
            self._tree_view_opt._get_scene_(self._scene_file_path)
            #
            self._rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(self._scene_file_path)
            if self._rsv_scene_properties:
                self._rsv_task = r.get_rsv_task(**self._rsv_scene_properties.value)
            else:
                contents.append(
                    u'scene file "{}" is not available'.format(self._scene_file_path)
                )
        else:
            if application == 'katana':
                contents.append(
                    'open a scene file in dcc and retry'
                )

        if contents:
            gui_core.GuiDialog.create(
                label=self._session.gui_name,
                content=u'\n'.join(contents),
                status=gui_core.GuiDialog.ValidationStatus.Error,
                #
                yes_label='Close', yes_method=self.set_window_close,
                #
                no_visible=False, cancel_visible=False,
                #
                use_exec=False
            )

    def _get_dcc_scene_file_path_(self):
        pass

    def _set_shotgun_version_status_update_(self):
        version_type = self._cfg_options_prx_node.get('shotgun.version.type')
        version_status_mapper = dict(
            daily='rev',
            check='pub',
            downstream='pub'
        )
        version_status = version_status_mapper[version_type]
        self._cfg_options_prx_node.set(
            'shotgun.version.status', version_status
        )

    def _set_validation_ignore_all_(self):
        [self._cfg_options_prx_node.set(k, True) for k, v in self._check_key_map.items()]

    def _set_validation_ignore_clear_(self):
        [self._cfg_options_prx_node.set(k, False) for k, v in self._check_key_map.items()]

    def execute_validation(self):
        if self._rsv_scene_properties:
            self._validation_check_options = {v: not self._cfg_options_prx_node.get(k) for k, v in
                                              self._check_key_map.items()}
            if bsc_core.SysApplicationMtd.get_is_dcc():
                if bsc_core.SysApplicationMtd.get_is_katana():
                    self._set_katana_validation_in_execute_()
                elif bsc_core.SysApplicationMtd.get_is_maya():
                    self._set_maya_validation_in_dcc_()
            else:
                application = self._rsv_scene_properties.get('application')
                if application == 'katana':
                    self._set_katana_validation_execute_by_shell_()
                elif application == 'maya':
                    self._set_maya_validation_execute_by_shell_()

    def _set_gui_validation_check_results_show_(self, session):
        self._validation_checker = session.get_validation_checker()
        self._validation_checker.set_options(
            self._validation_check_options
        )
        #
        self._result_tree_view.set_clear()
        self._tree_view_opt.set_results_at(
            self._rsv_scene_properties,
            self._validation_checker.get_data()
        )
        self.refresh_next_enable_fnc()

    def _set_dcc_validation_execute_(self, option_hook_key):
        s = ssn_commands.execute_option_hook(
            bsc_core.ArgDictStringOpt(
                option=dict(
                    option_hook_key=option_hook_key,
                    file=self._scene_file_path,
                    #
                    **self._validation_check_options
                )
            ).to_string()
        )

        self._set_gui_validation_check_results_show_(s)

    def _set_dcc_validation_execute_by_shell_(self, option_hook_key):
        def completed_fnc_(*args):
            self._set_gui_validation_check_results_show_(s)

        def finished_fnc_(*args):
            pass

        #
        s = ssn_commands.get_option_hook_session(
            bsc_core.ArgDictStringOpt(
                option=dict(
                    option_hook_key=option_hook_key,
                    file=self._scene_file_path,
                    #
                    **self._validation_check_options
                )
            ).to_string()
        )
        cmd = s.get_shell_script_command()
        #
        q_c_s = gui_core.GuiMonitorForCommand.set_create(
            'Validation for {}'.format(self._rsv_task),
            cmd,
            parent=self.widget
        )
        #
        q_c_s.completed.connect(completed_fnc_)
        q_c_s.finished.connect(finished_fnc_)

    def _set_katana_validation_in_execute_(self):
        self._set_dcc_validation_execute_(
            'rsv-task-methods/asset/katana/gen-surface-validation'
        )

    def _set_katana_validation_execute_by_shell_(self):
        self._set_dcc_validation_execute_by_shell_(
            'rsv-task-methods/asset/katana/gen-surface-validation'
        )

    def _set_maya_validation_in_dcc_(self):
        self._set_dcc_validation_execute_(
            'rsv-task-methods/asset/maya/gen-surface-validation'
        )

    def _set_maya_validation_execute_by_shell_(self):
        self._set_dcc_validation_execute_by_shell_(
            'rsv-task-methods/asset/maya/gen-surface-validation'
        )

    def refresh_publish_options(self):
        pass

    def refresh_publish_notice(self):
        def post_fnc_():
            pass

        def cache_fnc_():
            t_o = bsc_shotgun.StgTaskOpt(c.to_query(stg_task))
            notice_stg_users = t_o.get_notice_stg_users()
            return list(set([c.to_query(i).get('name').decode('utf-8') for i in notice_stg_users]))

        def built_fnc_(user_names):
            self._publish_options_prx_node.set(
                'notice', user_names
            )

        import lxbasic.shotgun as bsc_shotgun

        c = bsc_shotgun.StgConnector()

        p = self._publish_options_prx_node.get_port('notice')
        p.set_clear()
        p.set_shotgun_entity_kwargs(
            dict(
                entity_type='HumanUser',
                filters=[
                    ['sg_studio', 'is', 'CG'],
                    ['sg_status_list', 'is', 'act']
                ],
                fields=['name', 'email', 'sg_nickname']
            ),
            name_field='name',
            keyword_filter_fields=['name', 'email', 'sg_nickname'],
            tag_filter_fields=['department']
        )

        stg_task = c.get_stg_task(**self._rsv_task.properties.get_value())

        p.run_as_thread(
            cache_fnc_, built_fnc_, post_fnc_
        )

    def execute_show_next(self):
        if self._next_button.get_is_enable() is True:
            self.switch_current_layer_to('publish')
            self.get_layer_widget('publish').set_name(
                'publish for [{project}.{resource}.{task}]'.format(
                    **self._rsv_scene_properties.get_value()
                )
            )
            self.refresh_publish_options()
            self.refresh_publish_notice()

    def execute_publish(self):
        _PublishOptForSurface(
            self,
            self._session,
            self._scene_file_path,
            self._validation_info_file,
            self._rsv_task,
            self._rsv_scene_properties,
            self._publish_options_prx_node.to_dict()
        ).execute()

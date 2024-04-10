# coding:utf-8
import six

import functools

import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxuniverse.objects as unr_objects

import lxgui.proxy.widgets as prx_widgets

import lxgui.core as gui_core

import lxgui.qt.core as gui_qt_core

import lxgui.proxy.scripts as gui_prx_scripts
# session
import lxsession.core as ssn_core

import lxsession.objects as ssn_objects
# resolver
import lxresolver.core as rsv_core


class AbsPnlAssetLineup(prx_widgets.PrxSessionWindow):
    DCC_NAMESPACE = 'resolver'

    def __init__(self, *args, **kwargs):
        super(AbsPnlAssetLineup, self).__init__(*args, **kwargs)

    def restore_variants(self):
        self._session_dict = {}
        self._image_dict = {}

    def set_all_setup(self):
        self._option_hook_configure = self._session.configure
        self._hook_gui_configure = self._session.configure.get_as_content('option.gui')
        self._hook_resolver_configure = self._session.configure.get_as_content('resolver')
        self._hook_build_configure = self._session.configure.get_as_content('build')
        self._set_tool_panel_setup_()

    def _set_tool_panel_setup_(self):
        h_s = prx_widgets.PrxHSplitter()
        self.add_widget(h_s)
        v_s = prx_widgets.PrxVSplitter()
        h_s.add_widget(v_s)
        self._rsv_obj_tree_view_0 = prx_widgets.PrxTreeView()
        v_s.add_widget(self._rsv_obj_tree_view_0)

        s = prx_widgets.PrxVScrollArea()
        v_s.add_widget(s)
        self._options_prx_node = prx_widgets.PrxNode('options')
        s.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._hook_build_configure.get('node.options')
        )

        self._options_prx_node.set('refresh', self.set_refresh_all)
        self._options_prx_node.set('graph.reload', self._set_graph_reload_)
        self._options_prx_node.set('output.save', self._set_graph_save_)

        v_s.set_stretches([1, 1])

        self._rsv_obj_tree_view_0.set_header_view_create(
            [('name', 3)],
            self.get_definition_window_size()[0]*(1.0/4.0)-24
        )
        self._resolver = rsv_core.RsvBase.generate_root()
        # self._rsv_obj_tree_view_0.set_selection_use_single()
        self._prx_dcc_obj_tree_view_add_opt = gui_prx_scripts.GuiPrxScpForResolver(
            self._resolver,
            prx_tree_view=self._rsv_obj_tree_view_0,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem,
        )
        #
        self._node_graph = prx_widgets.PrxNGImageGraph()
        h_s.add_widget(self._node_graph)

        h_s.set_stretches([1, 3])

        menu = self.create_menu(
            'Tool(s)'
        )
        menu.set_menu_data(
            [
                ('Save Graph', None, self._set_graph_save_),
            ]
        )

        self.set_refresh_all()

    def set_refresh_all(self):
        self._project = self._options_prx_node.get('project')
        self._rsv_project = self._resolver.get_rsv_project(project=self._project)
        self._rsv_filter = self._hook_resolver_configure.get('filter')

        self._rsv_filter_opt = bsc_core.ArgDictStringOpt(self._rsv_filter)

        self._rsv_project.restore_all_gui_variants()
        self._prx_dcc_obj_tree_view_add_opt.restore()

        self._image_dict = {}

        self._set_gui_rsv_objs_refresh_()

    def _set_gui_rsv_objs_refresh_(self):
        self._set_gui_add_rsv_project_(self._rsv_project)

        self._set_add_rsv_entities_(self._rsv_project)

    def _set_gui_add_rsv_project_(self, rsv_project):
        is_create, prx_item = self._prx_dcc_obj_tree_view_add_opt.gui_add_as_tree(
            rsv_project
        )
        if is_create is True:
            prx_item.set_expanded(True, ancestors=True)

    def _set_add_rsv_entities_(self, rsv_project):
        def post_fnc_():
            self._end_timestamp = bsc_core.SysBaseMtd.get_timestamp()

            bsc_log.Log.trace_method_result(
                'load asset/shot from "{}"'.format(
                    rsv_project.path
                ),
                'count={}, cost-time="{}"'.format(
                    self._count,
                    bsc_core.RawIntegerMtd.second_to_time_prettify(int(self._end_timestamp-self._start_timestamp))
                )
            )

            self._set_graph_reload_()

        self._count = 0
        self._start_timestamp = bsc_core.SysBaseMtd.get_timestamp()
        #
        rsv_tags = rsv_project.get_rsv_resource_groups(**self._rsv_filter_opt.value)
        #
        if self._qt_thread_enable is True:
            ts = gui_qt_core.QtBuildThreadStack(self.widget)
            ts.run_finished.connect(post_fnc_)
            for i_rsv_tag in rsv_tags:
                ts.register(
                    functools.partial(
                        self.__cache_rsv_entities_by_tag_,
                        i_rsv_tag
                    ),
                    self._set_gui_add_rsv_entities_
                )
            ts.set_start()
        else:
            with bsc_log.LogProcessContext.create(maximum=len(rsv_tags), label='gui-add for entity') as g_p:
                for i_rsv_tag in rsv_tags:
                    g_p.do_update()
                    self._set_gui_add_rsv_entities_(
                        self.__cache_rsv_entities_by_tag_(i_rsv_tag)
                    )

    # entities for tag
    def __cache_rsv_entities_by_tag_(self, rsv_tag):
        return rsv_tag.get_rsv_resources(**self._rsv_filter_opt.value)

    def _set_gui_add_rsv_entities_(self, rsv_entities):
        for i_rsv_entity in rsv_entities:
            self._set_gui_add_rsv_entity_(i_rsv_entity)

        self._count += len(rsv_entities)

    def _set_gui_add_rsv_entity_(self, rsv_entity):
        is_create, prx_item = self._prx_dcc_obj_tree_view_add_opt.gui_add_as_tree(
            rsv_entity
        )
        if is_create is True:
            branch = rsv_entity.properties.get('branch')
            if branch == 'asset':
                asset_menu_content = self.get_rsv_asset_menu_content(rsv_entity)
                if asset_menu_content:
                    rsv_entity.set_gui_menu_content(
                        asset_menu_content
                    )

            self._set_gui_add_rsv_unit_(rsv_entity)

    def get_rsv_asset_menu_content(self, rsv_entity):
        hook_keys = self._option_hook_configure.get(
            'actions.asset.hooks'
        ) or []
        return self._get_menu_content_by_hook_keys_(
            self._session_dict, hook_keys, rsv_entity
        )

    def _set_gui_add_rsv_unit_(self, rsv_entity):
        rsv_entity_gui = rsv_entity.get_obj_gui()
        model_rsv_task = rsv_entity.get_rsv_task(
            step='mod', task='modeling'
        )
        if model_rsv_task is not None:
            component_registry_usd_rsv_unit = model_rsv_task.get_rsv_unit(
                keyword='asset-component-registry-usd-file'
            )
            component_registry_usd_file_path = component_registry_usd_rsv_unit.get_result(
                version='latest'
            )
            if component_registry_usd_file_path:
                preview_rsv_unit = model_rsv_task.get_rsv_unit(
                    keyword='asset-temporary-katana-render-video-png-file'
                )
                result = preview_rsv_unit.get_result(
                    version='latest',
                    variants_extend=dict(
                        camera='front',
                        layer='master',
                        light_pass='all',
                        look_pass='plastic',
                        quality='custom'
                    )
                )
                if result is not None:
                    self._image_dict[rsv_entity.path] = result
                    rsv_entity_gui.set_status(
                        rsv_entity_gui.ValidationStatus.Correct
                    )
                else:
                    rsv_entity_gui.set_status(
                        rsv_entity_gui.ValidationStatus.Disable
                    )
            else:
                rsv_entity_gui.set_status(
                    rsv_entity_gui.ValidationStatus.Warning
                )
        else:
            rsv_entity_gui.set_status(
                rsv_entity_gui.ValidationStatus.Error
            )

    def _set_graph_reload_(self):
        self._universe = unr_objects.ObjUniverse()

        self._u_asset_type = self._universe.generate_obj_type('lynxi', 'asset')

        self._u_image_type = self._universe.generate_type(
            self._universe.Category.CONSTANT, self._universe.Type.STRING
        )

        if self._image_dict:
            for k, v in self._image_dict.items():
                i_prx_item = self._rsv_obj_tree_view_0.get_item_by_key(k)
                i_rsv_entity = i_prx_item.get_gui_dcc_obj(namespace=self.DCC_NAMESPACE)
                if i_prx_item.get_is_checked() is True:
                    i_n = self._u_asset_type.create_obj(
                        '/{}'.format(
                            i_rsv_entity.name
                        )
                    )
                    p = i_n.generate_variant_port(
                        self._u_image_type, 'image'
                    )
                    p.set(v)

        self._node_graph.set_clear()
        self._node_graph.set_universe(self._universe)
        self._node_graph.set_node_show()

    @classmethod
    def _get_menu_content_by_hook_keys_(cls, session_dict, hooks, *args, **kwargs):
        content = ctt_core.Dict()
        for i_hook in hooks:
            if isinstance(i_hook, six.string_types):
                i_hook_key = i_hook
                i_hook_option = None
            elif isinstance(i_hook, dict):
                i_hook_key = i_hook.keys()[0]
                i_hook_option = i_hook.values()[0]
            else:
                raise RuntimeError()
            #
            i_args = cls._get_rsv_unit_action_hook_args_(
                session_dict, i_hook_key, *args, **kwargs
            )
            if i_args:
                i_session, i_execute_fnc = i_args
                if i_session.get_is_loadable() is True and i_session.get_is_visible() is True:
                    i_gui_configure = i_session.gui_configure
                    #
                    i_gui_parent_path = '/'
                    #
                    i_gui_name = i_gui_configure.get('name')
                    if i_hook_option:
                        if 'gui_name' in i_hook_option:
                            i_gui_name = i_hook_option.get('gui_name')
                        #
                        if 'gui_parent' in i_hook_option:
                            i_gui_parent_path = i_hook_option['gui_parent']
                    #
                    i_gui_parent_path_opt = bsc_core.PthNodeOpt(i_gui_parent_path)
                    #
                    if i_gui_parent_path_opt.get_is_root():
                        i_gui_path = '/{}'.format(i_gui_name)
                    else:
                        i_gui_path = '{}/{}'.format(i_gui_parent_path, i_gui_name)
                    #
                    i_gui_separator_name = i_gui_configure.get('group_name')
                    if i_gui_separator_name:
                        if i_gui_parent_path_opt.get_is_root():
                            i_gui_separator_path = '/{}'.format(i_gui_separator_name)
                        else:
                            i_gui_separator_path = '{}/{}'.format(i_gui_parent_path, i_gui_separator_name)
                        #
                        content.set(
                            '{}.properties.type'.format(i_gui_separator_path), 'separator'
                        )
                        content.set(
                            '{}.properties.name'.format(i_gui_separator_path), i_gui_configure.get('group_name')
                        )
                    #
                    content.set(
                        '{}.properties.type'.format(i_gui_path), 'action'
                    )
                    content.set(
                        '{}.properties.group_name'.format(i_gui_path), i_gui_configure.get('group_name')
                    )
                    content.set(
                        '{}.properties.name'.format(i_gui_path), i_gui_name
                    )
                    content.set(
                        '{}.properties.icon_name'.format(i_gui_path), i_gui_configure.get('icon_name')
                    )
                    if i_hook_option:
                        if 'gui_icon_name' in i_hook_option:
                            content.set(
                                '{}.properties.icon_name'.format(i_gui_path), i_hook_option.get('gui_icon_name')
                            )
                    #
                    content.set(
                        '{}.properties.executable_fnc'.format(i_gui_path), i_session.get_is_executable
                    )
                    content.set(
                        '{}.properties.execute_fnc'.format(i_gui_path), i_execute_fnc
                    )
        return content

    @classmethod
    def _get_rsv_unit_action_hook_args_(cls, session_dict, key, *args, **kwargs):
        def execute_fnc():
            session.execute_python_file(python_file_path, session=session)

        rsv_task = args[0]
        session_path = '{}/{}'.format(rsv_task.path, key)
        if session_path in session_dict:
            return session_dict[session_path]
        else:
            python_file_path = ssn_core.SsnHookFileMtd.get_python(key)
            yaml_file_path = ssn_core.SsnHookFileMtd.get_yaml(key)
            if python_file_path and yaml_file_path:
                python_file = bsc_storage.StgFileOpt(python_file_path)
                yaml_file = bsc_storage.StgFileOpt(yaml_file_path)
                if python_file.get_is_exists() is True and yaml_file.get_is_exists() is True:
                    configure = ctt_core.Content(value=yaml_file.path)
                    type_name = configure.get('option.type')
                    if type_name is not None:
                        kwargs['configure'] = configure
                        #
                        if type_name in ['asset', 'shot', 'step', 'task']:
                            session = ssn_objects.RsvActionSession(
                                *args,
                                **kwargs
                            )
                        elif type_name in ['unit']:
                            session = ssn_objects.RsvUnitActionSession(
                                *args,
                                **kwargs
                            )
                        else:
                            raise TypeError()
                        #
                        session_dict[session_path] = session, execute_fnc
                        return session, execute_fnc

    def _set_graph_save_(self):
        file_path = self._options_prx_node.get(
            'output.file'
        )
        if file_path:
            self._node_graph.set_graph_save_to(
                file_path
            )
            self._options_prx_node.get_port(
                'output.file'
            ).update_history()
            gui_core.GuiDialog.create(
                'Save Graph',
                content='"{}" save is completed'.format(file_path),
                status=gui_core.GuiDialog.ValidationStatus.Correct,
                #
                yes_label='Open Folder', yes_method=bsc_storage.StgPathOpt(file_path).open_in_system,
                no_label='Close',
                #
                cancel_visible=False
            )
        else:
            gui_core.GuiDialog.create(
                'Save Graph',
                content='enter a file name',
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )

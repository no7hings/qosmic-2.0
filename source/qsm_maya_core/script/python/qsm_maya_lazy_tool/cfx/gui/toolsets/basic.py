# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_general.core as qsm_gnl_core

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.general.core as qsm_mya_hdl_gnl_core

import qsm_maya.handles.cfx.core as qsm_mya_hdl_cfx_core

import qsm_maya.handles.cfx.scripts as qsm_mya_hdl_cfx_scripts

import lnx_maya_gui.core as qsm_mya_gui_core


class UnitForCfxResourceView(
    qsm_mya_gui_core.PrxTreeviewUnitForAssetOpt
):
    ROOT_NAME = 'Rigs'

    NAMESPACE = 'rig'

    RESOURCES_QUERY_CLS = qsm_mya_hdl_cfx_core.CfxAdvRigAssetsQuery

    CHECK_BOX_FLAG = False

    TOOL_INCLUDES = [
        'isolate-select',
        'reference',
    ]

    def __init__(self, window, unit, session, prx_tree_view):
        super(UnitForCfxResourceView, self).__init__(window, unit, session, prx_tree_view)

    def gui_add_resource_components(self, resource):
        data = resource.generate_cfx_component_data()
        if data:
            for k, v in data.items():
                self.gui_add_resource_component(k, v)
            return 'CFX'
        return None


class ToolsetUnitForCfxRigExport(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    # cloth
    # export

    def _get_export_args(self):
        resources = self._page._gui_asset_prx_unit.gui_get_checked_resources()
        if not resources:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.main.messages.no_resource')
                ),
                status='warning'
            )
            return

        with_alembic_cache = self._prx_options_node.get('cloth.with_alembic_cache')
        with_geometry_cache = self._prx_options_node.get('cloth.with_geometry_cache')

        if sum([with_alembic_cache, with_geometry_cache]) == 0:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.main.messages.no_cache_type')
                ),
                status='warning'
            )
            return

        return resources, with_alembic_cache, with_geometry_cache

    def do_dcc_export_cfx_cloth_cache_by_checked(self):
        args = self._get_export_args()
        if args:
            resources, with_alembic_cache, with_geometry_cache = args

            directory_path = self._prx_options_node.get('cloth.version_directory')
            frame_range = self._frame_range_port.get()
            frame_step = self._prx_options_node.get('setting.frame_step')
            frame_offset = self._prx_options_node.get('setting.frame_offset')

            with self._window.gui_progressing(
                maximum=len(resources), label='processing cfx clothes'
            ) as g_p:
                for i_resource in resources:
                    i_opt = qsm_mya_hdl_cfx_scripts.ShotCfxClothCacheOpt(i_resource)
                    i_opt.do_export(
                        directory_path,
                        frame_range, frame_step, frame_offset,
                        with_alembic_cache=with_alembic_cache, with_geometry_cache=with_geometry_cache
                    )
                    g_p.do_update()

            self.do_gui_refresh_version_by_version_scheme_changing()

    def do_dcc_export_cfx_cloth_cache_by_checked_as_backstage(self):
        import lxbasic.web as bsc_web

        import qsm_lazy_backstage.worker as lzy_bks_worker

        if lzy_bks_worker.TaskClient.get_server_status():
            args = self._get_export_args()
            if args:
                resources, with_alembic_cache, with_geometry_cache = args

                directory_path = self._prx_options_node.get('cloth.version_directory')
                frame_range = self._frame_range_port.get()
                frame_step = self._prx_options_node.get('setting.frame_step')
                frame_offset = self._prx_options_node.get('setting.frame_offset')

                namespaces = [x.namespace for x in resources]

                task_name, scene_src_path, cmd_script = qsm_mya_hdl_cfx_scripts.CfxNClothCacheProcess.generate_subprocess_args(
                    namespaces,
                    directory_path,
                    frame_range, frame_step, frame_offset, with_alembic_cache, with_geometry_cache
                )

                lzy_bks_worker.TaskClient.new_entity(
                    group=None,
                    type='cfx-cache',
                    name=task_name,
                    cmd_script=cmd_script,
                    icon_name='application/maya',
                    file=scene_src_path,
                    output_file=bsc_core.ensure_unicode(directory_path),
                    # must use string
                    completed_notice=bsc_web.UrlOptions.to_string(
                        dict(
                            title='通知',
                            message='缓存输出结束了, 是否打开文件夹?',
                            # todo? exec must use unicode
                            ok_python_script='import os; os.startfile("{}".decode("utf-8"))'.format(
                                # to string
                                bsc_core.ensure_string(directory_path)
                            ),
                            status='normal'
                        )
                    )
                )

                self._window.exec_message_dialog(
                    self._window.choice_gui_message(
                        self._window._configure.get('build.main.messages.task_submit_successful')
                    ),
                    status='correct'
                )
        else:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.main.messages.no_task_server')
                ),
                status='warning'
            )

    def do_dcc_export_cfx_cloth_cache_by_checked_as_farm(self):
        import lxbasic.deadline as bsc_deadline
        c = bsc_deadline.DdlBase.generate_connection()
        groups = c.Groups.GetGroupNames()
        if isinstance(groups, list):
            args = self._get_export_args()
            if args:
                resources, with_alembic_cache, with_geometry_cache = args

                directory_path = self._prx_options_node.get('cloth.version_directory')
                frame_range = self._frame_range_port.get()
                frame_step = self._prx_options_node.get('setting.frame_step')
                frame_offset = self._prx_options_node.get('setting.frame_offset')

                namespaces = [x.namespace for x in resources]

                option_hook = qsm_mya_hdl_cfx_scripts.CfxNClothCacheProcess.generate_farm_hook_option(
                    namespaces,
                    directory_path,
                    frame_range, frame_step, frame_offset, with_alembic_cache, with_geometry_cache
                )

                import lxsession.commands as ssn_commands

                ssn_commands.execute_option_hook_by_deadline(option_hook)

                self._window.exec_message_dialog(
                    self._window.choice_gui_message(
                        self._window._configure.get('build.main.messages.farm_submit_successful')
                    ),
                    status='correct'
                )
        else:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.main.messages.no_farm_server')
                ),
                status='warning'
            )

    # settings
    def do_dcc_refresh_by_fps_changing(self):
        pass

    def do_gui_refresh_fps(self):
        fps = qsm_mya_core.Frame.get_fps_tag()
        self._fps_port.set(fps)

    def do_gui_refresh_by_frame_scheme_changing(self):
        frame_scheme = self.gui_get_frame_scheme()
        if frame_scheme == 'frame_range':
            self._frame_range_port.set_locked(False)
        else:
            self._frame_range_port.set_locked(True)
            self.do_gui_refresh_by_dcc_frame_changing()

    def do_gui_refresh_by_dcc_frame_changing(self):
        frame_scheme = self.gui_get_frame_scheme()
        if frame_scheme == 'time_slider':
            frame_range = qsm_mya_core.Frame.get_frame_range()
            self._frame_range_port.set(frame_range)

    def do_gui_refresh_version_by_version_scheme_changing(self):
        directory_path = self._prx_options_node.get('cloth.directory')
        version_scheme = self._prx_options_node.get('cloth.version_scheme')

        options = dict(
            directory=directory_path,
            scene=bsc_storage.StgFileOpt(qsm_mya_core.SceneFile.get_current()).get_name_base()
        )

        if version_scheme == 'no_version':
            version_directory_ptn = '{directory}/{scene}'
            version_directory_path = version_directory_ptn.format(**options)
        elif version_scheme == 'new_version':
            version_directory_ptn = '{directory}/{scene}.v{{version}}'.format(
                **options
            )
            version_directory_path = bsc_core.BscVersion.generate_as_new_version(version_directory_ptn)
        elif version_scheme == 'specified_version':
            version_directory_ptn = '{directory}/{scene}.v{{version}}'.format(
                **options
            )
            options['version'] = str(self._prx_options_node.get('cloth.specified_version')).zfill(3)
            version_directory_path = version_directory_ptn.format(**options)
        else:
            raise RuntimeError()

        self._prx_options_node.set(
            'cloth.version_directory', version_directory_path
        )

    def __init__(self, window, unit, session):
        super(ToolsetUnitForCfxRigExport, self).__init__(window, unit, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._window._configure.get('build.main.units.export.options')
            )
        )
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.main.units.export.options.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='export',
            name=gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._window._configure.get('build.main.units.export')
            ),
            icon_name_text='export',
            tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                self._window._language, self._window._configure.get('build.main.units.export')
            )
        )
        self._prx_options_node.get_port('setting.frame_scheme').connect_input_changed_to(
            self.do_gui_refresh_by_frame_scheme_changing
        )

        self._fps_port = self._prx_options_node.get_port('setting.fps')
        self._frame_range_port = self._prx_options_node.get_port('setting.frame_range')

        self._prx_options_node.get_port('cloth.version_scheme').connect_input_changed_to(
            self.do_gui_refresh_version_by_version_scheme_changing
        )
        self._prx_options_node.get_port('cloth.specified_version').connect_input_changed_to(
            self.do_gui_refresh_version_by_version_scheme_changing
        )

        self._cfx_cloth_export_button = self._prx_options_node.get_port('cloth.export_cfx_cloth')
        self._cfx_cloth_export_button.set(
            self.do_dcc_export_cfx_cloth_cache_by_checked
        )

        self._cfx_cloth_export_button_as_backstage = self._prx_options_node.get_port(
            'cloth.export_cfx_cloth_as_backstage'
        )
        self._cfx_cloth_export_button_as_backstage.set(
            self.do_dcc_export_cfx_cloth_cache_by_checked_as_backstage
        )

        self._cfa_cloth_export_button_as_farm = self._prx_options_node.get_port(
            'cloth.export_cfx_cloth_as_farm'
        )
        self._cfa_cloth_export_button_as_farm.set(
            self.do_dcc_export_cfx_cloth_cache_by_checked_as_farm
        )

        directory_path = 'Z:/temporaries/{}/cfx'.format(bsc_core.BscSystem.get_user_name())
        self._prx_options_node.set('cloth.directory', directory_path)

    def gui_get_frame_scheme(self):
        return self._prx_options_node.get('setting.frame_scheme')

    def do_gui_refresh_all(self):
        self.do_gui_refresh_fps()
        self.do_gui_refresh_by_dcc_frame_changing()

        self.do_gui_refresh_version_by_version_scheme_changing()


class ToolsetUnitForCfxRigImport(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    CACHE_PATTERN = '{directory}'

    def do_gui_refresh_by_version_directory_changing(self):
        directory_path = self._prx_options_node.get(
            'cloth.version_directory'
        )
        if not directory_path:
            return

        pot = self._prx_options_node.get_port('cloth.file_tree')
        pot.set_root(directory_path)

        ptn = qsm_gnl_core.DccFilePatterns.CfxClothAbcFile
        ptn_opt = bsc_core.BscStgParseOpt(
            ptn
        )
        ptn_opt.update_variants(directory=directory_path)
        abc_paths = ptn_opt.get_match_results()
        pot.set(abc_paths)

    def do_dcc_load_cloth_cache_by_checked(self):
        directory_path = self._prx_options_node.get(
            'cloth.version_directory'
        )
        if not directory_path:
            return

        pot = self._prx_options_node.get_port('cloth.file_tree')

        resources_query = self._page._gui_asset_prx_unit.get_resources_query()

        cache_paths = pot.get_all(check_only=True)
        if cache_paths:
            ptn = qsm_gnl_core.DccFilePatterns.CfxClothAbcFile
            ptn_opt = bsc_core.BscStgParseOpt(
                ptn
            )
            with self._window.gui_progressing(
                maximum=len(cache_paths), label='load cfx clothes'
            ) as g_p:
                for i_cache_path in cache_paths:
                    if ptn_opt.check_is_matched(i_cache_path) is True:
                        i_properties = ptn_opt.get_variants(i_cache_path)
                        i_resource = resources_query.get(i_properties['namespace'])
                        if i_resource:
                            i_resource_opt = qsm_mya_hdl_cfx_scripts.ShotCfxClothCacheOpt(i_resource)
                            i_resource_opt.load_cache(i_cache_path)

                    g_p.do_update()

    def do_dcc_remove_cloth_cache_by_checked(self):
        resources = self._page._gui_asset_prx_unit.gui_get_selected_resources()
        if resources:
            for i_resource in resources:
                i_opt = qsm_mya_hdl_cfx_scripts.ShotCfxClothCacheOpt(i_resource)
                i_opt.remove_cache()

        self._page.do_gui_refresh_all(force=True)

        self._page._gui_asset_prx_unit.do_gui_refresh_by_dcc_selection()

    def __init__(self, window, unit, session):
        super(ToolsetUnitForCfxRigImport, self).__init__(window, unit, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._window._configure.get('build.main.units.import.options')
            )
        )
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.main.units.import.options.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='import',
            name=gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._window._configure.get('build.main.units.import')
            ),
            icon_name_text='import',
            tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                self._window._language, self._window._configure.get('build.main.units.import')
            )
        )

        self._prx_options_node.get_port(
            'cloth.version_directory'
        ).connect_input_changed_to(
            self.do_gui_refresh_by_version_directory_changing
        )

        self._prx_options_node.set(
            'cloth.load_cfx_cloth',
            self.do_dcc_load_cloth_cache_by_checked
        )

        self._prx_options_node.set(
            'cloth.remove_cfx_cloth',
            self.do_dcc_remove_cloth_cache_by_checked
        )

    def do_gui_refresh_all(self):
        self.do_gui_refresh_by_version_directory_changing()

# coding:utf-8
import functools
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.storage as bsc_storage

import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.proxy.scripts as gui_prx_scripts

import qsm_general.core as qsm_gnl_core

import lnx_parsor.swap as lnx_prs_swap

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.scenery.core as qsm_mya_hdl_scn_core

import qsm_maya.handles.scenery.scripts as qsm_mya_hdl_scn_scripts

import lnx_maya_resora.scripts as qsm_mya_lzy_rsc_scripts

import lnx_maya_gui.core as qsm_mya_gui_core


class PrxUnitForSceneryAssetView(
    qsm_mya_gui_core.PrxTreeviewUnitForAssetOpt
):
    ROOT_NAME = 'Sceneries'

    NAMESPACE = 'scenery'

    RESOURCES_QUERY_CLS = qsm_mya_hdl_scn_core.SceneryAssetQuery

    TOOL_INCLUDES = [
        'isolate-select',
        'reference',
    ]

    def __init__(self, window, unit, session, prx_tree_view):
        super(PrxUnitForSceneryAssetView, self).__init__(window, unit, session, prx_tree_view)
        self._unit_assembly_load_args_array = []
        self._gpu_instance_load_args_array = []


class PrxToolbarForSceneryReference(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    def __init__(self, window, unit, session, prx_input_for_asset):
        super(PrxToolbarForSceneryReference, self).__init__(window, unit, session)
        self._prs_root = lnx_prs_swap.Swap.generate_root()

        self._asset_prx_input = prx_input_for_asset

        self._asset_load_qt_button = qt_widgets.QtPressButton()
        self._asset_prx_input.add_widget(self._asset_load_qt_button)
        self._asset_load_qt_button._set_name_text_(
            self._window.choice_gui_name(
                self._window._configure.get('build.scenery.buttons.reference')
            )
        )
        self._asset_load_qt_button._set_tool_tip_text_(
            self._window.choice_gui_tool_tip(
                self._window._configure.get('build.scenery.buttons.reference')
            )
        )
        self._asset_load_qt_button._set_auto_width_(True)
        self._asset_load_qt_button.press_clicked.connect(self._on_dcc_load_asset)
        self._asset_load_qt_button._set_action_enable_(False)

        self._unit_assembly_load_qt_button = qt_widgets.QtPressButton()
        self._asset_prx_input.add_widget(self._unit_assembly_load_qt_button)
        self._unit_assembly_load_qt_button._set_name_text_(
            self._window.choice_gui_name(
                self._window._configure.get('build.scenery.buttons.load_unit_assembly')
            )
        )
        self._unit_assembly_load_qt_button._set_tool_tip_text_(
            self._window.choice_gui_tool_tip(
                self._window._configure.get('build.scenery.buttons.load_unit_assembly')
            )
        )
        self._unit_assembly_load_qt_button._set_auto_width_(True)
        self._unit_assembly_load_qt_button.press_clicked.connect(self._on_dcc_load_unit_assembly)
        self._unit_assembly_load_qt_button._set_action_enable_(False)

        self._asset_prx_input.connect_input_change_accepted_to(self._do_gui_refresh_resource_for)

        self._asset_path = None
        self._unit_assembly_path = None

        self._do_gui_refresh_resource_for(self._asset_prx_input.get_path())

    def _on_dcc_load_asset(self):
        if self._asset_path is not None:
            file_opt = bsc_storage.StgFileOpt(self._asset_path)
            qsm_mya_core.SceneFile.reference_file(
                self._asset_path,
                namespace=file_opt.name_base
            )
            self._page.do_gui_refresh_all()

    def _on_dcc_load_unit_assembly(self):
        if self._asset_path is not None and self._unit_assembly_path is not None:
            namespace = bsc_storage.StgFileOpt(self._asset_path).name_base

            qsm_mya_lzy_rsc_scripts.AssetUnitAssemblyOpt.load_cache(
                namespace, self._unit_assembly_path
            )

    def _do_gui_refresh_resource_for(self, path):
        self._asset_path = None
        self._unit_assembly_path = None

        self._asset_load_qt_button._set_action_enable_(False)
        self._unit_assembly_load_qt_button._set_action_enable_(False)

        entity = self._asset_prx_input.get_entity(path)
        if entity is not None:
            if entity.type == 'Asset':
                task = entity.task(self._prs_root.Tasks.model)
                if task is not None:
                    result = task.find_result(
                        self._prs_root.Patterns.MayaModelFIle
                    )
                    if result is not None:
                        self._asset_path = result
                        self._asset_load_qt_button._set_action_enable_(True)

                        unit_assembly_path = qsm_gnl_core.DccCache.generate_asset_unit_assembly_file_new(result)
                        if bsc_storage.StgPath.get_is_file(unit_assembly_path):
                            self._unit_assembly_path = unit_assembly_path
                            self._unit_assembly_load_qt_button._set_action_enable_(True)

    def do_update(self):
        self._asset_prx_input.do_update()


class PrxToolsetForUnitAssemblyLoad(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    # unit assembly
    def do_dcc_load_unit_assemblies(self):
        if self._unit_assembly_load_args_array:
            hide_scenery = self._prx_options_node.get('setting.hide_scenery')
            with self._window.gui_progressing(
                maximum=len(self._unit_assembly_load_args_array), label='load unit assemblies'
            ) as g_p:
                for i_opt, i_cache_path in self._unit_assembly_load_args_array:
                    if i_opt.is_resource_exists() is True:
                        i_opt.load_cache(i_cache_path, hide_scenery=hide_scenery)
                    g_p.do_update()

            self._page.do_gui_refresh_all(force=True)
            self._page._gui_switch_opt.do_dcc_update()

    def do_dcc_load_unit_assemblies_by_selection(self):
        if self._load_unit_assembly_button.get_is_started() is False:
            resources = self._page._gui_asset_prx_unit.gui_get_selected_resources()
            if resources:
                self._unit_assembly_load_args_array = []
                create_cmds = []

                with self._window.gui_progressing(
                    maximum=len(resources), label='processing unit assemblies'
                ) as g_p:
                    for i_resource in resources:
                        i_opt = qsm_mya_hdl_scn_scripts.UnitAssemblyOpt(i_resource)
                        if i_opt.is_exists() is False:
                            i_task_name, i_cmd_script, i_cache_path = i_opt.generate_args()
                            if i_cmd_script is not None:
                                create_cmds.append(i_cmd_script)

                            self._unit_assembly_load_args_array.append(
                                (i_opt, i_cache_path)
                            )

                        g_p.do_update()

                if create_cmds:
                    mtd = gui_prx_scripts.GuiThreadWorker(self._window)
                    mtd.execute(self._load_unit_assembly_button, create_cmds)
                else:
                    self.do_dcc_load_unit_assemblies()

    def do_dcc_load_unit_assembly(self):
        import lxbasic.session as bsc_session

        bsc_session.OptionHook.execute(
            bsc_core.ArgDictStringOpt(
                dict(
                    option_hook_key='dcc-script/maya/qsm-unit-assembly-load-script',
                )
            ).to_string()
        )

    def do_dcc_remove_unit_assemblies(self):
        resources = self._page._gui_asset_prx_unit.gui_get_selected_resources()
        if resources:
            w = gui_core.GuiDialog.create(
                label='Scenery',
                sub_label='Remove Unit Assembly',
                content='do you remove "Unit Assembly"?,\n press "Ok" to continue',
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                parent=self._window.widget
            )

            result = w.get_result()
            if result is True:
                for i_resource in resources:
                    i_opt = qsm_mya_hdl_scn_scripts.UnitAssemblyOpt(i_resource)
                    i_opt.remove_cache()

    # gpu instance
    def do_dcc_load_gpu_instances(self):
        if self._gpu_instance_load_args_array:
            hide_scenery = self._prx_options_node.get('setting.hide_scenery')
            with self._window.gui_progressing(
                maximum=len(self._gpu_instance_load_args_array), label='load gpu instances'
            ) as g_p:
                for i_opt, i_cache_path in self._gpu_instance_load_args_array:
                    if i_opt.is_resource_exists() is True:
                        i_opt.load_cache(i_cache_path, hide_scenery=hide_scenery)
                    g_p.do_update()

            self._page.do_gui_refresh_all(force=True)
            self._page._gui_switch_opt.do_dcc_update()

    def do_dcc_load_gpu_instances_by_selection(self):
        if self._load_gpu_instance_button.get_is_started() is False:
            resources = self._page._gui_asset_prx_unit.gui_get_selected_resources()
            if resources:
                self._gpu_instance_load_args_array = []
                create_cmds = []

                with self._window.gui_progressing(
                    maximum=len(resources), label='processing gpu instances'
                ) as g_p:
                    for i_resource in resources:
                        i_opt = qsm_mya_hdl_scn_scripts.GpuInstanceOpt(i_resource)
                        if i_opt.is_exists() is False:
                            i_cmd_script, i_cache_path = i_opt.generate_args()
                            if i_cmd_script is not None:
                                create_cmds.append(i_cmd_script)

                            self._gpu_instance_load_args_array.append(
                                (i_opt, i_cache_path)
                            )

                        g_p.do_update()

                if create_cmds:
                    mtd = gui_prx_scripts.GuiThreadWorker(self._window)
                    mtd.execute(self._load_gpu_instance_button, create_cmds)
                else:
                    self.do_dcc_load_gpu_instances()

    def do_dcc_remove_gpu_instances(self):
        resources = self._page._gui_asset_prx_unit.gui_get_selected_resources()
        if resources:
            w = gui_core.GuiDialog.create(
                label='Scenery',
                sub_label='Remove GPU Instance',
                content='do you remove "GPU Instance"?,\n press "Ok" to continue',
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                parent=self._window.widget
            )

            result = w.get_result()
            if result is True:
                for i_resource in resources:
                    i_opt = qsm_mya_hdl_scn_scripts.GpuInstanceOpt(i_resource)
                    i_opt.remove_cache()

    def __init__(self, window, unit, session):
        super(PrxToolsetForUnitAssemblyLoad, self).__init__(window, unit, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self._window.choice_gui_name(
                self._window._configure.get('build.scenery.units.unit_assembly_and_gpu_instance_load.options')
            )
        )
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.scenery.units.unit_assembly_and_gpu_instance_load.options.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='utility',
            name=self._window.choice_gui_name(
                self._window._configure.get('build.scenery.units.unit_assembly_and_gpu_instance_load')
            ),
            icon_name_text='utility',
            tool_tip=self._window.choice_gui_tool_tip(
                self._window._configure.get('build.scenery.units.unit_assembly_and_gpu_instance_load')
            )
        )

        self._load_unit_assembly_button = self._prx_options_node.get_port('unit_assembly.load')
        self._load_unit_assembly_button.set(self.do_dcc_load_unit_assembly)
        # self._load_unit_assembly_button.set(self.do_dcc_load_unit_assemblies_by_selection)
        # self._load_unit_assembly_button.connect_finished_to(self.do_dcc_load_unit_assemblies)
        self._prx_options_node.set(
            'unit_assembly.remove', self.do_dcc_remove_unit_assemblies
        )

        self._load_gpu_instance_button = self._prx_options_node.get_port('gpu_instance.load')
        self._load_gpu_instance_button.set(self.do_dcc_load_gpu_instances_by_selection)
        self._load_gpu_instance_button.connect_finished_to(self.do_dcc_load_gpu_instances)
        self._prx_options_node.set(
            'gpu_instance.remove', self.do_dcc_remove_gpu_instances
        )


class PrxToolsetForUnitAssemblySwitch(
    qsm_mya_gui_core.PrxUnitBaseOpt
):

    def do_dcc_unit_assembly_switch_to(self, key):
        if self._unit_assembly_paths:
            if len(self._unit_assembly_paths) > 100:
                with self._window.gui_progressing(
                    maximum=len(self._unit_assembly_paths), label='switch unit assembly'
                ) as g_p:
                    for i in self._unit_assembly_paths:
                        qsm_mya_hdl_scn_core.UnitAssemblyOpt(i).set_active(key)
                        g_p.do_update()
            else:
                [qsm_mya_hdl_scn_core.UnitAssemblyOpt(x).set_active(key) for x in self._unit_assembly_paths]
            # fixme: repair selection?
            qsm_mya_core.Selection.set(
                [x for x in self._unit_assembly_paths]
            )

            self.do_gui_refresh_buttons()

    def do_dcc_gpu_instance_switch_to(self, key):
        if self._gpu_instance_paths:
            if len(self._unit_assembly_paths) > 100:
                with self._window.gui_progressing(
                    maximum=len(self._gpu_instance_paths), label='switch unit assembly'
                ) as g_p:
                    for i in self._unit_assembly_paths:
                        qsm_mya_hdl_scn_core.GpuInstanceOpt(i).set_active(key)
                        g_p.do_update()
            else:
                [qsm_mya_hdl_scn_core.GpuInstanceOpt(x).set_active(key) for x in self._gpu_instance_paths]

            self.do_gui_refresh_buttons()

    def do_dcc_import_mesh(self):
        if self._unit_assembly_paths:
            [qsm_mya_hdl_scn_core.UnitAssemblyOpt(x).do_import_mesh() for x in self._unit_assembly_paths]
        if self._gpu_instance_paths:
            [qsm_mya_hdl_scn_core.GpuInstanceOpt(x).do_import_mesh() for x in self._gpu_instance_paths]

    def do_dcc_select_by_camera(self):
        camera = qsm_mya_core.Camera.get_active()
        qsm_mya_hdl_scn_scripts.CameraSelection(camera).execute()

    def do_dcc_update(self):
        pass

    def __init__(self, window, unit, session):
        super(PrxToolsetForUnitAssemblySwitch, self).__init__(window, unit, session)
        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self._window.choice_gui_name(
                self._window._configure.get('build.scenery.units.unit_assembly_and_gpu_instance_switch.options')
                )
        )
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.scenery.units.unit_assembly_and_gpu_instance_switch.options.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='switch',
            name=self._window.choice_gui_name(
                self._window._configure.get('build.scenery.units.unit_assembly_and_gpu_instance_switch')
            ),
            icon_name_text='switch',
            tool_tip=self._window.choice_gui_tool_tip(
                self._window._configure.get('build.scenery.units.unit_assembly_and_gpu_instance_switch')
            )
        )

        self._unit_assemblies_query = qsm_mya_hdl_scn_core.UnitAssembliesQuery()
        self._gpu_instances_query = qsm_mya_hdl_scn_core.GpuInstancesQuery()

        self._unit_assembly_button_dict = {}
        self._unit_assembly_paths = []
        self._gpu_instance_button_dict = {}
        self._gpu_instance_paths = []

        for i_key in qsm_mya_hdl_scn_core.Assembly.Keys.All:
            i_b = self._prx_options_node.get_port(
                'switch.unit_assembly.{}'.format(i_key)
            )
            i_b.set(
                functools.partial(self.do_dcc_unit_assembly_switch_to, i_key)
            )
            self._unit_assembly_button_dict[i_key] = i_b

        for i_key in qsm_mya_hdl_scn_core.Assembly.Keys.GPUs:
            i_b = self._prx_options_node.get_port(
                'switch.gpu_instance.{}'.format(i_key)
            )
            i_b.set(
                functools.partial(self.do_dcc_gpu_instance_switch_to, i_key)
            )
            self._gpu_instance_button_dict[i_key] = i_b

        self._prx_options_node.set(
            'import.mesh', self.do_dcc_import_mesh
        )
        self._prx_options_node.set(
            'selection.camera_visible', self.do_dcc_select_by_camera
        )

    def do_gui_refresh_buttons(self):
        _ = cmds.ls(selection=1, long=1) or []
        self.do_gui_refresh_buttons_for_unit_assembly(_)
        self.do_gui_refresh_buttons_for_gpu_instance(_)

    def do_gui_refresh_buttons_for_unit_assembly(self, paths):
        self._unit_assembly_paths = []

        for k, i_b in self._unit_assembly_button_dict.items():
            i_b.set_status(
                i_b.ValidationStatus.Disable
            )
            i_b.set_sub_name(None)

        mapper = self._unit_assemblies_query.to_mapper(paths)
        if mapper:
            for k, v in mapper.items():
                if k in self._unit_assembly_button_dict:
                    i_c = len(v)
                    i_b = self._unit_assembly_button_dict[k]
                    i_b.set_status(i_b.ValidationStatus.Enable)
                    i_b.set_sub_name('({})'.format(i_c))
                    self._unit_assembly_paths.extend(v)

    def do_gui_refresh_buttons_for_gpu_instance(self, paths):
        self._gpu_instance_paths = []

        for k, i_b in self._gpu_instance_button_dict.items():
            i_b.set_status(
                i_b.ValidationStatus.Disable
            )
            i_b.set_sub_name(None)

        mapper = self._gpu_instances_query.to_mapper(paths)
        if mapper:
            for k, v in mapper.items():
                if k in self._gpu_instance_button_dict:
                    i_c = len(v)
                    i_b = self._gpu_instance_button_dict[k]
                    i_b.set_status(i_b.ValidationStatus.Enable)
                    i_b.set_sub_name('({})'.format(i_c))
                    self._gpu_instance_paths.extend(v)

    def do_gui_refresh_by_dcc_selection(self):
        if self._page.gui_get_tool_tab_current_key() == 'switch':
            self.do_gui_refresh_buttons()


class PrxToolsetForCameraMask(
    qsm_mya_gui_core.PrxUnitBaseOpt
):

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

    def do_gui_refresh_by_camera_changing(self):
        cameras = qsm_mya_core.Cameras.get_all()
        active_camera = qsm_mya_core.Camera.get_active()
        self._camera_port.set(
            cameras
        )
        self._camera_port.set(
            active_camera
        )

    def do_gui_load_active_camera(self):
        self.do_gui_refresh_by_camera_changing()

    def __init__(self, window, unit, session):
        super(PrxToolsetForCameraMask, self).__init__(window, unit, session)
        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self._window.choice_gui_name(
                self._window._configure.get('build.scenery.units.camera_mask.options')
            )
        )
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.scenery.units.camera_mask.options.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='extend',
            name=self._window.choice_gui_name(
                self._window._configure.get('build.scenery.units.camera_mask')
            ),
            icon_name_text='extend',
            tool_tip=self._window.choice_gui_tool_tip(
                self._window._configure.get('build.scenery.units.camera_mask')
            )
        )

        self._prx_options_node.set(
            'camera_view_frustum.create', self.do_dcc_create_camera_view_frustum
        )
        self._prx_options_node.set(
            'camera_view_frustum.remove', self.do_dcc_remove_camera_view_frustum
        )

        self._prx_options_node.set(
            'camera_mask.create_dynamic', self.do_dcc_create_dynamic_camera_mask
        )
        self._prx_options_node.set(
            'camera_mask.create', self.do_dcc_create_camera_mask
        )
        self._prx_options_node.set(
            'camera_mask.remove_all', self.do_dcc_remove_all_camera_masks
        )

        self._prx_options_node.get_port('setting.frame_scheme').connect_input_changed_to(
            self.do_gui_refresh_by_frame_scheme_changing
        )

        self._camera_port = self._prx_options_node.get_port('setting.camera')
        self._frame_range_port = self._prx_options_node.get_port('setting.frame_range')

        self._prx_options_node.set(
            'camera_lod_switch.create', self.do_dcc_create_camera_lod_switch
        )

        self._prx_options_node.set(
            'setting.load_active_camera', self.do_gui_load_active_camera
        )

    def gui_get_frame_scheme(self):
        return self._prx_options_node.get('setting.frame_scheme')

    def get_frame_range(self):
        frame_scheme = self.gui_get_frame_scheme()
        if frame_scheme == 'time_slider':
            return qsm_mya_core.Frame.get_frame_range()
        return self._prx_options_node.get('setting.frame_range')

    def get_camera(self):
        return self._prx_options_node.get('setting.camera')

    # camera mask
    def do_dcc_create_camera_view_frustum(self):
        camera = qsm_mya_core.Camera.get_active()
        scp = qsm_mya_hdl_scn_scripts.CameraViewFrustum(camera)
        scp.execute()

    def do_dcc_remove_camera_view_frustum(self):
        qsm_mya_hdl_scn_scripts.CameraViewFrustum.restore()

    def do_dcc_create_dynamic_camera_mask(self):
        camera = qsm_mya_core.Camera.get_active()
        frame_range = self.get_frame_range()
        qsm_mya_hdl_scn_scripts.DynamicCameraMask(camera, frame_range).execute_for_all()

    def do_dcc_create_camera_mask(self):

        camera = qsm_mya_core.Camera.get_active()
        frame_range = self.get_frame_range()
        qsm_mya_hdl_scn_scripts.CameraMask(
            camera, frame_range
        ).execute_for_all()

    def do_dcc_remove_all_camera_masks(self):
        qsm_mya_hdl_scn_scripts.DynamicCameraMask.restore()
        qsm_mya_hdl_scn_scripts.CameraMask.restore()

    def do_dcc_create_camera_lod_switch(self):
        camera = qsm_mya_core.Camera.get_active()
        frame_range = self.get_frame_range()
        distance_range = self._prx_options_node.get('camera_lod_switch.distance_range')
        qsm_mya_hdl_scn_scripts.CameraLodSwitch(
            camera, frame_range
        ).execute(
            distance_range
        )

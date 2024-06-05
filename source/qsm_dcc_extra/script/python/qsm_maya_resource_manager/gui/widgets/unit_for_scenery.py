# coding:utf-8
import functools
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.proxy.scripts as gui_prx_scripts

import qsm_general.scan as qsm_gnl_scan

import qsm_maya.core as qsm_mya_core

import qsm_maya.scenery.core as qsm_mya_scn_core

import qsm_maya.scenery.scripts as qsm_mya_scn_scripts

from ... import core as _rsc_mng_core


class UnitForSceneryView(
    _rsc_mng_core.GuiResourceOpt
):
    ROOT_NAME = 'Sceneries'

    NAMESPACE = 'scenery'

    RESOURCES_QUERY_CLS = qsm_mya_scn_core.SceneriesQuery

    TOOL_INCLUDES = [
        'isolate-select',
        'reference',
    ]

    def __init__(self, window, unit, session, prx_tree_view):
        super(UnitForSceneryView, self).__init__(window, unit, session, prx_tree_view)
        self._unit_assembly_load_args_array = []
        self._gpu_instance_load_args_array = []


class UnitForSceneryReference(
    _rsc_mng_core.GuiBaseOpt
):
    def __init__(self, window, unit, session, prx_input_for_asset):
        super(UnitForSceneryReference, self).__init__(window, unit, session)
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
            gui_core.GuiUtil.choice_name(
                self._window._language, self._session.configure.get('build.buttons.reference')
            )
        )
        self._reference_button._set_tool_tip_text_(
            gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._session.configure.get('build.buttons.reference')
            )
        )
        self._reference_button.setMaximumWidth(64)
        self._reference_button.setMinimumWidth(64)
        self._reference_button.press_clicked.connect(self.do_dcc_reference_resource)
        self._reference_button._set_action_enable_(False)

        self._prx_input_for_asset.connect_input_change_accepted_to(self.do_gui_refresh_resource)

        self._resource_file_path = None

        self.do_gui_refresh_resource(self._prx_input_for_asset.get_path())

    def do_dcc_reference_resource(self):
        if self._resource_file_path is not None:
            file_opt = bsc_storage.StgFileOpt(self._resource_file_path)
            count = self._count_input._get_value_()
            for i in range(count):
                qsm_mya_core.SceneFile.reference_file(
                    self._resource_file_path,
                    namespace=file_opt.name_base
                )
            self._page.do_gui_refresh_all()

    def do_gui_refresh_resource(self, path):
        self._resource_file_path = None
        self._reference_button._set_action_enable_(False)
        entity = self._prx_input_for_asset.get_entity(path)
        if entity is not None:
            if entity.type == 'Asset':
                task = entity.task(self._scan_root.EntityTasks.Model)
                if task is not None:
                    result = task.find_result(
                        self._scan_root.ResultPatterns.ModelFIle
                    )
                    if result is not None:
                        self._resource_file_path = result
                        self._reference_button._set_action_enable_(True)

    def do_update(self):
        self._prx_input_for_asset.do_update()


class UnitForSceneryUtilityToolSet(
    _rsc_mng_core.GuiBaseOpt
):

    # unit assembly
    def do_dcc_load_unit_assemblies(self):
        if self._unit_assembly_load_args_array:
            with self._window.gui_progressing(
                maximum=len(self._unit_assembly_load_args_array), label='load unit assemblies'
            ) as g_p:
                for i_opt, i_cache_file in self._unit_assembly_load_args_array:
                    if i_opt.is_resource_exists() is True:
                        i_opt.load_cache(i_cache_file)
                    g_p.do_update()

            self._page.do_gui_refresh_all(force=True)
            self._page._gui_switch_opt.do_dcc_update()

    def do_dcc_do_dcc_load_unit_assemblies_by_selection(self):
        if self._load_unit_assembly_button.get_is_started() is False:
            resources = self._page._gui_resource_opt.gui_get_selected_resources()
            if resources:
                self._unit_assembly_load_args_array = []
                create_cmds = []

                with self._window.gui_progressing(
                    maximum=len(resources), label='processing unit assemblies'
                ) as g_p:
                    for i_resource in resources:
                        i_opt = qsm_mya_scn_scripts.UnitAssemblyOpt(i_resource)
                        if i_opt.is_exists() is False:
                            i_cmd, i_cache_file = i_opt.generate_args()
                            if i_cmd is not None:
                                create_cmds.append(i_cmd)

                            self._unit_assembly_load_args_array.append(
                                (i_opt, i_cache_file)
                            )

                        g_p.do_update()

                if create_cmds:
                    mtd = gui_prx_scripts.GuiThreadWorker(self._window)
                    mtd.execute(self._load_unit_assembly_button, create_cmds)
                else:
                    self.do_dcc_load_unit_assemblies()

    def do_dcc_remove_unit_assemblies(self):
        resources = self._page._gui_resource_opt.gui_get_selected_resources()
        if resources:
            w = gui_core.GuiDialog.create(
                label=self._session.gui_name,
                sub_label='Remove Unit Assembly',
                content='do you remove "Unit Assembly"?,\n press "Ok" to continue',
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                parent=self._window.widget
            )

            result = w.get_result()
            if result is True:
                for i_resource in resources:
                    i_opt = qsm_mya_scn_scripts.UnitAssemblyOpt(i_resource)
                    i_opt.remove_cache()

    # gpu instance
    def do_dcc_load_gpu_instances(self):
        if self._gpu_instance_load_args_array:
            with self._window.gui_progressing(
                maximum=len(self._gpu_instance_load_args_array), label='load gpu instances'
            ) as g_p:
                for i_opt, i_cache_file in self._gpu_instance_load_args_array:
                    if i_opt.is_resource_exists() is True:
                        i_opt.load_cache(i_cache_file)
                    g_p.do_update()

            self._page.do_gui_refresh_all(force=True)
            self._page._gui_switch_opt.do_dcc_update()

    def do_dcc_do_dcc_load_gpu_instances_by_selection(self):
        if self._load_gpu_instance_button.get_is_started() is False:
            resources = self._page._gui_resource_opt.gui_get_selected_resources()
            if resources:
                self._gpu_instance_load_args_array = []
                create_cmds = []

                with self._window.gui_progressing(
                    maximum=len(resources), label='processing gpu instances'
                ) as g_p:
                    for i_resource in resources:
                        i_opt = qsm_mya_scn_scripts.GpuInstanceOpt(i_resource)
                        if i_opt.is_exists() is False:
                            i_cmd, i_cache_file = i_opt.generate_args()
                            if i_cmd is not None:
                                create_cmds.append(i_cmd)

                            self._gpu_instance_load_args_array.append(
                                (i_opt, i_cache_file)
                            )

                        g_p.do_update()

                if create_cmds:
                    mtd = gui_prx_scripts.GuiThreadWorker(self._window)
                    mtd.execute(self._load_gpu_instance_button, create_cmds)
                else:
                    self.do_dcc_load_gpu_instances()

    def do_dcc_remove_gpu_instances(self):
        resources = self._page._gui_resource_opt.gui_get_selected_resources()
        if resources:
            w = gui_core.GuiDialog.create(
                label=self._session.gui_name,
                sub_label='Remove GPU Instance',
                content='do you remove "GPU Instance"?,\n press "Ok" to continue',
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                parent=self._window.widget
            )

            result = w.get_result()
            if result is True:
                for i_resource in resources:
                    i_opt = qsm_mya_scn_scripts.GpuInstanceOpt(i_resource)
                    i_opt.remove_cache()

    def __init__(self, window, unit, session):
        super(UnitForSceneryUtilityToolSet, self).__init__(window, unit, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._session.configure.get('build.options.scenery_utility')
            )
        )
        self._prx_options_node.create_ports_by_data(
            self._session.configure.get('build.options.scenery_utility.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='utility',
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._session.configure.get('build.tag-groups.scenery_utility')
            ),
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._session.configure.get('build.tag-groups.scenery_utility')
            )
        )

        self._load_unit_assembly_button = self._prx_options_node.get_port('unit_assembly.load')
        self._load_unit_assembly_button.set(self.do_dcc_do_dcc_load_unit_assemblies_by_selection)
        self._load_unit_assembly_button.connect_finished_to(self.do_dcc_load_unit_assemblies)
        self._prx_options_node.set(
            'unit_assembly.remove', self.do_dcc_remove_unit_assemblies
        )

        self._load_gpu_instance_button = self._prx_options_node.get_port('gpu_instance.load')
        self._load_gpu_instance_button.set(self.do_dcc_do_dcc_load_gpu_instances_by_selection)
        self._load_gpu_instance_button.connect_finished_to(self.do_dcc_load_gpu_instances)
        self._prx_options_node.set(
            'gpu_instance.remove', self.do_dcc_remove_gpu_instances
        )

        self._prx_options_node.get_port('selection_scheme').connect_input_changed_to(
            self._page._gui_resource_opt.do_dcc_refresh_resources_selection
        )

    def gui_get_selection_scheme(self):
        return self._prx_options_node.get('selection_scheme')


class UnitForScenerySwitchToolSet(
    _rsc_mng_core.GuiBaseOpt
):

    def do_dcc_unit_assembly_switch_to(self, key):
        if self._unit_assembly_paths:
            if len(self._unit_assembly_paths) > 100:
                with self._window.gui_progressing(
                    maximum=len(self._unit_assembly_paths), label='switch unit assembly'
                ) as g_p:
                    for i in self._unit_assembly_paths:
                        qsm_mya_scn_core.UnitAssemblyOpt(i).set_active(key)
                        g_p.do_update()
            else:
                [qsm_mya_scn_core.UnitAssemblyOpt(x).set_active(key) for x in self._unit_assembly_paths]
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
                        qsm_mya_scn_core.GpuInstanceOpt(i).set_active(key)
                        g_p.do_update()
            else:
                [qsm_mya_scn_core.GpuInstanceOpt(x).set_active(key) for x in self._gpu_instance_paths]

            self.do_gui_refresh_buttons()

    def do_dcc_import_mesh(self):
        if self._unit_assembly_paths:
            [qsm_mya_scn_core.UnitAssemblyOpt(x).do_import_mesh() for x in self._unit_assembly_paths]
        if self._gpu_instance_paths:
            [qsm_mya_scn_core.GpuInstanceOpt(x).do_import_mesh() for x in self._gpu_instance_paths]

    def do_dcc_select_by_camera(self):
        camera = qsm_mya_core.Camera.get_active()
        qsm_mya_scn_scripts.CameraSelection(camera).execute()

    def do_dcc_update(self):
        pass

    def __init__(self, window, unit, session):
        super(UnitForScenerySwitchToolSet, self).__init__(window, unit, session)
        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._session.configure.get('build.options.scenery_switch')
            )
        )
        self._prx_options_node.create_ports_by_data(
            self._session.configure.get('build.options.scenery_switch.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='switch',
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._session.configure.get('build.tag-groups.scenery_switch')
            ),
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._session.configure.get('build.tag-groups.scenery_switch')
            )
        )

        self._unit_assemblies_query = qsm_mya_scn_core.UnitAssembliesQuery()
        self._gpu_instances_query = qsm_mya_scn_core.GpuInstancesQuery()

        self._unit_assembly_button_dict = {}
        self._unit_assembly_paths = []
        self._gpu_instance_button_dict = {}
        self._gpu_instance_paths = []

        for i_key in qsm_mya_scn_core.Assembly.Keys.All:
            i_b = self._prx_options_node.get_port(
                'switch.unit_assembly.{}'.format(i_key)
            )
            i_b.set(
                functools.partial(self.do_dcc_unit_assembly_switch_to, i_key)
            )
            self._unit_assembly_button_dict[i_key] = i_b

        for i_key in qsm_mya_scn_core.Assembly.Keys.GPUs:
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
        if self._page.gui_get_current_tool_tab_key() == 'switch':
            self.do_gui_refresh_buttons()


class UnitForSceneryExtendToolSet(
    _rsc_mng_core.GuiBaseOpt
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

    def __init__(self, window, unit, session):
        super(UnitForSceneryExtendToolSet, self).__init__(window, unit, session)
        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._session.configure.get('build.options.scenery_camera')
            )
        )
        self._prx_options_node.create_ports_by_data(
            self._session.configure.get('build.options.scenery_camera.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='extend',
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._session.configure.get('build.tag-groups.scenery_extend')
            ),
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._session.configure.get('build.tag-groups.scenery_extend')
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
        camera = self.get_camera()
        scp = qsm_mya_scn_scripts.CameraViewFrustum(camera)
        scp.execute()

    def do_dcc_remove_camera_view_frustum(self):
        qsm_mya_scn_scripts.CameraViewFrustum.restore()

    def do_dcc_create_dynamic_camera_mask(self):
        camera = self.get_camera()
        frame_range = self.get_frame_range()
        qsm_mya_scn_scripts.DynamicCameraMask(camera, frame_range).execute_for_all()

    def do_dcc_create_camera_mask(self):
        camera = self.get_camera()
        frame_range = self.get_frame_range()
        qsm_mya_scn_scripts.CameraMask(
            camera, frame_range
        ).execute_for_all()

    def do_dcc_remove_all_camera_masks(self):
        qsm_mya_scn_scripts.DynamicCameraMask.restore()
        qsm_mya_scn_scripts.CameraMask.restore()

    def do_dcc_create_camera_lod_switch(self):
        camera = self.get_camera()
        frame_range = self.get_frame_range()
        distance_range = self._prx_options_node.get('camera_lod_switch.distance_range')
        qsm_mya_scn_scripts.CameraLodSwitch(
            camera, frame_range
        ).execute(
            distance_range
        )
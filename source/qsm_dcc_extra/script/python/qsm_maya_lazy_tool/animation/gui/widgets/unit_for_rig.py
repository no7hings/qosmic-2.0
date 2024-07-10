# coding:utf-8
import functools

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.proxy.scripts as gui_prx_scripts

import qsm_general.scan as qsm_gnl_scan

import qsm_maya.core as qsm_mya_core

import qsm_maya.general.core as qsm_mya_gnl_core

import qsm_maya.animation.core as qsm_mya_anm_core

import qsm_maya.animation.scripts as qsm_mya_anm_scripts

import qsm_maya.motion.core as qsm_mya_mtn_core

import qsm_maya_gui.core as qsm_mya_gui_core


class UnitForRigView(
    qsm_mya_gui_core.PrxTreeviewUnitForResourceOpt
):
    ROOT_NAME = 'Rigs'

    NAMESPACE = 'rig'

    RESOURCES_QUERY_CLS = qsm_mya_anm_core.AdvRigsQuery

    TOOL_INCLUDES = [
        'isolate-select',
        'reference',
    ]

    def __init__(self, window, unit, session, prx_tree_view):
        super(UnitForRigView, self).__init__(window, unit, session, prx_tree_view)


class ToolbarUnitForRigReference(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    def __init__(self, window, unit, session, prx_input_for_asset):
        super(ToolbarUnitForRigReference, self).__init__(window, unit, session)
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
                self._window._language, self._window._configure.get('build.rig.buttons.reference')
            )
        )
        self._reference_button._set_tool_tip_text_(
            gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.rig.buttons.reference')
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
                task = entity.task(self._scan_root.EntityTasks.Rig)
                if task is not None:
                    result = task.find_result(
                        self._scan_root.ResultPatterns.RigFile
                    )
                    if result is not None:
                        self._resource_file_path = result
                        self._reference_button._set_action_enable_(True)


class ToolsetUnitForRigUtility(
    qsm_mya_gui_core.PrxUnitBaseOpt
):

    # skin proxy
    def do_dcc_load_skin_proxies(self):
        if self._skin_proxy_load_args_array:
            keep_head = self._prx_options_node.get('skin_proxy.keep_head')
            check_bbox = self._prx_options_node.get('skin_proxy.check_bbox')
            with self._window.gui_progressing(
                maximum=len(self._skin_proxy_load_args_array), label='load skin proxies'
            ) as g_p:
                for i_opt, i_cache_file, i_data_file_path in self._skin_proxy_load_args_array:
                    g_p.do_update()
                    if i_opt.is_resource_exists() is True:
                        i_opt.load_cache(
                            i_cache_file, i_data_file_path, keep_head=keep_head, check_bbox=check_bbox
                        )

        self._page.do_gui_refresh_all(force=True)

        self._page._gui_resource_prx_unit.do_gui_refresh_by_dcc_selection()

    def do_dcc_do_dcc_load_skin_proxies_by_selection(self):
        if self._load_skin_proxy_button.get_is_started() is False:
            resources = self._page._gui_resource_prx_unit.gui_get_selected_resources()
            if resources:
                self._skin_proxy_load_args_array = []
                create_cmds = []

                with self._window.gui_progressing(
                    maximum=len(resources), label='processing skin proxies'
                ) as g_p:
                    for i_resource in resources:
                        if i_resource.reference_opt.is_loaded() is False:
                            continue

                        i_opt = qsm_mya_anm_scripts.SkinProxyOpt(i_resource)
                        if i_opt.is_exists() is False:
                            i_task_name, i_cmd_script, i_cache_file, i_data_file_path = i_opt.generate_args()
                            if i_cmd_script is not None:
                                create_cmds.append(i_cmd_script)

                            self._skin_proxy_load_args_array.append(
                                (i_opt, i_cache_file, i_data_file_path)
                            )

                        g_p.do_update()

                if create_cmds:
                    mtd = gui_prx_scripts.GuiThreadWorker(self._window)
                    mtd.execute(self._load_skin_proxy_button, create_cmds)
                else:
                    self.do_dcc_load_skin_proxies()

    def do_dcc_remove_skin_proxies(self):
        resources = self._page._gui_resource_prx_unit.gui_get_selected_resources()
        if resources:
            for i_resource in resources:
                i_opt = qsm_mya_anm_scripts.SkinProxyOpt(i_resource)
                i_opt.remove_cache()

        self._page.do_gui_refresh_all(force=True)

        self._page._gui_resource_prx_unit.do_gui_refresh_by_dcc_selection()

    # dynamic gpu
    def do_dcc_load_dynamic_gpus(self):
        if self._dynamic_gpu_load_args_array:
            with self._window.gui_progressing(
                maximum=len(self._dynamic_gpu_load_args_array), label='load dynamic gpus'
            ) as g_p:
                for i_opt, i_cache_file in self._dynamic_gpu_load_args_array:
                    g_p.do_update()
                    if i_opt.is_resource_exists() is True:
                        i_opt.load_cache(i_cache_file)

    def do_dcc_do_dcc_load_dynamic_gpus_bt_selection(self):
        if self._load_dynamic_gpu_button.get_is_started() is False:
            resources = self._page._gui_resource_prx_unit.gui_get_selected_resources()
            if resources:
                self._dynamic_gpu_load_args_array = []
                create_cmds = []

                start_frame, end_frame = self._prx_options_node.get('setting.frame_range')
                use_motion = self._prx_options_node.get('dynamic_gpu.use_motion')
                with self._window.gui_progressing(
                    maximum=len(resources), label='processing dynamic gpus'
                ) as g_p:
                    for i_resource in resources:
                        if i_resource.reference_opt.is_loaded() is False:
                            continue

                        i_opt = qsm_mya_anm_scripts.DynamicGpuCacheOpt(i_resource)
                        if i_opt.is_exists() is False:
                            i_task_name, i_cmd_script, i_cache_file = i_opt.generate_args(
                                start_frame, end_frame, use_motion=use_motion
                            )
                            if i_cmd_script is not None:
                                create_cmds.append(i_cmd_script)

                            self._dynamic_gpu_load_args_array.append(
                                (i_opt, i_cache_file))
                        g_p.do_update()

                if create_cmds:
                    mtd = gui_prx_scripts.GuiThreadWorker(self._window)
                    mtd.execute(self._load_dynamic_gpu_button, create_cmds)
                else:
                    self.do_dcc_load_dynamic_gpus()

        self._page.do_gui_refresh_all(force=True)

    def do_dcc_remove_dynamic_gpus(self):
        resources = self._page._gui_resource_prx_unit.gui_get_selected_resources()
        if resources:
            for i_resource in resources:
                i_opt = qsm_mya_anm_scripts.DynamicGpuCacheOpt(i_resource)
                i_opt.remove_cache()

        self._page.do_gui_refresh_all(force=True)

    def do_gui_refresh_by_camera_changing(self):
        cameras = qsm_mya_core.Cameras.get_all()
        active_camera = qsm_mya_core.Camera.get_active()
        self._camera_port.set(
            cameras
        )
        self._camera_port.set(
            active_camera
        )

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

    def do_gui_load_active_camera(self):
        self.do_gui_refresh_by_camera_changing()

    def __init__(self, window, unit, session):
        super(ToolsetUnitForRigUtility, self).__init__(window, unit, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.rig.units.skin_proxy_and_dynamic_gpu_load.options')
            )
        )
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.rig.units.skin_proxy_and_dynamic_gpu_load.options.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='utility',
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.rig.units.skin_proxy_and_dynamic_gpu_load')
            ),
            icon_name_text='utility',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.rig.units.skin_proxy_and_dynamic_gpu_load')
            )
        )

        self._load_skin_proxy_button = self._prx_options_node.get_port('skin_proxy.load')
        self._load_skin_proxy_button.set(self.do_dcc_do_dcc_load_skin_proxies_by_selection)
        self._load_skin_proxy_button.connect_finished_to(self.do_dcc_load_skin_proxies)

        self._prx_options_node.set(
            'skin_proxy.remove', self.do_dcc_remove_skin_proxies
        )

        self._load_dynamic_gpu_button = self._prx_options_node.get_port('dynamic_gpu.load')
        self._load_dynamic_gpu_button.set(self.do_dcc_do_dcc_load_dynamic_gpus_bt_selection)
        self._load_dynamic_gpu_button.connect_finished_to(self.do_dcc_load_dynamic_gpus)

        self._prx_options_node.set(
            'dynamic_gpu.remove', self.do_dcc_remove_dynamic_gpus
        )
        self._prx_options_node.get_port('setting.frame_scheme').connect_input_changed_to(
            self.do_gui_refresh_by_frame_scheme_changing
        )

        self._camera_port = self._prx_options_node.get_port('setting.camera')
        self._fps_port = self._prx_options_node.get_port('setting.fps')
        self._frame_range_port = self._prx_options_node.get_port('setting.frame_range')

        self.do_gui_refresh_by_camera_changing()
        self.do_gui_refresh_fps()
        self.do_gui_refresh_by_dcc_frame_changing()

        self._prx_options_node.set(
            'setting.load_active_camera', self.do_gui_load_active_camera
        )

    def gui_get_frame_scheme(self):
        return self._prx_options_node.get('setting.frame_scheme')


class ToolsetUnitForRigSwitch(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    def do_dcc_skin_proxy_switch_to(self, key):
        if key == 'enable':
            _ = self._skin_proxy_dict.get('disable') or []
        else:
            _ = self._skin_proxy_dict.get('enable') or []

        for i in _:
            i.set_skin_proxy_enable(True if key == 'enable' else False)

        self.do_gui_refresh_buttons()

    def do_dcc_dynamic_gpu_switch_to(self, key):
        if key == 'enable':
            _ = self._dynamic_gpu_dict.get('disable') or []
        else:
            _ = self._dynamic_gpu_dict.get('enable') or []

        for i in _:
            i.set_dynamic_gpu_enable(True if key == 'enable' else False)

        self.do_gui_refresh_buttons()

    def __init__(self, window, unit, session):
        super(ToolsetUnitForRigSwitch, self).__init__(window, unit, session)
        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.rig.units.skin_proxy_and_dynamic_gpu_switch.options')
            )
        )
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.rig.units.skin_proxy_and_dynamic_gpu_switch.options.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='switch',
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.rig.units.skin_proxy_and_dynamic_gpu_switch')
            ),
            icon_name_text='switch',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.rig.units.skin_proxy_and_dynamic_gpu_switch')
            )
        )

        self._keys = ['enable', 'disable']

        self._skin_proxy_button_dict = {}
        self._skin_proxy_dict = {}

        for i_key in self._keys:
            i_b = self._prx_options_node.get_port(
                'switch.skin_proxy.{}'.format(i_key)
            )
            i_b.set(
                functools.partial(self.do_dcc_skin_proxy_switch_to, i_key)
            )
            self._skin_proxy_button_dict[i_key] = i_b

        self._dynamic_gpu_button_dict = {}
        self._dynamic_gpu_dict = {}

        for i_key in self._keys:
            i_b = self._prx_options_node.get_port(
                'switch.dynamic_gpu.{}'.format(i_key)
            )
            i_b.set(
                functools.partial(self.do_dcc_dynamic_gpu_switch_to, i_key)
            )
            self._dynamic_gpu_button_dict[i_key] = i_b

        self._prx_options_node.set(
            'selection.all', self.do_gui_selection_all_resources
        )

    def do_gui_refresh_buttons(self):
        namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
        resources = list(
            filter(None, [self._page._gui_resource_prx_unit.get_resources_query().get(x) for x in namespaces])
        )
        self.do_gui_refresh_buttons_for_skin_proxy(resources)
        self.do_gui_refresh_buttons_for_dynamic_gpu(resources)

    def do_gui_refresh_buttons_for_skin_proxy(self, resources):
        for k, i_b in self._skin_proxy_button_dict.items():
            i_b.set_status(
                i_b.ValidationStatus.Disable
            )
            i_b.set_sub_name(None)

        self._skin_proxy_dict = {}
        for i_resource in resources:
            i_path = i_resource.get_skin_proxy_location()
            if i_path is not None:
                if qsm_mya_core.NodeDisplay.is_visible(i_path) is True:
                    self._skin_proxy_dict.setdefault(
                        'enable', []
                    ).append(i_resource)
                else:
                    self._skin_proxy_dict.setdefault(
                        'disable', []
                    ).append(i_resource)

        for k, v in self._skin_proxy_dict.items():
            if k in self._skin_proxy_button_dict:
                i_c = len(v)
                i_b = self._skin_proxy_button_dict[k]
                i_b.set_status(
                    i_b.ValidationStatus.Enable
                )
                i_b.set_sub_name('({})'.format(i_c))

    def do_gui_refresh_buttons_for_dynamic_gpu(self, resources):
        for k, i_b in self._dynamic_gpu_button_dict.items():
            i_b.set_status(
                i_b.ValidationStatus.Disable
            )
            i_b.set_sub_name(None)

        self._dynamic_gpu_dict = {}
        for i_resource in resources:
            i_path = i_resource.get_dynamic_gpu_location()
            if i_path is not None:
                if qsm_mya_core.NodeDisplay.is_visible(i_path) is True:
                    self._dynamic_gpu_dict.setdefault(
                        'enable', []
                    ).append(i_resource)
                else:
                    self._dynamic_gpu_dict.setdefault(
                        'disable', []
                    ).append(i_resource)

        for k, v in self._dynamic_gpu_dict.items():
            if k in self._dynamic_gpu_button_dict:
                i_c = len(v)
                i_b = self._dynamic_gpu_button_dict[k]
                i_b.set_status(
                    i_b.ValidationStatus.Enable
                )
                i_b.set_sub_name('({})'.format(i_c))

    def do_gui_refresh_by_dcc_selection(self):
        if self._page.gui_get_tool_tab_current_key() == 'switch':
            self.do_gui_refresh_buttons()

    def do_gui_selection_all_resources(self):
        self._page._gui_resource_prx_unit.do_gui_select_all_resources()


class ToolsetUnitForRigExtend(
    qsm_mya_gui_core.PrxUnitBaseOpt
):
    def __init__(self, window, unit, session):
        super(ToolsetUnitForRigExtend, self).__init__(window, unit, session)

        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.rig.units.motion.options')
            )
        )
        self._prx_options_node.build_by_data(
            self._window._configure.get('build.rig.units.motion.options.parameters'),
        )
        self._page.gui_get_tool_tab_box().add_widget(
            self._prx_options_node,
            key='extend',
            name=gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get('build.rig.units.motion')
            ),
            icon_name_text='extend',
            tool_tip=gui_core.GuiUtil.choice_tool_tip(
                self._window._language, self._window._configure.get('build.rig.units.motion')
            )
        )
        # control
        self._prx_options_node.set(
            'control.enable_playback_visible', self.do_dcc_enable_control_playback_visible
        )
        self._prx_options_node.set(
            'control.disable_playback_visible', self.do_dcc_disable_control_playback_visible
        )
        # transformation
        self._prx_options_node.set(
            'transformation.create_transformation_locator', self.do_dcc_create_transformation_locator
        )

        self._prx_options_node.set(
            'transformation.remove_transformation_locator', self.do_dcc_remove_transformation_locator
        )

        # animation transfer
        self._prx_options_node.set(
            'animation_transfer.transfer_all', self.do_dcc_transfer_animation
        )
        self._prx_options_node.set(
            'animation_transfer.copy_all', self.do_dcc_copy_animation
        )
        self._prx_options_node.set(
            'animation_transfer.paste_all', self.do_dcc_paste_animation
        )

    def do_dcc_copy_animation(self):
        file_path = qsm_mya_gnl_core.ResourceCache.generate_animation_file(
            bsc_core.BscSystem.get_user_name()
        )
        namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
        if not namespaces:
            return
        adv_rig_query = self._page._gui_resource_prx_unit.get_resources_query()
        valid_namespaces = adv_rig_query.to_valid_namespaces(namespaces)
        if not valid_namespaces:
            return

        namespace = valid_namespaces[0]
        qsm_mya_mtn_core.AdvMotionOpt(namespace).export_data_to(
            file_path, part_includes=['body', 'face']
        )

    def do_dcc_paste_animation(self):
        file_path = qsm_mya_gnl_core.ResourceCache.generate_animation_file(
            bsc_core.BscSystem.get_user_name()
        )
        if bsc_storage.StgPath.get_is_file(file_path) is False:
            return
        namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
        if not namespaces:
            return
        adv_rig_query = self._page._gui_resource_prx_unit.get_resources_query()
        valid_namespaces = adv_rig_query.to_valid_namespaces(namespaces)
        if not valid_namespaces:
            return
        namespace = valid_namespaces[0]
        force = self._prx_options_node.get('animation_transfer.force')
        frame_offset = self._prx_options_node.get('animation_transfer.frame_offset')
        qsm_mya_mtn_core.AdvMotionOpt(namespace).import_data_from(
            file_path, frame_offset=frame_offset, force=force
        )

    def do_dcc_transfer_animation(self):
        namespaces = qsm_mya_core.Namespaces.extract_roots_from_selection()
        namespace_src, namespace_dst = None, None
        if namespaces:
            self._dynamic_gpu_load_args_array = []

            adv_rig_query = self._page._gui_resource_prx_unit.get_resources_query()
            valid_namespaces = adv_rig_query.to_valid_namespaces(namespaces)
            if len(valid_namespaces) >= 2:
                namespace_src = valid_namespaces[-2]
                namespace_dst = valid_namespaces[-1]

        if namespace_src is not None and namespace_dst is not None:
            w = gui_core.GuiDialog.create(
                label=self._session.gui_name,
                sub_label='transfer-animation',
                content='do you want transfer animation from "{}" to "{}"?,\n press "Ok" to continue'.format(
                    namespace_src, namespace_dst
                ),
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                parent=self._window.widget
            )

            result = w.get_result()
            if result is True:
                force = self._prx_options_node.get('animation_transfer.force')
                frame_offset = self._prx_options_node.get('animation_transfer.frame_offset')
                qsm_mya_mtn_core.AdvMotionOpt(namespace_src).transfer_to(
                    namespace_dst, frame_offset=frame_offset, force=force
                )

    def do_dcc_enable_control_playback_visible(self):
        resources = self._page._gui_resource_prx_unit.gui_get_selected_resources()
        if resources:
            for i_resource in resources:
                if i_resource.is_exists() is False:
                    continue
                i_namespace = i_resource.namespace
                i_controls = qsm_mya_mtn_core.AdvMotionOpt(i_namespace).find_all_controls()
                [qsm_mya_core.NodeAttribute.set_value(x, 'hideOnPlayback', 0) for x in i_controls]

    def do_dcc_disable_control_playback_visible(self):
        resources = self._page._gui_resource_prx_unit.gui_get_selected_resources()
        if resources:
            for i_resource in resources:
                if i_resource.is_exists() is False:
                    continue
                i_namespace = i_resource.namespace
                i_controls = qsm_mya_mtn_core.AdvMotionOpt(i_namespace).find_all_controls()
                [qsm_mya_core.NodeAttribute.set_value(x, 'hideOnPlayback', 1) for x in i_controls]

    def do_dcc_create_transformation_locator(self):
        resources = self._page._gui_resource_prx_unit.gui_get_selected_resources()
        if resources:
            namespaces = [x.namespace for x in resources]
            qsm_mya_anm_scripts.AdvTransformationLocatorOpt(namespaces).create_transformation_locators()

    def do_dcc_remove_transformation_locator(self):
        resources = self._page._gui_resource_prx_unit.gui_get_selected_resources()
        if resources:
            namespaces = [x.namespace for x in resources]
            qsm_mya_anm_scripts.AdvTransformationLocatorOpt(namespaces).remove_transformation_locators()

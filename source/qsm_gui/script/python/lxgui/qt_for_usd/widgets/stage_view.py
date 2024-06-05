# coding=utf-8
import functools

import six

import lxbasic.resource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgeneral.texture as gnl_texture
# usd
import lxusd.core as usd_core
# gui
from ... import core as gui_core
# qt
from ...qt import core as gui_qt_core

from ...qt import abstracts as gui_qt_abstracts
# qt widgets
from ...qt.widgets import button as gui_qt_wgt_button

from ...qt.widgets import container as gui_qt_wgt_container

from ...qt.widgets import scroll as gui_qt_wgt_scroll
# qt for usd
from ..core.wrap import *
#
from .. import core as gui_qt_usd_core


if QT_USD_FLAG is True:
    class QtUsdStageView(Usdviewq.stageView.StageView):
        def __init__(self, *args, **kwargs):
            super(QtUsdStageView, self).__init__(*args, **kwargs)

    # noinspection PyUnusedLocal,PyPep8Naming,PyMethodMayBeStatic
    class QtUsdStageWidget(
        QtWidgets.QWidget,
        #
        gui_qt_abstracts.AbsQtActionBaseDef,
        gui_qt_abstracts.AbsQtThreadBaseDef
    ):
        # noinspection PyUnresolvedReferences
        UsdQUtils = Usdviewq._usdviewq.Utils
        #
        RefinementComplexities = UsdAppUtils.complexityArgs.RefinementComplexities
        ColorCorrectionModes = Usdviewq.common.ColorCorrectionModes
        BusyContext = Usdviewq.common.BusyContext
        DumpMallocTags = Usdviewq.common.DumpMallocTags
        PickModes = Usdviewq.common.PickModes
        CameraMaskModes = Usdviewq.common.CameraMaskModes

        snapshot_finished = qt_signal()

        pre_geometry_snapshot_finished = qt_signal()

        def _start_thread_draw_(self):
            self._stageView.hide()
            self._stageView.setUpdatesEnabled(False)
            super(QtUsdStageWidget, self)._start_thread_draw_()

        def _stop_thread_draw_(self):
            self._stageView.show()
            self._stageView.setUpdatesEnabled(True)
            super(QtUsdStageWidget, self)._stop_thread_draw_()

        def __init__(self, *args, **kwargs):
            super(QtUsdStageWidget, self).__init__(*args, **kwargs)
            self.installEventFilter(self)
            self.setMaximumSize(166667, 166667)
            self._is_focused = False

            self._frame_draw_margins = 0, 0, 0, 0
            self._rect_frame_draw = QtCore.QRect()
            self._stage_view_draw_rect = QtCore.QRect()
            self._frame_border_color = gui_qt_core.QtBorderColors.Light
            self._hovered_frame_border_color = gui_qt_core.QtBorderColors.Hovered
            self._selected_frame_border_color = gui_qt_core.QtBorderColors.Selected
            self._frame_background_color = gui_qt_core.QtBackgroundColors.Dim
            layout_g = gui_qt_core.QtGridLayout(self)
            layout_g.setContentsMargins(2, 2, 2, 2)
            layout_g.setSpacing(0)

            self._main_button = gui_qt_wgt_button.QtIconMenuButton()
            layout_g.addWidget(self._main_button, 0, 0, 1, 1)
            self._main_button._set_icon_file_path_(
                gui_core.GuiIcon.get('application/usd')
            )
            self._main_button._set_menu_data_generate_fnc_(
                self._get_main_menu_data_
            )
            self._main_button.setFixedSize(28, 28)
            #
            self.__build_usd_var_()
            self.__build_top_tool_bar_(layout_g)
            self.__build_left_tool_bar_(layout_g)
            self.__build_usd_stage_view_(layout_g)
            #
            self.__build_top_tools_()
            self.__build_left_tools_()

            self._init_action_base_def_(self)
            self._init_thread_base_def_(self)

            m = gnl_texture.TxrMethodForBuild.generate_instance()
            self._texture_types = m.get_usd_includes()
            self._texture_type_mapper = m.get_usd_mapper()

        def _get_main_menu_data_(self):
            return [
                ('Export to', 'file/file', self._usd_export_to_file_),
            ]

        def _refresh_usd_stage_for_texture_preview_(
            self, texture_preview_assigns=None, use_acescg=False, use_as_imperfection=False
        ):
            self._usd_stage.Reload()
            root_layer = self._usd_stage.GetRootLayer()
            root_layer.subLayerPaths.append(
                bsc_resource.ExtendResource.get('assets/library/geometry/sphere.usda')
            )
            if use_acescg is True:
                root_layer.subLayerPaths.append(
                    bsc_resource.ExtendResource.get('assets/library/acescg-preview-material.usda')
                )
                root_layer.subLayerPaths.append(
                    bsc_resource.ExtendResource.get('assets/library/acescg-preview-light.usda')
                )
            else:
                root_layer.subLayerPaths.append(
                    bsc_resource.ExtendResource.get('assets/library/preview-material.usda')
                )
                root_layer.subLayerPaths.append(
                    bsc_resource.ExtendResource.get('assets/library/preview-light.usda')
                )
            #
            for i_usd_prim in usd_core.UsdStageOpt(self._usd_stage).get_all_mesh_objs():
                usd_core.UsdMaterialAssignOpt(
                    i_usd_prim
                ).assign(
                    self._usd_stage.GetPrimAtPath('/mtl_preview')
                )
            #
            if texture_preview_assigns:
                for i_texture_type in self._texture_types:
                    if i_texture_type in self._texture_type_mapper:
                        i_node_key = self._texture_type_mapper[i_texture_type]
                    else:
                        i_node_key = i_texture_type

                    i_usd_prim = self._usd_stage.GetPrimAtPath('/mtl_preview/txr_{}'.format(i_node_key))
                    if i_usd_prim.IsValid() is False:
                        continue

                    if i_texture_type in texture_preview_assigns:
                        i_texture_path = texture_preview_assigns[i_texture_type]
                        usd_core.UsdShaderOpt(i_usd_prim).set_file(i_texture_path)
                    else:
                        usd_core.UsdShaderOpt(i_usd_prim).set_file('')

        def _refresh_usd_stage_for_texture_render_(
            self, texture_preview_assigns=None, use_acescg=False
        ):
            self._usd_stage.Reload()
            root_layer = self._usd_stage.GetRootLayer()
            root_layer.subLayerPaths.append(
                bsc_resource.ExtendResource.get('assets/library/geometry/sphere.usda')
            )
            if use_acescg is True:
                root_layer.subLayerPaths.append(
                    bsc_resource.ExtendResource.get('assets/library/acescg-arnold-material.usda')
                )
                root_layer.subLayerPaths.append(
                    bsc_resource.ExtendResource.get('assets/library/acescg-arnold-light.usda')
                )
            else:
                root_layer.subLayerPaths.append(
                    bsc_resource.ExtendResource.get('assets/library/arnold-material.usda')
                )
                root_layer.subLayerPaths.append(
                    bsc_resource.ExtendResource.get('assets/library/arnold-light.usda')
                )
            #
            for i_usd_prim in usd_core.UsdStageOpt(self._usd_stage).get_all_mesh_objs():
                usd_core.UsdMaterialAssignOpt(
                    i_usd_prim
                ).assign(
                    self._usd_stage.GetPrimAtPath('/materials/mtl_arnold')
                )
                usd_core.UsdArnoldGeometryPropertiesOpt(
                    i_usd_prim
                ).set_properties(
                    dict(
                        smoothing=True,
                        # subdiv_type='catclark',
                        # subdiv_iterations=2
                    )
                )
            #
            if texture_preview_assigns:
                for i_texture_type in self._texture_types:
                    if i_texture_type in self._texture_type_mapper:
                        i_node_key = self._texture_type_mapper[i_texture_type]
                    else:
                        i_node_key = i_texture_type

                    i_prim = self._usd_stage.GetPrimAtPath('/materials/mtl_arnold/txr_{}'.format(i_node_key))
                    if i_prim.IsValid() is False:
                        continue

                    if i_texture_type in texture_preview_assigns:
                        i_texture_path = texture_preview_assigns[i_texture_type]
                        usd_core.UsdShaderOpt(i_prim).set_as_asset(
                            'filename', i_texture_path
                        )
                    else:
                        usd_core.UsdShaderOpt(i_prim).set_as_asset('filename', '')

            # usd_core.UsdStageOpt(self._usd_stage).export_to(
            #     '/data/e/myworkspace/td/lynxi/script/python/lxusd/.etc/usd_arnold_surface_test.usda'
            # )

        def _refresh_usd_stage_for_asset_preview_(
            self,
            usd_file,
            look_preview_usd_file=None,
            texture_preview_assigns=None,
            use_as_imperfection=False,
            hdri_file=None,
            use_as_hdri=False
        ):
            self._usd_stage.Reload()
            session_layer = self._usd_stage.GetSessionLayer()
            session_layer.Clear()

            root_layer = self._usd_stage.GetRootLayer()
            root_layer.subLayerPaths.append(usd_file)
            root_layer.subLayerPaths.append(
                bsc_resource.ExtendResource.get('assets/library/camera.usda')
            )
            self._usd_update_camera_()

            if look_preview_usd_file is not None:
                root_layer.subLayerPaths.append(look_preview_usd_file)
            #
            root_layer.subLayerPaths.append(
                bsc_resource.ExtendResource.get('assets/library/preview-light.usda')
            )
            if hdri_file is not None:
                usd_core.UsdLightOpt(
                    self._usd_stage.GetPrimAtPath('/lights/lgt_preview/lgt_env/lgt_env_shape')
                ).set_texture_file(
                    hdri_file
                )

            if use_as_hdri is True:
                usd_core.UsdXformOpt(
                    self._usd_stage.GetPrimAtPath('/lights/lgt_preview/lgt_key')
                ).set_visible(False)
                usd_core.UsdXformOpt(
                    self._usd_stage.GetPrimAtPath('/lights/lgt_preview/lgt_fill')
                ).set_visible(False)
            else:
                (x, y, z), (c_x, c_y, c_z), (w, h, d) = usd_core.UsdStageOpt(self._usd_stage).compute_geometry_args('/')

                usd_core.UsdXformOpt(
                    self._usd_stage.GetPrimAtPath('/lights/lgt_preview/lgt_key')
                ).set_matrix(
                    ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (w+25, h+25, d+25, 1))
                )

                usd_core.UsdXformOpt(
                    self._usd_stage.GetPrimAtPath('/lights/lgt_preview/lgt_fill')
                ).set_matrix(
                    ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (-w-50, h/2, -d-25, 1))
                )

            # light_prim = self._usd_stage.GetPrimAtPath('/lights/lgt_preview/lgt_key/lgt_key_shape')
            # light_opt = usd_core.UsdLightOpt(light_prim)
            # light_opt.set_shadow_enable(True)
            #
            for i_usd_prim in usd_core.UsdStageOpt(self._usd_stage).get_all_mesh_objs():
                i_material_prim = self._usd_stage.GetPrimAtPath('/mtl_preview')
                if i_material_prim.IsValid() is True:
                    usd_core.UsdMaterialAssignOpt(
                        i_usd_prim
                    ).assign(
                        self._usd_stage.GetPrimAtPath('/mtl_preview')
                    )
            #
            texture_assigns = texture_preview_assigns or {}
            for i_texture_type in self._texture_types:
                if i_texture_type in self._texture_type_mapper:
                    i_node_key = self._texture_type_mapper[i_texture_type]
                else:
                    i_node_key = i_texture_type

                i_usd_prim = self._usd_stage.GetPrimAtPath('/mtl_preview/txr_{}'.format(i_node_key))
                if i_usd_prim.IsValid() is False:
                    continue

                if i_texture_type in texture_assigns:
                    i_texture_path = texture_assigns[i_texture_type]
                    usd_core.UsdShaderOpt(i_usd_prim).set_file(i_texture_path)
                else:
                    usd_core.UsdShaderOpt(i_usd_prim).set_file('')
            #
            if use_as_imperfection is True:
                shader_opt = usd_core.UsdShaderOpt(
                    self._usd_stage.GetPrimAtPath('/mtl_preview/mtl_shader')
                )
                shader_opt.set_as_float('ior', .470)
                shader_opt.set_as_float('metallic', 1.0)
                # no diffuse
                if 'diffuse_color' not in texture_preview_assigns:
                    diffuse_opt = usd_core.UsdShaderOpt(
                        self._usd_stage.GetPrimAtPath('/mtl_preview/txr_diffuse_color')
                    )
                    if 'specular_roughness' in texture_preview_assigns:
                        diffuse_opt.set_file(texture_preview_assigns['specular_roughness'])
                    elif 'glossiness' in texture_preview_assigns:
                        # todo: diffuse value error
                        diffuse_opt.set_as_float4('scale', (-1.0, -1.0, -1.0, 1.0))
                        diffuse_opt.set_as_float4('bias', (1.0, 1.0, 1.0, 1.0))
                        diffuse_opt.set_file(texture_preview_assigns['glossiness'])
                # no roughness but hs glossiness
                if 'specular_roughness' not in texture_preview_assigns and 'glossiness' in texture_preview_assigns:
                    roughness_opt = usd_core.UsdShaderOpt(
                        self._usd_stage.GetPrimAtPath('/mtl_preview/txr_specular_roughness')
                    )
                    roughness_opt.set_as_float4('scale', (-1.0, -1.0, -1.0, 1.0))
                    roughness_opt.set_as_float4('bias', (1.0, 1.0, 1.0, 1.0))
                    roughness_opt.set_file(
                        texture_preview_assigns['glossiness']
                    )
                # has coat_roughness
                if 'coat_roughness' in texture_preview_assigns:
                    shader_opt.set_as_float('clearcoat', 1.0)
            #
            if use_as_hdri is True:
                shader_opt = usd_core.UsdShaderOpt(
                    self._usd_stage.GetPrimAtPath('/mtl_preview/mtl_shader')
                )
                shader_opt.set_as_float('ior', .470)
                shader_opt.set_as_float('metallic', 1.0)
                shader_opt.disconnect_input_at('roughness')
                shader_opt.set_as_float('roughness', 0.0)
                shader_opt.disconnect_input_at('diffuseColor')
                shader_opt.set_as_rgb('diffuseColor', (1, 1, 1))

        def _refresh_usd_stage_for_asset_render_(
            self, usd_file, texture_preview_assigns=None, use_acescg=False
        ):
            self._usd_stage.Reload()
            root_layer = self._usd_stage.GetRootLayer()
            root_layer.subLayerPaths.append(usd_file)
            root_layer.subLayerPaths.append(
                bsc_resource.ExtendResource.get('assets/library/camera.usda')
            )
            self._usd_update_camera_()
            #
            if use_acescg is True:
                root_layer.subLayerPaths.append(
                    bsc_resource.ExtendResource.get('assets/library/acescg-arnold-material.usda')
                )
                root_layer.subLayerPaths.append(
                    bsc_resource.ExtendResource.get('assets/library/acescg-arnold-light.usda')
                )
            else:
                root_layer.subLayerPaths.append(
                    bsc_resource.ExtendResource.get('assets/library/arnold-material.usda')
                )
                root_layer.subLayerPaths.append(
                    bsc_resource.ExtendResource.get('assets/library/arnold-light.usda')
                )
            #
            # (x, y, z), (c_x, c_y, c_z), (w, h, d) = usd_core.UsdStageOpt(self._usd_stage).compute_geometry_args('/')
            #
            # usd_core.UsdXformOpt(
            #     self._usd_stage.GetPrimAtPath('/lights/lgt_render/lgt_key')
            # ).set_matrix(
            #     ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (w+100, w+100, w+50, 1))
            # )
            #
            # usd_core.UsdXformOpt(
            #     self._usd_stage.GetPrimAtPath('/lights/lgt_render/lgt_fill')
            # ).set_matrix(
            #     ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (-w-25, 25, 0, 1))
            # )
            #
            for i_usd_prim in usd_core.UsdStageOpt(self._usd_stage).get_all_mesh_objs():
                usd_core.UsdMaterialAssignOpt(
                    i_usd_prim
                ).assign(
                    self._usd_stage.GetPrimAtPath('/materials/mtl_arnold')
                )
                usd_core.UsdArnoldGeometryPropertiesOpt(
                    i_usd_prim
                ).set_properties(
                    dict(
                        smoothing=True,
                        # subdiv_type='catclark',
                        # subdiv_iterations=2
                    )
                )
            #
            if texture_preview_assigns:
                for i_texture_type in self._texture_types:
                    if i_texture_type in self._texture_type_mapper:
                        i_node_key = self._texture_type_mapper[i_texture_type]
                    else:
                        i_node_key = i_texture_type

                    i_prim = self._usd_stage.GetPrimAtPath('/materials/mtl_arnold/txr_{}'.format(i_node_key))
                    if i_prim.IsValid() is False:
                        continue

                    if i_texture_type in texture_preview_assigns:
                        i_texture_path = texture_preview_assigns[i_texture_type]
                        usd_core.UsdShaderOpt(i_prim).set_as_asset(
                            'filename', i_texture_path
                        )
                    else:
                        usd_core.UsdShaderOpt(i_prim).set_as_asset(
                            'filename', ''
                        )

            # usd_core.UsdStageOpt(self._usd_stage).export_to(
            #     '/data/e/myworkspace/td/lynxi/script/python/lxusd/.etc/usd_arnold_render.usda'
            # )

        def _load_usd_file_(self, usd_file):
            self._usd_stage.Reload()
            session_layer = self._usd_stage.GetSessionLayer()
            session_layer.Clear()
            if usd_file is None:
                return

            root_layer = self._usd_stage.GetRootLayer()
            root_layer.subLayerPaths.append(usd_file)
            root_layer.subLayerPaths.append(
                bsc_resource.ExtendResource.get('assets/library/camera.usda')
            )
            self._usd_update_camera_()

        def _restore_(self):
            self._dataModel.selection.clear()

            self._usd_stage.Reload()
            session_layer = self._usd_stage.GetSessionLayer()
            session_layer.Clear()

        def _usd_update_camera_(self):
            (x, y, z), (c_x, c_y, c_z), (w, h, d) = usd_core.UsdStageOpt(self._usd_stage).compute_geometry_args('/')
            # side-x
            (t_x, t_y, t_z), (r_x, r_y, r_z), (s_x, s_y, s_z) = bsc_core.CameraMtd.compute_front_transformation(
                geometry_args=((z, y, x), (c_z, c_y, c_x), (d, h, w)),
                angle=1,
                bottom=True
            )
            usd_core.UsdXformOpt(
                self._usd_stage.GetPrimAtPath('/cameras/cam_side/cam_side_shape')
            ).set_matrix(
                ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (t_x, t_y, t_z, 1))
            )
            # top-y
            (t_x, t_y, t_z), (r_x, r_y, r_z), (s_x, s_y, s_z) = bsc_core.CameraMtd.compute_front_transformation(
                geometry_args=((x, -z, y), (c_x, -c_z, c_y), (w, d, h)),
                angle=1,
            )
            usd_core.UsdXformOpt(
                self._usd_stage.GetPrimAtPath('/cameras/cam_top/cam_top_shape')
            ).set_matrix(
                ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (t_x, t_y, t_z, 1))
            )
            # front-z
            (t_x, t_y, t_z), (r_x, r_y, r_z), (s_x, s_y, s_z) = bsc_core.CameraMtd.compute_front_transformation(
                geometry_args=((x, y, z), (c_x, c_y, c_z), (w, h, d)),
                angle=1,
                bottom=True
            )
            usd_core.UsdXformOpt(
                self._usd_stage.GetPrimAtPath('/cameras/cam_front/cam_front_shape')
            ).set_matrix(
                ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (t_x, t_y, t_z, 1))
            )

        def _update_usd_stage_(self):
            self._stageView.setUpdatesEnabled(False)
            # self._dataModel.stage = self._usd_stage
            self._resetSettings()
            self._resetView()
            self._stageView.setUpdatesEnabled(True)
            # self._frameSelection()

        # ============================================================================================================ #
        def __open_usd_stage_(self, usd_stage):
            self._stageView.setUpdatesEnabled(False)
            self._usd_stage = usd_stage
            # light_xform_prim = self._usd_stage.DefinePrim('/test_light', 'Xform')
            # light_prim = self._usd_stage.DefinePrim('/test_light/test_light_shape', 'SphereLight')
            # light = UsdLux.DomeLight(light_prim)
            # light.CreateIntensityAttr().Set(5)
            # light.CreateExposureAttr().Set(1.0)
            # light.CreateTextureFileAttr().Set("/data/e/myworkspace/td/lynxi/script/python/lxusd/.etc/lgt/stinson-beach.jpg")
            # #
            # shaping_api = UsdLux.ShapingAPI(light_prim)
            # shaping_api.CreateShapingFocusAttr().Set(2.0)
            # UsdGeom.Xformable(light_xform_prim).MakeMatrixXform().Set(
            #     Gf.Matrix4d(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (100, 100, 100, 1)))
            # )
            #
            self._dataModel.stage = self._usd_stage
            self._stageView.setUpdatesEnabled(True)
            #
            self._stageView.updateView(forceComputeBBox=True)
            self._frameSelection()

        # usd fnc
        def onPrimSelected(self, path, instanceIndex, topLevelPath, topLevelInstanceIndex, point, button, modifiers):
            # Ignoring middle button until we have something
            # meaningfully different for it to do
            if button in [QtCore.Qt.LeftButton, QtCore.Qt.RightButton]:
                # Expected context-menu behavior is that even with no
                # modifiers, if we are activating on something already selected,
                # do not change the selection
                doContext = (button == QtCore.Qt.RightButton and path
                             and path != Sdf.Path.emptyPath)
                doSelection = True
                if doContext:
                    for selPrim in self._dataModel.selection.getPrims():
                        selPath = selPrim.GetPath()
                        if (selPath != Sdf.Path.absoluteRootPath and
                                path.HasPrefix(selPath)):
                            doSelection = False
                            break
                if doSelection:
                    self._dataModel.selection.setPoint(point)

                    shiftPressed = modifiers&QtCore.Qt.ShiftModifier
                    ctrlPressed = modifiers&QtCore.Qt.ControlModifier

                    if path != Sdf.Path.emptyPath:
                        prim = self._dataModel.stage.GetPrimAtPath(path)

                        # Model picking ignores instancing, but selects the enclosing
                        # model of the picked prim.
                        if self._dataModel.viewSettings.pickMode == self.PickModes.MODELS:
                            if prim.IsModel():
                                model = prim
                            else:
                                model = Usdviewq.common.GetEnclosingModelPrim(prim)
                            if model:
                                prim = model
                            instanceIndex = -1

                        # Prim picking selects the top level boundable: either the
                        # gprim, the top-level point instancer (if it's point
                        # instanced), or the top level USD instance (if it's marked
                        # instantiable), whichever is closer to namespace root.
                        # It discards the instance index.
                        elif self._dataModel.viewSettings.pickMode == self.PickModes.PRIMS:
                            topLevelPrim = self._dataModel.stage.GetPrimAtPath(topLevelPath)
                            if topLevelPrim:
                                prim = topLevelPrim
                            while prim.IsInstanceProxy():
                                prim = prim.GetParent()
                            instanceIndex = -1

                        # Instance picking selects the top level boundable, like
                        # prim picking; but if that prim is a point instancer or
                        # a USD instance, it selects the particular instance
                        # containing the picked object.
                        elif self._dataModel.viewSettings.pickMode == self.PickModes.INSTANCES:
                            topLevelPrim = self._dataModel.stage.GetPrimAtPath(topLevelPath)
                            if topLevelPrim:
                                prim = topLevelPrim
                                instanceIndex = topLevelInstanceIndex
                            if prim.IsInstanceProxy():
                                while prim.IsInstanceProxy():
                                    prim = prim.GetParent()
                                instanceIndex = -1

                        # Prototype picking selects a specific instance of the
                        # actual picked gprim, if the gprim is point-instanced.
                        # This differs from instance picking by selecting the gprim,
                        # rather than the prototype subtree; and selecting only one
                        # drawn instance, rather than all sub-instances of a top-level
                        # instance (for nested point instancers).
                        # elif self._dataModel.viewSettings.pickMode == PickModes.PROTOTYPES:
                        # Just pass the selection info through!

                        if shiftPressed:
                            # Clicking prim while holding shift adds it to the
                            # selection.
                            self._dataModel.selection.addPrim(prim, instanceIndex)
                        elif ctrlPressed:
                            # Clicking prim while holding ctrl toggles it in the
                            # selection.
                            self._dataModel.selection.togglePrim(prim, instanceIndex)
                        else:
                            # Clicking prim with no modifiers sets it as the
                            # selection.
                            self._dataModel.selection.switchToPrimPath(
                                prim.GetPath(), instanceIndex
                            )

                    elif not shiftPressed and not ctrlPressed:
                        # Clicking the background with no modifiers clears the
                        # selection.
                        self._dataModel.selection.clear()

                    self._stageView.updateView(forceComputeBBox=True)

                if doContext:
                    item = self._getItemAtPath(path)
                    self._showPrimContextMenu(item)

                    # context menu steals mouse release event from the StageView.
                    # We need to give it one so it can track its interaction
                    # mode properly
                    mrEvent = QtGui.QMouseEvent(
                        QtCore.QEvent.MouseButtonRelease,
                        QtGui.QCursor.pos(),
                        QtCore.Qt.RightButton,
                        QtCore.Qt.MouseButtons(QtCore.Qt.RightButton),
                        QtCore.Qt.KeyboardModifiers()
                    )
                    QtWidgets.QApplication.sendEvent(self._stageView, mrEvent)

        def _getItemAtPath(self, path, ensureExpanded=False):
            # If the prim hasn't been expanded yet, drill down into it.
            # Note the explicit str(path) in the following expr is necessary
            # because path may be a QString.
            path = path if isinstance(path, Sdf.Path) else Sdf.Path(str(path))
            parent = self._dataModel.stage.GetPrimAtPath(path)
            if not parent:
                raise RuntimeError("Prim not found at path in stage: %s"%str(path))
            pseudoRoot = self._dataModel.stage.GetPseudoRoot()
            if parent not in self._primToItemMap:
                # find the first loaded parent
                childList = []

                while parent != pseudoRoot \
                        and parent not in self._primToItemMap:
                    childList.append(parent)
                    parent = parent.GetParent()

                # go one step further, since the first item found could be hidden
                # under a norgie and we would want to populate its siblings as well
                if parent != pseudoRoot:
                    childList.append(parent)

                # now populate down to the child
                for parent in reversed(childList):
                    try:
                        item = self._primToItemMap[parent]
                        self._populateChildren(item)
                        if ensureExpanded:
                            item.setExpanded(True)
                    except:
                        item = None

            # finally, return the requested item, which now should be in
            # the map. If something has been added, this can fail. Not
            # sure how to rebuild or add this to the map in a minimal way,
            # but after the first hiccup, I don't see any ill
            # effects. Would love to know a better way...
            # - wave 04.17.2018
            prim = self._dataModel.stage.GetPrimAtPath(path)
            try:
                item = self._primToItemMap[prim]
            except:
                item = None
            return item

        def _showPrimContextMenu(self, item):
            self.contextMenu = Usdviewq.primContextMenu.PrimContextMenu(self, item, self)
            self.contextMenu.exec_(QtGui.QCursor.pos())

        def _resetSettings(self):
            """Reloads the UI and Sets up the initial settings for the
            _stageView object created in _reloadVaryingUI"""

            # Seems like a good time to clear the texture registry
            Glf.TextureRegistry.Reset()

            if self._stageView:
                self._stageView.update()

            if self._stageView:
                self._stageView.signalSwitchedToFreeCam.connect(lambda: self._cameraSelectionChanged(None))

        def _resetView(self, selectPrim=None):
            """ Reverts the GL frame to the initial camera view,
            and clears selection (sets to pseudoRoot), UNLESS 'selectPrim' is
            not None, in which case we'll select and frame it."""
            pRoot = self._dataModel.stage.GetPseudoRoot()
            if selectPrim is None:
                # if we had a command-line specified selection, re-frame it
                selectPrim = self._initialSelectPrim or pRoot

            if self._stageView:
                if (selectPrim and selectPrim != pRoot) or not self._startingPrimCamera:
                    # _frameSelection translates the camera from wherever it happens
                    # to be at the time.  If we had a starting selection AND a
                    # primCam, then before framing, switch back to the prim camera
                    if selectPrim == self._initialSelectPrim and self._startingPrimCamera:
                        self._dataModel.viewSettings.cameraPrim = self._startingPrimCamera
                    self._frameSelection()
                else:
                    self._dataModel.viewSettings.cameraPrim = self._startingPrimCamera
                    self._stageView.updateView()

        def onRollover(self, *args, **kwargs):
            pass

        def onStageViewMouseDrag(self, *args, **kwargs):
            pass

        def statusMessage(self, *args, **kwargs):
            pass

        def _storeAndReturnViewState(self):
            lastView = self._lastViewContext
            self._lastViewContext = self._stageView.copyViewState()
            return lastView

        def _frameSelection(self):
            if self._stageView:
                self._storeAndReturnViewState()
                self._stageView.updateView(resetCam=True, forceComputeBBox=True, frameFit=1.25)

        def _viewSettingChanged(self):
            # self._refreshViewMenubar()
            # self._displayPurposeChanged()
            # self._HUDInfoChanged()
            pass

        def _cameraSelectionChanged(self, camera):
            self._dataModel.viewSettings.cameraPrim = camera

        def _rendererPluginChanged(self, plugin):
            if self._stageView.SetRendererPlugin(plugin) is True:
                pass
                # self._configureRendererAovs()
                # self._configureRendererSettings()
                # self._configurePauseAction()
                # self._configureStopAction()

        # ================================================================================================================ #
        def __build_usd_stage_view_(self, layout):
            self._stageView = QtUsdStageView(
                parent=self,
                dataModel=self._dataModel,
                printTiming=self._printTiming
            )
            layout.addWidget(self._stageView, 1, 1, 1, 1)
            # self._stageView.setUpdatesEnabled(False)
            self._usd_model = gui_qt_usd_core.UsdModel(self._dataModel, self._stageView)

            self._stageView.fpsHUDInfo = self._fpsHUDInfo
            self._stageView.fpsHUDKeys = self._fpsHUDKeys
            self._stageView.upperHUDInfo = self._upperHUDInfo
            self._stageView.setFocusProxy(self)
            self.setFocusPolicy(QtCore.Qt.ClickFocus)

            self._stageView.signalPrimSelected.connect(self.onPrimSelected)
            self._stageView.signalPrimRollover.connect(self.onRollover)
            self._stageView.signalMouseDrag.connect(self.onStageViewMouseDrag)
            self._stageView.signalErrorMessage.connect(self.statusMessage)
            self._stageView.setFocus(QtCore.Qt.TabFocusReason)
            self._stageView.setAttribute(QtCore.Qt.WA_TranslucentBackground)

            # self._stageView._renderParams.overrideColor = Gf.Vec4f(1.0, 1.0, 1.0, 1.0)

            self._usd_stage = Usd.Stage.CreateInMemory()

            self._usd_lights = []

            self._usd_stage.SetEditTarget(self._usd_stage.GetSessionLayer())
            self._dataModel.stage = self._usd_stage

            self._dataModel.viewSettings.__dict__['clearColor'] = (0.0275, 0.0275, 0.0275, 1)
            self._dataModel.viewSettings.showBBoxes = False

            self._dataModel.viewSettings.autoComputeClippingPlanes = True
            # self._dataModel.viewSettings.freeCamera.overrideNear = 0.1
            # self._dataModel.viewSettings.freeCamera.overrideFar = 10000
            self._dataModel.viewSettings.freeCameraFOV = 35
            #
            self._dataModel.viewSettings.ambientLightOnly = False
            self._dataModel.viewSettings.domeLightEnabled = False
            #
            self._dataModel.viewSettings.displayRender = True
            self._dataModel.viewSettings.displayProxy = False
            self._dataModel.viewSettings.displayGuide = False
            # self._dataModel.viewSettings.cullBackfaces = True
            #
            self._dataModel.viewSettings.enableSceneLights = True
            # self._dataModel.viewSettings.showHUD_GPUstats = True
            self._dataModel.viewSettings.showHUD = False
            #
            self._freeCamera = Usdviewq.freeCamera.FreeCamera(
                False, self._dataModel.viewSettings.freeCameraFOV
            )
            self._dataModel.viewSettings.freeCamera = self._freeCamera
            self._dataModel.viewSettings.cameraMaskMode = self.CameraMaskModes.NONE

            self._dataModel.viewSettings.signalSettingChanged.connect(
                self._viewSettingChanged
            )

            self._stageView.rolloverPicking = self._dataModel.viewSettings.rolloverPrimInfo

            self._stageView.signalSwitchedToFreeCam.connect(
                lambda: self._cameraSelectionChanged(None)
            )

            # self._freeCamera.rotPhi = 45

            # self._refresh_usd_stage_for_texture_preview_()

        def _get_usd_model_(self):
            return self._usd_model

        # ================================================================================================================ #
        def _usd_complete_menu_data_by_prim_visibility_(self, menu_data, prims):
            def check_fnc_(opt_):
                return opt_.get_is_visible()

            def toggle_fnc_(opt_):
                opt_.swap_visibility()
                self._stageView.update()

            def enable_fnc_():
                return self._usd_model.get_scene_lights_is_enable()

            #
            for i_prim in prims:
                i_opt = usd_core.UsdStapeOpt(i_prim)
                i_name = i_opt.get_primvar('gui:name') or i_prim.GetName()
                menu_data.append(
                    (
                        i_name, 'box-check',
                        (
                            # check
                            functools.partial(check_fnc_, i_opt),
                            # toggle
                            functools.partial(toggle_fnc_, i_opt),
                            # enable
                            enable_fnc_
                        )
                    )
                )

        def _usd_get_all_geometry_prims_(self):
            return self.UsdQUtils._GetAllPrimsOfType(
                self._dataModel.stage, Tf.Type.Find(UsdGeom.PointBased)
            )

        def _usd_get_all_mesh_prims_(self):
            return self.UsdQUtils._GetAllPrimsOfType(
                self._dataModel.stage, Tf.Type.Find(UsdGeom.Mesh)
            )

        def _usd_get_all_camera_prims_(self):
            return self.UsdQUtils._GetAllPrimsOfType(
                self._dataModel.stage, Tf.Type.Find(UsdGeom.Camera)
            )

        def _usd_get_all_light_prims_(self):
            return self.UsdQUtils._GetAllPrimsOfType(
                self._dataModel.stage, Tf.Type.Find(UsdLux.Light)
            )

        @classmethod
        def _usd_reset_session_visible_(cls, stage):
            def rcs_fnc_(p_):
                try:
                    p_.RemoveProperty(p_.attributes[UsdGeom.Tokens.visibility])
                except IndexError:
                    pass
                for _i_c in p_.nameChildren:
                    rcs_fnc_(_i_c)

            session = stage.GetSessionLayer()
            with Sdf.ChangeBlock():
                rcs_fnc_(session.pseudoRoot)

        def _usd_hide_all_geometry_(self):
            prims = self._usd_get_all_geometry_prims_()
            for i_p in prims:
                UsdGeom.Imageable(i_p).MakeInvisible()

        def _usd_do_geometry_isolate_selection_(self):
            with self.BusyContext():
                self._usd_clear_session_visible_()
                self._usd_hide_all_geometry_()
                #
                for i_prim in self._dataModel.selection.getPrims():
                    fnc = UsdGeom.Imageable(i_prim)
                    if fnc:
                        fnc.MakeVisible()

                self._refresh_usd_view_()

        def _usd_do_clear_geometry_isolate_selection_(self):
            with self.BusyContext():
                self._usd_clear_session_visible_()
                self._refresh_usd_view_()

        def _usd_toggle_visible_texture_(self, boolean):
            pass

        def _usd_set_material_enable_(self, boolean):
            self._dataModel.viewSettings.enableSceneMaterials = boolean

        def _usd_swap_material_visible_(self, path):
            pass

        def _usd_get_material_menu_data_(self):
            return []

        def _usd_get_display_purpose_menu_data_(self):
            def get_is_enable_fnc_(key_):
                return self._dataModel.viewSettings.__dict__[key_]

            def swap_enable_fnc_(key_):
                self._dataModel.viewSettings.__dict__[key_] = not self._dataModel.viewSettings.__dict__[key_]
                self._stageView.update()

            list_ = []
            for i_name, i_key in [
                ('Guide', '_displayGuide'),
                ('Proxy', '_displayProxy'),
                ('Render', '_displayRender')
            ]:
                list_.append(
                    (
                        i_name, 'box-check',
                        (
                            functools.partial(get_is_enable_fnc_, i_key),
                            functools.partial(swap_enable_fnc_, i_key)
                        )
                    )
                )
            return list_

        # environment
        def _usd_set_environment_current_(self, key):
            self._usd_environment_cur = key
            prim = self._usd_stage.GetPrimAtPath(
                '/lights/lgt_render/lgt_env/lgt_env_shape'
            )
            usd_core.UsdLightOpt(prim).set_texture_file(
                bsc_resource.ExtendResource.get('assets/library/light/acescg/tx/{}.tx'.format(key))
            )

        def _usd_get_environment_current_is_(self, key):
            return self._usd_environment_cur == key

        def _usd_get_environment_menu_data_(self):
            list_ = []
            for i_name, i_key in [
                ('Stinson Beach', 'stinson-beach'),
                ('Malibu Overlook', 'malibu-overlook'),
                ('Mono Lake', 'mono-lake'),
                ('Skies Com', 'skies-com'),
                ('Kloofendal Partly Cloudy Puresky', 'kloofendal-partly-cloudy-puresky'),
            ]:
                list_.append(
                    (
                        i_name, 'radio-check',
                        (
                            functools.partial(self._usd_get_environment_current_is_, i_key),
                            functools.partial(self._usd_set_environment_current_, i_key)
                        )
                    )
                )
            return list_

        # light
        def _usd_get_light_menu_data_(self):
            list_ = [
                (
                    'Camera', 'box-check',
                    (
                        self._usd_model.get_camera_light_is_enable, self._usd_model.swap_camera_light_enable
                    ),
                ),
                (
                    'Dome', 'box-check',
                    (
                        self._usd_model.get_dome_light_is_enable, self._usd_model.swap_dome_light_enable
                    )
                ),
                (
                    'Scene', 'box-check',
                    (
                        self._usd_model.get_scene_lights_is_enable, self._usd_model.swap_scene_lights_enable
                    )
                ),
                (),
            ]
            prims = self._usd_get_all_light_prims_()
            self._usd_complete_menu_data_by_prim_visibility_(list_, prims)
            return list_

        # color space
        def _usd_get_color_space_menu_data_(self):
            return [
                (
                    'sRGB', 'radio-check',
                    (
                        lambda: self._usd_model.get_color_space_mode() == self.ColorCorrectionModes.SRGB,
                        functools.partial(self._usd_model.set_color_space_mode, self.ColorCorrectionModes.SRGB)
                    )
                ),
                (
                    'openColorIO', 'radio-check',
                    (
                        lambda: self._usd_model.get_color_space_mode() == self.ColorCorrectionModes.OPENCOLORIO,
                        functools.partial(self._usd_model.set_color_space_mode, self.ColorCorrectionModes.OPENCOLORIO)
                    )
                ),
            ]

        # camera
        def _usd_set_camera_current_(self, prim):
            if prim is None:
                self._dataModel.viewSettings.freeCamera = self._freeCamera
            self._usd_camera_cur = prim
            self._dataModel.viewSettings.cameraPrim = prim

        def _usd_switch_camera_to_(self, *args):
            _ = args[0]
            if isinstance(_, six.string_types):
                prim = self._usd_stage.GetPrimAtPath(_)
            else:
                prim = _
            if prim.IsValid():
                self._usd_set_camera_current_(prim)

        def _usd_isolate_select_geometry_to_(self, *args):
            _ = args[0]
            if isinstance(_, six.string_types):
                prim = self._usd_stage.GetPrimAtPath(_)
            else:
                prim = _

            if prim.IsValid():
                fnc = UsdGeom.Imageable(prim)
                if fnc:
                    self._usd_clear_session_visible_()
                    self._usd_hide_all_geometry_()
                    fnc.MakeVisible()

        def _usd_clear_session_visible_(self):
            self._usd_reset_session_visible_(self._usd_stage)

        def _usd_get_camera_current_is_(self, prim):
            return self._usd_camera_cur == prim

        def _usd_get_camera_current_(self):
            return self._usd_camera_cur

        def _usd_get_camera_menu_data_(self):
            list_ = [
                (
                    'Free', 'radio-check',
                    (
                        lambda: self._usd_camera_cur is None,
                        functools.partial(self._usd_set_camera_current_, None)
                    )
                ),
                (),
            ]
            prims = self._usd_get_all_camera_prims_()
            for i_prim in prims:
                i_opt = usd_core.UsdStapeOpt(i_prim)
                i_name = i_opt.get_primvar('gui:name') or i_prim.GetName()
                list_.append(
                    (
                        i_name, 'radio-check',
                        (
                            functools.partial(self._usd_get_camera_current_is_, i_prim),
                            functools.partial(self._usd_set_camera_current_, i_prim)
                        )
                    )
                )
            return list_

        # renderer
        def _usd_get_renderer_menu_data_(self):
            list_ = []
            renderer_plugins = self._stageView.GetRendererPlugins()
            renderer_plugin_cur = self._stageView.GetCurrentRendererId()
            for i_renderer_plugin in renderer_plugins:
                i_name = self._stageView.GetRendererDisplayName(i_renderer_plugin)
                if i_renderer_plugin == renderer_plugin_cur:
                    list_.append(
                        (i_name, 'radio-check',
                         (True, functools.partial(self._rendererPluginChanged, i_renderer_plugin)))
                    )
                else:
                    list_.append(
                        (i_name, 'radio-check',
                         (False, functools.partial(self._rendererPluginChanged, i_renderer_plugin)))
                    )
            return list_

        # complexity
        def _usd_update_complexity_mode_(self, value):
            self._usd_complexity_mode = value
            if self._usd_complexity_enable is True:
                self._dataModel.viewSettings.complexity = self._usd_complexity_mode
            else:
                self._dataModel.viewSettings.complexity = self.RefinementComplexities.LOW

        def _usd_set_complexity_enable_(self, boolean):
            self._usd_complexity_enable = boolean
            self._usd_update_complexity_mode_(
                self._usd_complexity_mode
            )

        def _usd_get_complexity_menu_data_(self):
            return [
                (
                    'Medium', 'radio-check',
                    (
                        lambda: self._usd_complexity_mode == self.RefinementComplexities.MEDIUM,
                        functools.partial(self._usd_update_complexity_mode_, self.RefinementComplexities.MEDIUM)
                    )
                ),
                (
                    'High', 'radio-check',
                    (
                        lambda: self._usd_complexity_mode == self.RefinementComplexities.HIGH,
                        functools.partial(self._usd_update_complexity_mode_, self.RefinementComplexities.HIGH)
                    )
                ),
                (
                    'Very High', 'radio-check',
                    (
                        lambda: self._usd_complexity_mode == self.RefinementComplexities.VERY_HIGH,
                        functools.partial(self._usd_update_complexity_mode_, self.RefinementComplexities.VERY_HIGH)
                    )
                ),
            ]

        # cull
        def _usd_update_cull_mode_(self, value):
            self._usd_cull_mode = value
            self._dataModel.viewSettings.cullBackfaces = self._usd_cull_enable

        def _usd_set_cull_enable_(self, boolean):
            self._usd_cull_enable = boolean
            self._usd_update_cull_mode_(
                self._usd_cull_mode
            )

        def _usd_get_cull_menu_data_(self):
            return [
                (
                    'Back', 'radio-check',
                    (False, None)
                ),
                (
                    'Front', 'radio-check',
                    (False, None)
                ),
                (
                    'Back Unless Double Sided', 'radio-check',
                    (True, None)
                )
            ]

        # camera mask
        def _usd_set_camera_mask_enable_(self, boolean):
            self._usd_camera_mask_enable = boolean
            self._usd_set_camera_mask_mode_(
                self._usd_camera_mask_mode
            )

        def _usd_set_camera_mask_mode_(self, value):
            self._usd_camera_mask_mode = value
            if self._usd_camera_mask_enable is True:
                self._dataModel.viewSettings.cameraMaskMode = self._usd_camera_mask_mode
            else:
                self._dataModel.viewSettings.cameraMaskMode = self.CameraMaskModes.NONE

        def _usd_get_camera_mask_menu_data_(self):
            return [
                (
                    'Partial', 'radio-check',
                    (
                        lambda: self._usd_camera_mask_mode == self.CameraMaskModes.PARTIAL,
                        functools.partial(self._usd_set_camera_mask_mode_, self.CameraMaskModes.PARTIAL)
                    ),
                ),
                (
                    'Full', 'radio-check',
                    (
                        lambda: self._usd_camera_mask_mode == self.CameraMaskModes.FULL,
                        functools.partial(self._usd_set_camera_mask_mode_, self.CameraMaskModes.FULL)
                    ),
                ),
            ]

        # hud
        def _usd_swap_hud_info_display_(self):
            self._dataModel.viewSettings.showHUD_Info = not self._dataModel.viewSettings.showHUD_Info

        def _usd_swap_hud_complexity_display_(self):
            self._dataModel.viewSettings.showHUD_Complexity = not self._dataModel.viewSettings.showHUD_Complexity

        def _usd_swap_hud_performance_display_(self):
            self._dataModel.viewSettings.showHUD_Performance = not self._dataModel.viewSettings.showHUD_Performance

        def _usd_swap_hud_gpu_status_display_(self):
            self._dataModel.viewSettings.showHUD_GPUstats = not self._dataModel.viewSettings.showHUD_GPUstats

        def _usd_set_hud_enable_(self, boolean):
            self._dataModel.viewSettings.showHUD = boolean

        def _usd_get_hud_menu_data_(self):
            return [
                (
                    'Subtree Info (Slow)', 'box-check',
                    (
                        lambda: self._dataModel.viewSettings._showHUD_Info is True,
                        self._usd_swap_hud_info_display_
                    )
                ),
                (
                    'Camera/Complexity', 'box-check',
                    (
                        lambda: self._dataModel.viewSettings._showHUD_Complexity is True,
                        self._usd_swap_hud_complexity_display_
                    )
                ),
                (
                    'Performance', 'box-check',
                    (
                        lambda: self._dataModel.viewSettings._showHUD_Performance is True,
                        self._usd_swap_hud_performance_display_
                    )
                ),
                (
                    'GPU stats', 'box-check',
                    (
                        lambda: self._dataModel.viewSettings._showHUD_GPUstats is True,
                        self._usd_swap_hud_gpu_status_display_
                    )
                ),
            ]

        # ================================================================================================================ #
        def _refresh_usd_view_(self):
            self._stageView.updateView(resetCam=False, forceComputeBBox=True)

        def _refresh_widget_draw_(self):
            self.update()

        def _refresh_usd_view_draw_(self):
            self._stageView.closeRenderer()
            # update time code
            time_code = Usd.TimeCode(self._usd_stage.GetStartTimeCode())
            self._dataModel.currentFrame = time_code
            # update bbox
            self._dataModel._bboxCache = UsdGeom.BBoxCache(
                time_code,
                includedPurposes=[Usdviewq.common.IncludedPurposes.DEFAULT, Usdviewq.common.IncludedPurposes.PROXY],
                useExtentsHint=True,
            )
            self._dataModel._xformCache = UsdGeom.XformCache(
                time_code
            )
            # clear selection
            self._dataModel.selection.clear()
            #
            self._stageView.updateView(resetCam=True, forceComputeBBox=True, frameFit=1.25)
            self._stageView.update()
            # self._stageView.SetRendererStopped(False)

        def _refresh_widget_draw_geometry_(self):
            x, y = 0, 0
            w, h = self.width(), self.height()
            # int left， int top， int right， int bottom
            m_l, m_t, m_r, m_b = self._frame_draw_margins

            frm_x, frm_y = x+m_l+1, y+m_t+1
            frm_w, frm_h = w-m_l-m_r-2, h-m_t-m_b-2
            self._rect_frame_draw.setRect(
                frm_x, frm_y, frm_w, frm_h
            )
            self._stage_view_draw_rect.setRect(
                self._stageView.x(), self._stageView.y(),
                self._stageView.width(), self._stageView.height()
            )

        def eventFilter(self, *args):
            widget, event = args
            if widget == self:
                if event.type() == QtCore.QEvent.Close:
                    pass
                elif event.type() == QtCore.QEvent.Resize:
                    self._refresh_widget_draw_geometry_()
                elif event.type() == QtCore.QEvent.FocusIn:
                    self._is_focused = True
                    self._refresh_widget_draw_()
                elif event.type() == QtCore.QEvent.FocusOut:
                    self._is_focused = False
                    self._refresh_widget_draw_()
                elif event.type() == QtCore.QEvent.KeyPress:
                    if event.key() == QtCore.Qt.Key_F:
                        self._frameSelection()
            return False

        def paintEvent(self, event):
            painter = gui_qt_core.QtPainter(self)
            #
            is_selected = self._is_focused
            bcg_color = gui_qt_core.QtBackgroundColors.Basic
            # swap border color on focus change
            bdr_color = [gui_qt_core.QtBorderColors.Basic, gui_qt_core.QtBorderColors.HighLight][is_selected]
            bdr_w = [1, 2][is_selected]
            painter._draw_frame_by_rect_(
                rect=self._rect_frame_draw,
                border_color=bdr_color,
                background_color=bcg_color,
                # border_radius=1,
                border_width=bdr_w,
            )
            if self._thread_draw_flag is True:
                painter._draw_loading_by_rect_(
                    rect=self._stage_view_draw_rect,
                    loading_index=self._thread_load_index
                )

        def __build_usd_var_(self):
            self._mallocTags = 'none'
            self._primToItemMap = {}
            self._lastViewContext = {}
            self._printTiming = False
            self._initialSelectPrim = None
            self._startingPrimCamera = None
            self._fpsHUDKeys = ('Render', 'Playback')
            self._fpsHUDInfo = dict(
                zip(
                    self._fpsHUDKeys,
                    ["N/A", "N/A"]
                )
            )
            self._upperHUDInfo = dict()

            self._settings2 = Usdviewq.settings2.Settings('1')

            self._dataModel = Usdviewq.appController.UsdviewDataModel(self._printTiming, self._settings2)
            #
            self._usd_complexity_enable = False
            self._usd_complexity_mode = self.RefinementComplexities.MEDIUM
            #
            self._usd_cull_enable = False
            self._usd_cull_mode = None
            #
            self._usd_camera_mask_enable = False
            self._usd_camera_mask_mode = self.CameraMaskModes.PARTIAL
            #
            self._usd_camera_cur = None

            self._usd_environment_cur = 'stinson-beach'

        def __build_top_tool_bar_(self, layout):
            self._top_tool_scroll_box = gui_qt_wgt_scroll.QtHScrollBox()
            self._top_tool_scroll_box._set_layout_align_left_or_top_()
            layout.addWidget(self._top_tool_scroll_box, 0, 1, 1, 1)
            self._top_tool_scroll_box.setFixedHeight(28)
            self._top_tool_scroll_box._set_line_styles_(
                [
                    self._top_tool_scroll_box.Style.Null,
                    self._top_tool_scroll_box.Style.Solid,
                    self._top_tool_scroll_box.Style.Null,
                    self._top_tool_scroll_box.Style.Null
                ]
            )

        def __build_top_tools_(self):

            self.__add_hud_and_camera_mask_display_tools_()
            self.__add_material_and_light_switch_tools_()
            self.__add_color_space_switch_tools_()
            self.__add_camera_and_renderer_switch_tools_()
            self.__add_environment_switch_tools_()
            self.__add_other_tools_()

        def __add_hud_and_camera_mask_display_tools_(self):
            def fnc_(boolean):
                self._dataModel.viewSettings.showHUD = boolean

            #
            tool_box = gui_qt_wgt_container.QtHToolBox()
            self._top_tool_scroll_box.addWidget(tool_box)
            tool_box._set_expanded_(True)
            tool_box._set_name_text_('hud-display and camera-mask')
            #
            for i_index, (i_key, i_value, i_enable_fnc, i_menu_data_gain_fnc) in enumerate(
                [
                    ('hud-display', False, self._usd_set_hud_enable_, self._usd_get_hud_menu_data_),
                    ('camera-mask', False, self._usd_set_camera_mask_enable_, self._usd_get_camera_mask_menu_data_)
                ]
            ):
                i_button = gui_qt_wgt_button.QtIconToggleButton()
                i_button._set_name_text_(i_key)
                i_button._set_tool_tip_text_(
                    '"LMB-click" to toggle "{0}"\n"RMB-click" for show more action'.format(i_key)
                )
                i_button._set_icon_file_path_(
                    gui_core.GuiIcon.get('tool/{}'.format(i_key))
                )
                i_button._set_checked_(i_value)
                i_button.check_toggled.connect(i_enable_fnc)
                i_button._set_menu_title_text_(i_key)
                i_button._set_menu_data_generate_fnc_(
                    i_menu_data_gain_fnc
                )

                tool_box._add_widget_(i_button)

        def __add_material_and_light_switch_tools_(self):
            tool_box = gui_qt_wgt_container.QtHToolBox()
            self._top_tool_scroll_box.addWidget(tool_box)
            tool_box._set_expanded_(True)
            tool_box._set_name_text_('material and light')
            #
            for i_index, (i_key, i_mode, i_value, i_enable_fnc, i_menu_data_gain_fnc) in enumerate(
                [
                    ('material', None, True, self._usd_model.set_scene_materials_enable, self._usd_get_material_menu_data_),
                    ('light', None, True, self._usd_model.set_lights_enable, self._usd_get_light_menu_data_),
                ]
            ):
                i_button = gui_qt_wgt_button.QtIconToggleButton()
                i_button._set_name_text_(i_key)
                i_button._set_tool_tip_text_(
                    '"LMB-click" to toggle "{0}"\n"RMB-click" for show more action'.format(i_key)
                )
                i_button._set_icon_file_path_(
                    gui_core.GuiIcon.get('tool/{}'.format(i_key))
                )
                i_button._set_checked_(i_value)
                i_button.check_toggled.connect(i_enable_fnc)
                i_button._set_menu_data_generate_fnc_(i_menu_data_gain_fnc)
                #
                tool_box._add_widget_(i_button)

        def __add_color_space_switch_tools_(self):
            tool_box = gui_qt_wgt_container.QtHToolBox()
            self._top_tool_scroll_box.addWidget(tool_box)
            tool_box._set_expanded_(True)
            tool_box._set_name_text_('color space')
            #
            for i_index, (i_key, i_mode, i_value, i_enable_fnc, i_menu_data_gain_fnc) in enumerate(
                [
                    ('color-manager', None, True, self._usd_model.set_color_space_enable,
                     self._usd_get_color_space_menu_data_),
                ]
            ):
                i_button = gui_qt_wgt_button.QtIconToggleButton()
                i_button._set_name_text_(i_key)
                i_button._set_tool_tip_text_('"LMB-click" to toggle "{0}"\n"RMB-click" to switch "{0}"'.format(i_key))
                i_button._set_icon_file_path_(
                    gui_core.GuiIcon.get('tool/{}'.format(i_key))
                )
                i_button._set_checked_(i_value)
                i_button.check_toggled.connect(i_enable_fnc)
                i_button._set_menu_data_generate_fnc_(i_menu_data_gain_fnc)

                tool_box._add_widget_(i_button)

        def __add_camera_and_renderer_switch_tools_(self):
            tool_box = gui_qt_wgt_container.QtHToolBox()
            self._top_tool_scroll_box.addWidget(tool_box)
            tool_box._set_expanded_(True)
            tool_box._set_name_text_('camera and renderer')
            self._camera_menu_data = [
                ('Free', 'radio-check', (True, None)),
            ]
            self._renderer_menu_data = [
                ('GL', 'radio-check', (True, None)),
                ('Arnold', 'radio-check', (False, None))
            ]
            #
            for i_index, (i_key, i_menu_data_gain_fnc) in enumerate(
                [
                    ('camera', self._usd_get_camera_menu_data_),
                    ('renderer', self._usd_get_renderer_menu_data_),
                    ('display-purpose', self._usd_get_display_purpose_menu_data_),
                ]
            ):
                i_button = gui_qt_wgt_button.QtIconPressButton()
                i_button._set_name_text_(i_key)
                i_button._set_tool_tip_text_('"LMB-click" to toggle "{0}"\n"RMB-click" to switch "{0}"'.format(i_key))
                i_button._set_icon_file_path_(
                    gui_core.GuiIcon.get('tool/{}'.format(i_key))
                )
                #
                i_button._set_menu_data_generate_fnc_(i_menu_data_gain_fnc)

                tool_box._add_widget_(i_button)

        def __add_environment_switch_tools_(self):
            tool_box = gui_qt_wgt_container.QtHToolBox()
            self._top_tool_scroll_box.addWidget(tool_box)
            tool_box._set_expanded_(True)
            tool_box._set_name_text_('display-purpose and environment')
            #
            for i_index, (i_key, i_menu_data_gain_fnc) in enumerate(
                [
                    ('environment', self._usd_get_environment_menu_data_),
                ]
            ):
                i_button = gui_qt_wgt_button.QtIconPressButton()
                i_button._set_name_text_(i_key)
                i_button._set_tool_tip_text_('"LMB-click" to toggle "{0}"\n"RMB-click" to switch "{0}"'.format(i_key))
                i_button._set_icon_file_path_(
                    gui_core.GuiIcon.get('tool/{}'.format(i_key))
                )
                i_button._set_menu_data_generate_fnc_(i_menu_data_gain_fnc)
                #
                tool_box._add_widget_(i_button)

        def __add_other_tools_(self):
            tool_box = gui_qt_wgt_container.QtHToolBox()
            self._top_tool_scroll_box.addWidget(tool_box)
            tool_box._set_expanded_(True)
            tool_box._set_name_text_('display-purpose and environment')
            #
            for i_index, (i_key, i_menu_data_gain_fnc, i_fnc) in enumerate(
                [
                    ('snapshot', self._usd_get_snapshot_menu_data_, self._usd_do_snapshot_),
                ]
            ):
                i_button = gui_qt_wgt_button.QtIconPressButton()
                i_button._set_name_text_(i_key)
                i_button._set_tool_tip_text_('"LMB-click" to toggle "{0}"\n"RMB-click" to switch "{0}"'.format(i_key))
                i_button._set_icon_file_path_(
                    gui_core.GuiIcon.get('tool/{}'.format(i_key))
                )
                i_button._set_menu_data_generate_fnc_(i_menu_data_gain_fnc)
                i_button.press_clicked.connect(i_fnc)
                #
                tool_box._add_widget_(i_button)

        def _usd_get_snapshot_menu_data_(self):
            return []

        def _usd_do_snapshot_(self):
            d = bsc_core.BscSystem.get_home_directory()
            file_path = six.u('{}/snapshot/untitled-{}.png').format(d, bsc_core.TimeExtraMtd.generate_time_tag_36())
            bsc_storage.StgFileOpt(file_path).create_directory()
            self._usd_save_snapshot_to_(file_path)

        def _usd_wait_for_painting_(self):
            while self._stageView.IsRendererConverged() is False:
                pass

        def _usd_save_snapshot_fnc(self, file_path):
            bsc_storage.StgFileOpt(file_path).create_directory()
            img = self._stageView.grabFrameBuffer(withAlpha=True)
            img.save(file_path, 'PNG')
            self.snapshot_finished.emit()
            bsc_log.Log.trace_result('usd snapshot finish: {}'.format(file_path))

        def _usd_save_snapshot_to_(self, file_path):
            bsc_log.Log.trace_result('usd snapshot start')
            t = gui_qt_core.QtMethodThread(self)
            # wait when render is stopped
            if self._stageView.IsRendererConverged() is False:
                t.append_method(self._usd_wait_for_painting_)
                t.run_finished.connect(functools.partial(self._usd_save_snapshot_fnc, file_path))
                t.start()
            else:
                self._usd_save_snapshot_fnc(file_path)

        def _usd_save_pre_geometry_snapshot_fnc_(self, file_p):
            for seq, i_prim in enumerate(self._usd_get_all_mesh_prims_()):
                self._usd_isolate_select_geometry_to_(i_prim)
                i_texture_path = file_p.format(index=seq)
                # update GL before save fnc
                self._stageView.updateView()
                self._usd_save_snapshot_fnc(i_texture_path)
            #
            self._usd_clear_session_visible_()
            self._stageView.updateView()
            self.pre_geometry_snapshot_finished.emit()

        def _usd_save_per_geometry_snapshot_to_(self, file_p):
            bsc_log.Log.trace_result('usd snapshot start')
            t = gui_qt_core.QtMethodThread(self)
            # wait when render is stopped
            if self._stageView.IsRendererConverged() is False:
                t.append_method(self._usd_wait_for_painting_)
                t.run_finished.connect(functools.partial(self._usd_save_pre_geometry_snapshot_fnc_, file_p))
                t.start()
            else:
                self._usd_save_pre_geometry_snapshot_fnc_(file_p)

        def __build_left_tool_bar_(self, layout):
            self._left_tool_scroll_box = gui_qt_wgt_scroll.QtVScrollBox()
            self._left_tool_scroll_box._set_layout_align_left_or_top_()
            layout.addWidget(self._left_tool_scroll_box, 1, 0, 1, 1)
            self._left_tool_scroll_box.setFixedWidth(28)
            self._left_tool_scroll_box._set_line_styles_(
                [
                    self._left_tool_scroll_box.Style.Null,
                    self._left_tool_scroll_box.Style.Null,
                    self._left_tool_scroll_box.Style.Null,
                    self._left_tool_scroll_box.Style.Solid
                ]
            )

        def __build_left_tools_(self):
            self.__add_isolate_select_switch_tools_()
            self.__add_draw_mode_switch_tools_()
            self.__add_other_switch_tools_()

        def __add_isolate_select_switch_tools_(self):
            def fnc_(boolean):
                if boolean is True:
                    self._usd_do_geometry_isolate_selection_()
                else:
                    self._usd_do_clear_geometry_isolate_selection_()

            #
            tool_box = gui_qt_wgt_container.QtVToolBox()
            self._left_tool_scroll_box.addWidget(tool_box)
            tool_box._set_expanded_(True)
            tool_box._set_name_text_('isolate select')
            #
            for i_index, (i_key, i_mode) in enumerate(
                [
                    ('isolate-select', None),
                ]
            ):
                i_button = gui_qt_wgt_button.QtIconToggleButton()
                i_button._set_name_text_(i_key)
                i_button._set_tool_tip_text_('"LMB-click" to "{}"'.format(i_key))
                i_button._set_icon_file_path_(
                    gui_core.GuiIcon.get('tool/{}'.format(i_key))
                )
                i_button.check_toggled.connect(fnc_)
                #
                if i_key == 'low':
                    i_button._set_checked_(True)

                tool_box._add_widget_(i_button)

        def __add_draw_mode_switch_tools_(self):
            def fnc_(value_):
                self._dataModel.viewSettings.renderMode = value_

            #
            tool_box = gui_qt_wgt_container.QtVToolBox()
            self._left_tool_scroll_box.addWidget(tool_box)
            tool_box._set_expanded_(True)
            tool_box._set_name_text_('render mode')
            #
            tools = []
            #
            for i_key, i_mode in [
                ('wireframe', Usdviewq.common.RenderModes.WIREFRAME),
                ('wireframe-on-surface', Usdviewq.common.RenderModes.WIREFRAME_ON_SURFACE),
                ('smooth-shaded', Usdviewq.common.RenderModes.SMOOTH_SHADED),
                ('flat-shaded', Usdviewq.common.RenderModes.FLAT_SHADED)
            ]:
                i_button = gui_qt_wgt_button.QtIconToggleButton()
                i_button._set_name_text_(i_key)
                i_button._set_tool_tip_text_('"LMB-click" for switch render mode to "{}"'.format(i_key))
                i_button._set_icon_file_path_(
                    gui_core.GuiIcon.get('tool/{}'.format(i_key))
                )
                i_button._set_exclusive_widgets_(tools)
                i_button.check_changed_as_exclusive.connect(functools.partial(fnc_, i_mode))
                # default
                if i_key == 'smooth-shaded':
                    i_button._set_checked_(True)
                #
                tools.append(i_button)
                #
                tool_box._add_widget_(i_button)

        def __add_other_switch_tools_(self):
            tool_box = gui_qt_wgt_container.QtVToolBox()
            self._left_tool_scroll_box.addWidget(tool_box)
            tool_box._set_expanded_(True)
            tool_box._set_name_text_('extend')
            #
            for i_index, (i_key, i_mode, i_value, i_enable_fnc, i_menu_data_gain_fnc) in enumerate(
                [
                    ('complexity', 'enable', False, self._usd_set_complexity_enable_,
                     self._usd_get_complexity_menu_data_),
                    ('cull-backfaces', 'enable', False, self._usd_set_cull_enable_, self._usd_get_cull_menu_data_),
                ]
            ):
                i_button = gui_qt_wgt_button.QtIconToggleButton()
                i_button._set_name_text_(i_key)
                i_button._set_tool_tip_text_(
                    '"LMB-click" to toggle "{0}"\n"RMB-click" to switch "{0}" mode'.format(i_key)
                )
                i_button._set_icon_file_path_(
                    gui_core.GuiIcon.get('tool/{}'.format(i_key))
                )
                i_button._set_checked_(i_value)
                if i_enable_fnc is not None:
                    i_button.check_toggled.connect(i_enable_fnc)
                i_button._set_menu_data_generate_fnc_(i_menu_data_gain_fnc)

                tool_box._add_widget_(i_button)

        def _get_usd_stage_(self):
            return self._usd_stage

        def _usd_export_to_file_(self):
            f = QtWidgets.QFileDialog()
            options = f.Options()
            # options |= f.DontUseNativeDialog
            s = f.getSaveFileName(
                self,
                'Save File',
                '',
                filter=None,
                options=options,
            )
            if s:
                _ = s[0]
                if _:
                    usd_core.UsdStageOpt(self._usd_stage).export_to(
                        _
                    )

        def _get_stage_view_(self):
            return self._stageView

else:
    class QtUsdStageWidgetProxy(QtWidgets.QWidget):
        def __init__(self, *args, **kwargs):
            super(QtUsdStageWidgetProxy, self).__init__(*args, **kwargs)

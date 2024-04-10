# coding:utf-8
# qt for usd
from .wrap import *


class UsdModel(object):
    if QT_USD_FLAG is True:
        RefinementComplexities = UsdAppUtils.complexityArgs.RefinementComplexities
        ColorCorrectionModes = Usdviewq.common.ColorCorrectionModes
        BusyContext = Usdviewq.common.BusyContext
        DumpMallocTags = Usdviewq.common.DumpMallocTags
        PickModes = Usdviewq.common.PickModes
        CameraMaskModes = Usdviewq.common.CameraMaskModes

    def __init__(self, data_model, stage_view):
        self._dataModel = data_model
        self._stageView = stage_view

        self._usd_color_space_enable = True
        self._usd_color_space_mode = self.ColorCorrectionModes.SRGB
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

    def set_scene_materials_enable(self, boolean):
        self._dataModel.viewSettings.enableSceneMaterials = boolean

    # light
    def set_lights_enable(self, boolean):
        self._stageView._renderParams.enableLighting = boolean
        self._stageView.update()

    def get_scene_lights_is_enable(self):
        return self._dataModel.viewSettings.enableSceneLights is True

    def set_scene_lights_enable(self, boolean):
        self._dataModel.viewSettings.enableSceneLights = boolean

    def swap_scene_lights_enable(self):
        self._dataModel.viewSettings.enableSceneLights = not self._dataModel.viewSettings.enableSceneLights

    def get_camera_light_is_enable(self):
        return self._dataModel.viewSettings.ambientLightOnly is True

    def set_camera_light_enable(self, boolean):
        self._dataModel.viewSettings.ambientLightOnly = boolean

    def swap_camera_light_enable(self):
        self._dataModel.viewSettings.ambientLightOnly = not self._dataModel.viewSettings.ambientLightOnly

    def get_dome_light_is_enable(self):
        return self._dataModel.viewSettings.domeLightEnabled is True

    def set_dome_light_enable(self, boolean):
        self._dataModel.viewSettings.domeLightEnabled = boolean

    def swap_dome_light_enable(self):
        self._dataModel.viewSettings.domeLightEnabled = not self._dataModel.viewSettings.domeLightEnabled

    # color space
    def get_color_space_mode(self):
        return self._usd_color_space_mode

    def set_color_space_enable(self, boolean):
        self._usd_color_space_enable = boolean
        self.set_color_space_mode(
            self._usd_color_space_mode
        )

    def set_color_space_mode(self, value):
        self._usd_color_space_mode = value
        if self._usd_color_space_enable is True:
            self._dataModel.viewSettings.colorCorrectionMode = self._usd_color_space_mode
        else:
            self._dataModel.viewSettings.colorCorrectionMode = self.ColorCorrectionModes.DISABLED

        self.update_background_color()

    def update_background_color(self):
        if self._usd_color_space_enable:
            if self._usd_color_space_mode == self.ColorCorrectionModes.SRGB:
                self._dataModel.viewSettings.__dict__['clearColor'] = (0.0275, 0.0275, 0.0275, 1)
            elif self._usd_color_space_mode == self.ColorCorrectionModes.OPENCOLORIO:
                self._dataModel.viewSettings.__dict__['clearColor'] = (0.077, 0.077, 0.077, 1)
        else:
            self._dataModel.viewSettings.__dict__['clearColor'] = (0.184, 0.184, 0.184, 1)
        #
        self._stageView.update()

    # color
    def set_background_color(self):
        pass

    def set_override_color(self):
        pass

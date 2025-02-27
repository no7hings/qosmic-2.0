# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class RenderSettings(object):
    RENDER_ATTR_DICT = {
        'renderer': 'defaultRenderGlobals.currentRenderer',
        'imagePrefix': 'defaultRenderGlobals.imageFilePrefix',
        #
        'start_frame': 'defaultRenderGlobals.startFrame',
        'end_frame': 'defaultRenderGlobals.endFrame',
        #
        'animation': 'defaultRenderGlobals.animation',
        'imageFormat': 'defaultRenderGlobals.imfPluginKey',
        'periodInExt': 'defaultRenderGlobals.periodInExt',
        'putFrameBeforeExt': 'defaultRenderGlobals.putFrameBeforeExt',
        'extensionPadding': 'defaultRenderGlobals.extensionPadding',
        'renderVersion': 'defaultRenderGlobals.renderVersion',
        #
        'width': 'defaultResolution.width',
        'height': 'defaultResolution.height',
        #
        'preMel': 'defaultRenderGlobals.preMel'
    }

    @classmethod
    def set_cameras(cls, cameras):
        all_cameras = cmds.ls(type='camera', long=1) or []
        for i in all_cameras:
            cmds.setAttr(i+'.renderable', 0)

        for i in cameras:
            cmds.setAttr(i+'.renderable', 1)

    @classmethod
    def set_renderer(cls, renderer):
        cmds.setAttr(cls.RENDER_ATTR_DICT['renderer'], renderer, type='string')

    @classmethod
    def set_frame_range(cls, start_frame=None, end_frame=None):
        if not start_frame:
            start_frame = int(cmds.playbackOptions(query=1, minTime=1))
        if not end_frame:
            end_frame = int(cmds.playbackOptions(query=1, maxTime=1))
        #
        cmds.setAttr(cls.RENDER_ATTR_DICT['start_frame'], start_frame)
        cmds.setAttr(cls.RENDER_ATTR_DICT['end_frame'], end_frame)

    @classmethod
    def get_frame_range(cls):
        start_frame = cmds.getAttr(cls.RENDER_ATTR_DICT['start_frame'])
        end_frame = cmds.getAttr(cls.RENDER_ATTR_DICT['end_frame'])
        return int(start_frame), int(end_frame)

    @classmethod
    def set_resolution(cls, width, height):
        # has minimum value
        width, height = max(width, 2), max(height, 2)

        cmds.setAttr(cls.RENDER_ATTR_DICT['width'], width)
        cmds.setAttr(cls.RENDER_ATTR_DICT['height'], height)
        if width == height:
            cmds.setAttr('defaultResolution.deviceAspectRatio', 1)
        cmds.setAttr('defaultResolution.pixelAspect', 1)

    @classmethod
    def get_resolution(cls):
        width = cmds.getAttr(cls.RENDER_ATTR_DICT['width'])
        height = cmds.getAttr(cls.RENDER_ATTR_DICT['height'])
        return int(width), int(height)

    @classmethod
    def open_color_transform(cls):
        cmds.colorManagementPrefs(edit=1, outputTransformEnabled=1, outputTarget='renderer')
        cmds.colorManagementPrefs(edit=1, outputUseViewTransform=1, outputTarget='renderer')


class HardwareRenderSettings(object):
    @classmethod
    def open_gpu_instancing(cls):
        cmds.setAttr(
            'hardwareRenderingGlobals.hwInstancing', 1
        )

    @classmethod
    def set_render_mode(cls, texture_enable, light_enable, shadow_enable):
        if texture_enable is True:
            cmds.setAttr('hardwareRenderingGlobals.renderMode', 4)
        else:
            cmds.setAttr('hardwareRenderingGlobals.renderMode', 1)

        if light_enable is True:
            cmds.setAttr('hardwareRenderingGlobals.lightingMode', 1)
        else:
            cmds.setAttr('hardwareRenderingGlobals.lightingMode', 0)

    @classmethod
    def set_display_mode(cls, display_mode):
        """
        renderMode:
            0: Wire
            1: Shaded
            2: Wire On Shaded
            3: Default Material
            4: Shaded And Textured
            5: Wire On Shaded And Textured
            6: Bounding Box

        lightMode:
            0: Default
            1: All
            2: None
            3: Active
            4: Full Ambient
        """
        if display_mode == 5:
            cmds.setAttr('hardwareRenderingGlobals.renderMode', 1)
            cmds.setAttr('hardwareRenderingGlobals.lightingMode', 0)
        elif display_mode == 6:
            cmds.setAttr('hardwareRenderingGlobals.renderMode', 4)
            cmds.setAttr('hardwareRenderingGlobals.lightingMode', 0)
        elif display_mode == 7:
            cmds.setAttr('hardwareRenderingGlobals.renderMode', 4)
            cmds.setAttr('hardwareRenderingGlobals.lightingMode', 1)

    @classmethod
    def set_display_filter(
        cls, **kwargs
    ):
        """
        $gTotalObjTypeFilters[0] = "NURBS Curves";
        $gTotalObjTypeFilters[1] = "NURBS Surfaces";
        $gTotalObjTypeFilters[2] = "Polygons";
        $gTotalObjTypeFilters[3] = "Subdiv Surface";
        $gTotalObjTypeFilters[4] = "Particles";
        $gTotalObjTypeFilters[5] = "Particle Instance";
        $gTotalObjTypeFilters[6] = "Fluids";
        $gTotalObjTypeFilters[7] = "Strokes";
        $gTotalObjTypeFilters[8] = "Image Planes";
        $gTotalObjTypeFilters[9] = "UI";
        $gTotalObjTypeFilters[10] = "Lights";
        $gTotalObjTypeFilters[11] = "Cameras";
        $gTotalObjTypeFilters[12] = "Locators";
        $gTotalObjTypeFilters[13] = "Joints";
        $gTotalObjTypeFilters[14] = "IK Handles";
        $gTotalObjTypeFilters[15] = "Deformers";
        $gTotalObjTypeFilters[16] = "Motion Trails";
        $gTotalObjTypeFilters[17] = "Components";
        $gTotalObjTypeFilters[18] = "Hair Systems";
        $gTotalObjTypeFilters[19] = "Follicles";
        $gTotalObjTypeFilters[20] = "Misc. UI";
        $gTotalObjTypeFilters[21] = "Ornaments";
        """
        keys = [
            'nurbs_curve',        # 0
            'nurbs_surface',      # 1
            'mesh',               # 2
            'subdiv_surface',     # 3
            'particle',           # 4
            'particle_instance',  # 5
            'fluid',              # 6
            'stroke',             # 7
            'image_plane',        # 8
            'ui',                 # 9
            'light',  # 10
            'camera',  # 11
            'locator',  # 12
            'joint',  # 13
            'ik_handle',  # 14
            'deformer',  # 15
            'motion_trail',  # 16
            'component',  # 17
            'hair_system',  # 18
            'follicle',  # 19
            'misc_ui',  # 20
            'ornament',  # 21
        ]

        args = [0]*len(keys)
        for i_idx, i in enumerate(keys):
            if i in kwargs:
                if kwargs[i]:
                    args[i_idx] = 1

        cmds.setAttr(
            'hardwareRenderingGlobals.objectTypeFilterValueArray',
            args,
            type='Int32Array'
        )

        # plug
        sub_keys = [
            'gpu_cache'
        ]
        sub_args = [0]*len(sub_keys)
        for i_idx, i in enumerate(sub_keys):
            if i in kwargs:
                if kwargs[i]:
                    sub_args[i_idx] = 1

        cmds.setAttr(
            'hardwareRenderingGlobals.pluginObjectTypeFilterValueArray',
            sub_args,
            type='Int32Array'
        )

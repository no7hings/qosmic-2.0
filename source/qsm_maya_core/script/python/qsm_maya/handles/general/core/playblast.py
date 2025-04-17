# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import qsm_maya.core as qsm_mya_core


class RenderSetting:
    @classmethod
    def setup(cls, camera, display_mode, texture_enable, light_enable, shadow_enable):
        if qsm_mya_core.Scene.get_is_ui_mode():
            pass
        else:
            # cmds.setAttr(camera+'.backgroundColor', 0.106, 0.106, 0.106, type='double3')\
            qsm_mya_core.RenderSettings.set_cameras([camera])
            qsm_mya_core.RenderSettings.set_renderer('mayaHardware2')
            qsm_mya_core.RenderSettings.open_color_transform()

            # cmds.setAttr('hardwareRenderingGlobals.lineAAEnable', 1)
            # anti_aliasing
            cmds.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
            # cmds.setAttr('hardwareRenderingGlobals.ssaoEnable', 1)
            cmds.setAttr('hardwareRenderingGlobals.hwInstancing', 1)

            # qsm_mya_core.HardwareRenderSettings.set_display_mode(display_mode)
            if texture_enable is True:
                qsm_mya_core.HardwareRenderSettings.set_render_mode(texture_enable, light_enable, shadow_enable)

            qsm_mya_core.HardwareRenderSettings.set_display_filter(
                nurbs_surface=1,
                mesh=1,
                subdiv_surface=1,
                particle=1,
                particle_instance=1,
                fluid=1,
                stroke=1,
                image_plane=1,
                gpu_cache=1
            )
            # set filter
            cmds.setAttr(
                'hardwareRenderingGlobals.pluginObjectTypeFilterValueArray',
                [1],
                type='Int32Array'
            )


class CameraDisplay:
    @classmethod
    def setup(cls, camera, options):
        if options is not None:
            display_resolution = options.get('display_resolution', 0)
            display_safe_action = options.get('display_safe_action', 0)
            display_safe_title = options.get('display_safe_title', 0)
            display_film_pivot = options.get('display_film_pivot', 0)
            display_film_origin = options.get('display_film_origin', 0)
            overscan = options.get('overscan', 0)
        else:
            display_resolution = qsm_mya_core.NodeAttribute.get_value(camera, 'displayResolution')
            display_safe_action = qsm_mya_core.NodeAttribute.get_value(camera, 'displaySafeAction')
            display_safe_title = qsm_mya_core.NodeAttribute.get_value(camera, 'displaySafeTitle')
            display_film_pivot = qsm_mya_core.NodeAttribute.get_value(camera, 'displayFilmPivot')
            display_film_origin = qsm_mya_core.NodeAttribute.get_value(camera, 'displayFilmOrigin')
            overscan = qsm_mya_core.NodeAttribute.get_value(camera, 'overscan')

        cmds.camera(
            camera,
            edit=1,
            displayFilmGate=0,
            displayResolution=display_resolution,
            #
            displayGateMask=display_resolution,
            #
            displaySafeAction=display_safe_action, displaySafeTitle=display_safe_title, displayFieldChart=0,
            displayFilmPivot=display_film_pivot, displayFilmOrigin=display_film_origin,
            #
            filmFit=1,
            overscan=overscan
        )

        if display_resolution:
            cmds.setAttr(camera+'.displayGateMaskOpacity', 1)
            cmds.setAttr(camera+'.displayGateMaskColor', 0, 0, 0, type='double3')


class Window:
    WINDOW_NAME = 'preview_window_2'

    @classmethod
    def setup_camera(cls, camera, display_resolution, display_safe_action, display_safe_title):
        cmds.camera(
            camera,
            edit=1,
            displayFilmGate=0,
            displayResolution=display_resolution,
            displayGateMask=display_resolution,
            displaySafeAction=display_safe_action,
            displaySafeTitle=display_safe_title,
            displayFieldChart=0,
            filmFit=1,
            overscan=1
        )
        cmds.setAttr(camera+'.displayGateMaskOpacity', 1)
        cmds.setAttr(camera+'.displayGateMaskColor', 0, 0, 0, type='double3')

    @classmethod
    def setup_for_view(cls, view_panel, use_default_material, hud_enable):
        rdr = 'vp2Renderer'

        # cmds.modelEditor(view_panel, edit=1, rendererName=rdr, rom='myOverride')

        cmds.modelEditor(
            view_panel,
            edit=1,
            activeView=1,
            # useDefaultMaterial=use_default_material,
            wireframeOnShaded=0,
            fogging=0,
            dl='default',
            twoSidedLighting=1,
            allObjects=0,
            manipulators=0,
            grid=0,
            hud=hud_enable,
            sel=0
        )

        cmds.modelEditor(
            view_panel,
            edit=1,
            activeView=1,
            polymeshes=1,
            nurbsSurfaces=1,
            subdivSurfaces=1,
            fluids=1,
            strokes=1,
            # nCloths=1,
            nParticles=1,
            pluginShapes=1,
            # show GPU
            pluginObjects=['gpuCacheDisplayFilter', 1],
            displayAppearance='smoothShaded'
        )

    @classmethod
    def create(
        cls, camera, width, height, display_mode, use_default_material, show_hud, show_window,
        texture_enable, light_enable, shadow_enable,
        hud_enable,
        use_exists_window=False,
    ):
        if use_exists_window is True:
            if qsm_mya_core.Window.is_exists(cls.WINDOW_NAME) is True:
                return

        window = qsm_mya_core.Window.create_force(cls.WINDOW_NAME, (width, height))
        if show_window is True:
            qsm_mya_core.Window.show(window)

        layout = cmds.paneLayout(width=width, height=height, parent=window)
        view_panel_name = cls.WINDOW_NAME+'_view_panel'

        if cmds.modelPanel(
            view_panel_name, query=1, exists=1
        ):
            cmds.deleteUI(view_panel_name, panel=1)

        view_panel = cmds.modelPanel(
            view_panel_name,
            label=cls.WINDOW_NAME+'_view_panel',
            parent=layout,
            menuBarVisible=1,
            modelEditor=1,
            camera=camera,
        )
        cls.setup_for_view(
            view_panel,
            use_default_material=use_default_material, hud_enable=hud_enable
        )
        # set latest
        qsm_mya_core.ViewPanel.set_render_mode(view_panel, texture_enable, light_enable, shadow_enable)
        # if show_hud is True:
        #     cls.setup_camera(
        #         camera,
        #         display_resolution=1, display_safe_title=0
        #     )
        # else:
        # cls.setup_camera(
        #     camera,
        #     display_resolution=0,
        #     display_safe_action=0,
        #     display_safe_title=0
        # )

    @classmethod
    def close(cls):
        qsm_mya_core.Window.delete(cls.WINDOW_NAME)


# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from . import window as _window

from . import viewport as _viewport

from . import transform as _transform

from . import render_for_hardware as _render_for_hardware

from . import bbox as _bbox


class Snapshot(object):

    @classmethod
    def setup_camera(cls, camera_shape):
        cmds.camera(
            camera_shape,
            edit=1,
            displayFilmGate=0,
            displayResolution=0,
            displayGateMask=0,
            displaySafeAction=0,
            displaySafeTitle=0,
            displayFieldChart=0,
            filmFit=1,
            overscan=1
        )
        cmds.setAttr(camera_shape+'.displayGateMaskOpacity', 1)
        cmds.setAttr(camera_shape+'.displayGateMaskColor', 0, 0, 0, type='double3')

    @classmethod
    def setup_viewport(cls, model_panel, mode=0):
        renderer = 'base_OpenGL_Renderer'
        if mode == 1:
            renderer = 'vp2Renderer'

        cmds.modelEditor(model_panel, edit=1, rendererName=renderer)
        if renderer == 'vp2Renderer':
            cmds.setAttr('hardwareRenderingGlobals.lineAAEnable', 1)
            cmds.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
            cmds.setAttr('hardwareRenderingGlobals.ssaoEnable', 1)

    @classmethod
    def create(
        cls, 
        locations,
        image_path,
        width=512, height=512,
        use_default_material=False, persp_view=True
    ):
        camera = 'persp'
        camera_shape = 'perspShape'

        directory_path_tmp = '{}/{}'.format(
            bsc_storage.StgUser.get_user_temporary_directory(),
            bsc_core.BscUuid.generate_new()
        )
        image_temp_path_ = '{}/image.jpg'.format(directory_path_tmp)
        image_temp_base = os.path.splitext(image_temp_path_)[0]

        window_name = 'qsm_snapshot'
        _window.Window.delete(window_name)
        cmds.window(window_name, title='Snap Shot')
        panel_layout = cmds.paneLayout(width=width, height=height)
        model_panel = cmds.modelPanel(
            label=window_name,
            parent=panel_layout,
            menuBarVisible=1,
            modelEditor=1,
            camera=camera
        )

        if use_default_material:
            _viewport.ViewPanel.set_display_mode(model_panel, 5)
            _render_for_hardware.HardwareRenderSetup.create_for(
                texture_enable=False, light_enable=False, shadow_enable=False
            )
        else:
            _viewport.ViewPanel.set_display_mode(model_panel, 6)
            _render_for_hardware.HardwareRenderSetup.create_for(
                texture_enable=True, light_enable=False, shadow_enable=False
            )

        cmds.displayRGBColor('background', .25, .25, .25)
        cmds.displayRGBColor('backgroundTop', .25, .25, .25)
        cmds.displayRGBColor('backgroundBottom', .25, .25, .25)
        cmds.showWindow(window_name)

        cls.setup_viewport(model_panel, 1)

        cmds.modelEditor(
            model_panel,
            edit=1,
            activeView=1,
            useDefaultMaterial=use_default_material,
            wireframeOnShaded=0,
            fogging=0,
            dl='default',
            twoSidedLighting=1,
            allObjects=0,
            manipulators=0,
            grid=0,
            hud=1,
            sel=0)

        cmds.modelEditor(
            model_panel,
            edit=1,
            activeView=1,
            polymeshes=1,
            nurbsSurfaces=1,
            subdivSurfaces=1,
            fluids=1,
            strokes=1,
            nCloths=1,
            nParticles=1,
            pluginShapes=1,
            pluginObjects=['gpuCacheDisplayFilter', 1],
            displayAppearance='smoothShaded'
        )

        cls.setup_camera(camera_shape)
        if persp_view is True:
            cmds.camera(
                camera_shape,
                edit=1,
                displayFilmGate=0,
                displaySafeAction=0,
                displaySafeTitle=0,
                displayFieldChart=0,
                displayResolution=0,
                displayGateMask=0,
                filmFit=1,
                focalLength=35.000,
                overscan=1.0,
                nearClipPlane=1.0,
                farClipPlane=1000000.0
            )

            cmds.camera(
                camera_shape,
                edit=1,
                position=(28.0, 21.0, 28.0),
                rotation=(-27.9383527296, 45, 0)
            )

            box = _bbox.BBox.create_bbox(
                locations
            )
            cmds.select(box)
            cmds.viewFit(camera_shape, fitFactor=1.0, animate=1)
            cmds.select(clear=1)
            cmds.delete(box)

            cmds.camera(
                camera_shape,
                edit=1,
                focalLength=67.177,
            )

            p_0 = cmds.xform(camera, translation=1, worldSpace=1, query=1)

            d = _transform.Transform.compute_distance(
                p_0, (0, 0, 0)
            )
            cmds.camera(
                camera_shape,
                edit=1,
                nearClipPlane=max(min(d*.001, 10), 0.01),
                farClipPlane=max(min(d*10, 1000000000), 1000)
            )

        cmds.playblast(
            startTime=0,
            endTime=0,
            format='iff',
            filename=image_temp_base,
            sequenceTime=0,
            clearCache=1,
            viewer=0,
            showOrnaments=0,
            offScreen=0,
            framePadding=4,
            percent=100,
            compression='jpg',
            quality=100,
            widthHeight=(width, height)
        )

        _window.Window.delete(window_name)

        image_temp_path = image_temp_base+'.0000.jpg'
        bsc_storage.StgFileOpt(image_temp_path).copy_to_file(image_path, replace=True)
        bsc_storage.StgDirectoryOpt(directory_path_tmp).do_delete()


class Turntable(object):
    @classmethod
    def create(
        cls
    ):
        pass

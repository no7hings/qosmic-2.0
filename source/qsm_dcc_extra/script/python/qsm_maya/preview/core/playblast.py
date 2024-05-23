# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.storage as bsc_storage

import lxbasic.core as bsc_core

from ... import core as _mya_core

from . import hud as _hud


class RenderSettings(object):
    @classmethod
    def setup(cls, camera, display_mode):
        if _mya_core.Scene.get_is_ui_mode():
            pass
        else:
            # cmds.setAttr(camera+'.backgroundColor', 0.106, 0.106, 0.106, type='double3')
            _mya_core.RenderSettings.set_renderer('mayaHardware2')
            _mya_core.RenderSettings.open_color_transform()

            # cmds.setAttr('hardwareRenderingGlobals.lineAAEnable', 1)
            # anti_aliasing
            cmds.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
            # cmds.setAttr('hardwareRenderingGlobals.ssaoEnable', 1)
            cmds.setAttr('hardwareRenderingGlobals.hwInstancing', 1)

            _mya_core.HardwareRenderSettings.set_display_mode(display_mode)
            # set filter
            # cmds.setAttr(
            #     'hardwareRenderingGlobals.objectTypeFilterValueArray',
            #     [0L, 1L, 1L, 1L, 1L, 1L, 1L, 1L, 1L, 1L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 1L, 1L],
            #     type='Int32Array'
            # )
            cmds.setAttr(
                'hardwareRenderingGlobals.objectTypeFilterValueArray',
                [0L, 1L, 1L, 1L, 1L, 1L, 1L, 1L, 1L, 1L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 1L, 0L],
                type='Int32Array'
            )

            # cmds.setAttr(
            #     'hardwareRenderingGlobals.pluginObjectTypeFilterNameArray', ['gpuCacheDisplayFilter'],
            #     type='stringArray'
            # )
            cmds.setAttr(
                'hardwareRenderingGlobals.pluginObjectTypeFilterValueArray',
                [1L],
                type='Int32Array'
            )


class Window(object):
    WINDOW_NAME = 'preview_window_0'

    @classmethod
    def setup_camera(cls, camera, display_resolution, display_safe_title):
        cmds.camera(
            camera,
            edit=1,
            displayFilmGate=0,
            displayResolution=display_resolution,
            displayGateMask=display_resolution,
            displaySafeAction=0,
            displaySafeTitle=display_safe_title,
            displayFieldChart=0,
            filmFit=1,
            overscan=1
        )
        cmds.setAttr(camera+'.displayGateMaskOpacity', 1)
        cmds.setAttr(camera+'.displayGateMaskColor', 0, 0, 0, type='double3')

    @classmethod
    def setup_for_view(cls, view_panel, use_default_material, show_hud):
        rdr = 'vp2Renderer'

        cmds.modelEditor(view_panel, edit=1, rendererName=rdr, rom='myOverride')

        cmds.modelEditor(
            view_panel,
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
            hud=show_hud,
            sel=0
        )

        cmds.modelEditor(
            view_panel,
            edit=1,
            activeView=1,
            polymeshes=1,
            subdivSurfaces=1,
            fluids=1,
            strokes=1,
            nCloths=1,
            nParticles=1,
            pluginShapes=1,
            # show GPU
            pluginObjects=['gpuCacheDisplayFilter', 1],
            displayAppearance='smoothShaded'
        )

    @classmethod
    def create(cls, camera, width, height, display_mode, use_default_material, show_hud):
        window = _mya_core.Window.create_force(cls.WINDOW_NAME, (width, height))
        _mya_core.Window.show(window)

        layout = cmds.paneLayout(width=width, height=height, parent=window)

        view_panel = cmds.modelPanel(
            label=cls.WINDOW_NAME+'_view_panel',
            parent=layout,
            menuBarVisible=1,
            modelEditor=1,
            camera=camera
        )
        _mya_core.ViewPanel.set_display_mode(view_panel, display_mode)
        # _mya_core.Scene.set_background_color((.25, .25, .25))
        cls.setup_for_view(
            view_panel,
            use_default_material=use_default_material, show_hud=show_hud
        )
        cls.setup_camera(
            camera,
            display_resolution=0, display_safe_title=0
        )

    @classmethod
    def close(cls):
        _mya_core.Window.delete(cls.WINDOW_NAME)


class Playblast(object):
    @classmethod
    def create_window(cls, camera, width, height, display_mode, show_hud):
        Window.create(
            camera=camera,
            width=width, height=height,
            display_mode=display_mode,
            use_default_material=0,
            show_hud=show_hud
        )

    @classmethod
    def hud_prc(cls, camera):
        _mya_core.Scene.clear_all_hud()
        _hud.HUD.restore()
        _hud.HUD.create(camera)

    @classmethod
    def render_setting_prc(cls, camera, display_mode):
        RenderSettings.setup(camera, display_mode)

    @classmethod
    def image_prc(cls, file_path, width, height, start_frame, end_frame, show_hud, percent, quality):
        file_opt = bsc_storage.StgFileOpt(file_path)
        file_path_base = file_opt.path_base
        compression = 'jpg'

        cmds.playblast(
            startTime=start_frame,
            endTime=end_frame,
            format='iff',
            filename=file_path_base,
            sequenceTime=0,
            clearCache=1,
            viewer=0,
            showOrnaments=show_hud,
            offScreen=1,
            offScreenViewportUpdate=1,
            framePadding=4,
            percent=percent,
            compression=compression,
            quality=quality,
            widthHeight=(width, height)
        )

    @classmethod
    def movie_prc(cls, image_file_path, movie_file_path, start_frame, end_frame, fps=24):
        image_file_opt = bsc_storage.StgFileOpt(image_file_path)
        image_file_path_base = image_file_opt.path_base

        image_file_path_ = '{}.####.jpg'.format(image_file_path_base)

        cmd_script = bsc_core.FfmpegMtd.get_image_concat_command(
            input=image_file_path_,
            output=movie_file_path,
            start_frame=start_frame,
            end_frame=end_frame,
            fps=fps
        )

        bsc_core.PrcBaseMtd.execute_as_trace(
            cmd_script
        )

    @classmethod
    def execute(
        cls,
        file_path,
        camera='|persp|perspShape',
        frame=None, resolution=(1280, 720),
        display_mode=6, show_hud=False,
        percent=100, quality=100, fps=24
    ):
        if resolution is None:
            resolution = _mya_core.RenderSettings.get_resolution()

        w, h = resolution
        # if show_hud is True:
        #     h += 60

        cls.create_window(
            camera=camera, width=w, height=h, display_mode=display_mode, show_hud=show_hud
        )
        cls.hud_prc(camera)

        cls.render_setting_prc(camera, display_mode)

        file_opt = bsc_storage.StgFileOpt(file_path)
        file_path_base = file_opt.path_base
        image_directory_path = '{}.images'.format(file_path_base)
        image_file_path = '{}/image.jpg'.format(image_directory_path)

        start_frame, end_frame = _mya_core.Frame.auto_range(frame)

        cls.image_prc(
            file_path=image_file_path, start_frame=start_frame, end_frame=end_frame,
            width=w, height=h, show_hud=show_hud,
            percent=percent, quality=quality
        )
        cls.movie_prc(
            image_file_path=image_file_path, movie_file_path=file_path, start_frame=start_frame, end_frame=end_frame,
            fps=fps
        )
        # clear image
        # bsc_storage.StgDirectoryOpt(image_directory_path).do_delete()
        # close window
        # Window.close()


# coding:utf-8
import os

import six

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
    def setup(cls, camera, display_mode, texture_enable, light_enable, shadow_enable):
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

            # _mya_core.HardwareRenderSettings.set_display_mode(display_mode)
            if texture_enable is True:
                _mya_core.HardwareRenderSettings.set_render_mode(texture_enable, light_enable, shadow_enable)
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
    WINDOW_NAME = 'preview_window_2'

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
    def create(
        cls, camera, width, height, display_mode, use_default_material, show_hud, show_window,
        texture_enable, light_enable, shadow_enable,
        hud_enable
    ):
        window = _mya_core.Window.create_force(cls.WINDOW_NAME, (width, height))
        if show_window is True:
            _mya_core.Window.show(window)

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
        _mya_core.ViewPanel.set_render_mode(view_panel, texture_enable, light_enable, shadow_enable)
        # if show_hud is True:
        #     cls.setup_camera(
        #         camera,
        #         display_resolution=1, display_safe_title=0
        #     )
        # else:
        cls.setup_camera(
            camera,
            display_resolution=0, display_safe_title=0
        )

    @classmethod
    def close(cls):
        _mya_core.Window.delete(cls.WINDOW_NAME)


class Playblast(object):
    @classmethod
    def create_window(
        cls, camera, width, height, display_mode, show_hud, show_window,
        texture_enable, light_enable, shadow_enable, hud_enable
    ):
        Window.create(
            camera=camera,
            width=width, height=height,
            display_mode=display_mode,
            use_default_material=0,
            show_hud=show_hud,
            show_window=show_window,
            texture_enable=texture_enable,
            light_enable=light_enable,
            shadow_enable=shadow_enable,
            hud_enable=hud_enable
        )

    @classmethod
    def hud_prc(cls, camera):
        _mya_core.Scene.clear_all_hud()
        _hud.HUD.restore()
        _hud.HUD.create(camera)

    @classmethod
    def render_setting_prc(cls, camera, display_mode, texture_enable, light_enable, shadow_enable):
        RenderSettings.setup(
            camera, display_mode,
            texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable
        )

    @classmethod
    def image_prc(cls, image_file_path, width, height, start_frame, end_frame, hud_enable, percent, quality):
        file_opt = bsc_storage.StgFileOpt(image_file_path)
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
            showOrnaments=hud_enable,
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
        movie_file_path,
        camera='|persp|perspShape',
        frame=None, frame_step=1, resolution=(1280, 720),
        display_mode=6, show_hud=False, show_window=False,
        percent=100, quality=100, fps=24,
        texture_enable=False, light_enable=False, shadow_enable=False,
        hud_enable=False, play_enable=False,
    ):
        if resolution is None:
            resolution = _mya_core.RenderSettings.get_resolution()

        w, h = resolution
        # if _mya_core.Scene.get_is_ui_mode():
        #     if show_hud is True:
        #         h += 60

        cls.create_window(
            camera=camera, width=480, height=320, display_mode=display_mode, show_hud=show_hud, show_window=show_window,
            texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable,
            hud_enable=hud_enable
        )
        if show_hud is True:
            cls.hud_prc(camera)

        cls.render_setting_prc(
            camera, display_mode,
            texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable
        )

        file_opt = bsc_storage.StgFileOpt(movie_file_path)
        file_path_base = file_opt.path_base

        directory_path_tmp = '{}/{}'.format(
            bsc_storage.StgUserMtd.get_user_temporary_directory(),
            bsc_core.UuidMtd.generate_new()
        )
        bsc_storage.StgPathMtd.create_directory(directory_path_tmp)
        # directory_path_tmp = '{}.images'.format(file_path_base)
        image_file_path_tmp = '{}/image.jpg'.format(directory_path_tmp)
        movie_file_path_tmp = '{}/movie.mov'.format(directory_path_tmp)

        start_frame, end_frame = _mya_core.Frame.auto_range(frame)
        if frame_step > 1:
            frames = bsc_core.RawFrameRangeMtd.get(
                (start_frame, end_frame), frame_step
            )
            for i_frame in frames:
                _mya_core.Frame.set_current(i_frame)
                cls.image_prc(
                    image_file_path=image_file_path_tmp, start_frame=i_frame, end_frame=i_frame,
                    width=w, height=h, hud_enable=hud_enable,
                    percent=percent, quality=quality
                )
        else:
            cls.image_prc(
                image_file_path=image_file_path_tmp, start_frame=start_frame, end_frame=end_frame,
                width=w, height=h, hud_enable=hud_enable,
                percent=percent, quality=quality
            )

        cls.movie_prc(
            image_file_path=image_file_path_tmp,
            movie_file_path=movie_file_path_tmp,
            start_frame=start_frame, end_frame=end_frame, fps=fps
        )
        # close window
        Window.close()
        # copy to source
        bsc_storage.StgFileOpt(movie_file_path_tmp).copy_to_file(
            movie_file_path, replace=True
        )
        # clear temp
        bsc_storage.StgDirectoryOpt(directory_path_tmp).do_delete()

        if play_enable is True:
            os.startfile(
                movie_file_path
            )

    @classmethod
    def generate_movie_file_path(cls, directory_path=None, update_scheme='new_version'):
        scene_file_path = _mya_core.SceneFile.get_current()
        file_opt = bsc_storage.StgFileOpt(scene_file_path)

        if directory_path is not None:
            if os.path.isdir(directory_path) is False:
                return None
            ptn = six.u(
                '{}/{}.v{{version}}.mov'
            ).format(
                bsc_core.auto_unicode(directory_path), bsc_core.auto_unicode(file_opt.name_base)
            )
            return bsc_core.PtnVersionPath.generate_as_new_version(ptn)
        else:
            ptn = six.u(
                '{}.v{{version}}.mov'
            ).format(bsc_core.auto_unicode(file_opt.path_base))
            return bsc_core.PtnVersionPath.generate_as_new_version(ptn)

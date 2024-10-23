# coding:utf-8
import os

import six
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

from .... import core as _mya_core

from ...animation import core as _animation_core

from .. import core as _prv_core


class PlayblastOpt(object):
    LOG_KEY = 'playblast'

    @classmethod
    def create_window(
        cls, camera, width, height, display_mode, show_hud, show_window,
        texture_enable, light_enable, shadow_enable, hud_enable,
        use_exists_window=False
    ):
        _prv_core.Window.create(
            camera=camera,
            width=width, height=height,
            display_mode=display_mode,
            use_default_material=0,
            show_hud=show_hud,
            show_window=show_window,
            texture_enable=texture_enable,
            light_enable=light_enable,
            shadow_enable=shadow_enable,
            hud_enable=hud_enable,
            use_exists_window=use_exists_window
        )

    @classmethod
    def hud_prc(cls, camera):
        _mya_core.Scene.clear_all_hud()
        _prv_core.HUD.restore()
        _prv_core.HUD.create(camera)

    @classmethod
    def render_setting_prc(cls, camera, display_mode, texture_enable, light_enable, shadow_enable):
        _prv_core.RenderSetting.setup(
            camera, display_mode,
            texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable
        )

    @classmethod
    def camera_prc(cls, camera, camera_display_options):
        _prv_core.CameraDisplay.setup(
            camera, camera_display_options
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
    def movie_prc(cls, image_file_path, movie_file_path, start_frame, end_frame, fps):
        image_file_opt = bsc_storage.StgFileOpt(image_file_path)
        image_file_path_base = image_file_opt.path_base

        image_file_path_ = '{}.####.jpg'.format(image_file_path_base)

        cmd_script = bsc_core.BscFfmpeg.generate_image_concat_cmd_script(
            input=image_file_path_,
            output=movie_file_path,
            start_frame=start_frame,
            end_frame=end_frame,
            fps=fps,
            coding=bsc_core.BscFfmpeg.Coding.H264
        )

        bsc_log.Log.trace_method_result(
            cls.LOG_KEY, 'run cmd script: `{}`'.format(cmd_script)
        )
        bsc_core.BscProcess.execute_as_trace(
            cmd_script
        )

    @classmethod
    def execute(
        cls,
        movie_file_path,
        camera='|persp|perspShape',
        frame=None, frame_step=1, fps=None,
        resolution=(1280, 720),
        display_mode=6, show_hud=False, show_window=False,
        percent=100, quality=100,
        texture_enable=False, light_enable=False, shadow_enable=False,
        hud_enable=False, play_enable=False,
        use_exists_window=False,
        camera_display_options=None
    ):
        if resolution is None:
            resolution = _mya_core.RenderSettings.get_resolution()

        w, h = resolution

        cls.create_window(
            camera=camera, width=480, height=320, display_mode=display_mode, show_hud=show_hud, show_window=show_window,
            texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable,
            hud_enable=hud_enable,
            use_exists_window=use_exists_window
        )
        if show_hud is True:
            cls.hud_prc(camera)

        cls.render_setting_prc(
            camera, display_mode,
            texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable
        )

        cls.camera_prc(camera, camera_display_options)

        cmds.select(clear=1)

        file_opt = bsc_storage.StgFileOpt(movie_file_path)
        file_path_base = file_opt.path_base

        directory_path_tmp = '{}/{}'.format(
            bsc_storage.StgUser.get_user_temporary_directory(),
            bsc_core.BscUuid.generate_new()
        )
        bsc_storage.StgPath.create_directory(directory_path_tmp)
        # directory_path_tmp = '{}.images'.format(file_path_base)
        image_file_path_tmp = '{}/image.jpg'.format(directory_path_tmp)
        movie_file_path_tmp = '{}/movie.mov'.format(directory_path_tmp)

        start_frame, end_frame = _mya_core.Frame.auto_range(frame)
        if fps is None:
            fps = _mya_core.Frame.get_fps_value()

        if frame_step > 1:
            frames = bsc_core.BscFrameRange.get(
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
        _prv_core.Window.close()
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
    def load_auto(cls, **kwargs):
        scheme = kwargs['scheme']
        if scheme == 'default':
            q = _animation_core.AdvRigAssetsQuery()

            q.do_update()

            for i in q.get_all():
                i.switch_to_original()
            # noinspection PyBroadException
            try:
                movie_file_path = cls.generate_movie_file_path(directory_path=None, update_scheme='no_version')
                camera = _mya_core.Camera.get_active()
                frame = _mya_core.Frame.get_frame_range()
                fps = _mya_core.Frame.get_fps_value()
                resolution = _mya_core.RenderSettings.get_resolution()
                cls.execute(
                    movie_file_path=movie_file_path,
                    camera=camera,
                    frame=frame, fps=fps,
                    resolution=resolution,
                    texture_enable=True, hud_enable=True, play_enable=True,
                    camera_display_options=None
                )
            except Exception:
                pass

            finally:
                for i in q.get_all():
                    i.switch_to_cache()

    @classmethod
    def show_window(
        cls,
        camera='|persp|perspShape',
        resolution=(1280, 720), display_mode=6, hud_enable=False, show_hud=False,
        texture_enable=False, light_enable=False, shadow_enable=False,
        show_window=True,
        node_filter_scheme='',
        camera_display_options=None,
    ):
        if resolution is None:
            resolution = _mya_core.RenderSettings.get_resolution()

        w, h = resolution

        cls.create_window(
            camera=camera, width=w, height=h, display_mode=display_mode, show_hud=show_hud, show_window=show_window,
            texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable,
            hud_enable=hud_enable
        )
        if show_hud is True:
            cls.hud_prc(camera)

        cls.render_setting_prc(
            camera, display_mode,
            texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable
        )

        cls.camera_prc(camera, camera_display_options)

    @classmethod
    def generate_movie_file_path(cls, directory_path=None, update_scheme='new_version'):
        scene_file_path = _mya_core.SceneFile.get_current()
        file_opt = bsc_storage.StgFileOpt(scene_file_path)

        if directory_path is not None:
            if os.path.isdir(directory_path) is False:
                return None
            if update_scheme == 'new_version':
                ptn = six.u(
                    '{}/{}.v{{version}}.mov'
                ).format(
                    bsc_core.auto_unicode(directory_path), bsc_core.auto_unicode(file_opt.name_base)
                )
                return bsc_core.BscVersion.generate_as_new_version(ptn)
            else:
                return six.u('{}/{}.mov').format(
                    bsc_core.auto_unicode(directory_path), bsc_core.auto_unicode(file_opt.name_base)
                )
        else:
            if update_scheme == 'new_version':
                ptn = six.u(
                    '{}.v{{version}}.mov'
                ).format(bsc_core.auto_unicode(file_opt.path_base))
                return bsc_core.BscVersion.generate_as_new_version(ptn)
            else:
                return six.u('{}.mov').format(
                    bsc_core.auto_unicode(file_opt.path_base)
                )


class PlayblastProcess(object):
    def __init__(
        self,
        file_path, movie_file_path, camera_path, start_frame, end_frame, frame_step, fps,
        width, height,
        texture_enable, light_enable, shadow_enable
    ):
        self._file_path = file_path
        self._movie_file_path = movie_file_path
        self._camera = camera_path
        self._start_frame, self._end_frame = start_frame, end_frame
        self._frame_step = frame_step
        self._fps = fps

        self._width, self._height = width, height

        self._texture_enable = texture_enable
        self._light_enable = light_enable
        self._shadow_enable = shadow_enable

    @classmethod
    def generate_task_args(
        cls,
        camera_path,
        frame, frame_step, fps,
        resolution,
        texture_enable, light_enable, shadow_enable
    ):
        file_path_current = _mya_core.SceneFile.get_current()
        file_path_opt_current = bsc_storage.StgFileOpt(file_path_current)
        ptn = six.u(
            '{}.export.v{{version}}.ma'
        ).format(
            bsc_core.auto_unicode(file_path_opt_current.path_base)
        )
        file_path = bsc_core.BscVersion.generate_as_new_version(
            ptn
        )
        file_opt = bsc_storage.StgFileOpt(file_path)

        _mya_core.SceneFile.export_file(
            file_path, keep_reference=True
        )
        start_frame, end_frame = frame
        width, height = resolution
        movie_file_path = six.u('{}.mov').format(bsc_core.auto_unicode(file_opt.path_base))
        cmd_script = qsm_gnl_core.MayaCacheProcess.generate_cmd_script_by_option_dict(
            'playblast',
            dict(
                file=file_path,
                movie=movie_file_path,
                camera=camera_path,
                start_frame=start_frame, end_frame=end_frame, frame_step=frame_step, fps=fps,
                width=width, height=height,
                texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable
            )
        )
        task_name = '[playblast][{}][{}][{}]'.format(
            file_opt.name, '{}x{}'.format(width, height), '{}-{}'.format(start_frame, end_frame)
        )
        return task_name, file_path, movie_file_path, cmd_script

    def execute(self):
        # print self._file_path
        file_opt = bsc_storage.StgFileOpt(self._file_path)
        if file_opt.get_is_file():
            _mya_core.SceneFile.open(self._file_path)

            q = _animation_core.AdvRigAssetsQuery()

            q.do_update()

            for i in q.get_all():
                i.switch_to_original()

            PlayblastOpt.execute(
                movie_file_path=self._movie_file_path,
                camera=self._camera,
                frame=(self._start_frame, self._end_frame), frame_step=self._frame_step, fps=self._fps,
                resolution=(self._width, self._height),
                texture_enable=self._texture_enable, light_enable=self._light_enable, shadow_enable=self._shadow_enable
            )
        else:
            raise RuntimeError()

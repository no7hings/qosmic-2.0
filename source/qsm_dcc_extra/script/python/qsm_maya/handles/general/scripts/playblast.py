# coding:utf-8
import os

import six

import functools
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.web as bsc_web

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import qsm_general.process as qsm_gnl_process

import qsm_general.prc_task as qsm_gnl_prc_task

import qsm_maya.core as qsm_mya_core

from ...animation import core as _tsk_anm_core

from .. import core as _core


class PlayblastOpt(object):
    LOG_KEY = 'playblast'

    @classmethod
    def create_window(
        cls, camera, width, height, display_mode, show_hud, show_window,
        texture_enable, light_enable, shadow_enable, hud_enable,
        use_exists_window=False
    ):
        _core.Window.create(
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
        qsm_mya_core.Scene.clear_all_hud()
        _core.HUD.restore()
        _core.HUD.create(camera)

    @classmethod
    def render_setting_prc(cls, camera, display_mode, texture_enable, light_enable, shadow_enable):
        _core.RenderSetting.setup(
            camera, display_mode,
            texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable
        )

    @classmethod
    def camera_prc(cls, camera, camera_display_options):
        _core.CameraDisplay.setup(
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
    def movie_prc(cls, image_file_path, movie_file_path, start_frame, end_frame, clip_start, fps):
        image_file_opt = bsc_storage.StgFileOpt(image_file_path)
        image_file_path_base = image_file_opt.path_base

        image_file_path_ = '{}.####.jpg'.format(image_file_path_base)

        if clip_start is not None:
            start_frame = clip_start

        bsc_core.BscFfmpegVideo.create_by_image_sequence(
            image_sequence=image_file_path_,
            video_path=movie_file_path,
            start_frame=start_frame,
            end_frame=end_frame,
            fps=fps,
            replace=True
        )

    @classmethod
    def execute(
        cls,
        movie_file_path,
        camera='|persp|perspShape',
        frame=None, 
        clip_start=None, 
        frame_step=1, 
        fps=None,
        resolution=(1280, 720),
        display_mode=6, show_hud=False, show_window=False,
        percent=100, quality=100,
        texture_enable=False, light_enable=False, shadow_enable=False,
        hud_enable=False, play_enable=False,
        use_exists_window=False,
        camera_display_options=None
    ):

        bsc_log.Log.trace_method_result(
            cls.LOG_KEY, 'camera is {}'.format(camera)
        )

        if resolution is None:
            resolution = qsm_mya_core.RenderSettings.get_resolution()

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

        start_frame, end_frame = qsm_mya_core.Frame.auto_range(frame)
        if fps is None:
            fps = qsm_mya_core.Frame.get_fps_value()

        if frame_step > 1:
            frames = bsc_core.BscFrameRange.get(
                (start_frame, end_frame), frame_step
            )
            for i_frame in frames:
                qsm_mya_core.Frame.set_current(i_frame)
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
            start_frame=start_frame, end_frame=end_frame, clip_start=clip_start, fps=fps
        )
        # close window
        _core.Window.close()
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
    def execute_auto(cls, **kwargs):
        scheme = kwargs['scheme']
        clip_start = kwargs['clip_start']
        # noinspection PyBroadException
        try:
            clip_start = int(clip_start)
        except Exception:
            clip_start = None

        if scheme == 'default':
            q = _tsk_anm_core.AdvRigAssetsQuery()

            q.do_update()

            for i in q.get_all():
                i.switch_to_original()
            # noinspection PyBroadException
            try:
                movie_file_path = cls.generate_movie_file_path(directory_path=None, update_scheme='no_version')
                camera = qsm_mya_core.Camera.get_non_default_with_dialog()
                frame = qsm_mya_core.Frame.get_frame_range()
                fps = qsm_mya_core.Frame.get_fps_value()
                resolution = qsm_mya_core.RenderSettings.get_resolution()
                cls.execute(
                    movie_file_path=movie_file_path,
                    camera=camera,
                    frame=frame, clip_start=clip_start, fps=fps,
                    resolution=resolution,
                    texture_enable=True, hud_enable=True, play_enable=True,
                    camera_display_options=None
                )
            except Exception:
                pass

            finally:
                for i in q.get_all():
                    i.switch_to_cache()
        elif scheme == 'subprocess':
            def open_fnc_(movie_file_path_):
                bsc_storage.StgFileOpt(movie_file_path_).start_in_system()

            camera = qsm_mya_core.Camera.get_non_default_with_dialog()
            frame = qsm_mya_core.Frame.get_frame_range()
            fps = qsm_mya_core.Frame.get_fps_value()
            resolution = qsm_mya_core.RenderSettings.get_resolution()

            task_name, file_path, movie_file_path, cmd_script = PlayblastProcess.generate_subprocess_args(
                camera_path=camera,
                frame=frame, 
                clip_start=clip_start, 
                frame_step=1, 
                fps=fps,
                resolution=resolution,
                texture_enable=True, light_enable=False, shadow_enable=False
            )

            import lxgui.proxy.widgets as gui_prx_widgets

            task_window = gui_prx_widgets.PrxSprcTaskWindow()
            if task_window._language == 'chs':
                task_window.set_window_title('拍屏')
                task_window.set_tip(
                    '正在拍屏，请耐心等待；\n'
                    '这个过程可能会让MAYA前台操作产生些许卡顿；\n'
                    '如需要终止任务，请点击“关闭”'
                )
            else:
                task_window.set_window_title('Playblast')

            task_window.submit(
                'playblast',
                task_name,
                cmd_script,
                completed_fnc=functools.partial(open_fnc_, movie_file_path),
            )

            task_window.show_window_auto(exclusive=False)
        elif scheme == 'backstage':
            if qsm_gnl_prc_task.BackstageTaskSubmit.check_is_valid() is False:
                return

            camera = qsm_mya_core.Camera.get_non_default_with_dialog()
            frame = qsm_mya_core.Frame.get_frame_range()
            fps = qsm_mya_core.Frame.get_fps_value()
            resolution = qsm_mya_core.RenderSettings.get_resolution()

            task_name, file_path, movie_file_path, cmd_script = PlayblastProcess.generate_subprocess_args(
                camera_path=camera,
                frame=frame, 
                clip_start=clip_start, 
                frame_step=1, 
                fps=fps,
                resolution=resolution,
                texture_enable=True, light_enable=False, shadow_enable=False
            )

            qsm_gnl_prc_task.BackstageTaskSubmit.execute(
                task_group=None, task_type='playblast', task_name=task_name,
                cmd_script=cmd_script, icon_name='application/maya',
                file_path=file_path, output_file_path=movie_file_path,
                completed_notice_dict=dict(
                    title='通知',
                    message='拍屏结束了, 是否打开视频?',
                    # todo? exec must use unicode
                    ok_python_script='import os; os.startfile("{}".decode("utf-8"))'.format(
                        bsc_core.ensure_string(movie_file_path)
                    ),
                    status='normal'
                )
            )
        elif scheme == 'farm':
            if qsm_gnl_prc_task.FarmTaskSubmit.check_is_valid() is False:
                return

            camera = qsm_mya_core.Camera.get_non_default_with_dialog()
            frame = qsm_mya_core.Frame.get_frame_range()
            fps = qsm_mya_core.Frame.get_fps_value()
            resolution = qsm_mya_core.RenderSettings.get_resolution()

            option_hook = PlayblastProcess.generate_farm_hook_option(
                camera_path=camera,
                frame=frame, 
                clip_start=clip_start, 
                frame_step=1, 
                fps=fps,
                resolution=resolution,
                texture_enable=True, light_enable=False, shadow_enable=False
            )

            qsm_gnl_prc_task.FarmTaskSubmit.execute_by_hook_option(option_hook)

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
            resolution = qsm_mya_core.RenderSettings.get_resolution()

        w, h = resolution

        cls.create_window(
            camera=camera, width=w, height=h, display_mode=display_mode, show_hud=show_hud, show_window=show_window,
            texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable,
            hud_enable=hud_enable
        )
        if show_hud is True:
            cls.hud_prc(camera)

        # update render setting
        cls.render_setting_prc(
            camera, display_mode,
            texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable
        )

        # update camera setting
        cls.camera_prc(camera, camera_display_options)

    @classmethod
    def generate_movie_file_path(cls, directory_path=None, update_scheme='new_version'):
        scene_file_path = qsm_mya_core.SceneFile.get_current()
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
    def __init__(self, **kwargs):
        self._kwargs = kwargs

        self._file_path = kwargs.get('file')
        self._movie_file_path = kwargs.get('movie')
        self._camera_path = kwargs.get('camera')
        self._start_frame, self._end_frame = kwargs.get('start_frame'), kwargs.get('end_frame')
        self._clip_start = kwargs.get('clip_start')
        self._frame_step = kwargs.get('frame_step')
        self._fps = kwargs.get('fps')

        self._width, self._height = kwargs.get('width'), kwargs.get('height')

        self._texture_enable = kwargs.get('texture_enable')
        self._light_enable = kwargs.get('light_enable')
        self._shadow_enable = kwargs.get('shadow_enable')

    @classmethod
    def generate_subprocess_args(
        cls,
        camera_path,
        frame, clip_start, frame_step, fps,
        resolution,
        texture_enable, light_enable, shadow_enable
    ):
        file_current = qsm_mya_core.SceneFile.get_current()
        file_opt_current = bsc_storage.StgFileOpt(file_current)
        ptn = six.u(
            '{}/playblast/{}.v{{version}}.ma'
        ).format(
            bsc_core.ensure_unicode(file_opt_current.directory_path),
            bsc_core.ensure_unicode(file_opt_current.name_base),
        )
        file_path = bsc_core.BscVersion.generate_as_new_version(
            ptn
        )
        file_opt = bsc_storage.StgFileOpt(file_path)

        qsm_mya_core.SceneFile.export_file(
            file_path, keep_reference=True
        )
        start_frame, end_frame = frame
        width, height = resolution
        movie_file_path = six.u('{}.mov').format(bsc_core.auto_unicode(file_opt.path_base))
        cmd_script = qsm_gnl_process.MayaCacheSubprocess.generate_cmd_script_by_option_dict(
            'playblast',
            dict(
                file=file_path,
                movie=movie_file_path,
                camera=camera_path,
                start_frame=start_frame, end_frame=end_frame, 
                clip_start=clip_start, 
                frame_step=frame_step, 
                fps=fps,
                width=width, height=height,
                texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable
            )
        )
        task_name = '[playblast][{}][{}][{}]'.format(
            file_opt.name, '{}x{}'.format(width, height), '{}-{}'.format(start_frame, end_frame)
        )
        return task_name, file_path, movie_file_path, cmd_script

    @classmethod
    def generate_farm_hook_option(
        cls,
        camera_path,
        frame, 
        clip_start, 
        frame_step, 
        fps,
        resolution,
        texture_enable, light_enable, shadow_enable
    ):
        file_current = qsm_mya_core.SceneFile.get_current()
        file_opt_current = bsc_storage.StgFileOpt(file_current)
        ptn = six.u(
            '{}/playblast/{}.v{{version}}.ma'
        ).format(
            bsc_core.ensure_unicode(file_opt_current.directory_path),
            bsc_core.ensure_unicode(file_opt_current.name_base),
        )
        file_path = bsc_core.BscVersion.generate_as_new_version(
            ptn
        )
        file_opt = bsc_storage.StgFileOpt(file_path)

        qsm_mya_core.SceneFile.export_file(
            file_path, keep_reference=True
        )
        start_frame, end_frame = frame
        width, height = resolution
        movie_file_path = six.u('{}.mov').format(bsc_core.ensure_unicode(file_opt.path_base))

        task_name = '[playblast][{}][{}][{}]'.format(
            file_opt.name, '{}x{}'.format(width, height), '{}-{}'.format(start_frame, end_frame)
        )

        hook_option = qsm_gnl_process.MayaCacheSubprocess.generate_hook_option_fnc(
            'playblast',
            dict(
                file=file_path,
                movie=movie_file_path,
                camera=camera_path,
                start_frame=start_frame, end_frame=end_frame, 
                clip_start=clip_start, 
                frame_step=frame_step, 
                fps=fps,
                width=width, height=height,
                texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable
            ),
            job_name=task_name,
            output_file=bsc_web.UrlValue.quote(movie_file_path)
        )

        return hook_option

    def execute(self):
        # print self._file_path
        file_opt = bsc_storage.StgFileOpt(self._file_path)
        if file_opt.get_is_file():
            with bsc_log.LogProcessContext.create(maximum=3) as l_p:
                # step 1
                qsm_mya_core.SceneFile.open(self._file_path)
                l_p.do_update()
                # step 2
                q = _tsk_anm_core.AdvRigAssetsQuery()
                q.do_update()
                for i in q.get_all():
                    i.switch_to_original()
                l_p.do_update()
                # step 3
                PlayblastOpt.execute(
                    movie_file_path=self._movie_file_path,
                    camera=self._camera_path,
                    frame=(self._start_frame, self._end_frame), 
                    clip_start=self._clip_start, 
                    frame_step=self._frame_step, fps=self._fps,
                    resolution=(self._width, self._height),
                    texture_enable=self._texture_enable,
                    light_enable=self._light_enable,
                    shadow_enable=self._shadow_enable
                )
                l_p.do_update()
        else:
            raise RuntimeError()

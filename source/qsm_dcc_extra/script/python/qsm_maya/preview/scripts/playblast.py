# coding:utf-8
import six

import lxbasic.core as bsc_core

import lxbasic.web as bsc_web

import lxbasic.storage as bsc_storage

from ... import core as _mya_core

from ...asset import core as _ast_core

from ...rig import core as _rig_core

from .. import core as _prv_core


class PlayblastOpt(object):
    @classmethod
    def get_file_path(cls, file_path):
        file_opt = bsc_storage.StgFileOpt(file_path)

    @classmethod
    def generate_args(cls, camera_path, frame, frame_step, resolution, texture_enable, light_enable, shadow_enable):
        file_path_current = _mya_core.SceneFile.get_current()
        file_path_opt_current = bsc_storage.StgFileOpt(file_path_current)
        ptn = six.u(
            '{}.export.v{{version}}.ma'
        ).format(
            bsc_core.auto_unicode(file_path_opt_current.path_base)
        )
        file_path = bsc_core.PtnVersionPath.generate_as_new_version(
            ptn
        )
        file_opt = bsc_storage.StgFileOpt(file_path)

        # _mya_core.SceneFile.export_file(
        #     file_path, keep_reference=True
        # )
        start_frame, end_frame = frame
        width, height = resolution
        movie_file_path = six.u('{}.mov').format(bsc_core.auto_unicode(file_opt.path_base))
        cmd_script = _ast_core.MayaCacheProcess.generate_command(
            (
                'method=playblast&file={file}&movie={movie}&camera={camera}'
                '&start_frame={start_frame}&end_frame={end_frame}&frame_step={frame_step}'
                '&width={width}&height={height}'
                '&texture_enable={texture_enable}&light_enable={light_enable}&shadow_enable={shadow_enable}'
            ).format(
                file=bsc_web.UrlValue.quote(file_path),
                movie=bsc_web.UrlValue.quote(movie_file_path),
                camera=camera_path,
                start_frame=start_frame, end_frame=end_frame, frame_step=frame_step,
                width=width, height=height,
                texture_enable=texture_enable, light_enable=light_enable, shadow_enable=shadow_enable
            )
        )
        task_name = '[playblast][{}][{}][{}]'.format(
            file_opt.name, '{}x{}'.format(width, height), '{}-{}'.format(start_frame, end_frame)
        )
        return task_name, file_path, movie_file_path, cmd_script


class PlayblastProcess(object):
    def __init__(
        self, file_path, movie_file_path, camera_path, start_frame, end_frame, frame_step, width, height,
        texture_enable, light_enable, shadow_enable
    ):
        self._file_path = file_path
        self._movie_file_path = movie_file_path
        self._camera = camera_path
        self._start_frame, self._end_frame = start_frame, end_frame
        self._frame_step = frame_step
        self._width, self._height = width, height

        self._texture_enable = texture_enable
        self._light_enable = light_enable
        self._shadow_enable = shadow_enable

    def execute(self):
        file_opt = bsc_storage.StgFileOpt(self._file_path)
        if file_opt.get_is_file():
            _mya_core.SceneFile.open(self._file_path)

            q = _rig_core.AdvRigsQuery()

            q.do_update()

            for i in q.get_all():
                i.switch_to_original()

            movie_file_path = '{}.mov'.format(file_opt.get_path_base())

            _prv_core.Playblast.execute(
                movie_file_path=movie_file_path,
                camera=self._camera,
                frame=(self._start_frame, self._end_frame), frame_step=self._frame_step,
                resolution=(self._width, self._height),
                texture_enable=self._texture_enable, light_enable=self._light_enable, shadow_enable=self._shadow_enable
            )

# coding:utf-8
import lxbasic.storage as bsc_storage

from ... import core as _mya_core

from ...asset import core as _ast_core

from .. import core as _prv_core


class PlayblastOpt(object):
    @classmethod
    def get_file_path(cls, file_path):
        file_opt = bsc_storage.StgFileOpt(file_path)

    @classmethod
    def generate_args(cls, file_path, camera_path, frame, resolution):
        start_frame, end_frame = frame
        width, height = resolution
        cmd_script = _ast_core.MayaCacheProcess.generate_command(
            (
                'method=playblast&file={file}&camera={camera}'
                '&start_frame={start_frame}&end_frame={end_frame}'
                '&width={width}&height={height}'
            ).format(
                file=file_path,
                camera=camera_path,
                start_frame=start_frame, end_frame=end_frame,
                width=width, height=height
            )
        )
        return cmd_script


class PlayblastProcess(object):
    def __init__(self, file_path, camera_path, start_frame, end_frame, width, height):
        self._file_path = file_path
        self._camera = camera_path
        self._start_frame, self._end_frame = start_frame, end_frame
        self._width, self._height = width, height

    def execute(self):
        file_opt = bsc_storage.StgFileOpt(self._file_path)
        if file_opt.get_is_file():
            _mya_core.SceneFile.open(self._file_path)

            movie_file_path = '{}.mov'.format(file_opt.get_path_base())

            _prv_core.Playblast.execute(
                file_path=movie_file_path,
                camera=self._camera,
                frame=(self._start_frame, self._end_frame),
                resolution=(self._width, self._height)
            )

# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

from . import time_ as _time


class GpuCache(object):
    """
gpuCache -startTime 1 -endTime 1 -optimize -optimizationThreshold 40000 -writeMaterials -dataFormat ogawa -directory "X:/QSM_TST/Assets/prp/test_gpu_assembly/Maya/Final/tmp/gpu" -fileName "test" -saveMultipleFiles false pCube1 pSphere1;
    """
    @classmethod
    def to_mel_script(cls, gpu_file_path, location, frame=None, with_material=False):
        directory_path = os.path.dirname(gpu_file_path)
        file_name = os.path.splitext(os.path.basename(gpu_file_path))[0]
        start_frame, end_frame = _time.Time.to_frame_range(frame)
        if isinstance(location, (tuple, list)):
            location = ' '.join(location)
        return (
            'gpuCache'
            ' -startTime {start_frame} -endTime {end_frame}'
            ' -optimize -optimizationThreshold 40000'
            ' -writeMaterials -dataFormat ogawa'
            ' -directory "{directory_path}" -fileName "{file_name}"'
            ' -saveMultipleFiles false {location};'
        ).format(
            start_frame=start_frame, end_frame=end_frame,
            directory_path=directory_path, file_name=file_name,
            location=location
        )

    @classmethod
    def export_frame_(cls, gpu_file_path, location, frame=None, with_material=False):
        mel_script = cls.to_mel_script(
            gpu_file_path, location, frame, with_material
        )
        print mel_script
        # mel.eval(mel_script)

    @classmethod
    def export_frame(cls, gpu_file_path, location, frame=None, with_material=False):
        cmds.loadPlugin('gpuCache', quiet=1)
        if cmds.objExists(location):
            start_frame, end_frame = _time.Time.to_frame_range(frame)

            directory_path = os.path.dirname(gpu_file_path)
            file_name = os.path.splitext(os.path.basename(gpu_file_path))[0]
            cmds.gpuCache(
                location,
                startTime=start_frame, endTime=end_frame,
                optimize=1, optimizationThreshold=40000,
                writeMaterials=with_material,
                dataFormat='ogawa',
                directory=directory_path,
                fileName=file_name
            )

    @classmethod
    def export_sequence(cls, gpu_file_path, location, frame, with_material=False):
        start_frame, end_frame = _time.Time.to_frame_range(frame)

        frame_range = range(start_frame, end_frame+1)
        seq_range = range(end_frame-start_frame+1)
        for i_seq in seq_range:
            i_frame = frame_range[i_seq]
            i_frame_seq = i_seq+1
            i_gpu_file_path = ('.'+str(i_frame_seq).zfill(4)).join(os.path.splitext(gpu_file_path))
            cls.export_frame(location, i_gpu_file_path, i_frame, with_material)

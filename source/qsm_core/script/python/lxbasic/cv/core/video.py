# coding:utf-8
from __future__ import print_function

import sys

import os

import threading

import lxbasic.core as bsc_core

from .wrap import *


class VideoCaptureOpt(object):
    def __init__(self, video_path):
        self._video_path = bsc_core.auto_unicode(video_path)
        self._cpt = cv2.VideoCapture(self._video_path)

    def is_valid(self):
        return self._cpt.isOpened()

    def get_data(self, frame_index):
        self._cpt.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = self._cpt.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            return frame, width, height, channel

    def create_thumbnail(self, file_path, frame_index=None):
        directory_path = os.path.dirname(file_path)
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

        frame_count = self.get_frame_count()
        if frame_index is None:
            frame_index = int(frame_count/2)

        self._cpt.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = self._cpt.read()
        if ret:
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite(file_path, frame)

    def get_frame_count(self):
        return int(self._cpt.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_fps_tag(self):
        return int(self._cpt.get(cv2.CAP_PROP_FPS))

    def release(self):
        self._cpt.release()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cpt.release()


class FrameExtractor(object):
    def __init__(self, video_path, image_path, frame_index=0, timeout=10):
        self._video_path = video_path
        self._frame_index = frame_index
        self._image_path = image_path
        self._timeout = timeout
        self._frame = None
        self._ret = False

    def extract_frame(self):
        self._cpt = cv2.VideoCapture(self._video_path)

        if not self._cpt.isOpened():
            sys.stderr.write('Error: Cannot open video file.\n')
            return

        frame_count = int(self._cpt.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(self._cpt.get(cv2.CAP_PROP_FPS))

        frame_index = min(fps*30, int(frame_count/2))

        # frame_index = 0

        self._cpt.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        self._ret, self._frame = self._cpt.read()
        self._cpt.release()

    def save_frame(self):
        if self._ret:
            directory_path = os.path.dirname(self._image_path)
            if os.path.exists(directory_path) is False:
                os.makedirs(directory_path)

            cv2.imwrite(self._image_path, self._frame)
            sys.stdout.write('Thumbnail saved at: "{}"\n'.format(bsc_core.auto_string(self._image_path)))
        else:
            sys.stderr.write('Error: Cannot read frame.\n')

    def execute(self):
        thread = threading.Thread(target=self.extract_frame)
        thread.start()
        thread.join(self._timeout)

        if thread.is_alive():
            sys.stderr.write('Error: Reading frame timed out.\n')
        else:
            self.save_frame()


class ImageConcat(object):
    def __init__(self, image_paths,  video_path, fps=24):
        self._image_paths = image_paths
        self._video_path = video_path
        self._fps = fps

    def execute(self):
        frame = cv2.imread(self._image_paths[0])
        height, width, channels = frame.shape
        # coding is mpeg
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(self._video_path, fourcc, self._fps, (width, height))

        for i_image_path in self._image_paths:
            i_rgb_image = cv2.imread(i_image_path)
            # do not convert
            # i_bgr_image = cv2.cvtColor(i_rgb_image, cv2.COLOR_RGB2BGR)
            video.write(i_rgb_image)

        video.release()
        cv2.destroyAllWindows()

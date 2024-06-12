# coding:utf-8
from __future__ import print_function

import six

import os

import cv2

import threading

import lxbasic.core as bsc_core


class VideoCaptureOpt(object):
    def __init__(self, video_path):
        self._video_path = bsc_core.auto_unicode(video_path)
        self._cpt = cv2.VideoCapture(self._video_path)
        # if not self._cpt.isOpened():
        #     raise Exception('Cannot open video file: {}'.format(bsc_core.auto_string(video_path)))

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

    def get_fps(self):
        return self._cpt.get(cv2.CAP_PROP_FPS)

    def release(self):
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
            print("Error: Cannot open video file.")
            return

        frame_count = int(self._cpt.get(cv2.CAP_PROP_FRAME_COUNT))

        frame_index = min(24*100, int(frame_count/2))

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
            print("Thumbnail saved at:", self._image_path)
        else:
            print("Error: Cannot read frame.")

    def run(self):
        thread = threading.Thread(target=self.extract_frame)
        thread.start()
        thread.join(self._timeout)

        if thread.is_alive():
            print("Error: Reading frame timed out.")
        else:
            self.save_frame()

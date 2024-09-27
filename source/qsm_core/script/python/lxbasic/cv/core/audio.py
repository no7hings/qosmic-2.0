# coding:utf-8
import os.path

import numpy as np

import cv2

import pydub

import pyaudio

import threading

import six

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import pickle


class AudioCaptureOpt(object):
    @classmethod
    def _load_audio(cls, file_path, cache_root):
        key, cache_directory_path = cls._generate_cache_directory(file_path, cache_root)

        cache_file_path = '{}/{}.pkl'.format(cache_directory_path, key)

        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'rb') as f:
                audio = pickle.load(f)
        else:
            audio = pydub.AudioSegment.from_file(file_path)
            with open(cache_file_path, 'wb') as f:
                pickle.dump(audio, f)

        return audio
    
    @classmethod
    def _generate_cache_directory(cls, file_path, cache_root):
        key = bsc_core.BscUuid.generate_by_file(file_path)
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)

        cache_directory_path = '{}/{}'.format(cache_root, region)
        if not os.path.exists(cache_directory_path):
            os.makedirs(cache_directory_path)
        
        return key, cache_directory_path

    def create_pickle(self, cache_file_path):
        audio = pydub.AudioSegment.from_file(self._file_path)
        with open(cache_file_path, 'wb') as f:
            pickle.dump(audio, f)

    def __init__(self, file_path):
        file_path = bsc_core.ensure_unicode(file_path)
        
        self._cache_root = 'Z:/caches/temporary/.audio-cache'

        self._file_path = file_path
        self._audio_segment = self._load_audio(self._file_path, self._cache_root)

        self._fps = 1000

    def is_valid(self):
        return True

    def get_data(self):
        n_channels = self._audio_segment.channels
        frame_rate = self._audio_segment.frame_rate
        samples = np.array(self._audio_segment.get_array_of_samples())
        # split channel
        if n_channels == 2:
            samples = samples.reshape((-1, 2))
        return samples, frame_rate, self._audio_segment.duration_seconds, n_channels

    def get_frame_rate(self):
        return self._fps

    def generate_qt_image(self, qt_img_cls):
        waveform, frame_rate, duration, n_channels = self.get_data()
        img_width, img_height = self.compute_image_size()
        cv_img = self._generate_cv_image(waveform, img_width, img_height, n_channels)
        # convert bgr to rgb
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        height, width, channel = cv_img.shape
        return qt_img_cls(cv_img.data, width, height, channel*width, qt_img_cls.Format_RGB888)
    
    def generate_at_image_from_cache(self, qt_img_cls):
        key, cache_directory_path = self._generate_cache_directory(self._file_path, self._cache_root)
        cache_file_path = '{}/{}.png'.format(cache_directory_path, key)
        if os.path.isfile(cache_file_path) is False:
            self.create_thumbnail(cache_file_path)
        
        qt_image = qt_img_cls()
        qt_image.load(cache_file_path)
        return qt_image

    def get_frame_count(self):
        return len(self._audio_segment)

    @classmethod
    def _get_waveform_data(cls, wav_path):
        audio = pydub.AudioSegment.from_file(wav_path)
        n_channels = audio.channels
        frame_rate = audio.frame_rate
        samples = np.array(audio.get_array_of_samples())
        # split channel
        if n_channels == 2:
            samples = samples.reshape((-1, 2))

        return samples, frame_rate, audio.duration_seconds, n_channels

    @classmethod
    def _generate_cv_image(cls, waveform, img_width, img_height, n_channels):
        cv_img = np.ones((img_height, img_width, 3), dtype=np.uint8)*31
        mid_y = img_height//2
        max_value = np.max(np.abs(waveform))
        step = len(waveform)//img_width

        for i in range(img_width):
            index = i*step
            if index < len(waveform):
                left_value = waveform[index, 0] if n_channels == 2 else waveform[index]
                y_value = int((float(left_value)/float(max_value))*(mid_y-1))
                # left channel is orange, b, g, r
                cv2.line(cv_img, (i, mid_y), (i, mid_y-y_value), (63, 127, 255), 1)

                if n_channels == 2 and index+1 < len(waveform):
                    right_value = waveform[index, 1]
                    right_y_value = int((float(right_value)/float(max_value))*(mid_y-1))
                    # right channel is blue, b, g, r
                    cv2.line(cv_img, (i, mid_y), (i, mid_y+right_y_value), (255, 127, 63), 1)
        return cv_img

    @classmethod
    def _save_image(cls, cv_img, file_path):
        # create directory first
        directory_path = os.path.dirname(file_path)
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

        file_path = file_path.encode('mbcs')
        cv2.imwrite(file_path, cv_img)

    def play_from(self, percent):
        frame_count = self.get_frame_count()
        start_time = frame_count*percent

        segment_to_play = self._audio_segment[start_time:]

        p = pyaudio.PyAudio()

        stream = p.open(
            format=pyaudio.paInt16,
            channels=segment_to_play.channels,
            rate=segment_to_play.frame_rate,
            output=True
        )

        samples = segment_to_play.get_array_of_samples()
        stream.write(samples.tostring())

        stream.stop_stream()
        stream.close()
        p.terminate()

    def play_from_with_thread(self, percent):
        thread = threading.Thread(target=self.play_from, kwargs=dict(percent=percent))
        thread.start()

    def compute_image_size(self):
        img_w_min, img_w_max = 512, 4096
        img_w = int(self._audio_segment.frame_count()/(self._audio_segment.frame_rate/128))
        img_w = max(min(img_w, img_w_max), img_w_min)
        return img_w, 256

    def create_thumbnail(self, file_path, replace=False):
        # fixme: has chinese word
        file_path = bsc_core.ensure_unicode(file_path)

        if os.path.isfile(file_path) is True:
            if replace is False:
                return

        waveform, frame_rate, duration, n_channels = self.get_data()
        img_width, img_height = self.compute_image_size()
        cv_img = self._generate_cv_image(waveform, img_width, img_height, n_channels)
        self._save_image(cv_img, file_path)

    def create_compress(self, file_path, bit_rate='64k', sample_rate=22050, replace=False):
        # fixme: has chinese word
        file_path = bsc_core.ensure_unicode(file_path)

        # create directory first
        directory_path = os.path.dirname(file_path)
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

        if os.path.isfile(file_path) is True:
            if replace is False:
                return

        if sample_rate < self._audio_segment.frame_rate:
            self._audio_segment = self._audio_segment.set_frame_rate(sample_rate)
        self._audio_segment.export(file_path, format='mp3', bitrate=bit_rate)


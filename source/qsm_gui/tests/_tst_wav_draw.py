# coding:utf-8
import os

os.environ['PATH'] += ';Y:/deploy/rez-packages/external/ffmpeg/6.0/platform-windows/bin'

import sys
import wave
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from pydub import AudioSegment
from tempfile import NamedTemporaryFile


def convert_mp3_to_wav(mp3_path):
    audio = AudioSegment.from_mp3(mp3_path)
    temp_wav = NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(temp_wav.name, format="wav")
    return temp_wav.name


def get_waveform_data(wav_path):
    wav_file = wave.open(wav_path, "r")
    frames = wav_file.getnframes()
    framerate = wav_file.getframerate()
    duration = frames / float(framerate)
    audio_data = wav_file.readframes(frames)
    waveform = np.frombuffer(audio_data, dtype=np.int16)
    wav_file.close()
    return waveform, duration


class WaveformWidget(QtWidgets.QWidget):
    def __init__(self, waveform, duration, parent=None):
        super(WaveformWidget, self).__init__(parent)
        self.waveform = waveform
        self.duration = duration
        self.setMinimumSize(800, 400)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        rect = self.rect()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Draw background
        painter.fillRect(rect, QtGui.QColor(30, 30, 30))

        # Draw waveform
        pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
        pen.setWidth(1)
        painter.setPen(pen)

        w = rect.width()
        h = rect.height()
        mid_y = h//2

        time = np.linspace(0., self.duration, len(self.waveform))
        step = len(self.waveform)//w

        for i in range(0, w):
            x = i
            index = i*step
            if index < len(self.waveform):
                y = int((self.waveform[index]/np.max(np.abs(self.waveform)))*mid_y)
                painter.drawLine(x, mid_y-y, x, mid_y+y)


def main(mp3_path):
    wav_path = convert_mp3_to_wav(mp3_path)
    waveform, duration = get_waveform_data(wav_path)
    print waveform, duration

    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QMainWindow()
    # window.setWindowTitle("Waveform Viewer")
    #
    # waveform_widget = WaveformWidget(waveform, duration)
    # window.setCentralWidget(waveform_widget)
    # window.show()
    #
    # sys.exit(app.exec_())


if __name__ == "__main__":
    mp3_path = "Z:/temporaries/tst_wav/test-1.mp3"  # Replace with your MP3 file path
    main(mp3_path)


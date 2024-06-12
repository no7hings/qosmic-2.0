# coding:utf-8
import sys
import time
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
import cv2
import numpy as np
import os

class TransparentWindow(QMainWindow):
    def __init__(self):
        super(TransparentWindow, self).__init__()
        self.setWindowTitle('Transparent Window')
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.autoFillBackground()
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 800, 600)
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        self.start_button = QPushButton('Start Recording', self)
        self.start_button.setGeometry(320, 250, 160, 40)
        self.start_button.clicked.connect(self.start_stop_recording)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_screen)
        self.recording = False

        self.frame_count = 0
        self.recording_duration = 10  # seconds
        self.output_directory = 'Z:/temeporaries/dongchangbao/snapshot'
        self.video_writer = None

    def start_stop_recording(self):
        if not self.recording:
            self.start_recording()
            self.start_button.setText('Stop Recording')
        else:
            self.stop_recording()
            self.start_button.setText('Start Recording')

    def capture_screen(self):
        if self.recording:
            screenshot = QApplication.primaryScreen().grabWindow(self.winId()).toImage()
            screenshot = screenshot.convertToFormat(QImage.Format_ARGB32)
            width = screenshot.width()
            height = screenshot.height()
            ptr = screenshot.bits()
            ptr.setsize(screenshot.byteCount())
            img_arr = np.array(ptr).reshape(height, width, 4)  # ARGB format
            img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGRA2BGR)

            frame_filename = os.path.join(self.output_directory, 'frame_{:04d}.png'.format(self.frame_count))
            cv2.imwrite(frame_filename, img_arr)
            self.frame_count += 1

            current_time = time.time()
            if current_time - self.start_recording_time >= self.recording_duration:
                self.stop_recording()

    def start_recording(self):
        self.frame_count = 0
        self.start_recording_time = time.time()
        self.recording = True
        self.create_output_directory()
        self.timer.start(33)  # Start the timer with 30 FPS

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.timer.stop()
            print("Frames saved in directory: " + self.output_directory)

    def create_output_directory(self):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setPen(Qt.red)
    #     # painter.setFont(painter.font().family(), 30)
    #     painter.drawText(self.rect(), Qt.AlignCenter, 'Recording Screen')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.setWindowOpacity(0.5)  # 设置窗口透明度
    window.show()
    sys.exit(app.exec_())






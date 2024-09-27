# coding:utf-8
import os

os.environ['PATH'] += ';Y:/deploy/rez-packages/external/ffmpeg/6.0/platform-windows/bin'

import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt
from pydub import AudioSegment
import pyaudio

class AudioThread(QThread):
    progress = pyqtSignal(float)  # 发送进度百分比
    finished = pyqtSignal()  # 播放结束信号

    def __init__(self, audio_segment):
        super(AudioThread, self).__init__()
        self.audio_segment = audio_segment
        self.stop_flag = False
        self.start_time = 0  # 播放起始时间，单位为毫秒
        self.loop = False     # 默认不循环播放

    def set_start_time(self, start_time):
        """设置播放的起始时间，单位为毫秒"""
        self.start_time = start_time

    def run(self):
        p = pyaudio.PyAudio()

        while not self.stop_flag:
            segment_to_play = self.audio_segment[self.start_time:]  # 根据起始时间切片

            # 设置音频流参数
            stream = p.open(format=pyaudio.paInt16,
                            channels=segment_to_play.channels,
                            rate=segment_to_play.frame_rate,
                            output=True)

            samples = segment_to_play.get_array_of_samples()
            total_frames = len(samples)
            chunk_size = 1024

            # 每次播放一部分数据，发送进度百分比信号
            for i in range(0, total_frames, chunk_size):
                if self.stop_flag:
                    break
                chunk = samples[i:i + chunk_size].tostring()
                stream.write(chunk)

                # 计算并发送进度百分比
                progress_percentage = (i + chunk_size) / float(total_frames) * 100
                self.progress.emit(progress_percentage)

            # 如果不循环，则退出播放循环
            if not self.loop or self.stop_flag:
                break

        # 停止和关闭流
        stream.stop_stream()
        stream.close()
        p.terminate()

        # 发出播放完成的信号
        self.finished.emit()

    def stop(self):
        """停止播放"""
        self.stop_flag = True


class AudioPlayer(QWidget):
    def __init__(self):
        super(AudioPlayer, self).__init__()
        self.setWindowTitle('Audio Player with Slider')

        # 布局
        layout = QVBoxLayout()

        # 播放按钮
        self.play_button = QPushButton('Play from Slider Position')
        self.play_button.clicked.connect(self.start_playback)
        layout.addWidget(self.play_button)

        # 停止按钮
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_playback)
        layout.addWidget(self.stop_button)

        # 进度滑块
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)  # 假设音频的长度是100%
        self.slider.sliderMoved.connect(self.slider_moved)  # 当用户滑动滑块时调整播放位置
        layout.addWidget(self.slider)

        # 显示进度的标签
        self.progress_label = QLabel('Progress: 0%')
        layout.addWidget(self.progress_label)

        self.setLayout(layout)

        # 加载音频文件
        self.audio_segment = AudioSegment.from_file('Z:/temporaries/tst_wav/751515__recalltv__happy-piano-tag.mp3')  # 替换为你的音频文件路径

        # 初始化播放线程
        self.audio_thread = None
        self.slider_dragging = False  # 标识滑块是否正在被拖动

    def start_playback(self):
        # 停止当前播放
        self.stop_playback()

        # 获取滑块当前的进度百分比
        slider_value = self.slider.value()
        audio_duration = len(self.audio_segment)  # 获取音频的时长（毫秒）
        start_time = (slider_value / 100.0) * audio_duration  # 根据滑块位置计算起始时间

        # 创建新的线程并从滑块指定位置开始播放
        self.audio_thread = AudioThread(self.audio_segment)
        self.audio_thread.set_start_time(start_time)

        # 连接信号，更新进度
        self.audio_thread.progress.connect(self.update_progress)
        self.audio_thread.finished.connect(self.on_finished)
        self.audio_thread.start()

    def stop_playback(self):
        if self.audio_thread is not None:
            self.audio_thread.stop()
            self.audio_thread.wait()  # 等待线程结束

    def update_progress(self, percentage):
        """更新播放进度的显示，并且同步更新滑块的位置"""
        if not self.slider_dragging:  # 如果没有拖动滑块，才更新滑块位置
            self.slider.setValue(int(percentage))
        # self.progress_label.setText(f'Progress: {percentage:.2f}%')

    def on_finished(self):
        """处理播放结束的逻辑"""
        self.progress_label.setText('Progress: 100%')
        print("Playback finished")

    def slider_moved(self, value):
        """用户拖动滑块时，立即调整播放进度"""
        self.slider_dragging = True  # 标记正在拖动滑块
        audio_duration = len(self.audio_segment)  # 获取音频时长（毫秒）
        start_time = (value / 100.0) * audio_duration  # 根据滑块值计算新的起始时间

        if self.audio_thread is not None and self.audio_thread.isRunning():
            self.audio_thread.stop()  # 停止当前的播放线程
            self.audio_thread.wait()

        # 重新创建线程，从新的位置开始播放
        self.audio_thread = AudioThread(self.audio_segment)
        self.audio_thread.set_start_time(start_time)
        self.audio_thread.progress.connect(self.update_progress)
        self.audio_thread.finished.connect(self.on_finished)
        self.audio_thread.start()
        self.slider_dragging = False  # 拖动结束

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = AudioPlayer()
    player.show()
    sys.exit(app.exec_())


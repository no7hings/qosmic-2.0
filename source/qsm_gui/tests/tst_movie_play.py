# coding=utf-8
import sys
import cv2
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget


class VideoPreview(QGraphicsView):
    def __init__(self, video_path, parent=None):
        super(VideoPreview, self).__init__(parent)
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise Exception("Cannot open video file: {}".format(video_path))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_interval = int(1000/self.fps)  # 帧间隔时间，单位为毫秒
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        self.setMouseTracking(True)

        # 添加计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play_video)
        self.play_timer = QTimer(self)
        self.play_timer.timeout.connect(self.next_frame)
        self.is_playing = False
        self.current_frame_index = 0

    def update_frame(self, frame_index):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3*width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.pixmap_item.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio))

    def mouseMoveEvent(self, event):
        pos = event.pos()
        if 0 <= pos.x() < self.width():
            frame_index = int((float(pos.x())/self.width())*self.total_frames)
            frame_index = min(self.total_frames-1, frame_index)  # 防止索引越界
            self.update_frame(frame_index)
            self.current_frame_index = frame_index
            if self.is_playing:
                self.is_playing = False
                self.play_timer.stop()
        self.timer.start(1000)  # 鼠标移动时重新启动计时器
        super(VideoPreview, self).mouseMoveEvent(event)

    def enterEvent(self, event):
        self.timer.start(1000)  # 鼠标悬停1秒后触发
        super(VideoPreview, self).enterEvent(event)

    def leaveEvent(self, event):
        self.timer.stop()
        self.is_playing = False
        self.play_timer.stop()
        super(VideoPreview, self).leaveEvent(event)

    def play_video(self):
        self.is_playing = True
        self.timer.stop()
        self.play_timer.start(self.frame_interval)

    def next_frame(self):
        if self.is_playing and self.current_frame_index < self.total_frames:
            self.update_frame(self.current_frame_index)
            self.current_frame_index += 1
        else:
            self.play_timer.stop()

    def resizeEvent(self, event):
        self.update_frame(int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))
        super(VideoPreview, self).resizeEvent(event)

    def closeEvent(self, event):
        self.cap.release()
        super(VideoPreview, self).closeEvent(event)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Video Preview Example")

        layout = QVBoxLayout()

        # 使用视频文件路径
        video_path = "Z:/temeporaries/dongchangbao/playblast_tool/test.export.v004.mov"

        self.video_preview = VideoPreview(video_path)
        layout.addWidget(self.video_preview)

        self.setLayout(layout)
        self.resize(640, 480)  # 初始化窗口大小


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())




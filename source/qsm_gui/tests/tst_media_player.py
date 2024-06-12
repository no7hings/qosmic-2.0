# coding:utf-8
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl

class VideoPlayer(QWidget):
    def __init__(self):
        super(VideoPlayer, self).__init__()

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        # Create a slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addWidget(self.slider)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("path/to/your/video.mp4")))

        # Connect signals
        self.slider.sliderMoved.connect(self.set_position)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        # Connect mouse events to video widget
        videoWidget.setMouseTracking(True)
        videoWidget.installEventFilter(self)

        self.mediaPlayer.play()

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def eventFilter(self, source, event):
        if event.type() == event.MouseMove and source is self.mediaPlayer.videoOutput():
            pos = event.pos()
            duration = self.mediaPlayer.duration()
            video_widget_width = self.mediaPlayer.videoOutput().width()
            new_position = duration * pos.x() / video_widget_width
            self.mediaPlayer.setPosition(new_position)
        return super(VideoPlayer, self).eventFilter(source, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())

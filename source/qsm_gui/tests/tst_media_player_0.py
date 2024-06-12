# coding:utf-8
import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QGraphicsView, QGraphicsScene
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtMultimedia import QGraphicsVideoItem
from PySide2.QtCore import Qt, QUrl, QPointF

class VideoPlayer(QWidget):
    def __init__(self):
        super(VideoPlayer, self).__init__()

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoItem = QGraphicsVideoItem()

        # Create a QGraphicsView
        self.graphicsView = QGraphicsView()
        self.graphicsView.setScene(QGraphicsScene())
        self.graphicsView.scene().addItem(self.videoItem)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.installEventFilter(self)

        # Create a slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.graphicsView)
        layout.addWidget(self.slider)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(self.videoItem)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("path/to/your/video.mp4")))

        # Connect signals
        self.slider.sliderMoved.connect(self.set_position)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        self.mediaPlayer.play()

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def eventFilter(self, source, event):
        if event.type() == event.MouseMove and source is self.graphicsView.viewport():
            pos = event.pos()
            duration = self.mediaPlayer.duration()
            video_widget_width = self.graphicsView.viewport().width()
            new_position = duration * pos.x() / video_widget_width
            self.mediaPlayer.setPosition(new_position)
        return super(VideoPlayer, self).eventFilter(source, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())

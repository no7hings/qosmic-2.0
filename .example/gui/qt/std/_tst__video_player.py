from lxgui.qt.core.wrap import *


class TestVideoPlayer(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(TestVideoPlayer, self).__init__(*args, **kwargs)

        self.mediaPlayer = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)

        videoWidget = QtMultimediaWidgets.QVideoWidget()

        self.playButton = QtWidgets.QPushButton()
        # self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QtWidgets.QLabel()
        self.errorLabel.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Maximum
        )

        # Create new action
        openAction = QtWidgets.QAction(QtGui.QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        # exitAction.triggered.connect(self.exitCall)

        # Create a widget for window contents

        # Create layouts to place inside widget
        controlLayout = QtWidgets.QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.mediaPlayer.setMedia(
            QtMultimedia.QMediaContent(
                QtCore.QUrl.fromLocalFile(
                    '/production/shows/nsa_dev/assets/chr/nikki/shared/srf/surfacing/nikki.srf.surfacing.v007/review/nikki.srf.surfacing.v007.mov'
                )
            )
        )

    def openFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
                QtCore.QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    # def exitCall(self):
    #     sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


class W(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.Window)

        wgt = QtWidgets.QWidget()
        self.setCentralWidget(wgt)

        lot = QtWidgets.QVBoxLayout(wgt)

        self._m = TestVideoPlayer()
        lot.addWidget(self._m)


app = QtWidgets.QApplication(sys.argv)

w = W()

w.setFixedSize(480, 480)
w.show()

sys.exit(app.exec_())
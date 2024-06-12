# coding:utf-8
import sys
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition, QMutexLocker
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import time


class WorkerThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, name, parent):
        super(WorkerThread, self).__init__()
        self.name = name
        self.parent = parent
        self.is_running = True

    def run(self):
        with QMutexLocker(self.parent.mutex):
            while self.parent.current_threads >= self.parent.max_concurrent_threads:
                self.parent.condition.wait(self.parent.mutex)
            self.parent.current_threads += 1

        self.update_signal.emit('Thread {} started'.format(self.name))
        for i in range(10):  # 模拟耗时操作，分段执行以便检查标志
            if not self.is_running:
                self.update_signal.emit('Thread {} terminated'.format(self.name))
                break
            time.sleep(0.5)
        else:
            self.update_signal.emit('Thread {} finished'.format(self.name))

        with QMutexLocker(self.parent.mutex):
            self.parent.current_threads -= 1
            self.parent.condition.wakeAll()

    def stop(self):
        self.is_running = False

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.current_threads = 0
        self.max_concurrent_threads = 3
        self.threads = []
        self.start_threads()

    def initUI(self):
        self.setWindowTitle('QThread Example with QMutex')
        self.setGeometry(300, 300, 300, 200)

        self.layout = QVBoxLayout()
        self.start_button = QPushButton('Start Threads')
        self.stop_button = QPushButton('Stop All Threads')
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.label = QLabel('')
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

        self.start_button.clicked.connect(self.start_threads)
        self.stop_button.clicked.connect(self.stop_threads)

    def start_threads(self):
        for i in range(5):
            thread = WorkerThread('#{}'.format(i + 1), self)
            thread.update_signal.connect(self.update_label)
            self.threads.append(thread)
            thread.start()  # Start thread in a non-blocking manner

    def stop_threads(self):
        for thread in self.threads:
            thread.stop()
        for thread in self.threads:
            thread.wait()  # 等待线程完成
        self.threads = []

    def update_label(self, message):
        current_text = self.label.text()
        self.label.setText(current_text + '\n' + message)

    def closeEvent(self, event):
        self.stop_threads()  # 确保在关闭窗口时停止所有线程
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin1 = MainWindow()
    mainWin1.show()
    mainWin2 = MainWindow()
    mainWin2.show()
    sys.exit(app.exec_())


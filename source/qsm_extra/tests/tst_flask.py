from __future__ import print_function

from flask import Flask

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
import multiprocessing
import threading

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, Flask is running alongside PyQt!"


def run_flask():
    app.run(debug=False, use_reloader=False)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("PyQt and Flask")
        self.setGeometry(100, 100, 600, 400)
        self.label = QLabel("Flask and PyQt Running", self)
        self.label.setGeometry(50, 50, 500, 50)

    def display_error(self, error_message):
        print(error_message)
        # self.label.setText(f"Error: {error_message}")


def start_server_use_process():
    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()
    return flask_process


def main():
    flask_process = start_server_use_process()

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    def cleanup():
        flask_process.terminate()
        flask_process.join()

    app.aboutToQuit.connect(cleanup)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

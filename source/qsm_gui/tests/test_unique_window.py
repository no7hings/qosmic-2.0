# coding:utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QSharedMemory, QTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow).__init__()
        self.setWindowTitle("Unique Window Example")
        self.setGeometry(100, 100, 600, 400)


def is_already_running():
    # Unique key for the shared memory segment
    shared_memory_key = "UniquePyQtTool"

    shared_memory = QSharedMemory(shared_memory_key)

    if shared_memory.attach():
        # If attach() returns True, it means the shared memory segment already exists
        return True
    else:
        if not shared_memory.create(1):
            # If create() fails, it means we couldn't create the shared memory segment
            return True

    return False


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if is_already_running():
        QMessageBox.warning(None, "Warning", "The application is already running.")
        sys.exit(1)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

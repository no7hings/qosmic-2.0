import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSystemSemaphore, QSharedMemory

# from ui import window_ui  # .py file compiled from .ui file
# 
# 
# class LoginWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
# 
#         self.ui = window_ui.Ui_MainWindow()  # call to init ui
#         self.ui.setupUi(self)


def launch():
    app = QtWidgets.QApplication(sys.argv)  # create app instance at top, to able to show QMessageBox is required
    window_id = 'pingidapplication'
    shared_mem_id = 'pingidsharedmem'
    semaphore = QSystemSemaphore(window_id, 1)
    semaphore.acquire()  # Raise the semaphore, barring other instances to work with shared memory

    if sys.platform != 'win32':
        # in linux / unix shared memory is not freed when the application terminates abnormally,
        # so you need to get rid of the garbage
        nix_fix_shared_mem = QSharedMemory(shared_mem_id)
        if nix_fix_shared_mem.attach():
            nix_fix_shared_mem.detach()

    shared_memory = QSharedMemory(shared_mem_id)

    if shared_memory.attach():  # attach a copy of the shared memory, if successful, the application is already running
        is_running = True
    else:
        shared_memory.create(1)  # allocate a shared memory block of 1 byte
        is_running = False

    semaphore.release()

    if is_running:  # if the application is already running, show the warning message
        QtWidgets.QMessageBox.warning(None, 'Application already running',
                                      'One instance of the application is already running.')
        return

    # normal process of creating & launching MainWindow
    # window = LoginWindow()
    # window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    launch()
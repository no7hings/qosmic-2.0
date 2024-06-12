# coding:utf-8
import sys
import time
from PyQt5.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super(Worker, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
        except Exception as e:
            self.signals.error.emit((type(e), e.args))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()

def example_task(seconds):
    time.sleep(2)
    return seconds

class ThreadPoolManager(QObject):
    def __init__(self, max_threads):
        super(ThreadPoolManager, self).__init__()
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(max_threads)
        self.tasks = []

    def add_task(self, func, *args, **kwargs):
        worker = Worker(func, *args, **kwargs)
        worker.signals.finished.connect(self.task_finished)
        worker.signals.error.connect(self.task_error)
        worker.signals.result.connect(self.task_result)
        self.threadpool.start(worker)
        self.tasks.append(worker)

    def task_finished(self):
        # Check if any threads are still running
        while self.threadpool.activeThreadCount() > 0:
            time.sleep(0.1)  # Adjust sleep time as needed
        self.tasks = []

    def task_error(self, err):
        print "Error:", err

    def task_result(self, result):
        print "Result:", result


if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = ThreadPoolManager(max_threads=2)  # 设置最大线程数量为2
    manager.add_task(example_task, 1)
    manager.add_task(example_task, 2)
    manager.add_task(example_task, 3)
    manager.add_task(example_task, 4)
    manager.add_task(example_task, 5)
    sys.exit(app.exec_())

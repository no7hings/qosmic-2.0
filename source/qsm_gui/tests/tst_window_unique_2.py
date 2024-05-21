# coding:utf-8
# from PyQt5 import QtWidgets, QtCore, QtNetwork
#
# class SingleApplication(QtWidgets.QApplication):
#     messageAvailable = QtCore.pyqtSignal(object)
#
#     def __init__(self, argv, key):
#         super().__init__(argv)
#         # cleanup (only needed for unix)
#         QtCore.QSharedMemory(key).attach()
#         self._memory = QtCore.QSharedMemory(self)
#         self._memory.setKey(key)
#         if self._memory.attach():
#             self._running = True
#         else:
#             self._running = False
#             if not self._memory.create(1):
#                 raise RuntimeError(self._memory.errorString())
#
#     def isRunning(self):
#         return self._running
#
# class SingleApplicationWithMessaging(SingleApplication):
#     def __init__(self, argv, key):
#         super().__init__(argv, key)
#         self._key = key
#         self._timeout = 1000
#         self._server = QtNetwork.QLocalServer(self)
#         if not self.isRunning():
#             self._server.newConnection.connect(self.handleMessage)
#             self._server.listen(self._key)
#
#     def handleMessage(self):
#         socket = self._server.nextPendingConnection()
#         if socket.waitForReadyRead(self._timeout):
#             self.messageAvailable.emit(
#                 socket.readAll().data().decode('utf-8'))
#             socket.disconnectFromServer()
#         else:
#             QtCore.qDebug(socket.errorString())
#
#     def sendMessage(self, message):
#         if self.isRunning():
#             socket = QtNetwork.QLocalSocket(self)
#             socket.connectToServer(self._key, QtCore.QIODevice.WriteOnly)
#             if not socket.waitForConnected(self._timeout):
#                 print(socket.errorString())
#                 return False
#             if not isinstance(message, bytes):
#                 message = message.encode('utf-8')
#             socket.write(message)
#             if not socket.waitForBytesWritten(self._timeout):
#                 print(socket.errorString())
#                 return False
#             socket.disconnectFromServer()
#             return True
#         return False
#
# class Window(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         self.edit = QtWidgets.QLineEdit(self)
#         self.edit.setMinimumWidth(300)
#         layout = QtWidgets.QVBoxLayout(self)
#         layout.addWidget(self.edit)
#
#     def handleMessage(self, message):
#         self.edit.setText(message)
#
# if __name__ == '__main__':
#
#     import sys
#
#     key = 'app-name'
#
#     # send commandline args as message
#     if len(sys.argv) > 1:
#         app = SingleApplicationWithMessaging(sys.argv, key)
#         if app.isRunning():
#             print('app is already running')
#             app.sendMessage(' '.join(sys.argv[1:]))
#             sys.exit(1)
#     else:
#         app = SingleApplication(sys.argv, key)
#         if app.isRunning():
#             print('app is already running')
#             sys.exit(1)
#
#     window = Window()
#     app.messageAvailable.connect(window.handleMessage)
#     window.show()
#
#     sys.exit(app.exec_())
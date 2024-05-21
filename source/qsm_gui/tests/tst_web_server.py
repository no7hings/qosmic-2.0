# # coding:utf-8
# from PyQt5.QtCore import QObject, pyqtSlot, QCoreApplication
# from PyQt5.QtWebSockets import QWebSocketServer, QWebSocket
#
#
# class WebSocketServer(QObject):
#     def __init__(self, parent=None):
#         super(WebSocketServer, self).__init__(parent)
#         self.server = QWebSocketServer('Test Server', QWebSocketServer.NonSecureMode)
#
#         if self.server.listen(port=12345):
#             print('WebSocket server listening on port 12345')
#
#         self.server.newConnection.connect(self.onNewConnection)
#         self.clients = []
#
#     @pyqtSlot()
#     def onNewConnection(self):
#         client_socket = self.server.nextPendingConnection()
#         client_socket.textMessageReceived.connect(self.processMessage)
#         client_socket.disconnected.connect(self.socketDisconnected)
#         self.clients.append(client_socket)
#         print('New client connected')
#
#     @pyqtSlot(str)
#     def processMessage(self, message):
#         sender = self.sender()
#         print(f'Received message: {message}')
#         # Echo the message back to all connected clients
#         for client in self.clients:
#             client.sendTextMessage(message)
#
#     @pyqtSlot()
#     def socketDisconnected(self):
#         sender = self.sender()
#         self.clients.remove(sender)
#         sender.deleteLater()
#         print('Client disconnected')
#
#
# if __name__ == '__main__':
#     import sys
#
#     app = QCoreApplication(sys.argv)
#     server = WebSocketServer()
#     sys.exit(app.exec_())

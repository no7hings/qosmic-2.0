# coding:utf-8

from PySide2 import QtCore, QtGui, QtWidgets


class Splash(QtWidgets.QDialog):
    """
    Splash screen with customizable message shown during the application startup.
    """
    def __init__(self, parent=None):
        """
        Constructor. Widget is initially hidden.
        """
        QtWidgets.QDialog.__init__(self, parent)

        # self.setWindowFlags(QtCore.Qt.SplashScreen)

    def set_message(self, text):
        """
        Sets the message to display on the widget.

        :param text: Text to display.
        """
        self.setWindowTitle(text)
        QtWidgets.QApplication.instance().processEvents()

    def show(self):
        """
        Shows the dialog of top of all other dialogs.
        """
        QtWidgets.QDialog.show(self)
        self.raise_()
        self.activateWindow()

    def hide(self):
        """
        Hides the dialog and clears the current message.
        """
        # There's no sense showing the previous message when we show the
        # splash next time.
        self.set_message("")
        QtWidgets.QDialog.hide(self)


if __name__ == '__main__':
    import time
    import sys
    #
    app = QtWidgets.QApplication(sys.argv)
    w = Splash()
    w.show()
    #
    for i in range(10):
        time.sleep(1)
        w.set_message(str(i))
    #
    #
    sys.exit(app.exec_())

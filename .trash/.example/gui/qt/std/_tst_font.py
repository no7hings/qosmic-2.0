# coding:utf-8
import sys

import textwrap

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.title = "Available fonts"
        self.width = 500
        self.height = 500
        self.top = 10
        self.left = 10
        self.initUI()
        self.show()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.layout = QVBoxLayout()

        self.comboBox = QComboBox(self)
        self.families = QFontDatabase().families()
        print(type(self.families))
        self.comboBox.addItems(self.families)
        self.comboBox.setEditable(True)
        # Dont Add the new values to combobox
        self.comboBox.setInsertPolicy(QComboBox.NoInsert)
        # Autocompleting
        self.comboBox.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        song = ("""
            My Heart Will Go On\n
            by Celine Dion\n
            Every night in my dreams
            I see you, I feel you
            That is how I know you go on
            Far across the distance
            And spaces between us
            You have come to show you go on
            Near, far, wherever you are
            I believe that the heart does go on
            Once more, you open the door
            And you're here in my heart
            And my heart will go on and on
            Love can touch us one time
            And last for a lifetime
            And never let go 'til we're gone
            Love was when I loved you
            One true time I'd hold to
            In my life, we'll always go on
            Near, far, wherever you are
            I believe that the heart does go on
            Once more, you open the door
            And you're here in my heart
            And my heart will go on and on
            You're here, there's nothing I fear
            And I know that my heart will go on
            We'll stay forever this way
            You are safe in my heart and
            My heart will go on and """)
        # print(song)
        # when ever new item is selected from comboxbox call textChanged method
        self.comboBox.currentTextChanged.connect(self.textChanged)
        self.textEdit = QPlainTextEdit(song)
        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.textEdit)
        # setting layout
        self.setLayout(self.layout)

    # Called when combo box current text is changed
    def textChanged(self):
        fontStr = self.comboBox.currentText()
        if fontStr in self.families:
            self.textEdit.setFont(QFont(fontStr))


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())
import sys

from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QStackedWidget, QLabel, QHBoxLayout


class StackedWidgetExample(QWidget):
    def __init__(self):
        super(StackedWidgetExample, self).__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('QStackedWidget Example')
        self.setGeometry(100, 100, 400, 300)

        # Create a stacked widget
        self.stackedWidget = QStackedWidget(self)

        # Create multiple pages (widgets) to add to the stacked widget
        self.page1 = QWidget()
        layout1 = QVBoxLayout()
        label1 = QLabel('This is Page 1')
        layout1.addWidget(label1)
        self.page1.setLayout(layout1)

        self.page2 = QWidget()
        layout2 = QVBoxLayout()
        label2 = QLabel('This is Page 2')
        layout2.addWidget(label2)
        self.page2.setLayout(layout2)

        self.page3 = QWidget()
        layout3 = QVBoxLayout()
        label3 = QLabel('This is Page 3')
        layout3.addWidget(label3)
        self.page3.setLayout(layout3)

        # Add pages to the stacked widget
        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)
        self.stackedWidget.addWidget(self.page3)

        # Create buttons to switch between pages
        self.button1 = QPushButton('Page 1', self)
        self.button1.clicked.connect(self.showPage1)

        self.button2 = QPushButton('Page 2', self)
        self.button2.clicked.connect(self.showPage2)

        self.button3 = QPushButton('Page 3', self)
        self.button3.clicked.connect(self.showPage3)

        # Create a layout for the buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.button1)
        buttonLayout.addWidget(self.button2)
        buttonLayout.addWidget(self.button3)

        # Create a main layout for the window
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.stackedWidget)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

    def showPage1(self):
        self.stackedWidget.setCurrentWidget(self.page1)

    def showPage2(self):
        self.stackedWidget.setCurrentWidget(self.page2)

    def showPage3(self):
        self.stackedWidget.setCurrentWidget(self.page3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StackedWidgetExample()
    window.show()
    sys.exit(app.exec_())
# coding:utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtGui import QOpenGLShader, QOpenGLShaderProgram, QMatrix4x4
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from pyfbx import *

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.fbx_loader = FBXLoader()
        self.fbx_scene = None
        self.rotation = 0

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

        # Load FBX file
        self.fbx_scene = self.fbx_loader.load_scene("path/to/your/fbx/file.fbx")

        # Create shader program
        self.program = QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, "vertex_shader.glsl")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, "fragment_shader.glsl")
        self.program.link()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.program.bind()

        # Set modelview and projection matrices
        modelview = QMatrix4x4()
        modelview.translate(0.0, 0.0, -5.0)
        modelview.rotate(self.rotation, 0.0, 1.0, 0.0)
        self.program.setUniformValue("modelview_matrix", modelview)

        projection = QMatrix4x4()
        projection.perspective(45.0, self.width() / self.height(), 0.1, 100.0)
        self.program.setUniformValue("projection_matrix", projection)

        # Render FBX scene
        if self.fbx_scene is not None:
            self.fbx_scene.render()

        self.program.release()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

    def timerEvent(self, event):
        self.rotation += 1
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.glWidget = GLWidget()
        self.setCentralWidget(self.glWidget)
        self.setWindowTitle("Display FBX with PyQt")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

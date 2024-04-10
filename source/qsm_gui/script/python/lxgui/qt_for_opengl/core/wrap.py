# coding:utf-8
import pkgutil as _pkgutil

QT_OPENGL_FLAG = False

__pyopengl = _pkgutil.find_loader('pxr')

if __pyopengl:
    QT_OPENGL_FLAG = True

    from OpenGL import GL, GLUT

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
based on python 2.7 amd64, PyQt4
needed modules : PIL, openEXR

put an exr file in same path as this script and enter exr name below
gammaCorrected 0 takes exrToJpg function, 1 takes exrToJpgGamma function (lot slower !)
"""
import sys, array
from PyQt4 import QtGui, QtCore

from PIL.ImageQt import ImageQt as PilImageQt
import OpenEXR, Imath, Image

exrPath = "Seq_0144.exr"
gammaCorrected = 0

class exr(QtGui.QWidget):
    def __init__(self):
        super(exr, self).__init__()
        self.resize(600, 300)
        self.setWindowTitle('EXR QT')

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.show()
        self.showEXR()
    #
    def showEXR(self):
        width = 280
        height = 160

        if gammaCorrected == 1:
            imageq = PilImageQt(exrToJpgGamma(exrPath))
        else:
            imageq = PilImageQt(exrToJpg(exrPath))
        qimage = QtGui.QImage(imageq)
        pixmap = QtGui.QPixmap.fromImage(qimage)
        ScaledPixmap = pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)

        label = QtGui.QLabel("bibi", self)
        label.setPixmap(ScaledPixmap)
        self.layout.addWidget(label, 0, 0)
    #
#
def exrToJpg(exrfile):
    file = OpenEXR.InputFile(exrfile)
    pt = Imath.PixelType(Imath.PixelType.FLOAT)
    dw = file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    rgbf = [Image.fromstring("F", size, file.channel(c, pt)) for c in "RGB"]

    extrema = [im.getextrema() for im in rgbf]
    darkest = min([lo for (lo,hi) in extrema])
    lighest = max([hi for (lo,hi) in extrema])
    scale = 255 / (lighest - darkest)
    def normalize_0_255(v):
         return (v * scale) + darkest
    rgb8 = [im.point(normalize_0_255).convert("L") for im in rgbf]
    myjpg = Image.merge("RGB", rgb8)
    return myjpg
#
def exrToJpgGamma(exrfile):
    file = OpenEXR.InputFile(exrfile)
    pt = Imath.PixelType(Imath.PixelType.FLOAT)
    dw = file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    RedStr = file.channel('R', pt)
    GreenStr = file.channel('G', pt)
    BlueStr = file.channel('B', pt)

    Red = array.array('f', RedStr)
    Green = array.array('f', GreenStr)
    Blue = array.array('f', BlueStr)

    def EncodeToSRGB(v):
        if (v <= 0.0031308):
            return (v * 12.92) * 255.0
        else:
            return (1.055*(v**(1.0/2.2))-0.055) * 255.0

    for I in range(len(Red)):
        Red[I] = EncodeToSRGB(Red[I])

    for I in range(len(Green)):
        Green[I] = EncodeToSRGB(Green[I])

    for I in range(len(Blue)):
        Blue[I] = EncodeToSRGB(Blue[I])

    rgbf = [Image.fromstring("F", size, Red.tostring())]
    rgbf.append(Image.fromstring("F", size, Green.tostring()))
    rgbf.append(Image.fromstring("F", size, Blue.tostring()))

    rgb8 = [im.convert("L") for im in rgbf]
    myqimage = Image.merge("RGB", rgb8)
    return myqimage
#
def main():
    app = QtGui.QApplication(sys.argv)
    win = exr()
    sys.exit(app.exec_())
#
if __name__ == '__main__':
    main()
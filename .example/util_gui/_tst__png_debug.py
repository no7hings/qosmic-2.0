# coding:utf-8
from PIL import Image

# f = '/data/e/myworkspace/td/lynxi/script/python/.resources/icons/window/texture.png'
#
# img = Image.open(f)
#
# img = img.convert('RGB')
#
# # 保存为PNG24格式
# img.save('/data/e/myworkspace/td/lynxi/script/python/.resources/icons/window/texture-1.png', format='PNG', optimize=True)

from PySide2 import QtWidgets, QtGui

f = '/data/e/myworkspace/td/lynxi/script/python/.resources/icons/window/texture-1.png'

i = QtGui.QImage(f)

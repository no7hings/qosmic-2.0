# coding:utf-8
from .... import core as _gui_core
# qt
from ....qt.core.wrap import *

from ....qt import core as _qt_core


class QtAccountWidget(QtWidgets.QWidget):
    class Model(object):
        def __init__(self, widget):
            self._wgt = widget

            self._data = _gui_core.DictOpt(
                flag=False,
                icon=_gui_core.DictOpt(
                    rect=QtCore.QRect(),
                    border_color=QtGui.QColor(95, 95, 95),

                    file_flag=False,
                    file=None,

                    image_flag=False,
                    image=None,
                ),
                name=_gui_core.DictOpt(
                    rect=QtCore.QRect(),
                    text=None,
                    text_color=QtGui.QColor(223, 223, 223),
                    text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                    font=_qt_core.QtFont.generate()
                ),
                department=_gui_core.DictOpt(
                    rect=QtCore.QRect(),
                    text=None,
                    text_color=QtGui.QColor(223, 223, 223),
                    text_option=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                    font=_qt_core.QtFont.generate()
                )
            )

        @property
        def data(self):
            return self._data

        def load_entity(self, entity):
            if entity:
                self._data.flag = True
                self._data.name.text = entity.properties.entity_gui_name
                self._data.department.text = entity.department_name

        def set_icon_data(self, data):
            print(data)
            if data:
                # noinspection PyBroadException
                try:
                    image = QtGui.QImage()
                    image.loadFromData(data)
                    if image.isNull() is False:
                        self._data.icon.image_flag = True
                        self._data.icon.image = image
                except Exception:
                    pass

        def update(self):
            x, y, w, h = 1, 1, self._wgt.width()-2, self._wgt.height()-2
            self._wgt.update()

            spc = 2

            # icon
            img_w, img_h = h, h
            self._data.icon.rect.setRect(
                x, y, img_w, img_h
            )

            txt_w, txt_h = w-img_w-spc, h

            # name
            if self._data.name.text:
                name_w = QtGui.QFontMetrics(self._data.name.font).width(self._data.name.text)+8
            else:
                name_w = 0
            self._data.name.rect.setRect(
                x+img_w+spc, y, name_w, txt_h
            )
            if self._data.department.text:
                department_w = QtGui.QFontMetrics(self._data.department.font).width(self._data.department.text)+8
            else:
                department_w = 0

            # department
            self._data.department.rect.setRect(
                x+img_w+spc+name_w, y, department_w, txt_h
            )

        def draw(self, painter):
            painter.save()

            # icon
            if self._data.icon.file_flag:
                pass
            elif self._data.icon.image_flag:
                print('ABC')
                pass
            else:
                _qt_core.QtItemDrawBase._draw_icon_by_text(
                    painter,
                    self._data.icon.rect,
                    self._data.name.text
                )

            # name
            if self._data.name.text:
                _qt_core.QtItemDrawBase._draw_name_text(
                    painter, self._data.name.rect, self._data.name.text,
                    self._data.name.text_color, self._data.name.text_option, self._data.name.font
                )

            # department
            if self._data.department.text:
                _qt_core.QtItemDrawBase._draw_name_text(
                    painter, self._data.department.rect, self._data.department.text,
                    self._data.department.text_color, self._data.department.text_option, self._data.department.font
                )

            painter.restore()

    def __init__(self, *args, **kwargs):
        super(QtAccountWidget, self).__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setFixedHeight(20)

        self._model = self.Model(self)

        self.installEventFilter(self)

    def eventFilter(self, *args):
        widget, event = args
        if widget == self:
            if event.type() == QtCore.QEvent.Resize:
                self._model.update()
        return False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self._model.draw(painter)



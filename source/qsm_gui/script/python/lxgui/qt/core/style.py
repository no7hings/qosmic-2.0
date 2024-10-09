# coding:utf-8
import lxbasic.content as bsc_content
# gui
from ... import core as _gui_core

from .wrap import *


class QtRgba(_gui_core.GuiRgba):
    """
    override tuple to QColor
    """
    pass


class QtRgbaBrush(_gui_core.GuiRgba):
    pass


class QtStyle(object):
    CONTENT = None

    @classmethod
    def _generate_content(cls):
        if cls.CONTENT is not None:
            return cls.CONTENT

        content = bsc_content.Content(
            value='{}/qt-style.yml'.format(_gui_core.GuiBase.DATA_ROOT)
        )
        content.set(
            'option.icon-dir', _gui_core.GuiIconDirectory.get('qt-style')
        )
        for k, v in _gui_core.GuiRgba.__dict__.items():
            if isinstance(v, tuple):
                if len(v) == 4:
                    content.set('option.rgba.{}'.format(k), ', '.join(map(str, v)))
                    setattr(QtRgba, k, QtGui.QColor(*v))
                    setattr(QtRgbaBrush, k, QtGui.QBrush(QtGui.QColor(*v)))
                elif len(v) == 3:
                    content.set('option.rgba.{}'.format(k), ', '.join(map(str, list(v)+[255])))
                    setattr(QtRgba, k, QtGui.QColor(*v))
                    setattr(QtRgbaBrush, k, QtGui.QBrush(QtGui.QColor(*v)))

        content.do_flatten()
        cls.CONTENT = content
        return cls.CONTENT

    @classmethod
    def get(cls, key):
        c = cls._generate_content()
        return c.get(
            'widget.{}'.format(key)
        )


QtStyle._generate_content()

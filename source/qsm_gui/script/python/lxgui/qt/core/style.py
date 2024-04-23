# coding:utf-8
import lxbasic.content as bsc_content
# gui
from ... import core as gui_core


class GuiQtStyle(object):
    CONTENT = None

    @classmethod
    def _generate_content(cls):
        if cls.CONTENT is not None:
            return cls.CONTENT
        cls.CONTENT = bsc_content.Content(
            value='{}/qt-style.yml'.format(gui_core.GuiBase.DATA_ROOT)
        )
        cls.CONTENT.set(
            'option.icon-dir', gui_core.GuiIconDirectory.get('qt-style')
        )
        cls.CONTENT.do_flatten()
        return cls.CONTENT

    @classmethod
    def get(cls, key):
        c = cls._generate_content()
        return c.get(
            'widget.{}'.format(key)
        )

    @classmethod
    def get_border(cls, key):
        c = cls._generate_content()
        return eval(
            c.get(
                'option.border.{}'.format(key)
            )
        )

    @classmethod
    def get_background(cls, key):
        c = cls._generate_content()
        return eval(
            c.get(
                'option.background.{}'.format(key)
            )
        )

    @classmethod
    def get_font(cls, key):
        c = cls._generate_content()
        return eval(
            c.get(
                'option.font.{}'.format(key)
            )
        )
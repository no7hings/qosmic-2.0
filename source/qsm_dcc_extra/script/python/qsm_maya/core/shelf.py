# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxgui.core as gui_core


class ShelfLayout(object):
    CACHE = None

    @classmethod
    def get_main(cls):
        if cls.CACHE is not None:
            return cls.CACHE

        _ = mel.eval('global string $gShelfTopLevel; string $tmp=$gShelfTopLevel;')
        cls.CACHE = _
        return _

    @classmethod
    def get_all_shelves(cls):
        name = cls.get_main()
        if cmds.shelfTabLayout(name, query=1, exists=1):
            return cmds.shelfTabLayout(name, query=1, childArray=1) or []
        return []


class Shelf(object):
    @classmethod
    def is_exists(cls, name):
        return cmds.shelfLayout(name, query=1, exists=1)

    @classmethod
    def delete(cls, name):
        if cmds.shelfLayout(name, query=1, exists=1):
            cmds.deleteUI(name)

    @classmethod
    def create(cls, name, **kwargs):
        options = dict(
            parent=ShelfLayout.get_main(),
            annotation='...',
            backgroundColor=(0.267, 0.267, 0.267),
            horizontal=1
        )
        options.update(**kwargs)
        return cmds.shelfLayout(
            name,
            **options
        )

    @classmethod
    def create_separator(cls, shelf, **kwargs):
        options = dict(
            style='shelf',
            width=12,
            height=35,
            horizontal=0,
        )
        options.update(**kwargs)
        return cmds.separator(
            parent=shelf,
            **options
        )

    @classmethod
    def create_button(cls, shelf, **kwargs):
        options = dict(
            enable=1,
            manage=1,
            font='plainLabelFont',
            commandRepeatable=1,
            style='iconOnly',
            image=gui_core.GuiIcon.get('tool/python_base'),
            annotation='...',
            width=35,
            height=34,
            flat=1,
            command='print "Test"',
            overlayLabelBackColor=(0, 0, 0, 0)
        )
        options.update(
            parent=shelf,
            **kwargs
        )
        return cmds.shelfButton(
            **options
        )

    @classmethod
    def create_button_action(cls, button, name, script):
        cmds.shelfButton(
            button,
            edit=1,
            menuItem=(name, 'python(\"{}\")'.format(script.replace('"', r'\"')))
        )

# coding:utf-8
import six

import types
# qt
from ..core.wrap import *

from .. import core as gui_qt_core


class AsbGuiQtDccMenuSetup(object):
    def __init__(self, *args):
        pass

    @classmethod
    def get_menu(cls, menu_title):
        raise NotImplementedError()

    @classmethod
    def get_fnc(cls, text):
        exec text

    @classmethod
    def add_action_fnc(cls, action_item, action_data):
        name, icon_name, method = action_data
        #
        action_item.setText(name)
        #
        icon = gui_qt_core.GuiQtIcon.generate_by_text(name)
        action_item.setIcon(icon)
        if method is not None:
            if isinstance(method, (types.FunctionType, types.MethodType)):
                action_item.triggered.connect(method)
            elif isinstance(method, six.string_types):
                action_item.triggered.connect(lambda *args, **kwargs: cls.get_fnc(method))

    @classmethod
    def set_menu_setup(cls, menu, menu_raw):
        if menu_raw:
            for i in menu_raw:
                if i:
                    if len(i) > 0:
                        if isinstance(i, tuple):
                            if i:
                                name = i[0]
                                action_item = menu.addAction(name)
                                cls.add_action_fnc(action_item, i)
                        elif isinstance(i, list):
                            sub_name, sub_icon_name, sub_menu_data = i
                            action_item = menu.addAction(sub_name)
                            icon = gui_qt_core.GuiQtIcon.generate_by_text(sub_name)
                            action_item.setIcon(icon)
                            #
                            i_menu = QtWidgets.QMenu()
                            action_item.setMenu(i_menu)
                            for j in sub_menu_data:
                                if j:
                                    if len(j) > 0:
                                        sub_name = j[0]
                                        sub_action_item = i_menu.addAction(sub_name)
                                        cls.add_action_fnc(sub_action_item, j)
                                    else:
                                        pass
                                else:
                                    i_menu.addSeparator()
                    else:
                        pass
                else:
                    menu.addSeparator()

    @classmethod
    def build_menu_by_configure(cls, configure):
        menu_raw = []
        #
        name = configure.get('option.name')
        keys = configure.get('option.tool')
        for i_key in keys:
            if isinstance(i_key, six.string_types):
                if i_key.startswith('separator'):
                    menu_raw.append(())
                else:
                    i_type = configure.get('tools.{}.type'.format(i_key))
                    i_name = configure.get('tools.{}.name'.format(i_key))
                    i_icon = configure.get('tools.{}.icon'.format(i_key))
                    i_command = configure.get('tools.{}.command'.format(i_key))
                    if i_type == 'item':
                        menu_raw.append(
                            (i_name, i_icon, i_command)
                        )
                    elif i_type == 'group':
                        i_menu_raw = []
                        i_sub_raw = [i_name, i_icon, i_menu_raw]
                        i_keys = configure.get('tools.{}.items'.format(i_key))
                        for j_key in i_keys:
                            if j_key.startswith('separator'):
                                i_menu_raw.append(())
                            else:
                                j_type = configure.get('tools.{}.type'.format(j_key))
                                j_name = configure.get('tools.{}.name'.format(j_key))
                                j_icon = configure.get('tools.{}.icon'.format(j_key))
                                j_command = configure.get('tools.{}.command'.format(j_key))
                                if j_type == 'item':
                                    i_menu_raw.append(
                                        (j_name, j_icon, j_command)
                                    )
                        #
                        menu_raw.append(i_sub_raw)
            else:
                pass
        #
        menu = cls.get_menu(name)
        if menu is not None:
            menu.clear()
            cls.set_menu_setup(menu, menu_raw)

    @classmethod
    def build_menu_by_content(cls, menu, menu_content):
        if menu is not None:
            menu.clear()

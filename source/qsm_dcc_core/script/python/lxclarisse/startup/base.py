# coding:utf-8
import lxcontent.core as ctt_core
# clarisse
from ..core.wrap import *


class MenuBuild(object):
    def __init__(self):
        pass

    @classmethod
    def _get_menu_bar_(cls):
        return ix.application.get_main_menu()

    @classmethod
    def _add_menu_(cls, path):
        path += '>'
        menu_bar = cls._get_menu_bar_()
        item = menu_bar.get_item(path)
        if item:
            return item
        return menu_bar.add_command(path)

    @classmethod
    def _add_separator_(cls, path):
        name = path.split('>')[-1]
        path = '>'.join(path.split('>')[:-1])+'>{{{}}}'.format(name)
        menu_bar = cls._get_menu_bar_()
        item = menu_bar.get_item(path)
        if item:
            return item
        return cls._get_menu_bar_().add_command(path)

    @classmethod
    def _add_action_(cls, path, command):
        menu_bar = cls._get_menu_bar_()
        item = menu_bar.get_item(path)
        if item:
            return item
        return cls._get_menu_bar_().add_command_as_script(
            ix.application.get_default_scripting_engine_class_name(), path, command, '', ''
        )

    @classmethod
    def _create_by_yaml_(cls, file_path):
        import lxgui.core as gui_core

        c = ctt_core.Content(
            value=file_path
        )

        menu_bar = cls._get_menu_bar_()

        for i_k in c.get_all_leaf_keys():
            if i_k.endswith('type'):
                i_type = c.get(i_k)
                i_args = i_k.split('.')[:-1]
                i_path = '>'.join(i_args)
                #
                i_key = '.'.join(i_args)
                if i_type == 'menu':
                    i_item = cls._add_menu_(i_path)
                    menu_bar.remove_all_commands(i_item.get_path())
                    i_icon_name = c.get('{}.icon_name'.format(i_key))
                    if i_icon_name:
                        i_item.set_icon(
                            gui_core.GuiIcon.get(i_icon_name)
                        )
                elif i_type == 'separator':
                    i_item = cls._add_separator_(i_path)
                elif i_type == 'action':
                    i_command = c.get('{}.command'.format(i_key))
                    i_item = cls._add_action_(i_path, i_command)
                    i_icon_name = c.get('{}.icon_name'.format(i_key))
                    if i_icon_name:
                        i_item.set_icon(
                            gui_core.GuiIcon.get(i_icon_name)
                        )

                print 'add {}: "{}"'.format(i_type, '.'.join(i_args))

    def execute(self):
        pass
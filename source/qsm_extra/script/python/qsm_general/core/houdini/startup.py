# coding:utf-8
from __future__ import print_function

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

from . import menu as _menu


class HoudiniStartupCreate(object):

    def generate_fnc(self, menu_content):
        menu_dict = {}
        for k, v in menu_content.get('build.options').items():
            i_path = k
            i_path_opt = bsc_core.BscNodePathOpt(i_path)
            i_parent_path = i_path_opt.get_parent_path()
            i_type = v['type']
            i_name = v.get('name') or k
            i_name_chs = v.get('name_chs')
            if i_type == 'menu':
                if i_parent_path is None:
                    i_menu = self._menu_bar.create_menu(i_name)
                    i_menu.name = i_name
                    menu_dict[i_path] = i_menu
                else:
                    i_parent_menu = menu_dict.get(i_parent_path)
                    if i_parent_menu is None:
                        raise RuntimeError()
                    i_menu = i_parent_menu.create_menu(i_name)
                    i_menu.name = i_name
                    menu_dict[i_path] = i_menu
            elif i_type == 'separator':
                i_parent_menu = menu_dict.get(i_parent_path)
                if i_parent_menu is None:
                    raise RuntimeError()
                i_parent_menu.add_separator()
            elif i_type == 'action':
                i_parent_menu = menu_dict.get(i_parent_path)
                if i_parent_menu is None:
                    raise RuntimeError()
                
                i_action = i_parent_menu.add_action(i_name)
                i_script = v['script']
                i_action.name = i_name
                i_action.python_command = i_script

    def __init__(self, file_path):
        self._file_path = file_path

    def create_main_menu_xml(self):
        self._menu_bar = _menu.HouMenuXmlForMenuBar()

        content = bsc_resource.RscExtendConfigure.get_as_content('houdini/menus/main')

        self.generate_fnc(content)
        # create_menu_fnc_(content, 0)
        #
        xml_file_path = '{}/MainMenuCommon.xml'.format(self._file_path)
        self.write_file(xml_file_path, self._menu_bar.__str__())
        return xml_file_path

    @classmethod
    def write_file(cls, file_path, raw):
        with open(file_path, 'w') as f:
            f.write(raw)

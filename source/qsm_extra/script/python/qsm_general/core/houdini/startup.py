# coding:utf-8
from __future__ import print_function

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

from . import menu as _menu


class HoudiniStartupCreate(object):

    def generate_fnc(self, menu_content):
        menu_dict = {}
        for k, v in menu_content['build'].items():
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
            #     i_menu = self._menu_bar.create_menu(menu_name)
            #     menu_dict[k] = i_menu
            # elif i_type == 'separator':
            #     menu.add_separator()

    def __init__(self, file_path):
        self._file_path = file_path

    def create_main_menu_xml(self):
        def create_menu_fnc_(tool_config_, seq):
            _m = self._menu_bar.create_menu('tool_menu_{}'.format(seq))
            _m.name = tool_config_.get('menu.name')
            _tools = tool_config_.get('menu.tools')
            for _i_key in _tools:
                if _i_key == 'separator':
                    _m.add_separator()
                else:
                    _i_name = tool_config_.get('tool.{}.name'.format(_i_key))
                    _i_children = tool_config_.get('tool.{}.items'.format(_i_key))
                    if _i_children:
                        _i_menu = _m.create_menu(_i_key)
                        _i_menu.name = _i_name
                        for _j_key in _i_children:
                            if _j_key == 'separator':
                                _i_menu.add_separator()
                            else:
                                _j_name = tool_config_.get('tool.{}.name'.format(_j_key))
                                _j_command = tool_config_.get('tool.{}.command'.format(_j_key))
                                #
                                _j_action = _i_menu.add_action(_j_key)
                                _j_action.name = _j_name
                                _j_action.python_command = _j_command
                    else:
                        _i_command = tool_config_.get('tool.{}.command'.format(_i_key))
                        #
                        _i_action = _m.add_action(_i_key)
                        _i_action.name = _i_name
                        _i_action.python_command = _i_command

        self._menu_bar = _menu.HouMenuXmlForMenuBar()

        content = bsc_resource.RscExtendConfigure.get_as_content('houdini/menu/main')

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

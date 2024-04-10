# coding:utf-8
import lxresource as bsc_resource

from .. import abstracts as bsc_dcc_abstracts

from . import houdini_menu as bsc_dcc_core_houdini_menu


class HoudiniSetupCreator(object):
    def __init__(self, file_path):
        self._file_path = file_path

    def create_main_menu_xml(self):
        def create_menu_fnc_(tool_config_, seq):
            _menu = self._menu_bar.create_menu('tool_menu_{}'.format(seq))
            _menu.name = tool_config_.get('menu.name')
            _tools = tool_config_.get('menu.tools')
            for _i_key in _tools:
                if _i_key == 'separator':
                    _menu.set_separator_add()
                else:
                    _i_name = tool_config_.get('tool.{}.name'.format(_i_key))
                    _i_children = tool_config_.get('tool.{}.items'.format(_i_key))
                    if _i_children:
                        _i_menu = _menu.create_menu(_i_key)
                        _i_menu.name = _i_name
                        for _j_key in _i_children:
                            if _j_key == 'separator':
                                _i_menu.set_separator_add()
                            else:
                                _j_name = tool_config_.get('tool.{}.name'.format(_j_key))
                                _j_command = tool_config_.get('tool.{}.command'.format(_j_key))
                                #
                                _j_action = _i_menu.set_action_add(_j_key)
                                _j_action.name = _j_name
                                _j_action.python_command = _j_command
                    else:
                        _i_command = tool_config_.get('tool.{}.command'.format(_i_key))
                        #
                        _i_action = _menu.set_action_add(_i_key)
                        _i_action.name = _i_name
                        _i_action.python_command = _i_command

        self._menu_bar = bsc_dcc_core_houdini_menu.HouMenuXmlForMenuBar()

        configure = bsc_resource.RscExtendConfigure.get_as_content('houdini/menu')
        create_menu_fnc_(configure, 0)

        main_menu_xml_file = '{}/MainMenuCommon.xml'.format(self._file_path)
        self.write_file(main_menu_xml_file, self._menu_bar.__str__())
        return main_menu_xml_file

    @classmethod
    def write_file(cls, file_path, raw):
        with open(file_path, 'w') as f:
            f.write(raw)


class OcioSetup(bsc_dcc_abstracts.AbsDccSetup):
    def __init__(self, root):
        super(OcioSetup, self).__init__(root)

    def set_run(self):
        self.set_environ_fnc(
            'OCIO', '{}/config.ocio'.format(self._root)
        )
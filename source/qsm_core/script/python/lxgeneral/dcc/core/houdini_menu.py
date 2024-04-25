# coding:utf-8
import os


class _HouMenuXmlBase(object):
    XML_HEAD = 'subMenu'
    INDENT_COUNT = 4

    def __init__(self):
        self._indent = 0

    def get_head(self):
        return self.XML_HEAD

    def get_indent_count(self):
        return self._indent

    def set_indent_count(self, count):
        self._indent = count

    def get_xml_attributes(self):
        raise NotImplementedError()

    def get_xml_elements(self):
        raise NotImplementedError()

    def get_xml(self):
        lis = [
            (self.get_indent_count(), '<{}'.format(self.get_head()), '')
        ]
        ports = self.get_xml_attributes()
        elements = self.get_xml_elements()
        if ports:
            for i in ports:
                k, v = i
                lis.append(
                    (0, ' {}="{}"'.format(k, v), '')
                )
            if elements:
                lis.append(
                    (0, '>', os.linesep)
                )
        if elements:
            for i in elements:
                if isinstance(i, _HouMenuXmlBase):
                    lis.extend(i.get_xml())
                else:
                    k, v = i
                    lis.append(
                        (self.get_indent_count()+1, '<{}>{}</{}>'.format(k, v, k), os.linesep)
                    )
            lis.append(
                (self.get_indent_count(), '</{}>'.format(self.get_head()), os.linesep)
            )
        else:
            lis.append(
                (0, ' />'.format(self.get_head()), os.linesep)
            )
        return lis


class HouMenuXmlForAction(_HouMenuXmlBase):
    XML_HEAD = 'scriptItem', 'separatorItem'

    def __init__(self, key=None):
        super(HouMenuXmlForAction, self).__init__()
        self._key = key
        self._name = None
        self._is_separator = False
        self._python_command = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, text):
        self._name = text

    @property
    def python_command(self):
        return self._python_command

    @python_command.setter
    def python_command(self, text):
        self._python_command = text

    def get_head(self):
        if self._is_separator is True:
            return self.XML_HEAD[1]
        return self.XML_HEAD[0]

    def set_is_separator(self, boolean):
        self._is_separator = boolean

    def get_is_separator(self):
        return self._is_separator

    def get_xml_attributes(self):
        if self.get_is_separator() is True:
            return []
        return [
            ('id', self._key)
        ]

    def get_xml_elements(self):
        if self.get_is_separator() is True:
            return []
        lis = [
            ('label', self.name)
        ]
        if self.python_command is not None:
            lis.append(
                ('scriptCode', '<![CDATA[{}]]>'.format(self._python_command))
            )
        return lis


class HouMenuXmlForMenu(_HouMenuXmlBase):
    ACTION_CLS = HouMenuXmlForAction
    XML_HEAD = 'subMenu'

    def __init__(self, key, sub=False):
        super(HouMenuXmlForMenu, self).__init__()
        self._key = key
        self._name = None
        self._sub = sub
        self._children = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, text):
        self._name = text

    def set_action_add(self, key):
        action = self.ACTION_CLS(key)
        self._children.append(action)
        return action

    def create_menu(self, key):
        menu = self.__class__(key, True)
        self._children.append(menu)
        return menu

    def get_actions(self):
        return self._children

    def set_separator_add(self):
        action = self.ACTION_CLS()
        action.set_is_separator(True)
        self._children.append(action)
        return action

    def get_xml_attributes(self):
        return [
            ('id', self._key)
        ]

    def get_xml_elements(self):
        if self._sub is True:
            lis = [
                ('label', self.name)
            ]
        else:
            lis = [
                ('label', self.name),
                ('insertBefore', 'help_menu')
            ]
        for i in self.get_actions():
            i.set_indent_count(self.get_indent_count()+1)
            lis.append(i)
        return lis


class HouMenuXmlForMenuBar(_HouMenuXmlBase):
    MENU_CLS = HouMenuXmlForMenu
    XML_HEAD = 'menuBar'

    def __init__(self):
        super(HouMenuXmlForMenuBar, self).__init__()
        self._menus = []

    @property
    def menus(self):
        return self._menus

    def create_menu(self, name):
        menu = self.MENU_CLS(name)
        self._menus.append(menu)
        return menu

    def get_menus(self):
        return self._menus

    def get_xml_attributes(self):
        return []

    def get_xml_elements(self):
        lis = []
        return lis

    def set_convert_to_xml(self):
        lis = [
            (0, '<?xml version="1.0" encoding="UTF-8"?>', os.linesep),
            (0, '<mainMenu>', os.linesep),
            (1, '<menuBar>', os.linesep)
        ]
        for i in self.get_menus():
            i.set_indent_count(2)
            lis.extend(i.get_xml())
        lis.extend(
            [
                (1, '</menuBar>', os.linesep),
                (0, '</mainMenu>', '')
            ]
        )
        return ''.join(['{}{}{}'.format(c*' '*self.INDENT_COUNT, i, l) for c, i, l in lis])

    def __str__(self):
        return self.set_convert_to_xml()

# coding:utf-8
import lxresource as bsc_resource

import lxuniverse.abstracts as unr_abstracts

from .. import abstracts as bsc_dcc_abstracts


class Node(
    bsc_dcc_abstracts.AbsDccBaseDef,
    unr_abstracts.AbsObjDagExtraDef,
    unr_abstracts.AbsGuiExtraDef
):
    PATHSEP = '/'

    # noinspection PyMissingConstructor
    def __init__(self, path, **kwargs):
        self._init_obj_dag_extra_def_(path)
        if self.path.startswith(self.PATHSEP):
            self._name = self.path.split(self.PATHSEP)[-1]
        else:
            self._name = self.path

        if 'icon_name' in kwargs:
            self._icon_file_path = bsc_resource.RscExtendIcon.get(kwargs.get('icon_name'))
        else:
            self._icon_file_path = bsc_resource.RscExtendIcon.get('obj/object')

        if 'type_name' in kwargs:
            self._type_name = kwargs.get('type_name')
        else:
            self._type_name = 'null'

        self._init_gui_extra_def_()

    def get_type_name(self):
        return self._type_name

    @property
    def type(self):
        return self._type_name

    @property
    def icon(self):
        return self._icon_file_path

    def create_dag_fnc(self, path):
        _ = self.__class__(path)
        _._icon_file_path = bsc_resource.RscExtendIcon.get('obj/group')
        return _

    def _get_child_paths_(self, path):
        pass

    def _get_child_(self, path):
        pass


class Component(
    bsc_dcc_abstracts.AbsGuiExtraDef
):
    PATHSEP = '.'
    TYPE_DICT = {
        'f': 'face',
        'e': 'edge',
        'vtx': 'vertex'
    }

    def __init__(self, path):
        self._path = path
        self._name = self._path.split('.')[-1]
        keyword = self.name.split('[')[0]
        self._type = self.TYPE_DICT.get(keyword)

    def get_type(self):
        return self._type

    type = property(get_type)

    def get_name(self):
        return self._name

    name = property(get_name)

    def get_path(self):
        return self._path

    path = property(get_path)

    def get_icon(self):
        return bsc_resource.RscExtendIcon.get('obj/{}'.format(self.type))

    icon = property(get_icon)

    def __str__(self):
        return '{}(type="{}", path="{}")'.format(
            self.__class__.__name__,
            self.type,
            self.path
        )

    def __repr__(self):
        return self.__str__()

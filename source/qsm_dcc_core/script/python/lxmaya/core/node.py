# coding:utf-8
import six

import fnmatch

import math

import lxbasic.core as bsc_core
# maya
from .wrap import *

from . import configure as mya_cor_configure

from . import base as mya_cor_base

from . import node_api as mya_cor_node_api


class CmdXgenSplineGuideOpt(object):
    def __init__(self, path):
        # todo, use cmd
        self._om2_obj_fnc = mya_cor_node_api.Om2Base._get_om2_dag_node_fnc_(path)
        self._obj_path = self._om2_obj_fnc.fullPathName()

    @property
    def path(self):
        return self._obj_path

    def get_control_points(self):
        lis = []
        # xgmGuideGeom [-guide STRING] [-numVertices] [-basePoint | -controlPoints] [-lockBasePt BOOL] [-guideNormal] [-uvLocation] [-isCached]
        _ = cmds.xgmGuideGeom(guide=self._obj_path, controlPoints=1)
        for seq, i in enumerate(_):
            if not seq%3:
                lis.append(tuple([_[seq+j] for j in range(3)]))
        return lis

    def get_vertex_points(self):
        lis = []
        _ = cmds.xgmGuideGeom(guide=self._obj_path, numVertices=True) or []
        if _:
            c = _[0]
            for i in range(int(c)):
                lis.append(cmds.getAttr('xgGuide1Shape.vtx[{}]'.format(i))[0])
        return lis

    def _test_(self):
        cmd = 'curve -d '
        cmd += '1'
        _ = cmds.xgmGuideGeom(guide=self._obj_path, numVertices=True) or []
        if _:
            c = _[0]
            for i in range(int(c)):
                cmd += ' -p '
                cmd += ' '.join([str(i) for i in cmds.getAttr('xgGuide1Shape.vtx[{}]'.format(i))[0]])
        print cmd


class CmdAtrQueryOpt(object):
    PORT_PATHSEP = mya_cor_base.MyaUtil.PORT_PATHSEP

    def __init__(self, atr_path):
        self._atr_path = atr_path
        _ = atr_path.split(self.PORT_PATHSEP)
        self._obj_path, self._port_path = _[0], self._get_port_path_(self.PORT_PATHSEP.join(_[1:]))

    @classmethod
    def _get_port_path_(cls, port_path):
        _ = port_path.split('.')[-1]
        if _.endswith(']'):
            return _.split('[')[0]
        return _

    #
    @property
    def atr_path(self):
        return self._atr_path

    @property
    def obj_path(self):
        return self._obj_path

    @property
    def port_path(self):
        return self._port_path

    def get_type(self):
        return cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            attributeType=1
        )

    type = property(get_type)

    #
    def get_is_exists(self):
        return cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            exists=1
        )

    def get_parent_path(self):
        _ = cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            listParent=1
        )
        if _ is not None:
            return _[0]

    def get_channel_names(self, alpha=True):
        _ = cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            numberOfChildren=1
        )
        if _ is not None:
            names = cmds.attributeQuery(
                self.port_path,
                node=self.obj_path,
                listChildren=1
            ) or []
            if alpha is True:
                if self.port_path == 'outColor':
                    alpha_port_path = 'outAlpha'
                else:
                    alpha_port_path = '{}A'.format(self.port_path)
                if cmds.attributeQuery(
                        alpha_port_path,
                        node=self.obj_path,
                        exists=1
                ) is True:
                    names.append(alpha_port_path)
            return names
        return []

    def get_is_channel(self):
        return cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            listParent=1
        ) is not None

    def get_alpha_channel_name(self):
        if self.port_path == 'outColor':
            alpha_port_path = 'outAlpha'
        else:
            alpha_port_path = '{}A'.format(self.port_path)
        if cmds.attributeQuery(
                self._get_port_path_(alpha_port_path),
                node=self.obj_path,
                exists=1
        ) is True:
            return alpha_port_path

    def get_element_indices(self):
        _ = cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            multi=1
        )
        if _ is True:
            return [int(i) for i in cmds.getAttr(self.atr_path, multiIndices=1, silent=1) or []]

    def get_is_enumerate(self):
        return cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            enum=1
        )

    def get_enumerate_strings(self):
        _ = cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            listEnum=1
        )
        if _:
            return _[0].split(':')
        return []

    def get_default(self):
        _ = cmds.attributeQuery(
            self.port_path,
            node=self.obj_path,
            listDefault=1
        )
        if _:
            if self.get_channel_names():
                return tuple(_)
            return _[0]

    def set(self):
        pass


class CmdPortQueryOpt(object):
    PATHSEP = '.'

    def __init__(self, obj_type_name, port_query_path):
        self._obj_type_name = obj_type_name
        self._port_query_path = port_query_path

    def get_obj_type_name(self):
        return self._obj_type_name

    def get_port_query_path(self):
        return self._port_query_path

    def __get_query_key_(self):
        _ = self._port_query_path.split(self.PATHSEP)[-1]
        if _.endswith(u']'):
            return _.split(u'[')[0]
        return _

    def __get_query_kwargs_(self, obj_path, **kwargs):
        if obj_path is not None:
            kwargs['node'] = obj_path
        else:
            kwargs['type'] = self.get_obj_type_name()
        return kwargs

    def get_type_name(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, attributeType=True)
        )

    def get_has_channels(self, obj_path=None):
        return (cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listChildren=True)
        ) or []) != []

    def get_channel_names(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listChildren=True)
        ) or []

    def get_child_names(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listChildren=True)
        ) or []

    def get_parent_name(self, obj_path=None):
        _ = cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listParent=True)
        )
        if _:
            return _[0]

    def get_has_parent(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listParent=True)
        ) is not None

    def get_is_array(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, multi=True)
        ) or False

    def get_is_writable(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, writable=True)
        ) or False

    def get_is_readable(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, readable=True)
        ) or False

    def get_is_message(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, readable=True)
        ) or False

    def get_is_enumerate(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, enum=True)
        ) or False

    #
    def get_enumerate_strings(self, obj_path=None):
        _ = cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listEnum=True)
        )
        if _:
            return _[0].split(':')
        return []

    def get_short_name(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, shortName=True)
        )

    def get_ui_name(self, obj_path=None):
        return cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, niceName=True)
        )

    def get_default(self, obj_path=None):
        _ = cmds.attributeQuery(
            self.__get_query_key_(),
            **self.__get_query_kwargs_(obj_path, listDefault=True)
        )
        if _:
            if self.get_has_channels() is True:
                return tuple(_)
            return _[0]

    def __str__(self):
        return '{}(path="{}.{}")'.format(
            self.get_type_name(), self.get_obj_type_name(), self.get_port_query_path()
        )


class CmdCustomizePortQueryOpt(object):
    pass


class CmdObjQueryOpt(object):
    def __init__(self, obj_type_name):
        self._obj_type_name = obj_type_name

    #
    def get_type_name(self):
        return self._obj_type_name

    @classmethod
    def _set_cleanup_to_(cls, lis):
        lis_ = list(filter(None, set(lis)))
        lis_.sort(key=lis.index)
        return lis_

    def get_port_query_is_exists(self, port_query_path):
        return cmds.attributeQuery(
            port_query_path,
            type=self.get_type_name(),
            exists=1
        )

    def get_port_query(self, port_query_path):
        return CmdPortQueryOpt(
            self.get_type_name(),
            port_query_path
        )

    def get_port_query_paths(self):
        def rcs_fnc_(port_query_path_):
            _child_names = self.get_port_query(
                port_query_path_
            ).get_channel_names()
            if _child_names:
                for _i in _child_names:
                    _i_port_query_path = u'{}.{}'.format(port_query_path_, _i)
                    lis.append(_i_port_query_path)
                    rcs_fnc_(_i_port_query_path)

        #
        lis = []
        #
        _ = self._set_cleanup_to_(
            cmds.attributeInfo(
                allAttributes=True,
                type=self.get_type_name()
            ) or []
        )
        if _:
            for port_query_path in _:
                if self.get_port_query(port_query_path).get_has_parent() is False:
                    lis.append(port_query_path)
                    rcs_fnc_(port_query_path)
        return lis

    def get_port_queries(self):
        return [
            self.get_port_query(i) for i in self.get_port_query_paths()
        ]


class CmdPortOpt(object):
    PATHSEP = '.'

    def __init__(self, obj_path, port_path):
        self._obj_path = obj_path
        self._port_path = port_path
        _ = '.'.join(
            [self._obj_path, port_path]
        )
        self._atr_path = self._to_atr_path_(
            self._obj_path, self._port_path
        )
        if cmds.objExists(self._atr_path) is True:
            self._port_type = cmds.getAttr(self._atr_path, type=1)
            self._port_query = CmdPortQueryOpt(
                CmdObjOpt(obj_path).get_type_name(),
                self._port_path
            )
            self._atr_query = CmdAtrQueryOpt(self._atr_path)
        else:
            raise RuntimeError()

    @classmethod
    def _set_create_(cls, obj_path, port_path, type_name, enumerate_strings=None):
        if cls._get_is_exists_(obj_path, port_path) is False:
            if type_name == 'string':
                cmds.addAttr(
                    obj_path,
                    longName=port_path,
                    dataType=type_name
                )
            elif type_name == 'enum':
                if isinstance(enumerate_strings, (tuple, list)):
                    cmds.addAttr(
                        obj_path,
                        longName=port_path,
                        attributeType=type_name,
                        enumName=':'.join(enumerate_strings)
                    )
                else:
                    cmds.addAttr(
                        obj_path,
                        longName=port_path,
                        attributeType=type_name
                    )
            else:
                cmds.addAttr(
                    obj_path,
                    longName=port_path,
                    attributeType=type_name
                )

    @classmethod
    def _get_is_exists_(cls, obj_path, port_path):
        atr_path = cls._to_atr_path_(obj_path, port_path)
        return cmds.objExists(atr_path)

    @classmethod
    def _to_atr_path_(cls, obj_path, port_path):
        return cls.PATHSEP.join(
            [obj_path, port_path]
        )

    @classmethod
    def _set_connection_create_(cls, atr_path_src, atr_path_tgt):
        if cmds.isConnected(atr_path_src, atr_path_tgt) is False:
            if cmds.getAttr(atr_path_tgt, lock=1) is False:
                cmds.connectAttr(atr_path_src, atr_path_tgt, force=1)

    def get_port_query(self):
        return self._port_query

    def get_obj_path(self):
        return self._obj_path

    obj_path = property(get_obj_path)

    def get_type_name(self):
        return self._port_type

    type_name = property(get_type_name)

    def get_path(self):
        return self._atr_path

    path = property(get_path)

    def join_by(self):
        return self._atr_path

    atr_path = property(join_by)

    def get_port_path(self):
        return self._port_path

    port_path = property(get_port_path)

    def get_array_indices(self):
        if self.get_port_query().get_is_array(self.get_obj_path()) is True:
            return cmds.getAttr(
                '.'.join([self.get_obj_path(), self.get_port_path()]),
                multiIndices=1,
                silent=1
            ) or []
        return []

    def get(self, as_string=False):
        if self.get_type_name() in {'message', 'TdataCompound'}:
            return None

        if as_string is True:
            return cmds.getAttr(self.path, asString=True) or ''
        #
        _ = cmds.getAttr(self.get_path())
        if self.get_port_query().get_has_channels(self.get_obj_path()):
            return _[0]
        return _

    def set(self, value, enumerate_strings=None):
        if self.has_source() is False:
            # unlock first
            is_lock = cmds.getAttr(self.get_path(), lock=1)
            if is_lock:
                cmds.setAttr(self.get_path(), lock=0)
            #
            if self.get_port_query().get_is_writable(self.get_obj_path()) is True:
                if self.get_type_name() == 'string':
                    cmds.setAttr(self.get_path(), value, type=self.get_type_name())
                elif self.get_type_name() == 'enum':
                    if enumerate_strings is not None:
                        cmds.addAttr(
                            self.get_path(),
                            enumName=':'.join(enumerate_strings),
                            edit=1
                        )
                    #
                    if isinstance(value, six.string_types):
                        enumerate_strings = self.get_port_query().get_enumerate_strings(self.get_obj_path())
                        index = enumerate_strings.index(value)
                        cmds.setAttr(self.get_path(), index)
                    else:
                        cmds.setAttr(self.get_path(), value)
                else:
                    if isinstance(value, (tuple, list)):
                        cmds.setAttr(self.get_path(), *value, clamp=1)
                    else:
                        # Debug ( Clamp Maximum or Minimum Value )
                        cmds.setAttr(self.get_path(), value, clamp=1)

    def get_default(self):
        if self.get_type_name() == 'message':
            return None
        elif self.get_type_name() == 'TdataCompound':
            return None
        #
        _ = self.get_port_query().get_default()
        if self.get_type_name() == 'bool':
            return bool(int(_))
        elif self.get_type_name() == 'matrix':
            return [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        return _

    def get_is_changed(self):
        return self.get() != self.get_default()

    def get_is_enumerate(self):
        return self.get_port_query().get_is_enumerate(self.get_obj_path())

    def get_enumerate_strings(self):
        return self.get_port_query().get_enumerate_strings(
            self.get_obj_path()
        )

    def set_enumerate_strings(self, strings):
        cmds.addAttr(
            self._atr_path,
            edit=1, enumName=':'.join(strings)
        )

    def has_source(self):
        _ = cmds.connectionInfo(
            self.get_path(), isExactDestination=True
        )
        if self.get_port_query().get_has_channels(self.get_obj_path()) is True:
            return cmds.connectionInfo(
                self.get_path(), isDestination=True
            )
        elif self.get_port_query().get_has_parent(self.get_obj_path()) is True:
            return cmds.connectionInfo(
                self.get_path(), isDestination=True
            )
        return _

    def get_has_source_(self, exact=False):
        if exact is True:
            return cmds.connectionInfo(
                self.get_path(), isExactDestination=True
            )
        return cmds.connectionInfo(
            self.get_path(), isDestination=True
        )

    def get_source(self):
        _ = cmds.connectionInfo(
            self.get_path(),
            sourceFromDestination=1
        )
        if _:
            a = bsc_core.PthAttributeOpt(_)
            obj_path = a.obj_path
            if CmdObjOpt._get_is_exists_(obj_path) is True:
                port_path = a.port_path
                return self.PATHSEP.join(
                    [CmdObjOpt(obj_path).get_path(), port_path]
                )

    def set_disconnect(self):
        source = self.get_source()
        if source:
            cmds.disconnectAttr(source, self.get_path())

    def set_default(self):
        default_value = self.get_default()
        if default_value is not None:
            self.set(default_value)

    def get_is_naming_match(self, pattern):
        return fnmatch.filter(
            [self.get_port_path()], pattern
        ) != []

    def get_is_naming_matches(self, patterns):
        for i in patterns:
            if self.get_is_naming_match(i) is True:
                return True
        return False

    def __str__(self):
        return '{}(path="{}")'.format(
            self.get_type_name(), self.get_path()
        )

    def __repr__(self):
        return self.__str__()


class CmdAtrOpt(object):
    PATHSEP = '.'

    # noinspection PyUnusedLocal
    def __init__(self, atr_path):
        pass


class ShaderCategory(object):
    CACHE = {}

    @classmethod
    def create_cache(cls):
        if not cls.CACHE:
            # custom
            for i_category in ['shader', 'texture', 'light', 'utility']:
                for j_type in cmds.listNodeTypes(i_category) or []:
                    cls.CACHE[j_type] = i_category
            # arnold
            for i_category in ['shader', 'texture', 'light', 'utility']:
                for j_type in cmds.listNodeTypes('rendernode/arnold/'+i_category) or []:
                    cls.CACHE[j_type] = i_category

    @classmethod
    def get(cls, type_name, default='unknown'):
        cls.create_cache()
        return cls.CACHE.get(type_name, default)

    @classmethod
    def is_shader_type(cls, type_name):
        cls.create_cache()
        return type_name in cls.CACHE

    @classmethod
    def get_(cls, type_name):
        return cmds.getClassification(type_name)[0]


class CmdObjOpt(object):
    PATHSEP = '|'
    PORT_PATHSEP = '.'
    #
    OBJ_NAME_0 = 'renderPartition'
    OBJ_NAME_1 = 'lightLinker1'
    OBJ_NAME_2 = 'defaultLightSet'

    #
    def __init__(self, obj_path):
        _ = cmds.ls(obj_path, long=1)
        if _:
            self._obj_path = _[0]
            self._uuid = cmds.ls(self._obj_path, uuid=1)[0]
            self._obj_type = cmds.nodeType(self._obj_path)
            self._obj_query_opt = CmdObjQueryOpt(self._obj_type)
        else:
            raise RuntimeError()

    @classmethod
    def _get_is_exists_(cls, obj_path):
        return cmds.objExists(obj_path)

    @classmethod
    def _set_create_(cls, obj_path, type_name):
        if type_name == mya_cor_configure.MyaNodeTypes.Material:
            cls._create_material_(obj_path, type_name)
        elif type_name in ShaderCategory.is_shader_type(type_name):
            cls._create_shader_(obj_path, type_name)
        else:
            _ = cmds.createNode(
                type_name, name=obj_path, skipSelect=1
            )

    @classmethod
    def _create_shader_(cls, obj_name, type_name):
        if cls._get_is_exists_(obj_name) is False:
            category = ShaderCategory.get(type_name, 'utility')
            kwargs = dict(
                name=obj_name,
                skipSelect=1
            )
            if category == 'shader':
                kwargs['asShader'] = 1
            elif category == 'texture':
                kwargs['asTexture'] = 1
            elif category == 'light':
                kwargs['asLight'] = 1
            elif category == 'utility':
                kwargs['asUtility'] = 1
            #
            _ = cmds.shadingNode(type_name, **kwargs)

    @classmethod
    def _create_material_(cls, obj_name, type_name):
        if cls._get_is_exists_(obj_name) is False:
            result = cmds.shadingNode(
                type_name,
                name=obj_name,
                asUtility=1,
                skipSelect=1
            )
            cls._create_material_light_link_(result)

    @classmethod
    def _create_material_light_link_(cls, shading_engine):
        def get_connection_index_():
            for i in range(5000):
                if get_is_partition_connected_at_(i) \
                        and get_is_obj_link_connected_at_(i) \
                        and get_is_obj_shadow_link_connected_at_(i) \
                        and get_is_light_link_connected_at_(i) \
                        and get_is_light_shadow_link_connected_at_(i):
                    return i

        #
        def get_is_connected_(connection):
            boolean = False
            if cmds.objExists(connection):
                if not cmds.connectionInfo(connection, isDestination=1):
                    boolean = True
            return boolean

        #
        def get_is_partition_connected_at_(index):
            connection = cls.OBJ_NAME_0+'.sets[%s]'%index
            return get_is_connected_(connection)

        #
        def get_is_obj_link_connected_at_(index):
            connection = cls.OBJ_NAME_1+'.link[%s].object'%index
            return get_is_connected_(connection)

        #
        def get_is_obj_shadow_link_connected_at_(index):
            connection = cls.OBJ_NAME_1+'.shadowLink[%s].shadowObject'%index
            return get_is_connected_(connection)

        #
        def get_is_light_link_connected_at_(index):
            connection = cls.OBJ_NAME_1+'.link[%s].light'%index
            return get_is_connected_(connection)

        #
        def get_is_light_shadow_link_connected_at_(index):
            connection = cls.OBJ_NAME_1+'.shadowLink[%s].shadowLight'%index
            return get_is_connected_(connection)

        #
        def main_fnc_():
            index = get_connection_index_()
            if index:
                # Debug ( Repeat )
                if not cmds.connectionInfo(shading_engine+'.partition', isSource=1):
                    cmds.connectAttr(shading_engine+'.partition', cls.OBJ_NAME_0+'.sets[%s]'%index)
                    cmds.connectAttr(
                        shading_engine+'.message',
                        cls.OBJ_NAME_1+'.link[%s].object'%index
                    )
                    cmds.connectAttr(
                        shading_engine+'.message',
                        cls.OBJ_NAME_1+'.shadowLink[%s].shadowObject'%index
                    )
                    cmds.connectAttr(
                        cls.OBJ_NAME_2+'.message',
                        cls.OBJ_NAME_1+'.link[%s].light'%index
                    )
                    cmds.connectAttr(
                        cls.OBJ_NAME_2+'.message',
                        cls.OBJ_NAME_1+'.shadowLink[%s].shadowLight'%index
                    )

        #
        main_fnc_()

    def clear_array_ports(self):
        ports = self.get_ports()
        for port in ports:
            if port.get_port_query().get_is_array(self.get_path()) is True:
                array_indices = port.get_array_indices()
                for array_index in array_indices:
                    cmds.removeMultiInstance('{}[{}]'.format(port.get_path(), array_index), b=True)

    def get_obj_query(self):
        return self._obj_query_opt

    def get_type_name(self):
        return self._obj_type

    type_name = property(get_type_name)

    def get_path(self):
        return self._obj_path

    path = property(get_path)

    def update_path(self):
        _ = cmds.ls(self._uuid, long=1)
        if _:
            self._obj_path = _[0]

    def get_parent_path(self):
        _ = cmds.listRelatives(self.get_path(), parent=1, fullPath=1)
        if _:
            return _[0]

    def parent_to_path(self, path):
        if path == self.PATHSEP:
            if cmds.listRelatives(self.get_path(), parent=1):
                cmds.parent(self.get_path(), world=1)
        else:
            if cmds.objExists(path) is True:
                if self.get_parent_path() != path:
                    cmds.parent(self.get_path(), path)

    def __get_port_paths_(self, port_paths):
        def rcs_fnc_(port_path_):
            _port_query = self.get_obj_query().get_port_query(
                port_path_
            )
            _condition = _port_query.get_is_array(obj_path), _port_query.get_has_channels(obj_path)
            if _condition == (True, True):
                _array_indices = CmdPortOpt(self.get_path(), port_path_).get_array_indices()
                _child_port_names = _port_query.get_channel_names()
                for _i_array_index in _array_indices:
                    for _i_child_port_name in _child_port_names:
                        _i_port_path = '{}[{}].{}'.format(port_path_, _i_array_index, _i_child_port_name)
                        lis.append(_i_port_path)
                        rcs_fnc_(_i_port_path)
            elif _condition == (True, False):
                _array_indices = CmdPortOpt(self.get_path(), port_path_).get_array_indices()
                for _i_array_index in _array_indices:
                    _i_port_path = '{}[{}]'.format(port_path_, _i_array_index)
                    lis.append(_i_port_path)
                    rcs_fnc_(_i_port_path)
            elif _condition == (False, True):
                _child_port_names = _port_query.get_channel_names()
                for _i_child_port_name in _child_port_names:
                    _i_port_path = '{}.{}'.format(port_path_, _i_child_port_name)
                    lis.append(_i_port_path)
                    rcs_fnc_(_i_port_path)
            elif _condition == (False, False):
                pass

        #
        lis = []
        obj_path = self.get_path()
        for port_path in port_paths:
            port_query = self.get_obj_query().get_port_query(
                port_path
            )
            if CmdPortOpt._get_is_exists_(obj_path, port_path) is True:
                if port_query.get_has_parent(obj_path) is False:
                    lis.append(port_path)
                    rcs_fnc_(port_path)
        return lis

    def get_port_paths(self):
        return self.__get_port_paths_(
            cmds.attributeInfo(
                allAttributes=True,
                type=self.get_type_name()
            ) or []
        )

    def get_ports(self, includes=None):
        _ = self.get_port_paths()
        if isinstance(includes, (tuple, list)):
            _ = includes
        return [
            self.get_port(i) for i in _
        ]

    def get_customize_port_paths(self):
        return self.__get_port_paths_(
            cmds.listAttr(self.get_path(), userDefined=1) or []
        )

    def get_customize_ports(self, includes=None):
        _ = self.get_customize_port_paths()
        if isinstance(includes, (tuple, list)):
            _ = includes
        return [
            self.get_port(i) for i in _ if CmdPortOpt._get_is_exists_(
                self.get_path(), i
            )
        ]

    def create_customize_attributes(self, attributes):
        # 'message',
        # 'bool',
        # 'byte',
        # 'enum',
        # 'typed',
        # 'short',
        # 'float',
        # 'float3',
        # 'compound',
        # 'double',
        # 'time',
        # 'generic',
        # 'doubleLinear',
        # 'doubleAngle',
        # 'matrix',
        # 'long',
        # 'double3',
        # 'lightData',
        # 'addr',
        # 'float2',
        # 'double2',
        # 'double4',
        # 'fltMatrix',
        # 'char',
        # 'floatAngle',
        # 'floatLinear',
        # 'long3',
        # 'short2',
        # 'polyFaces',
        # 'long2'
        obj_path = self.get_path()
        for i_port_path, i_value in attributes.items():
            if isinstance(i_value, six.string_types):
                type_name = 'string'
            elif isinstance(i_value, bool):
                type_name = 'bool'
            elif isinstance(i_value, int):
                type_name = 'long'
            elif isinstance(i_value, float):
                type_name = 'double'
            else:
                raise RuntimeError()
            #
            CmdPortOpt._set_create_(
                obj_path=obj_path,
                port_path=i_port_path,
                type_name=type_name
            )
            #
            port = CmdPortOpt(obj_path, i_port_path)
            if i_value is not None:
                port.set(i_value)

    def create_customize_attribute(self, port_path, value):
        if value is not None:
            obj_path = self.get_path()
            if isinstance(value, six.string_types):
                type_name = 'string'
            elif isinstance(value, bool):
                type_name = 'bool'
            elif isinstance(value, int):
                type_name = 'long'
            elif isinstance(value, float):
                type_name = 'double'
            else:
                raise RuntimeError()
            #
            CmdPortOpt._set_create_(
                obj_path=obj_path,
                port_path=port_path,
                type_name=type_name
            )
            #
            port = CmdPortOpt(obj_path, port_path)
            port.set(value)

    def get_port(self, port_path):
        return CmdPortOpt(self._obj_path, port_path)

    def get_port_opt(self, port_path):
        return CmdPortOpt(self._obj_path, port_path)

    def new_file(self):
        for i_port in self.get_ports():
            i_port.set_disconnect()
        #
        for i_port in self.get_ports():
            # noinspection PyBroadException
            try:
                i_port.set_default()
            except Exception:
                bsc_core.ExceptionMtd.set_print()

    def set(self, key, value):
        self.get_port(key).set(value)

    def get(self, key):
        if CmdPortOpt._get_is_exists_(self.get_path(), key) is True:
            return self.get_port(key).get()

    def delete(self):
        cmds.delete(self.get_path())

    def __str__(self):
        return '{}(path="{}")'.format(
            self.get_type_name(), self.get_path()
        )

    def __repr__(self):
        return self.__str__()


class CmdCameraOpt(CmdObjOpt):
    def __init__(self, obj_path):
        super(CmdCameraOpt, self).__init__(obj_path)

    @classmethod
    def get_front_frame_args(cls, geometry_args, angle):
        _, (c_x, c_y, c_z), (w, h, d) = geometry_args
        z_1 = h/math.tan(math.radians(angle))
        return (c_x, c_y, z_1-c_z), (0, 0, 0)


class CmdShapeOpt(CmdObjOpt):
    def __int__(self, path):
        super(CmdShapeOpt, self).__init__(path)

    def get_transform_name(self):
        return bsc_core.PthNodeMtd.get_dag_parent_name(
            self.get_path(), self.PATHSEP
        )

    def get_transform_path(self):
        return bsc_core.PthNodeMtd.get_dag_parent_path(
            self.get_path(), self.PATHSEP
        )

    def get_subsets_by_material_assign(self):
        subset_dict = {}
        transform_path = self.get_transform_path()
        shape_path = self.get_path()
        material_paths = cmds.listConnections(
            shape_path, destination=1, source=0, type=mya_cor_configure.MyaNodeTypes.Material
        ) or []
        if len(material_paths) > 1:
            for i_material_path in material_paths:
                i_elements = cmds.sets(i_material_path, query=1)
                if i_elements:
                    i_element_paths = [i for i in cmds.ls(i_elements, leaf=1, noIntermediate=1, long=1)]
                    for j_element_path in i_element_paths:
                        if j_element_path.startswith(transform_path):
                            j_comp = j_element_path.split('.f[')[-1][:-1]
                            if ':' in j_comp:
                                j_ = j_comp.split(':')
                                j_indices = range(int(j_[0]), int(j_[1])+1)
                            else:
                                j_indices = [int(j_comp)]
                            subset_dict.setdefault(i_material_path, []).extend(j_indices)
        return subset_dict

    def duplicate_by_material_subsets(self):
        pass

    def rename_transform(self, new_name):
        cmds.rename(self.get_transform_path(), new_name)
        self.update_path()

    def parent_transform_to_path(self, path):
        self.__class__(self.get_transform_path()).parent_to_path(path)
        self.update_path()

    def assign_material_to_path(self, path):
        if cmds.objExists(path) is True:
            _ = cmds.sets(path, query=1) or []
            _ = [cmds.ls(i, long=1)[0] for i in _]
            if self.get_path() not in _:
                # noinspection PyBroadException
                try:
                    cmds.sets(self.get_path(), forceElement=path)
                except Exception:
                    bsc_core.ExceptionMtd.set_print()

    def get_render_properties(self, renderer='arnold'):
        properties = {}
        if renderer == 'arnold':
            import lxarnold.core as and_core

            for i_key in and_core.AndGeometryProperties.AllKeys:
                if i_key in and_core.AndGeometryProperties.MayaMapper:
                    i_port_path = and_core.AndGeometryProperties.MayaMapper[i_key]
                    value = self.get(i_port_path)
                    properties[i_key] = value
        return properties

    def assign_render_properties(self, properties, renderer='arnold'):
        if renderer == 'arnold':
            import lxarnold.core as and_core

            for i_key, i_value in properties.items():
                if i_key in and_core.AndGeometryProperties.MayaMapper:
                    i_port_path = and_core.AndGeometryProperties.MayaMapper[i_key]
                    self.set(i_port_path, i_value)

    def delete_transform(self):
        self.__class__(self.get_transform_path()).delete()


# noinspection PyUnusedLocal
class CmdMeshesOpt(object):
    EVALUATE_A = {
        'shell': 1,
        'triangle': 768,
        'area': 2.3317136764526367,
        'geometry': 1,
        'vertex': 386,
        'face': 384,
        'world-area': 2.3317136764526367,
        'uv-map': 441,
        'edge': 768,
        #
        'clip-x': -0.4245877265930176,
        'clip-y': -0.4245877265930176,
        'clip-z': -0.4245877265930176,
        #
        'width': 0.8491754531860352,
        'height': 0.8491754531860352,
        'depth': 0.8491754531860352,
        #
        'center-x': 0.0,
        'center-y': 0.0,
        'center-z': 0.0,
    }

    def __init__(self, root):
        self._root = root
        self._mesh_paths = cmds.ls(
            self._root,
            type='mesh',
            noIntermediate=1,
            dagObjects=1,
            long=1
        ) or []

    def get_evaluate(self):
        kwargs = dict(
            vertex='vertex'
        )
        dic = {}
        if self._mesh_paths:
            keys = [
                'vertex',
                'edge',
                'face',
                'triangle',
                'uvcoord',
                'area',
                'worldArea',
                'shell',
                'boundingBox'
            ]
            dic_0 = {}
            for i in keys:
                v = cmds.polyEvaluate(
                    self._mesh_paths, **{i: True}
                )
                dic_0[i] = v
            #
            count = len(self._mesh_paths)
            b_box = dic_0['boundingBox']
            #
            dic['geometry'] = count
            dic['vertex'] = dic_0['vertex']
            dic['edge'] = dic_0['edge']
            dic['face'] = dic_0['face']
            dic['triangle'] = dic_0['triangle']
            dic['uv-map'] = dic_0['uvcoord']
            dic['area'] = dic_0['area']
            dic['world-area'] = dic_0['worldArea']
            dic['shell'] = dic_0['shell']
            dic['center-x'] = b_box[0][0]+b_box[0][1]
            dic['center-y'] = b_box[1][0]+b_box[1][1]
            dic['center-z'] = b_box[2][0]+b_box[2][1]
            dic['clip-x'] = b_box[0][0]
            dic['clip-y'] = b_box[1][0]
            dic['clip-z'] = b_box[2][0]
            dic['width'] = b_box[0][1]-b_box[0][0]
            dic['height'] = b_box[1][1]-b_box[1][0]
            dic['depth'] = b_box[2][1]-b_box[2][0]
        #
        return dic

    def get_radar_chart_data(self):
        evaluate = self.get_evaluate()
        radar_chart_data = []
        if evaluate:
            tgt_keys = [
                'face',
                'edge',
                'vertex',
            ]
            for key in [
                'geometry',
                'shell',
                'area',
                'face',
                'edge',
                'vertex',
            ]:
                if key in tgt_keys:
                    a_0 = self.EVALUATE_A['area']
                    a_1 = evaluate['area']
                    v_0 = self.EVALUATE_A[key]
                    src_value = (a_1/a_0)*v_0
                else:
                    src_value = evaluate[key]
                #
                tgt_value = evaluate[key]
                radar_chart_data.append(
                    (key, src_value, tgt_value)
                )
        return radar_chart_data

    def set_reduce_by(self, percent):
        for i_mesh_path in self._mesh_paths:
            self._set_mesh_reduce_(i_mesh_path, percent)

    @classmethod
    def _set_mesh_reduce_(cls, mesh_path, percent):
        cmds.polyReduce(
            mesh_path,
            version=1,
            termination=0,
            percentage=percent*100,
            symmetryPlaneX=0,
            symmetryPlaneY=1,
            symmetryPlaneZ=0,
            symmetryPlaneW=0,
            keepQuadsWeight=0,
            vertexCount=0,
            triangleCount=0,
            sharpness=0,
            keepColorBorder=0,
            keepFaceGroupBorder=0,
            keepHardEdge=1,
            keepCreaseEdge=1,
            keepBorderWeight=0.5,
            keepMapBorderWeight=1,
            keepColorBorderWeight=0.5,
            keepFaceGroupBorderWeight=0.5,
            keepHardEdgeWeight=0.5,
            keepCreaseEdgeWeight=0.5,
            useVirtualSymmetry=0,
            symmetryTolerance=0.01,
            vertexMapName='',
            replaceOriginal=1,
            cachingReduce=1,
            constructionHistory=0
        )
        cmds.polyTriangulate(mesh_path, constructionHistory=0)
        cmds.delete(mesh_path, constructionHistory=1)

    def get_bounding_box(self):
        return cmds.polyEvaluate(self._mesh_paths, boundingBox=1)

    def compute_geometry_args(self):
        b_box = self.get_bounding_box()
        x_0, y_0, z_0 = b_box[0][0], b_box[1][0], b_box[2][0]
        x_1, y_1, z_1 = b_box[0][1], b_box[1][1], b_box[2][1]
        c_x, c_y, c_z = x_0+(x_1-x_0)/2, y_0+(y_1-y_0)/2, z_0+(z_1-z_0)/2
        w, h, d = x_1-x_0, y_1-y_0, z_1-z_0
        return (x_0, y_0, z_0), (c_x, c_y, c_z), (w, h, d)


class CmdUndoStack(object):
    def __init__(self, key=None):
        if key is None:
            key = bsc_core.UuidMtd.generate_new()
        #
        self._key = key

    def __enter__(self):
        cmds.undoInfo(openChunk=1, undoName=self._key)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        cmds.undoInfo(closeChunk=1, undoName=self._key)


class QtControlOpt(object):
    def __init__(self, name):
        self._name = name

    def get_is_exists(self):
        return cmds.workspaceControl(self._name, exists=True)

    def set_visible(self, boolean):
        if self.get_is_exists():
            cmds.workspaceControl(
                self._name,
                edit=True,
                visible=boolean,
            )

    def restore_all(self):
        cmds.workspaceControl(
            self._name,
            edit=True,
            restore=True,
        )

    def do_delete(self):
        if cmds.workspaceControl(self._name, exists=True):
            cmds.workspaceControl(
                self._name,
                edit=True,
                close=True
            )
            #
            cmds.deleteUI(self._name)

    def set_script(self, script):
        cmds.workspaceControl(
            self._name,
            edit=True,
            uiScript=script
        )

    def set_create(self, width, height):
        if self.get_is_exists():
            self.restore_all()
            # self.set_visible(True)
        else:
            cmds.workspaceControl(
                self._name,
                label=bsc_core.RawStrUnderlineOpt(self._name).to_prettify(capitalize=False),
                dockToMainWindow=['right', False],
                initialWidth=width, initialHeight=height,
                widthProperty='free', heightProperty='free'
            )

    @classmethod
    def _to_qt_instance_(cls, ptr, base):
        # noinspection PyUnresolvedReferences
        from shiboken2 import wrapInstance

        return wrapInstance(long(ptr), base)

    def to_qt_widget(self):
        from PySide2 import QtWidgets

        ptr = OpenMayaUI.MQtUtil.findControl(self._name)
        if ptr is not None:
            return self._to_qt_instance_(
                ptr, base=QtWidgets.QWidget
            )

    def get_qt_layout(self):
        widget = self.to_qt_widget()
        if widget is not None:
            return widget.layout()


def undo_stack(key=None):
    return CmdUndoStack(key)

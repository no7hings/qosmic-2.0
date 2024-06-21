# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class PortQuery(object):
    PATHSEP = '.'

    def __init__(self, node_type_name, port_query_path):
        self._node_type_name = node_type_name
        self._port_query_path = port_query_path

    def get_node_type_name(self):
        return self._node_type_name

    def get_port_query_path(self):
        return self._port_query_path

    def _to_query_key(self):
        _ = self._port_query_path.split(self.PATHSEP)[-1]
        if _.endswith(']'):
            return _.split('[')[0]
        return _

    def _to_query_kwargs(self, node_path, **kwargs):
        if node_path is not None:
            kwargs['node'] = node_path
        else:
            kwargs['type'] = self.get_node_type_name()
        return kwargs

    def get_type_name(self, node_path=None):
        return cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, attributeType=True)
        )

    def has_channels(self, node_path=None):
        return (
            cmds.attributeQuery(
                self._to_query_key(),
                **self._to_query_kwargs(node_path, listChildren=True)
            ) or []
        ) != []

    def get_channel_names(self, node_path=None):
        return cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, listChildren=True)
        ) or []

    def get_child_names(self, node_path=None):
        return cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, listChildren=True)
        ) or []

    def get_parent_name(self, node_path=None):
        _ = cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, listParent=True)
        )
        if _:
            return _[0]

    def has_parent(self, node_path=None):
        return cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, listParent=True)
        ) is not None

    def is_array(self, node_path=None):
        return cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, multi=True)
        ) or False

    def is_writeable(self, node_path=None):
        return cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, writable=True)
        ) or False

    def is_keyable(self, node_path=None):
        return cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, keyable=True)
        ) or False

    def is_readable(self, node_path=None):
        return cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, readable=True)
        ) or False

    def is_channel_box_showable(self, node_path=None):
        return cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, channelBox=True)
        ) or False

    def is_message(self, node_path=None):
        return cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, readable=True)
        ) or False

    def is_enumerate(self, node_path=None):
        return cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, enum=True)
        ) or False

    def get_enumerate_strings(self, node_path=None):
        _ = cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, listEnum=True)
        )
        if _:
            return _[0].split(':')
        return []

    def get_short_name(self, node_path=None):
        return cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, shortName=True)
        )

    def get_gui_name(self, node_path=None):
        return cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, niceName=True)
        )

    def get_default(self, node_path=None):
        _ = cmds.attributeQuery(
            self._to_query_key(),
            **self._to_query_kwargs(node_path, listDefault=True)
        )
        if _:
            if self.has_channels() is True:
                return tuple(_)
            return _[0]

    def __str__(self):
        return '{}(path="{}.{}")'.format(
            self.__class__.__name__,
            self._node_type_name, self._port_query_path
        )

    def __repr__(self):
        return '\n'+self.__str__()


class NodeQuery(object):
    class Types(object):
        Transform = 'transform'
        Mesh = 'mesh'
        GPU = 'gpuCache'
        AssemblyReference = 'assemblyReference'
        Material = 'shadingEngine'

    @classmethod
    def _to_node_path(cls, name_or_path):
        _ = cmds.ls(name_or_path, long=1)
        if not _:
            raise RuntimeError()
        return _[0]

    def __init__(self, node_type_name):
        self._node_type_name = node_type_name

    def get_type_name(self):
        return self._node_type_name

    @classmethod
    def _cleanup_fnc(cls, lis):
        list_ = list(filter(None, set(lis)))
        list_.sort(key=lis.index)
        return list_

    def get_port_query_is_exists(self, port_query_path):
        return cmds.attributeQuery(
            port_query_path,
            type=self.get_type_name(),
            exists=1
        )

    def get_port_query(self, port_query_path):
        return PortQuery(
            self.get_type_name(),
            port_query_path
        )

    def get_all_port_query_paths(self):
        def rcs_fnc_(port_query_path_):
            _child_names = self.get_port_query(
                port_query_path_
            ).get_channel_names()
            if _child_names:
                for _i_name in _child_names:
                    _i_port_query_path = '{}.{}'.format(port_query_path_, _i_name)
                    list_.append(_i_port_query_path)
                    rcs_fnc_(_i_port_query_path)

        list_ = []

        _ = self._cleanup_fnc(
            cmds.attributeInfo(
                allAttributes=True,
                type=self.get_type_name()
            ) or []
        )
        if _:
            for i_port_query_path in _:
                if self.get_port_query(i_port_query_path).has_parent() is False:
                    list_.append(i_port_query_path)
                    rcs_fnc_(i_port_query_path)
        return list_

    def get_all_port_queries(self):
        return [
            self.get_port_query(i) for i in self.get_all_port_query_paths()
        ]
